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
    <div class="header-nav-right2">
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
header {
    margin: 0;
    padding: 0;
    display: flex;
    background-color: #333333;
    background-color: white;
}
.header-nav-right2 {
    display: flex;
    width: 200px;
    justify-content: right;
}
.header-nav-left {
    display: flex;
    width: 75px;
    justify-content: left;
}
.header-item {
    margin: auto 5px;
    padding: 5px;
    color: black;
    text-decoration: none;
    font-size: 0.8em;
    font-weight: 550;
}
</style>