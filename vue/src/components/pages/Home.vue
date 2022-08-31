<template>
    <div class="card"> 
        <h3>Welcome {{ data.userData.username }}</h3>
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