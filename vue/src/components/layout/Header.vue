<template>
    <div class="header-nav-left">
        <router-link class="header-item" :to="{name: 'index'}">
            SHADOW
        </router-link>
    </div>
    <div id="header-title">
        <a class="header-item">
            {{ headerTitle }}
        </a>
    </div>
    <div class="header-nav-right">
        <router-link :to="{name: 'login'}"><button class="button">Log In</button></router-link>
        <router-link :to="{name: 'createAccount'}"><button class="button">Create Account</button></router-link>
    </div>  
</template>

<script>


export default {
    name: 'Header'
}
</script>

<style>
</style>