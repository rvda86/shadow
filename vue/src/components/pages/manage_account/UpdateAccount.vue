<template>
    
    <div class="card">

        <h4>Edit Your Account</h4>
        <form class="flex" @submit.prevent="submitHandler">
            <p class="small-font">Username:</p>
            <input class="input input-large" type="text" v-model="username" v-on:input="enableFeedbackUsername()">
            <p class="feedback-message" :style="{color: (validateUsernameHandler()) ? 'green' : 'red'}" v-show="showFeedbackUsername">
                    {{ (validateUsernameHandler()) ? 'username ok' : 'minimum of 5 characters, no special characters' }}
            </p>
            <p class="small-font">Email:</p>
            <input class="input input-large" type="email" v-model="email" v-on:input="enableFeedbackEmail()">
            <p class="feedback-message" :style="{color: (validateEmailHandler()) ? 'green' : 'red'}" v-show="showFeedbackEmail">
                    {{ (validateEmailHandler()) ? 'email ok' : 'this email is invalid' }}
            </p>

            <p class="small-font" v-show="!emailVerified"><strong>your email is not verified</strong></p>
            <p><a class="link small-font" href="#" @click="resendVerificationLinkHandler">resend verification link</a></p>

            <p class="small-font">Password:</p>
            <p class="link small-font" @click="togglePasswordEdit">{{ editPasswordText }}</p>
            <input class="input input-large" v-if="editingPassword" type="password" placeholder="new password" v-model="newPassword" 
                    v-on:input="enableFeedbackNewPassword()">
            <p class="feedback-message" :style="{color: (validatePasswordHandler(this.newPassword)) ? 'green' : 'red'}" v-show="showFeedbackNewPassword">
                    {{ (validatePasswordHandler(this.newPassword)) ? 'password ok' : 'minimum of 8 characters, at least one number and one letter' }}
            </p>
            <input class="input input-large" v-if="editingPassword" type="password" placeholder="confirm new password" v-model="newPasswordConfirmed" 
                    v-on:input="enableFeedbackNewPasswordConfirmed()">
            <p class="feedback-message" :style="{color: (validatePasswordMatch()) ? 'green' : 'red'}" v-show="showFeedbackNewPasswordConfirmed">
                    {{ (validatePasswordMatch()) ? 'passwords match' : 'passwords do not match' }}
            </p>

            <p class="small-font">Current Password:</p>
            <input class="input input-large" type="password" placeholder="current password" v-model="currentPassword">
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
        ...mapMutations(["toggleModal", "setModalPayload", "setFlashMessage"]),
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
            if (this.currentPassword.length === 0) {
                this.setFlashMessage("please enter your current password")
            } else {
            this.password = this.editingPassword ? this.newPassword : this.currentPassword
            this.setModalPayload({func: this.updateAccountRequest, 
                                payload: {username: this.username, email: this.email, password: this.password, currentPassword: this.currentPassword}})
            this.toggleModal()
            }
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