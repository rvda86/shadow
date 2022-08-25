<template>
<div>

    <SettingsModal v-show="showSettingsModal" />

    <div class="card">

        <h4>ToDo</h4>
        <p>{{ topic.name }} <font-awesome-icon @click="showSettings" icon="fa-solid fa-gear" /></p>

    </div>

    <div class="card">
        <button class="button" @click="toggleNewTask">New Task</button>
        <div v-show="showNewTask">
             <form class="flex" @submit.prevent="submitHandler">
                <input class="input" type="text" placeholder="task" v-model="task" required>
                <p>Due date:</p>
                <input type="date" v-model="dueDate">
                <button class="button">Submit</button>
            </form>
            <button class="button-small background-red" @click="toggleNewTask">Cancel</button>
        </div>

        <a href="#" class="link" @click="toggleShowCompleted">{{ showCompleted ? 'Hide completed' : 'Show Completed' }}</a>
    </div>

    <div :key="entry.id" v-for="entry in topic.entries" v-show="(((entry.completed == '1' && showCompleted) || (entry.completed == '0')) ? true : false)">
        <EntryTodo :entry=entry />
    </div>

</div>

</template>

<script>

import { mapState, mapActions, mapMutations } from 'vuex'

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
            dueDate: '',
            showNewTask: false,
            showCompleted: false
        }
    },
    computed: {
        ...mapState(["showSettingsModal"]),
        topic() {
            for (let category of this.$store.state.data.categories) {
                for (let topic of category.topics) {
                    if (topic.id == this.$route.params.topicId) {
                        return topic
                    }
                }
            }
        }
    },
    methods: {
        ...mapActions(["sendEntryDataRequest"]),
        ...mapMutations(["setHeaderTitle", "toggleSettingsModal", "setSettingsModalData"]),
        toggleNewTask() {
            this.showNewTask = !this.showNewTask
        },
        submitHandler(){
            this.sendEntryDataRequest(['POST', {type: 'todo', task: this.task, due_date: this.dueDate, topic_id: this.topic.id}])
            this.title = ''
            this.dueDate = ''
            this.toggleNewTask()
        },
        toggleShowCompleted() {
            this.showCompleted = !this.showCompleted
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