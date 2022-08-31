<template>
    <div class="backdrop" @click="cancelHandler">
        
        <div class="modal flex" @click="dontCancelHandler">
            <font-awesome-icon @click="cancelHandler" class="margin-left-auto" icon='fa-solid fa-xmark' />
            <p><strong>{{ settingsModalData.topic_type }} {{ settingsModalData.entry_type }}</strong> "{{ settingsModalData.name }}"</p>

            <div class="flex-row">
                <span class="input-title">Name</span>
                <input class="input" type="text" v-model=settingsModalData.newName required>
                <font-awesome-icon icon="fa-solid fa-trash" class="margin-3-padding-3" @click="deleteHandler" />
                <font-awesome-icon icon="fa-solid fa-floppy-disk" class="margin-3-padding-3" @click="confirmHandler"/>
            </div>

        </div>
    </div>
</template>

<script>

import { mapState, mapActions, mapMutations } from 'vuex'

export default {
    name: 'settingsModal',
    data() {
        return {
            dontCancel: false
        }
    },
    computed: {
        ...mapState(["settingsModalData"])
    },
    methods: {
        ...mapMutations(["toggleSettingsModal", "setModalPayload", "toggleModal", "resetSettingsModalData"]),
        ...mapActions(["sendEntryDataRequest"]),
        cancelHandler() {
            if (!this.dontCancel) {
                this.toggleSettingsModal()
                this.resetSettingsModalData()                
            }
            this.dontCancel = false
        },
        dontCancelHandler() {
            this.dontCancel = true
        },
        confirmHandler() {
            this.toggleSettingsModal()
            this.sendEntryDataRequest(['PUT', {type: this.settingsModalData.entry_type, name: this.settingsModalData.newName, id: this.settingsModalData.id}])
            this.resetSettingsModalData()
        },
        deleteHandler() {
            this.setModalPayload({func: this.sendEntryDataRequest, payload: ['DELETE', {type: this.settingsModalData.entry_type, id: this.settingsModalData.id}]})
            this.toggleSettingsModal()
            this.resetSettingsModalData()
            this.toggleModal()
        }
    }
}

</script>

<style>

</style>