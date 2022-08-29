import { createStore } from 'vuex'
import router from '../router/router'

const store = createStore({
    state() {
        return {
            authenticated: (Date.now() < localStorage.getItem('expires')) ? true : false,
            headerTitle: '',
            showMenu: false,
            showModal: false,
            showSettingsModal: false,
            settingsModalData: {},
            apiLink: "http://192.168.2.3:5000/api",
            data: {userData: {}, categories: {}},
            dataIsLoaded: false,
            topicTypes: ["journal", "todo"] 
        }
    },
    mutations: {
        login(state, result) {
            localStorage.setItem("token", result.access_token)
            localStorage.setItem("expires", Date.now() + 7200000)
            state.authenticated = true
            router.replace("/home")
        },
        logout(state) {
            localStorage.removeItem("token")
            localStorage.removeItem("expires")
            state.authenticated = false
            router.replace("/")
        },
        toggleMenu(state) {
            state.showMenu = !state.showMenu
        },
        toggleModal(state) {
            state.showModal = !state.showModal
        },
        toggleSettingsModal(state) {
            state.showSettingsModal = !state.showSettingsModal
        },
        setSettingsModalData(state, payload) {
            state.settingsModalData = payload
            state.settingsModalData.newName = state.settingsModalData.name
        },
        resetSettingsModalData(state) {
            state.settingsModalData = {}
        },
        setModalPayload(state, payload) {
            state.modalPayload = payload
        },
        resetModalPayload(state) {
            state.modalPayload = {}
        },
        hideMenu(state) {
            state.showMenu = false
        },
        setData(state, data) {
            state.data = {userData: data.user_data, categories: data.user_categories}
            state.dataIsLoaded = true
        },
        addResourceLocal(state, newEntry) {
            if (newEntry.entry_type === "category") {
                state.data.categories.push(newEntry)
            } else if (newEntry.entry_type === "topic") {
                for (let category of state.data.categories) {
                    if (category.id === newEntry.category_id) {
                        category.topics.push(newEntry)
                    }
                }
            } else {
                for (let category of state.data.categories) {
                    for (let topic of category.topics) {
                        if (topic.id === newEntry.topic_id) {
                            topic.entries.push(newEntry)
                        }
                    }
                }
            }
            state.dataIsLoaded = true
        },
        updateResourceLocal(state, updatedEntry) {
            let categories = state.data.categories
            for (let category of categories) {
                if (category.id === updatedEntry.id) {
                    categories[categories.indexOf(category)] = updatedEntry
                    break
                }
                for (let topic of category.topics) {
                    if (topic.id === updatedEntry.id) {
                        category.topics[category.topics.indexOf(topic)] = updatedEntry
                        break
                    }
                    for (let entry of topic.entries) {
                        if (entry.id === updatedEntry.id) {
                            topic.entries[topic.entries.indexOf(entry)] = updatedEntry
                            break
                        }
                    }
                }
            }
            state.dataIsLoaded = true
        },
        deleteResourceLocal(state, deletedEntry) {

            let categories = state.data.categories
            for (let category of categories) {
                if (category.id === deletedEntry.id) {
                    categories.splice(categories.indexOf(category), 1)
                    break
                }
                for (let topic of category.topics) {
                    if (topic.id === deletedEntry.id) {
                        category.topics.splice(category.topics.indexOf(topic),1)
                        break
                    }
                    for (let entry of topic.entries) {
                        if (entry.id === deletedEntry.id) {
                            topic.entries.splice(topic.entries.indexOf(entry), 1)
                            break
                        }
                    }
                }
            }
            state.dataIsLoaded = true
        },
        updateAccountLocal(state, updatedUser) {
            state.data.userData = updatedUser
            state.dataIsLoaded = true
        },
        setHeaderTitle(state, headerTitle){
            state.headerTitle = headerTitle
        },
        setFlashMessage(state, msg) {
            state.flashMessage = msg
            state.showFlashMessage = true
            setTimeout( () => state.showFlashMessage = false,  5000)
        },
        setDataIsLoaded(state, boolean) {
            state.dataIsLoaded = boolean
        },
        rerouteAfterDelete(state, entry) {
            if (entry.type === "topic") {
                if (window.location.pathname.slice(-36) === entry.id) {
                    router.replace("/home")
                }
            }
        }
    },
    actions: {
        async fetchDataRequest(context) {
            context.commit("setDataIsLoaded", false)
            let response = await fetch(`${this.state.apiLink}/data`, 
                                        {method: 'GET', 
                                        headers: {'Content-type': 'application/json', 'Authorization': "Bearer " + localStorage.getItem("token")}})
            if (response.ok) {
                let data = await response.json()
                context.commit('setData', data)
               } else {                 
                context.commit("logout") 
            }
        },
        async sendEntryDataRequest(context, payload) {
            context.commit("setDataIsLoaded", false)
            let [method, data] = payload
            let response = await fetch(`${this.state.apiLink}/entries`, 
                                        {method: method, 
                                        headers: {'Content-type': 'application/json', 'Authorization': "Bearer " + localStorage.getItem("token")}, 
                                        body: JSON.stringify(data)})
            response.json().then(result => {
                if (response.ok) {
                    result.status = "success"
                    context.commit("setFlashMessage", result.msg)
                    if (method === "POST") {
                        context.commit("addResourceLocal", result.entry)
                    } else if (method === "PUT") {
                        context.commit("updateResourceLocal", result.entry)
                    } else if (method === "DELETE") {
                        context.commit("deleteResourceLocal", data)
                        context.commit("rerouteAfterDelete", data)
                    } else {
                        context.dispatch('fetchDataRequest')
                    }
                    
                } else {
                    context.commit("setFlashMessage", result.msg)
                }
            })
        },
        async createAccountRequest(context, data) {
            let response = await fetch(`${this.state.apiLink}/users`, {method: 'POST', headers: {'Content-type': 'application/json'}, body: JSON.stringify(data)})
            response.json().then(result => {
                if (response.ok) {
                    result.status = "success"
                    context.commit("setFlashMessage", result.msg)
                    router.replace("/login")            
                } else {
                    context.commit("setFlashMessage", result.msg)
                }
            })      
        },
        async updateAccountRequest(context, data) {
            context.commit("setDataIsLoaded", false)
            let response = await fetch(`${this.state.apiLink}/users`,
                                        {method: 'PUT', 
                                        headers: {'Content-type': 'application/json', 'Authorization': "Bearer " + localStorage.getItem("token")}, 
                                        body: JSON.stringify(data)})
            response.json().then(result => {
                if (response.ok) {
                    result.status = "success"
                    context.commit("updateAccountLocal", result.data)
                    context.commit("setFlashMessage", result.msg)
                } else {
                    context.commit("setFlashMessage", result.msg)
                }
            })
        },
        async deleteAccountRequest(context, data) {
            let response = await fetch(`${this.state.apiLink}/users`, 
                                        {method: 'DELETE', 
                                        headers: {'Content-type': 'application/json', 'Authorization': "Bearer " + localStorage.getItem("token")}, 
                                        body: JSON.stringify(data)})
            response.json().then(result => {
                if (response.ok) {
                    result.status = "success"
                    context.commit("setFlashMessage", result.msg)
                    context.commit("logout")
                } else {
                    context.commit("setFlashMessage", result.msg)
                }
            })
        },
        async getTokenRequest(context, data) {
            let response = await fetch(`${this.state.apiLink}/users/token`, 
                                        {method: 'POST', 
                                        headers: {'Content-type': 'application/json'}, 
                                        body: JSON.stringify(data)})
            response.json().then(result => {
                if (response.ok) {              
                    context.commit("login", result)
                    context.dispatch('fetchDataRequest')
                } else {
                    context.commit("setFlashMessage", result.msg)
                }
            })
        }, 
        async sendPasswordResetLinkRequest(context, data) {
            let response = await fetch(`${this.state.apiLink}/users/reset_password_send_link`, 
                                        {method: 'POST', 
                                        headers: {'Content-type': 'application/json'},
                                        body: JSON.stringify(data)})
            response.json().then(result => {
                if (response.ok) {              
                    result.status = "success"
                    context.commit("setFlashMessage", result.msg)
                } else {
                    context.commit("setFlashMessage", result.msg)
                }
            })
        },
        async sendEmailVerificationLinkRequest(context) {
            let response = await fetch (`${this.state.apiLink}/users/verify_email_send_link`,
                                        {method: 'GET',
                                        headers: {'Content-type': 'application/json', 'Authorization': "Bearer " + localStorage.getItem("token")}})
            response.json().then(result => {
                if (response.ok) {
                    result.status = "success"
                    context.commit("setFlashMessage", result.msg)
                } else {
                    context.commit("setFlashMessage", result.msg)
                }
            })
        },
        async passwordResetRequest(context, data) {
            let response = await fetch(`${this.state.apiLink}/users/reset_password`, 
                                        {method: 'POST', 
                                        headers: {'Content-type': 'application/json', 'Authorization': "Bearer " + data.token},
                                        body: JSON.stringify({password: data.password})})
            response.json().then(result => {
                if (response.ok) {              
                    result.status = "success"
                    context.commit("setFlashMessage", result.msg)
                    router.replace("/login")    
                } else {
                    context.commit("setFlashMessage", result.msg)
                }
            })
        },
        async verifyEmailRequest(context, token) {
            let response = await fetch(`${this.state.apiLink}/users/verify_email`, 
                                        {method: 'POST', 
                                        headers: {'Content-Length': 0, 'Authorization': "Bearer " + token}})
            response.json().then(result => {
                if (response.ok) {              
                    result.status = "success"
                    context.commit("setFlashMessage", result.msg)
                    router.replace("/login")    
                } else {
                    context.commit("setFlashMessage", result.msg)
                }
            })
        },

    }
})

export default store 