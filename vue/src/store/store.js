import { createStore } from 'vuex'
import router from '../router/router'

const store = createStore({
    state() {
        return {
            authenticated: (Date.now() < localStorage.getItem('expires')) ? true : false,
            headerTitle: '',
            showMenu: false,
            showModal: false,
            apiLink: "http://192.168.2.2:5000/api",
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
            router.replace("/login")
        },
        toggleMenu(state) {
            state.showMenu = !state.showMenu
        },
        toggleModal(state) {
            state.showModal = !state.showModal
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
        setHeaderTitle(state, headerTitle){
            state.headerTitle = headerTitle
        },
        setUsernameEmailAvailability(state, data) {
            state.usernameAvailable = data.username
            state.emailAvailable = data.email
        },
        setFlashMessage(state, result) {
            state.flashMessage = result.msg
            state.showFlashMessage = true
            setTimeout( () => state.showFlashMessage = false,  5000)
        },
    },
    actions: {
        async fetchDataRequest(context) {
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
            let [method, data] = payload
            let response = await fetch(`${this.state.apiLink}/entries`, 
                                        {method: method, 
                                        headers: {'Content-type': 'application/json', 'Authorization': "Bearer " + localStorage.getItem("token")}, 
                                        body: JSON.stringify(data)})
            response.json().then(result => {
                if (response.ok) {
                    result.status = "success"
                    context.commit("setFlashMessage", result)
                    context.dispatch('fetchDataRequest')
                } else {
                    context.commit("setFlashMessage", result)
                }
            })
        },
        async createAccountRequest(context, data) {
            let response = await fetch(`${this.state.apiLink}/users`, {method: 'POST', headers: {'Content-type': 'application/json'}, body: JSON.stringify(data)})
            response.json().then(result => {
                if (response.ok) {
                    result.status = "success"
                    context.commit("setFlashMessage", result)
                    router.replace("/login")            
                } else {
                    context.commit("setFlashMessage", result)
                }
            })      
        },
        async updateAccountRequest(context, data) {
            let response = await fetch(`${this.state.apiLink}/users`,
                                        {method: 'PUT', 
                                        headers: {'Content-type': 'application/json', 'Authorization': "Bearer " + localStorage.getItem("token")}, 
                                        body: JSON.stringify(data)})
            response.json().then(result => {
                if (response.ok) {
                    result.status = "success"
                    context.commit("setFlashMessage", result)
                } else {
                    context.commit("setFlashMessage", result)
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
                    context.commit("setFlashMessage", result)
                    context.commit("logout")
                } else {
                    context.commit("setFlashMessage", result)
                }
            })
        },
        async getTokenRequest(context, data) {
            let response = await fetch(`${this.state.apiLink}/users/token`, 
                                        {method: 'POST', 
                                        headers: {'Content-type': 'application/json'}, 
                                        body: JSON.stringify(data)})
            response.json().then(data => {
                if (response.ok) {              
                    context.commit("login", data)
                    context.dispatch('fetchDataRequest')
                } else {
                    context.commit("setFlashMessage", data)
                }
            })
        },  
        async checkUsernameEmailAvailabilityRequest(context, data) {
            let response = await fetch(`${this.state.apiLink}/users/check_availability`, 
                                        {method: 'POST', 
                                        headers: {'Content-type': 'application/json', 'Authorization': "Bearer " + localStorage.getItem("token")},
                                        body: JSON.stringify(data)})
            response.json().then(data => {
                if (response.ok) {              
                    context.commit("setUsernameEmailAvailability", data)
                } else {
                    context.commit("setFlashMessage", data)
                }
            })
        }

    }
})

export default store 