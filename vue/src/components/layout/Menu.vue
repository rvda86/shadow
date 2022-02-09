<template>
    <div id="menu">
        <ul class="menu-list">
            <li class="menu-item">
                <router-link class="menu-text link" @click="logoutHandler" to="/login">Log Out</router-link>
            </li>
            <li class="menu-item">
                <router-link class="menu-text link" @click="toggleMenu" to="/manage_categories">Manage Categories and Topics</router-link>
            </li>
            <li class="menu-item">
                <router-link class="menu-text link" @click="toggleMenu" to="/manage_account">Manage Account</router-link>
            </li>
            <li class="menu-item" :key="category.id" v-for="category in data.categories">
                <span class="menu-text">{{ category.name }}</span> 
                <ul class="menu-list">
                    <li class="menu-item" :key="topic.id" v-for="topic in category.topics">
                        <router-link class="menu-text link" @click="toggleMenu" :to="{name: topic.topic_type, params: { topicId: topic.id }}">{{ topic.topic_type }} - {{ topic.name }}</router-link>
                    </li>
                </ul>
            </li>
        </ul>
    </div>   
</template>

<script>
import { mapState, mapMutations } from 'vuex'

export default {
    name: 'Menu',
    computed: {
        ...mapState(["data"])
    },
    methods: {
        ...mapMutations(["toggleMenu", "logout"]),
        logoutHandler() {
            this.toggleMenu()
            this.logout()
        }
    }
}
</script>

<style>
#menu {
    background-color: white;
    color: black;
}
.menu-list {
    margin: 0;
    padding: 0;
    list-style-type: none;
    display: flex;
    flex-direction: column;
}
.menu-item {
    margin: 5px;
    padding: 0 5px;
}
.menu-text {
    color: black;
    text-decoration: none;
    font-size: 0.8em;
    font-weight: 400;
}
</style>