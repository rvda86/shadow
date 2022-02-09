<template>
    <div class="card">

        <div v-show="!editing">
            <h3>{{ entry.title }}</h3>
            <button class="button-small" @click="toggleEditing">Edit</button>
            <button class="button-small background-red" @click="deleteHandler">Delete</button>
            <p class="small-font">Created: {{ entry.date_posted }}</p>
            <p class="small-font">{{ (entry.date_edited) ? 'Edited:' : '' }} {{entry.date_edited}} </p>
            <p><Markdown :source=entry.content /></p>
        </div>

        <div v-show="editing">
            <form class="flex" @submit.prevent="updateHandler">
                <span>Title</span>
                <input class="input" type="text" placeholder="title" v-model="title" required>
                <span>Content</span>
                <textarea class="textarea" placeholder="content" v-model="content" required></textarea>
                <button class="button">Save</button>
            </form>
            <button class="button-small background-red" @click="toggleEditing">Cancel</button>
        </div>

    </div>
</template>

<script>

import { mapMutations, mapActions } from 'vuex'
import Markdown from 'vue3-markdown-it'

export default {
    name: 'EntryJournal',
    data() {
        return {
            editing: false,
            title: this.entry.title,
            content: this.entry.content
        }
    },
    props: {
        entry: Object
    },
    components: {
        Markdown
    },
    methods: {
        ...mapActions(["sendEntryDataRequest"]),
        ...mapMutations(["toggleModal", "setModalPayload"]),
        toggleEditing() {
            this.editing = !this.editing
        },
        updateHandler() {
            this.setModalPayload({func: this.sendEntryDataRequest, payload: ['PUT', {type: 'journal', title: this.title, content: this.content, id: this.entry.id}]})
            this.toggleModal()
            this.toggleEditing()
        },
        deleteHandler() {
            this.setModalPayload({func: this.sendEntryDataRequest, payload: ['DELETE', {type: 'journal', id: this.entry.id}]})
            this.toggleModal()
        }
    }
}

</script>