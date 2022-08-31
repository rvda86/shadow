<template>
<div>

    <div class="card card-grey">
        <h4>ToDo</h4>
        <p>{{ topic.name }} <font-awesome-icon @click="showSettings" icon="fa-solid fa-gear" /></p>
        <a href="#" class="link small-font" @click="toggleShowCompleted">{{ topic.showCompleted ? 'Hide completed' : 'Show Completed' }}</a>
    </div>

    <div class="card card-grey">
        <div>
            <input class="input" type="text" placeholder="Add a task" v-model="task" required>
            <font-awesome-icon icon="fa-solid fa-plus" @click="addToDoHandler"/>
        </div>        
    </div>


    <div :key="entry.id" v-for="entry in topic.entries" v-show="(((entry.completed == '1' && topic.showCompleted) || (entry.completed == '0')) ? true : false)">
        <EntryTodo :entry=entry />
    </div>

</div>

</template>

<script>

import { mapActions, mapMutations } from 'vuex'

import EntryTodo from './todo/EntryTodo.vue'
import SettingsModal from '../settings/SettingsModal.vue'

export default {
    name: 'ToDo',
    components: {
        EntryTodo,
        SettingsModal
    },
    data() {
        return {
            task: '',
            showCompleted: false
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
        toggleNewTask() {
            this.showNewTask = !this.showNewTask
        },
        addToDoHandler(){
            if (this.task.length === 0) {
                this.setFlashMessage("enter task's name")
            } else {
            this.sendEntryDataRequest(['POST', {type: 'todo', task: this.task, topic_id: this.topic.id}])
            this.task = ''
            this.toggleNewTask()
            }
        },
        toggleShowCompleted() {
            this.topic.showCompleted = !this.topic.showCompleted
        },
        showSettings() {
            this.setSettingsModalData(this.topic)
            this.toggleSettingsModal()
        }
    },
    updated() {
        this.setHeaderTitle(this.topic.name)
    },
    mounted () {
        this.setHeaderTitle(this.topic.name)
    }
}
</script>

<style>

</style>