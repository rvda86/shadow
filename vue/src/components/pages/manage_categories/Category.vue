<template>

    <div class="card">
        
        <p><b>Category</b> {{ category.name }}</p>
        <div class="flex-row" v-show="!editing">
            <button class="button-small" @click="toggleEditing">Edit Category</button>
            <button class="button-small background-red" @click="deleteCategoryHandler">Delete Category</button>
        </div>
            <p class="feedback-message" v-show="showDeleteCategoryError">{{ deleteCategoryErrorMsg }}</p>

        <div v-show="editing">
            <form class="flex-row" @submit.prevent="updateCategoryHandler">
                <span>Name</span>
                <input class="input" type="text" v-model=categoryName required>
                <button class="button">Save</button>
            </form>
            <button class="button-small background-red" @click="toggleEditing">Cancel</button>
        </div>

        <p>{{ (category.topics.length > 0) ? 'Topics in this category' : 'There are no topics, try adding one' }}</p>
        <div :key="topic.id" v-for="topic in category.topics">
            <Topic :topic=topic />
        </div>   

        <h5>Add a new topic</h5>

        <form class="flex" @submit.prevent="createTopicHandler">
                <input class="input" type="text" v-model="newTopicName" placeholder="new topic" required>
                <select v-model=topicType required>
                    <option value="" selected disabled>Select topic type</option>
                    <option>{{ topicTypes[0] }}</option>
                    <option>{{ topicTypes[1] }}</option>
                </select>
                <button class="button">Add Topic</button>
        </form>

    </div>


</template>

<script>

import { mapState, mapActions, mapMutations } from 'vuex'

import Topic from "./Topic.vue"

export default {
    name: 'Category',
    data() {
        return {
            categoryName: this.category.name,
            newTopicName: '',
            showDeleteCategoryError: false,
            deleteCategoryErrorMsg: "There are still topics in this category",
            topicType: '',
            editing: false
        }
    },
    components: {
        Topic
    },
    computed: {
        ...mapState(["topicTypes"])
    },
    props: {
        category: Object
    },
    methods: {
        ...mapMutations(["toggleModal", "setModalPayload"]),
        ...mapActions(["sendEntryDataRequest"]),
        toggleEditing() {
            this.editing = !this.editing
        },
        createTopicHandler(){
            this.sendEntryDataRequest(['POST', {type: 'topic', topic_type: this.topicType, name: this.newTopicName, category_id: this.category.id}])
            this.newTopicName = ''  
        },
        updateCategoryHandler(){
           this.sendEntryDataRequest(['PUT', {type: 'category', name: this.categoryName, id: this.category.id}])
           this.toggleEditing()
        },
        deleteCategoryHandler(){
            if (this.category.topics.length > 0) {
                this.showDeleteCategoryError = true
                setTimeout( () => this.showDeleteCategoryError = false, 5000)
            } else {
                this.setModalPayload({func: this.sendEntryDataRequest, payload: ['DELETE', {type: 'category', id: this.category.id}]})
                this.toggleModal()
            }
        }
    }
}

</script>

<style>

.settings-category {
    padding: 10px;
    margin: 5px;
    border: 1px solid;
    border-color:rgb(245, 245, 245);
}

</style>