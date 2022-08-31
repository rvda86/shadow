<template>

<div>
    <div class="card card-grey">
        <h4>Add a new category</h4>

        <form class="flex" @submit.prevent="submitHandler">
                <input class="input" type="text" v-model="newCategoryName" placeholder="new category" required>
                <button class="button">Add</button>
        </form>
    </div>

    <div :key="category.id" v-for="category in data.categories">
        <Category :category=category />
    </div>
</div>

</template>

<script>

import Category from './manage_categories/Category.vue'

import { mapState, mapActions, mapMutations } from 'vuex'

export default {
    name: 'Settings',
    components: {
        Category
    },
    data() {
        return {
            newCategoryName: ''
        }
    },
    computed: {
        ...mapState(["data"])
    },
    methods: {
        ...mapActions(["sendEntryDataRequest"]),
        ...mapMutations(["setHeaderTitle"]),
        submitHandler() {
            this.sendEntryDataRequest(['POST', {type: 'category', name: this.newCategoryName}])
            this.newCategoryName = ''
        }
    },
    mounted() {
        this.setHeaderTitle('Manage Categories and Topics')
    }
}

</script>

<style>
</style>