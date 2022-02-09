<template>
    <div class="header-nav-left">
        <router-link class="header-item" @click="hideMenu" to="/">
            Home
        </router-link>
    </div>
    <div id="header-title">
        <a class="header-item">
            {{ headerTitle }}
        </a>
    </div>
    <div class="header-nav-right">
        <a class="header-item" @click="toggleMenu" href="#">
            <div class="hamburger-menu"></div>  
            <div class="hamburger-menu"></div>  
            <div class="hamburger-menu"></div>            
        </a>
    </div>  
</template>

<script>

import { mapState, mapMutations } from 'vuex'

export default {
    name: 'Header',
    computed: {
        ...mapState(["headerTitle"])
    },
    methods: {
        ...mapMutations(["toggleMenu", "hideMenu"])
    }
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
#header-title {
    display: flex;
    margin: auto;
}
.header-nav-right {
    display: flex;
    width: 75px;
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
.hamburger-menu {
    width: 20px;
    height: 2px;
    margin: 4px 0;
    background-color: black;
}
</style>