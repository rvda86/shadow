<template>
    <div id="grid">
        <Modal v-show="showModal"/>

        <header v-show="authenticated" id="header">
            <HeaderAuth />
        </header>
        <header v-show="!authenticated" id="header">
            <Header />
        </header>
        <main id="main">
          <nav v-show="showMenu">
            <Menu />
          </nav>
          <FlashMessage v-show="showFlashMessage" />
          <slot></slot>
        </main>
    </div>
</template>

<script>

import { mapState } from 'vuex'
import HeaderAuth from './HeaderAuth.vue'
import Header from './Header.vue'
import Menu from './Menu.vue'
import FlashMessage from '../ui/FlashMessage.vue'
import Modal from '../ui/Modal.vue'

export default {
  name: 'Layout',
  components: {
      Header,
      HeaderAuth,
      Menu,
      FlashMessage,
      Modal
  },
  computed: {
      ...mapState(["authenticated", "showMenu", "showFlashMessage", "showModal", "showJournalSettingsModal"])
  }
}
</script>

<style>
html { box-sizing: border-box; }
* { box-sizing: inherit; }

body {
    margin: 0;
    font-size: 100%;
    font-family: sans-serif;
    background-color:rgb(245, 245, 245);
    background-color: #eff7fa;
}
#grid {
    display: grid;
    grid-template-rows: 1fr auto;
    grid-template-areas: 
        "header"
        "main";
}
#header {
    grid-area: header;
    margin: 0;
    padding: 5px;
}
#main{
    grid-area: main;
    margin: 0;
    padding: 0;
}

.card {
  margin: 10px auto;
  padding: 10px;
  max-width: 800px;
  background-color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.flex {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.flex-row {
  display: flex;
  flex-direction: row;
}

.input {
  margin: 3px;
  padding: 5px;
}

.input-title {
  margin: 3px;
  padding: 5px;
}

.textarea {
  min-width: 300px;
  min-height: 300px;
}

.w-200 {
  width: 200px;
}

h4, h5 {
  margin: 2px;
}

.button {
  background-color: #1b4e8c;
  color: white;
  font-weight: 600;
  padding: 10px;
  margin: 5px;
  border: 0;
  border-radius: 5px;
}

.button-small {
  background-color: #1b4e8c;
  color: white;
  padding: 8px;
  margin: 0 5px;
  border: 0;
  border-radius: 5px;
}

.background-red {
  background-color: #ce2316;
}

.small-font {
  font-size: 0.8em;
}

.medium-font {
  font-size: 1em;
}

.link {
  color: blue;
  text-decoration: none;
  margin: 0 2px;
}

.link-red {
  color: red;
  text-decoration: none;
  margin: 0 2px;
}

p {
  margin: 0;  
}

.feedback-message {
    font-size: 0.8em;
    font-weight: 600;
    margin: 3px;
    color: red
}

.backdrop {
    position: fixed;
    left: 0;
    top: 0;
    height: 100%;
    width: 100%;
    background-color: rgba(109, 109, 109, 0.8);
    z-index: 1
}


.modal {
    position: relative;
    display: flex;
    top: 20%;
    margin: auto;
    padding: 1em;
    max-width: 400px;
    background-color: white;
    z-index: 999
}


</style>