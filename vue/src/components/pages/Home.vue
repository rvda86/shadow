<template>
    <div>
    <div class="card card-grey"> 
        <h4>Welcome {{ data.userData.username }}</h4>
    </div>

    <div class="card">
        <div class="home-text">
            <h4 class="margin-10">How it works</h4>
            <p class="margin-10">You can create topic (journal, todo or habit tracker) pages which you organize by category.</p>
            <p class="margin-10">Start by going to <router-link class="link" to="/manage_categories">Manage Categories and Topics</router-link>.</p>
            <p class="margin-10">Here you can create your first category, 
                then add topics to this category and start writing in your journal, 
                keeping track of your habits, 
                and creating todo lists.
            </p>
        </div>
    </div>

    </div>
</template>

<script>

import { mapState, mapMutations } from 'vuex'

export default {
    name: 'home',
    computed: {
        ...mapState(["data"])
    },
    methods: {
        ...mapMutations(["setHeaderTitle"])
    },
    mounted () {
        this.setHeaderTitle('Home')
    }
}

</script>

<style>
</style>