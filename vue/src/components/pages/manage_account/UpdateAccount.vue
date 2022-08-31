<template>
    
    <div class="card">

        <h3>Edit Your Account</h3>
        <form class="flex" @submit.prevent="submitHandler">
            <p>Username:</p>
            <input class="input" type="text" v-model="username" v-on:input="enableFeedbackUsername()" required>
            <p class="feedback-message" :style="{color: (validateUsernameHandler()) ? 'green' : 'red'}" v-show="showFeedbackUsername">
                    {{ (validateUsernameHandler()) ? 'username ok' : 'minimum of 5 characters, no special characters' }}
            </p>
            <p>Email:</p>
            <input class="input" type="email" v-model="email" v-on:input="enableFeedbackEmail()" required>
            <p class="feedback-message" :style="{color: (validateEmailHandler()) ? 'green' : 'red'}" v-show="showFeedbackEmail">
                    {{ (validateEmailHandler()) ? 'email ok' : 'this email is invalid' }}
            </p>

            <p class="small-font" v-show="!emailVerified">your email is not verified: <a class="link" href="#" @click="resendVerificationLinkHandler">resend verification link</a></p>

            <p>Password:</p>
            <p class="link" @click="togglePasswordEdit">{{ editPasswordText }}</p>
            <input class="input" v-if="editingPassword" type="password" placeholder="new password" v-model="newPassword" 
                    v-on:input="enableFeedbackNewPassword()" required>
            <p class="feedback-message" :style="{color: (validatePasswordHandler(this.newPassword)) ? 'green' : 'red'}" v-show="showFeedbackNewPassword">
                    {{ (validatePasswordHandler(this.newPassword)) ? 'password ok' : 'minimum of 8 characters, at least one number and one letter' }}
            </p>
            <input class="input" v-if="editingPassword" type="password" placeholder="confirm new password" v-model="newPasswordConfirmed" 
                    v-on:input="enableFeedbackNewPasswordConfirmed()" required>
            <p class="feedback-message" :style="{color: (validatePasswordMatch()) ? 'green' : 'red'}" v-show="showFeedbackNewPasswordConfirmed">
                    {{ (validatePasswordMatch()) ? 'passwords match' : 'passwords do not match' }}
            </p>

            <p>Current Password:</p>
            <input class="input" type="password" placeholder="current password" v-model="currentPassword" required>
            <button class="button">Update Account</button>
        </form>

    </div>

</template>

<script>

import { mapActions, mapMutations } from 'vuex'
import { validateEmail, validatePassword, validateUsername } from '../../../validation-rules'

export default {
    name: 'UpdateAccount',
    data() {
        return {
            username: this.userData.username,
            email: this.userData.email,
            emailVerified: (this.userData.email_verified === 1) ? true : false,
            currentPassword: '',
            newPassword: '',
            newPasswordConfirmed: '',
            editingPassword: false,
            editPasswordText: "edit",
            showFeedbackUsername: false,
            showFeedbackEmail: false,
            showFeedbackNewPassword: false,
            showFeedbackNewPasswordConfirmed: false
        }
    },
    props: {
        userData: Object
    },
    methods: {
        ...mapActions(["updateAccountRequest", "sendEmailVerificationLinkRequest"]),
        ...mapMutations(["toggleModal", "setModalPayload"]),
        enableFeedbackUsername() {
            this.showFeedbackUsername = true
        },
        enableFeedbackEmail() {
            this.showFeedbackEmail = true
        },
        enableFeedbackNewPassword() {
            this.showFeedbackNewPassword = true
        },
        enableFeedbackNewPasswordConfirmed() {
            this.showFeedbackNewPasswordConfirmed = true
        },
        togglePasswordEdit() {
            this.editingPassword = !this.editingPassword
            this.editPasswordText = this.editingPassword ? 'cancel' : 'change password'
        },
        submitHandler() {
            this.newPassword = this.editingPassword ? this.newPassword : this.currentPassword
            this.setModalPayload({func: this.updateAccountRequest, 
                                payload: {username: this.username, email: this.email, password: this.newPassword, currentPassword: this.currentPassword}})
            this.toggleModal()
        },
        validateEmailHandler() {
            return validateEmail(this.email)
        },
        validatePasswordHandler(password) {
            return validatePassword(password)
        },
        validateUsernameHandler() {
            return validateUsername(this.username)
        },
        validatePasswordMatch() {
            return this.newPassword === this.newPasswordConfirmed
        },
        resendVerificationLinkHandler() {
            this.sendEmailVerificationLinkRequest()
        }
    }
}

</script>

<style>
</style>