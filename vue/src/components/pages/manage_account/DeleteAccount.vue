<template>
    
    <div class="card">

        <h4>Delete Your Account</h4>
        <form class="flex" @submit.prevent="submitHandler">            
            <input class="input input-large" type="password" placeholder="current password" v-model="currentPassword" />
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