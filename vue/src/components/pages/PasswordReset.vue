<template>
    <div class="card">
        <div>
            <h3>Enter your new password:</h3>
            <form class="flex" @submit.prevent="submitHandler">
                <input class="input" type="password" placeholder="new password" v-model="newPassword" required>
                <input class="input" type="password" placeholder="confirm new password" v-on:input="showFeedback()" v-model="newPasswordConfirmed" required>
                <p class="feedback-message" :style="{color: (this.newPassword === this.newPasswordConfirmed) ? 'green' : 'red'}" v-show="showFeedbackPassword">
                    {{ (this.newPassword === this.newPasswordConfirmed) ? 'passwords match' : 'passwords do not match' }}
                </p>
                <button class="button">Submit</button>
            </form>
        </div>
    </div>

  
</template>

<script>

import { mapActions } from 'vuex'

export default {
    name: 'PasswordReset',
    data() {
        return {
            newPassword: '',
            newPasswordConfirmed: '',
            showFeedbackPassword: false
        }
    },
    methods: {
        ...mapActions(["passwordResetRequest"]),
        submitHandler() {
            const urlParams = new URLSearchParams(window.location.search)
            const token = urlParams.get('token')
            if (this.newPassword === this.newPasswordConfirmed) {
                this.passwordResetRequest({password: this.newPassword, token: token})
            }
        },
        showFeedback() {
            this.showFeedbackPassword = (this.newPasswordConfirmed.length > 0) ? true : false  
        }
    }
}
</script>

<style>

</style>