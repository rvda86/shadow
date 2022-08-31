<template>

    <div>
        <p>
            {{ topic.topic_type }}
            <router-link class="link" :to="{name: topic.topic_type, params: { topicId: topic.id }}">{{ topic.name }}</router-link>
            <font-awesome-icon @click="showSettings" class="margin-left-3" icon="fa-solid fa-gear" />
        </p>
    </div>

</template>

<script>

import SettingsModal from '../../settings/SettingsModal.vue'
import { mapMutations } from 'vuex'

export default {
    name: 'TopicSettings',
    components: {
        SettingsModal
    },
    props: {
        topic: Object
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