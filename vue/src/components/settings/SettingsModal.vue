<template>
    <div class="backdrop">
        
        <div class="modal flex">
            <h5> {{ settingsModalData.name }} - {{ settingsModalData.topic_type }} {{ settingsModalData.entry_type }}</h5>

            <div class="flex-row">
                <span class="input-title">Name</span>
                <input class="input" type="text" v-model=settingsModalData.newName required>
            </div>

            <div class="flex-row">
                <button class="button background-red" @click="deleteHandler">Delete {{ settingsModalData.topic_type }} {{ settingsModalData.entry_type }}</button>
                <button class="button" @click="cancelHandler">Cancel</button>
                <button class="button" @click="confirmHandler">Save</button>
            </div>

        </div>
    </div>
</template>

<script>

import { mapState, mapActions, mapMutations } from 'vuex'

export default {
    name: 'settingsModal',
    computed: {
        ...mapState(["settingsModalData"])
    },
    methods: {
        ...mapMutations(["toggleSettingsModal", "setModalPayload", "toggleModal"]),
        ...mapActions(["sendEntryDataRequest"]),
        cancelHandler() {
            this.toggleSettingsModal()
        },
        confirmHandler() {
            this.toggleSettingsModal()
            this.sendEntryDataRequest(['PUT', {type: this.settingsModalData.entry_type, name: this.settingsModalData.newName, id: this.settingsModalData.id}])
        },
        deleteHandler() {
            this.setModalPayload({func: this.sendEntryDataRequest, payload: ['DELETE', {type: this.settingsModalData.entry_type, id: this.settingsModalData.id}]})
            this.toggleSettingsModal()
            this.toggleModal()
        }
    }
}

</script>

<style>

</style>