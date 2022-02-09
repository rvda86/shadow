<template>
    
    <div>

    <UpdateAccount :userData=data.userData />
    <DeleteAccount :userData=data.userData />

    </div>


</template>

<script>

import { mapState, mapMutations } from 'vuex'

import UpdateAccount from './manage_account/UpdateAccount.vue'
import DeleteAccount from './manage_account/DeleteAccount.vue'

export default {
    name: 'Settings',
    components: {
        UpdateAccount,
        DeleteAccount
    },
    computed: {
        ...mapState(["data"]),
    },
    methods: {
        ...mapMutations(["setHeaderTitle"])
    },
    mounted () {
        this.setHeaderTitle('Manage Your Account')
  }
}

</script>

<style>

</style>