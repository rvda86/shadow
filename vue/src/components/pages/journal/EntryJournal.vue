<template>
    <div class="card">

        <div class="journal-entry" v-show="!editing">
            <div class="flex-row">
                <h4 class="margin-right-auto">{{ entry.title }}</h4>
                <font-awesome-icon class="margin-right-10" icon="fa-solid fa-pen" @click="toggleEditing" />
                <font-awesome-icon icon="fa-solid fa-trash" @click="deleteHandler" />
            </div>
            <p class="small-font text-grey">Created: {{ entry.date_posted }}</p>
            <p class="small-font text-grey">{{ (entry.date_edited) ? 'Last Edited:' : '' }} {{entry.date_edited}} </p>
            <p v-bind:id="entry.id">  </p>
        </div>

        <div v-show="editing">
                <form class="flex" @submit.prevent="updateHandler">
                    <input class="input" type="text" placeholder="title" v-model="title" required>
                    <ckeditor :editor="editor" v-model="editorData" :config="editorConfig"></ckeditor>
                    <button class="button">Submit</button>
                </form>
                <button class="button-small background-red" @click="toggleEditing">Cancel</button>
        </div>

    </div>
</template>

<script>

import { mapMutations, mapActions } from 'vuex'
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';

export default {
    name: 'EntryJournal',
    data() {
        return {
            editing: false,
            title: this.entry.title,
            content: this.entry.content,
            editor: ClassicEditor,
            editorData: this.entry.content,
            editorConfig: {
                toolbar: { shouldNotGroupWhenFull: true }
                }
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
            this.setModalPayload({func: this.sendEntryDataRequest, payload: ['PUT', {type: 'journal', title: this.title, content: this.editorData, id: this.entry.id}]})
            this.toggleModal()
            this.toggleEditing()
        },
        deleteHandler() {
            this.setModalPayload({func: this.sendEntryDataRequest, payload: ['DELETE', {type: 'journal', id: this.entry.id}]})
            this.toggleModal()
        }
    },
    mounted() {
        const content = document.getElementById(this.entry.id)
        content.innerHTML = this.entry.content
    }
}

</script>