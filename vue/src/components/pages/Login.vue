<template>
    <div class="card card-grey"> 

        <h3>Log In</h3>

        <form class="flex" @submit.prevent="submitHandler">
            <input class="input input-large" type="text" v-model="username" placeholder="Username" required>
            <input class="input input-large" type="password" v-model="password" placeholder="Password" required>
            <button class="button">Log In</button>
        </form>

        <p class="small-font">
            No account? Click 
            <router-link class="link" :to="{name: 'createAccount'}">here</router-link>
            to create an account
        </p>
        <p class="small-font">
            <router-link class="link" :to="{name: 'requestPasswordReset'}">Forget your password?</router-link>
        </p>

    </div>
</template>

<script>

import { mapActions } from 'vuex'

export default {
    name: 'Login',
    data() {
        return {
            username: "",
            password: ""
        }
    },
    methods: {
        ...mapActions(["getTokenRequest"]),
        submitHandler() {
            this.getTokenRequest({username: this.username, password: this.password})
        }

    }
}
</script>

<style>

</style>