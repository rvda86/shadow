<template>
    
    <div class="card">

        <h3>Create Your Account</h3>

        <form class="flex" @submit.prevent="submitHandler">
            <input class="input" type="text" v-model="username" placeholder="Username" v-on:input="checkAvailability(); showFeedback()" required>
            <p class="feedback-message" :style="{color: (usernameAvailable ? 'green' : 'red')}" v-show="showFeedbackUsername">
                    {{ usernameAvailable ? 'This username is available' : 'this username is taken' }}
            </p>
            <input class="input" type="email" v-model="email" placeholder="Email" v-on:input="checkAvailability(); showFeedback()" required>
            <p class="feedback-message" :style="{color: (emailAvailable && validateEmail()) ? 'green' : 'red'}" v-show="showFeedbackEmail">
                    {{ (emailAvailable && validateEmail()) ? 'This email is available' : validateEmail() ? 'this email is taken' : 'this email is invalid' }}
            </p>
            <input class="input" type="password" v-model="password" placeholder="Password" v-on:input="showFeedback()" required>
            <p class="feedback-message" :style="{color: (password.length >= 8) ? 'green' : 'red'}" v-show="showFeedbackPassword">
                    {{ (password.length >= 8) ? 'password ok' : 'use at least 8 characters' }}
            </p>
            <button class="button">Create!</button>
        </form>

        <p class="small-font">
            Already have an account? Click
            <router-link class="link" :to="{name: 'login'}">here</router-link>
            to log in
        </p>

    </div>

</template>

<script>

import { mapState, mapActions } from 'vuex'

export default {
    name: 'CreateAccount',
    data() {
        return {
            username: "",
            email: "",
            password: "",
            showFeedbackUsername: false,
            showFeedbackEmail: false,
            showFeedbackPassword: false
        }
    },
    computed: {
        ...mapState(["usernameAvailable", "emailAvailable"])
    },
    methods: {
        ...mapActions(["createAccountRequest", "checkUsernameEmailAvailabilityRequest"]),
        checkAvailability() {
            this.checkUsernameEmailAvailabilityRequest({username: this.username, email: this.email})   
        },
        showFeedback() {
            this.showFeedbackUsername = (this.username.length > 0) ? true : false
            this.showFeedbackEmail = (this.email.length > 0) ? true : false    
            this.showFeedbackPassword = (this.password.length > 0) ? true : false      
        },
        validateEmail() {
            return (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(this.email))
        },
        submitHandler() {
            this.createAccountRequest({username: this.username, email: this.email, password: this.password})
        }

    }
}
</script>

<style>

</style>