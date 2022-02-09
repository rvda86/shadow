<template>
    
    <div class="card">

        <h3>Delete Your Account</h3>
        <form class="flex" @submit.prevent="submitHandler">            
            <input class="input" type="password" placeholder="current password" v-model="currentPassword" required />
            <button class="button background-red" type="submit">Delete Account</button>
        </form>

    </div>

</template>

<script>

import { mapActions, mapMutations } from 'vuex'

export default {
    name: 'UpdateAccount',
    data() {
        return {
            currentPassword: ''
        }
    },
    props: {
        userData: Object
    },
    methods: {
        ...mapActions(["deleteAccountRequest"]),
        ...mapMutations(["toggleModal", "setModalPayload"]),
        submitHandler() {
            this.setModalPayload({func: this.deleteAccountRequest, 
                                payload: {password: this.currentPassword}})
            this.toggleModal()
        }
    }
}

</script>

<style>

</style>