<template>
    <div class="card">

        <div class="flex-row todo-entry" v-show="!editing">
            <input class="margin-right-10" type="checkbox" v-model="completed" @click="updateHandlerCompleted">
            <p class="margin-right-auto">{{ entry.task }}</p>
            <font-awesome-icon class="margin-right-10" icon="fa-solid fa-pen" @click="toggleEditing"/>
            <font-awesome-icon icon="fa-solid fa-trash" @click="deleteHandler" />
        </div>

        <div class="flex-row todo-entry" v-show="editing">
            <input class="input margin-right-auto" type="text" placeholder="task" v-model="task" required>
            <font-awesome-icon icon="fa-solid fa-floppy-disk" class="margin-3-padding-3" @click="updateHandler"/>
            <font-awesome-icon icon="fa-solid fa-xmark" class="margin-3-padding-3" @click="toggleEditing" />
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
            completed: (this.entry.completed == 0 ) ? false : true
        }
    },
    props: {
        entry: Object
    },
    methods: {
        ...mapActions(["sendEntryDataRequest"]),
        ...mapMutations(["toggleModal", "setModalPayload", "setFlashMessage"]),
        toggleEditing() {
            this.editing = !this.editing
        },
        updateHandler() {
            if (this.task.length === 0) {
                this.setFlashMessage("task name required")
            } else {
            this.completed = this.completed ? '1' : '0'
            this.sendEntryDataRequest(['PUT', {type: 'todo', task: this.task, completed: this.completed, id: this.entry.id}])
            this.toggleEditing()
            }
        },
        deleteHandler() {
            this.setModalPayload({func: this.sendEntryDataRequest, payload: ['DELETE', {type: 'todo', id: this.entry.id}]})
            this.toggleModal()
        },
        updateHandlerCompleted() {
            this.completed = !this.completed
            this.sendEntryDataRequest(['PUT', {type: 'todo', task: this.entry.task, completed: this.completed ? '1' : '0', id: this.entry.id}])
        }
    }
}

</script>