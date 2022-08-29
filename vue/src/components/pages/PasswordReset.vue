<template>
    <div class="card">
        <div>
            <h3>Enter your new password:</h3>
            <form class="flex" @submit.prevent="submitHandler">
                <input class="input" type="password" placeholder="new password" v-on:input="enableFeedbackNewPassword()" v-model="newPassword" required>
                <p class="feedback-message" :style="{color: (validatePasswordHandler()) ? 'green' : 'red'}" v-show="showFeedbackNewPassword">
                    {{ (validatePasswordHandler()) ? 'password ok' : 'minimum of 8 characters, at least one number and one letter' }}
                </p>
                <input class="input" type="password" placeholder="confirm new password" v-on:input="enableFeedbackNewPasswordConfirmed()" v-model="newPasswordConfirmed" required>
                <p class="feedback-message" :style="{color: (validatePasswordMatch()) ? 'green' : 'red'}" v-show="showFeedbackNewPasswordConfirmed">
                        {{ (validatePasswordMatch()) ? 'passwords match' : 'passwords do not match' }}
                </p>
                <button class="button">Submit</button>
            </form>
        </div>
    </div>

  
</template>

<script>

import { mapActions } from 'vuex'
import { validatePassword } from '../../validation-rules'

export default {
    name: 'PasswordReset',
    data() {
        return {
            newPassword: '',
            newPasswordConfirmed: '',
            showFeedbackNewPassword: false,
            showFeedbackNewPasswordConfirmed: false
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
        enableFeedbackNewPassword() {
            this.showFeedbackNewPassword = (this.newPassword.length > 0) ? true : false  
        },
        enableFeedbackNewPasswordConfirmed() {
            this.showFeedbackNewPasswordConfirmed = (this.newPasswordConfirmed.length > 0) ? true : false  
        },
        validatePasswordHandler() {
            return validatePassword(this.newPassword)
        },
        validatePasswordMatch() {
            return this.newPassword === this.newPasswordConfirmed
        }
    }
}
</script>

<style>

</style>