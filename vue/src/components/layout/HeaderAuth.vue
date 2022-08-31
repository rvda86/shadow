<template>
    <div class="header-nav-left">
        <router-link class="header-item" @click="hideMenu" to="/home">
            <font-awesome-icon icon="fa-solid fa-house" />
        </router-link>
    </div>

    <div id="header-title">
        <p class="small-font">{{ headerTitle }}</p>
    </div>

    <div class="header-nav-right-menu">
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
    name: 'HeaderAuth',
    computed: {
        ...mapState(["headerTitle"])
    },
    methods: {
        ...mapMutations(["toggleMenu", "hideMenu"])
    }
}
</script>

<style>
</style>