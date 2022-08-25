<template>

    <div>

        <SettingsModal v-show="showSettingsModal" />
        <p><strong>{{ topic.topic_type }}</strong> {{ topic.name }} <font-awesome-icon @click="showSettings" icon="fa-solid fa-gear" /></p>
        
    </div>

</template>

<script>

import SettingsModal from '../../settings/SettingsModal.vue'
import { mapState, mapMutations } from 'vuex'

export default {
    name: 'TopicSettings',
    components: {
        SettingsModal
    },
    props: {
        topic: Object
    },
    computed: {
        ...mapState(["showSettingsModal"]),
    },
    methods: {
        ...mapMutations(["toggleSettingsModal", "setSettingsModalData"]),
        showSettings() {
            this.setSettingsModalData(this.topic)
            this.toggleSettingsModal()
        }
    }
}

</script>

<style>

</style>