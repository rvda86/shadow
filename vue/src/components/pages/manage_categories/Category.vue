<template>

    <div class="card">

        <p class="category-settings">
            <strong>{{ category.entry_type }}</strong> {{ category.name }} 
            <font-awesome-icon @click="showSettings" class="margin-left-3" icon="fa-solid fa-gear" />
        </p>
        
        <p class="small-font">{{ (category.topics.length > 0) ? 'Topics in this category' : '' }}</p>

        <div class="margin-top-5" :key="topic.id" v-for="topic in category.topics">
            <Topic :topic=topic />
        </div>   

        <!-- <form class="flex margin-10" @submit.prevent="createTopicHandler">
            <p class="small-font">Add a new topic to this category</p>
            <input class="input" type="text" v-model="newTopicName" placeholder="new topic" required>
            <select v-model=topicType required>
                <option value="" selected disabled>Select topic type</option>
                <option>{{ topicTypes[0] }}</option>
                <option>{{ topicTypes[1] }}</option>
                <option>{{ topicTypes[2] }}</option>
            </select>
            <button class="button">Add</button>
        </form> -->

        <p class="small-font margin-top-5">Add a new topic to this category</p>
        <div class="flex-row">
            <input class="input" type="text" v-model="newTopicName" placeholder="new topic" required>
            <select class="margin-3-padding-3" v-model=topicType required>
                <option value="" selected disabled>Select topic type</option>
                <option>{{ topicTypes[0] }}</option>
                <option>{{ topicTypes[1] }}</option>
                <option>{{ topicTypes[2] }}</option>
            </select>
            <font-awesome-icon class="margin-3-padding-3" icon="fa-solid fa-plus" @click="createTopicHandler"/>
        </div>

    </div>


</template>

<script>

import SettingsModal from '../../settings/SettingsModal.vue'
import { mapState, mapActions, mapMutations } from 'vuex'

import Topic from "./Topic.vue"

export default {
    name: 'Category',
    data() {
        return {
            newTopicName: '',
            topicType: '',
        }
    },
    components: {
        Topic,
        SettingsModal
    },
    computed: {
        ...mapState(["topicTypes"])
    },
    props: {
        category: Object
    },
    methods: {
        ...mapMutations(["toggleSettingsModal", "setSettingsModalData", "setFlashMessage"]),
        ...mapActions(["sendEntryDataRequest"]),
        showSettings() {
            this.setSettingsModalData(this.category)
            this.toggleSettingsModal()
        },
        createTopicHandler(){
            if (this.newTopicName.length === 0) {
                this.setFlashMessage("enter topics's name")
            } else if (this.topicType.length === 0) {
                this.setFlashMessage("select a topic type")
            } else {
            this.sendEntryDataRequest(['POST', {type: 'topic', topic_type: this.topicType, name: this.newTopicName, category_id: this.category.id}])
            this.newTopicName = ''  
            }
        },
     }
}

</script>

<style>
</style>