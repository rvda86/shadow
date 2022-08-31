<template>
    <div class="card">
        <div>
            <h3>Enter your email address</h3>
            <form class="flex" @submit.prevent="submitHandler">
                <input class="input" type="email" placeholder="email" v-model="email" v-on:input="showFeedback()" required>
                <p class="feedback-message" :style="{color: (validateEmailHandler()) ? 'green' : 'red'}" v-show="showFeedbackEmail">
                    {{ (validateEmailHandler()) ? 'valid email' : 'invalid email' }}
                </p>
                <button class="button">Submit</button>
            </form>
        </div>
    </div>

</template>

<script>

import { mapActions } from 'vuex'
import { validateEmail } from '../../validation-rules'

export default {
    name: 'RequestPasswordReset',
    data() {
        return {
            email: '',
            showFeedbackEmail: false
        }
    },
    methods: {
        ...mapActions(["sendPasswordResetLinkRequest"]),
        submitHandler() {
            this.sendPasswordResetLinkRequest({email: this.email})
        },
        showFeedback() {
            this.showFeedbackEmail = (this.email.length > 0) ? true : false  
        },
        validateEmailHandler() {
            return validateEmail(this.email)
        },
    }
}
</script>

<style>

</style>