<template>
    <div class="card">
        <div>
            <h3>Verify your email</h3>
            <form class="flex" @submit.prevent="submitHandler">
                <button class="button">Verify email</button>
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
        ...mapActions(["verifyEmailRequest"]),
        submitHandler() {
            const urlParams = new URLSearchParams(window.location.search)
            const token = urlParams.get('token')
            this.verifyEmailRequest(token)
        },
        showFeedback() {
            this.showFeedbackPassword = (this.newPasswordConfirmed.length > 0) ? true : false  
        }
    }
}
</script>

<style>

</style>