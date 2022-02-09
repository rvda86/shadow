<template>
    <div class="card">

        <div class="flex-row" v-show="!editing">
            <input type="checkbox" v-model="completed" @click="updateHandlerCompleted">
            <div>
                <p><b>{{ entry.task }}</b></p>
                <p>Due: {{ entry.due_date }}</p>
            </div>
            <button class="button-small" @click="toggleEditing">Edit</button>
            <button class="button-small background-red" @click="deleteHandler">Delete</button>       
        </div>

        <div v-show="editing">

            <p>Edit Task</p>
            <form class="flex" @submit.prevent>
                <p>Task:<input class="input" type="text" placeholder="task" v-model="task" required></p>
                <p>Due date:<input type="date" v-model="dueDate"></p>
                <p>Completed:<input type="checkbox" v-model="completed"></p>
                <div class="flex-row">
                    <button class="button background-red" @click="toggleEditing">Cancel</button>
                    <button class="button" @click="updateHandler">Save</button>
                </div>
            </form>
        </div>

    </div>
</template>

<script>

import { mapMutations, mapActions } from 'vuex'

export default {
    name: 'EntryTodo',
    data() {
        return {
            editing: false,
            task: this.entry.task,
            dueDate: this.entry.due_date,
            completed: (this.entry.completed == 0 ) ? false : true
        }
    },
    props: {
        entry: Object
    },
    methods: {
        ...mapActions(["sendEntryDataRequest"]),
        ...mapMutations(["toggleModal", "setModalPayload"]),
        toggleEditing() {
            this.editing = !this.editing
        },
        updateHandler() {
            this.completed = this.completed ? '1' : '0'
            this.sendEntryDataRequest(['PUT', {type: 'todo', task: this.task, due_date: this.dueDate, completed: this.completed, id: this.entry.id}])
            this.toggleEditing()
        },
        deleteHandler() {
            this.setModalPayload({func: this.sendEntryDataRequest, payload: ['DELETE', {type: 'todo', id: this.entry.id}]})
            this.toggleModal()
        },
        updateHandlerCompleted() {
            this.completed = !this.completed
            this.sendEntryDataRequest(['PUT', {type: 'todo', task: this.task, due_date: this.dueDate, completed: this.completed ? '1' : '0', id: this.entry.id}])
        }
    }
}

</script>