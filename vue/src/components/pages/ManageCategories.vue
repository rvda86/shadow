<template>

<div>
    <div class="card card-grey">
        <h5>Add a new category</h5>

        <div class="flex-row">
                <input class="input" type="text" v-model="newCategoryName" placeholder="new category">
                <font-awesome-icon class="margin-3-padding-3" icon="fa-solid fa-plus" @click="submitHandler"/>
        </div>
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
        ...mapMutations(["setHeaderTitle", "setFlashMessage"]),
        submitHandler() {
            if (this.newCategoryName.length === 0) {
                this.setFlashMessage("enter category's name")
            } else {
            this.sendEntryDataRequest(['POST', {type: 'category', name: this.newCategoryName}])
            this.newCategoryName = ''
            }
        }
    },
    mounted() {
        this.setHeaderTitle('Manage Categories and Topics')
    }
}

</script>

<style>
</style>