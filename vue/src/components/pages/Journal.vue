<template>
    <div>

        <div class="card">

            <h4>Journal</h4>
            <p>{{ topic.name }} <font-awesome-icon @click="showSettings" icon="fa-solid fa-gear" /></p>

        </div>

        <div class="card">
          <button class="button" @click="toggleNewEntry">New Entry</button>
          <div v-show="showNewEntry">
              <form class="flex" @submit.prevent="submitHandler">
                  <input class="input" type="text" placeholder="title" v-model="title" required>
                  <textarea class="textarea" v-model="content" placeholder="content" required></textarea>
                  <button class="button">Submit</button>
              </form>
              <button class="button-small background-red" @click="toggleNewEntry">Cancel</button>
          </div>
        </div>

        <div :key="entry.id" v-for="entry in topic.entries">
            <EntryJournal :entry=entry />
        </div>

    </div>
</template>

<script>

import { mapState, mapActions, mapMutations } from 'vuex'

import EntryJournal from './journal/EntryJournal.vue'
import SettingsModal from '../settings/SettingsModal.vue'

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
            showNewEntry: false
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
    ...mapMutations(["setHeaderTitle", "toggleSettingsModal", "setSettingsModalData"]),
    toggleNewEntry() {
        this.showNewEntry = !this.showNewEntry
    },
    submitHandler(){
        this.sendEntryDataRequest(['POST', {type: 'journal', title: this.title, content: this.content, topic_id: this.topic.id}])
        this.title = ''
        this.content = ''
        this.toggleNewEntry()
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