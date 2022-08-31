<template>
    <div>

        <div class="card card-grey">

            <h4>Habits</h4>
            <p>{{ topic.name }} <font-awesome-icon @click="showSettings" icon="fa-solid fa-gear" /></p>

        </div>
        
        <div class="card card-grey">
            <div>
                <input class="input" type="text" placeholder="Add a habit" v-model="name" required>
                <font-awesome-icon icon="fa-solid fa-plus" @click="addHabitHandler"/>
            </div>        
        </div>

        <div :key="entry.id" v-for="entry in topic.entries">
            <EntryHabit :entry=entry :topic=topic />
        </div>

    </div>
</template>

<script>

import { mapActions, mapMutations } from 'vuex'

import SettingsModal from '../settings/SettingsModal.vue'
import EntryHabit from './habit/EntryHabit.vue'

export default {
    name: 'Habit',
    components: {
      SettingsModal,
      EntryHabit
    },
    data() {
        return {
            name: '',
            content: ''
            }
    },
    computed: {
        topic() {
            for (let category of this.$store.state.data.categories) {
                for (let topic of category.topics) {
                    if (topic.id == this.$route.params.topicId) {
                        return topic
                    }
                }
            }
        },
    },
    methods: {
        ...mapActions(["sendEntryDataRequest"]),
        ...mapMutations(["setHeaderTitle", "toggleSettingsModal", "setSettingsModalData", "setFlashMessage"]),
        addHabitHandler(){
            if (this.name.length === 0) {
                this.setFlashMessage("enter habit's name")
            } else {
            this.sendEntryDataRequest(['POST', {type: 'habit', name: this.name, topic_id: this.topic.id}])
            this.name = ''
            }
        },
        showSettings() {
            this.setSettingsModalData(this.topic)
            this.toggleSettingsModal()
        }
    },
    updated() {
            this.setHeaderTitle(this.topic.name)
    },
    mounted() {
            this.setHeaderTitle(this.topic.name)
    }
}
</script>

<style>
</style>