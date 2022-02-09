<template>

    <div class="card">
        
        <div class="flex-row" v-show="!editing">
            <div>
                <p class="w-200">Name: {{ topic.name }}</p>
                <p class="w-200">Type: {{ topic.topic_type }}</p>
            </div>
            <button class="button-small" @click="toggleEditing">Edit Topic</button>
            <button class="button-small background-red" @click="deleteTopicHandler">Delete Topic</button>
        </div>
            <p class="feedback-message" v-show="showDeleteTopicError">{{ deleteTopicErrorMsg }}</p>

        <div v-show="editing">
            <form class="flex-row" @submit.prevent="updateTopicHandler">
                <span>Name</span>
                <input class="input" type="text" v-model=topicName required>
                <button class="button">Save</button>
            </form>
            <button class="button-small background-red" @click="toggleEditing">Cancel</button>
        </div>

    </div>

</template>

<script>

import { mapActions, mapMutations } from 'vuex'

export default {
    name: 'TopicSettings',
    props: {
        topic: Object
    },
    data() {
        return {
            topicName: this.topic.name,
            showDeleteTopicError: false,
            deleteTopicErrorMsg: "There are still entries in this topic",
            editing: false
        }
    },
    methods: {
        ...mapMutations(["toggleModal", "setModalPayload"]),
        ...mapActions(["sendEntryDataRequest"]),
        toggleEditing() {
            this.editing = !this.editing
        },
        updateTopicHandler(){
           this.sendEntryDataRequest(['PUT', {type: 'topic', name: this.topicName, id: this.topic.id}])
           this.toggleEditing()
        },
        deleteTopicHandler(){
            if (this.topic.entries.length > 0) {
                this.showDeleteTopicError = true
                setTimeout( () => this.showDeleteTopicError = false, 5000)
            } else {
                this.setModalPayload({func: this.sendEntryDataRequest, payload: ['DELETE', {type: 'topic', id: this.topic.id}]})
                this.toggleModal()
            }
        }
    }
}

</script>

<style>

</style>