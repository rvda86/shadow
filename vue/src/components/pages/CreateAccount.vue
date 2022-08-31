<template>
    
    <div class="card card-grey">

        <h3>Create Your Account</h3>

        <form class="flex" @submit.prevent="submitHandler">
            <input class="input" type="text" v-model="username" placeholder="Username" v-on:input="showFeedback()" required>
            <p class="feedback-message" :style="{color: (validateUsernameHandler()) ? 'green' : 'red'}" v-show="showFeedbackUsername">
                    {{ (validateUsernameHandler()) ? 'username ok' : 'minimum of 5 characters, no special characters' }}
            </p>
            <input class="input" type="email" v-model="email" placeholder="Email" v-on:input="showFeedback()" required>
            <p class="feedback-message" :style="{color: (validateEmailHandler()) ? 'green' : 'red'}" v-show="showFeedbackEmail">
                    {{ (validateEmailHandler()) ? 'email ok' : 'this email is invalid' }}
            </p>
            <input class="input" type="password" v-model="password" placeholder="Password" v-on:input="showFeedback()" required>
            <p class="feedback-message" :style="{color: (validatePasswordHandler()) ? 'green' : 'red'}" v-show="showFeedbackPassword">
                    {{ (validatePasswordHandler()) ? 'password ok' : 'minimum of 8 characters, at least one number and one letter' }}
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

import { mapActions } from 'vuex'
import { validateEmail, validatePassword, validateUsername } from '../../validation-rules'

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
    methods: {
        ...mapActions(["createAccountRequest"]),
        showFeedback() {
            this.showFeedbackUsername = (this.username.length > 0) ? true : false
            this.showFeedbackEmail = (this.email.length > 0) ? true : false    
            this.showFeedbackPassword = (this.password.length > 0) ? true : false      
        },
        validateEmailHandler() {
            return validateEmail(this.email)
        },
        validatePasswordHandler() {
            return validatePassword(this.password)
        },
        validateUsernameHandler() {
            return validateUsername(this.username)
        },
        submitHandler() {
            this.createAccountRequest({username: this.username, email: this.email, password: this.password})
        }

    }
}
</script>

<style>

</style>