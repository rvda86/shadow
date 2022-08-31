<template>
    <div>

        <div class="card card-grey">

            <h4>Journal</h4>
            <p>{{ topic.name }} <font-awesome-icon @click="showSettings" icon="fa-solid fa-gear" /></p>

        </div>

        <div class="card card-grey">
            <button class="button" v-show="!showNewEntry" @click="toggleNewEntry">New Entry</button>
            <div v-show="showNewEntry">
                <form class="flex" @submit.prevent="submitHandler">
                    <font-awesome-icon @click="toggleNewEntry" class="margin-left-auto" icon='fa-solid fa-xmark' />
                    <input class="input" type="text" placeholder="title" v-model="title">
                    <ckeditor :editor="editor" v-model="editorData" :config="editorConfig"></ckeditor>
                    <button class="button">Create new entry</button>
                </form>
          </div>
        </div>

        <div :key="entry.id" v-for="entry in topic.entries">
            <EntryJournal :entry=entry />
        </div>

    </div>
</template>

<script>

import { mapActions, mapMutations } from 'vuex'

import EntryJournal from './journal/EntryJournal.vue'
import SettingsModal from '../settings/SettingsModal.vue'

import ClassicEditor from '@ckeditor/ckeditor5-build-classic';


export default {
    name: 'Journal',
    components: {
      EntryJournal,
      SettingsModal
    },
    data() {
        return {
            title: '',
            content: '',
            showNewEntry: false,
            editor: ClassicEditor,
            editorData: '',
            editorConfig: {
                toolbar: { shouldNotGroupWhenFull: true }
                }
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
    toggleNewEntry() {
        this.showNewEntry = !this.showNewEntry
    },
    submitHandler(){
        if (this.title.length === 0) {
            this.setFlashMessage("title is required")
        } else {
            this.sendEntryDataRequest(['POST', {type: 'journal', title: this.title, content: this.editorData, topic_id: this.topic.id}])
            this.title = ''
            this.content = ''
            this.toggleNewEntry()
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