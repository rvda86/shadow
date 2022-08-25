<template>
    <div class="backdrop">
        
        <div class="modal flex">
            <h5> edit {{ topicSettingsModalData.name }} - {{ topicSettingsModalData.topic_type }}</h5>

            <div class="flex-row">
                <span class="input-title">Name</span>
                <input class="input" type="text" v-model=topicSettingsModalData.newName required>
            </div>

            <div class="flex-row">
                <button class="button background-red" @click="deleteHandler">Delete {{ topicSettingsModalData.topic_type }} </button>
                <button class="button" @click="cancelHandler">Cancel</button>
                <button class="button" @click="confirmHandler">Save</button>
            </div>

        </div>
    </div>
</template>

<script>

import { mapState, mapActions, mapMutations } from 'vuex'

export default {
    name: 'TopicSettingsModal',
    computed: {
        ...mapState(["topicSettingsModalData"])
    },
    methods: {
        ...mapMutations(["toggleTopicSettingsModal", "setModalPayload", "toggleModal"]),
        ...mapActions(["sendEntryDataRequest"]),
        cancelHandler() {
            this.toggleTopicSettingsModal()
        },
        confirmHandler() {
            this.toggleTopicSettingsModal()
            this.sendEntryDataRequest(['PUT', {type: this.topicSettingsModalData.entry_type, name: this.topicSettingsModalData.newName, id: this.topicSettingsModalData.id}])
        },
        deleteHandler() {
            this.setModalPayload({func: this.sendEntryDataRequest, payload: ['DELETE', {type: this.topicSettingsModalData.entry_type, id: this.topicSettingsModalData.id}]})
            this.toggleTopicSettingsModal()
            this.toggleModal()
        }
    }
}

</script>

<style>

</style>