<template>
    
    <div class="card">

        <h3>Edit Your Account</h3>
        <form class="flex" @submit.prevent="submitHandler">
            <p>Username:</p>
            <input class="input" type="text" v-model="username" required>
            <p>Email:</p>
            <input class="input" type="email" v-model="email" required>

            <p>Password:</p>
            <p class="link" @click="togglePasswordEdit">{{ editPasswordText }}</p>
            <input class="input" v-if="editingPassword" type="password" placeholder="new password" v-model="newPassword" required>
            <input class="input" v-if="editingPassword" type="password" placeholder="confirm new password" v-model="newPasswordConfirmed" required>

            <p>Current Password:</p>
            <input class="input" type="password" placeholder="current password" v-model="currentPassword" required>
            <button class="button">Update Account</button>
        </form>

    </div>

</template>

<script>

import { mapActions, mapMutations } from 'vuex'

export default {
    name: 'UpdateAccount',
    data() {
        return {
            username: this.userData.username,
            email: this.userData.email,
            currentPassword: '',
            newPassword: '',
            newPasswordConfirmed: '',
            editingPassword: false,
            editPasswordText: "edit",
        }
    },
    props: {
        userData: Object
    },
    methods: {
        ...mapActions(["updateAccountRequest"]),
        ...mapMutations(["toggleModal", "setModalPayload"]),
        togglePasswordEdit() {
            this.editingPassword = !this.editingPassword
            this.editPasswordText = this.editingPassword ? 'cancel' : 'edit'
        },
        submitHandler() {
            this.newPassword = this.editingPassword ? this.newPassword : this.currentPassword
            this.setModalPayload({func: this.updateAccountRequest, 
                                payload: {username: this.username, email: this.email, password: this.newPassword, currentPassword: this.currentPassword}})
            this.toggleModal()
        }
    }
}

</script>

<style>



.settings-account {
    margin: 10px;
    display: flex;
    flex-direction: column;
}

#settings-categories {
    min-width: 600px;
}

.settings-categories {
    display: flex;
    flex-direction: row;
}

</style>