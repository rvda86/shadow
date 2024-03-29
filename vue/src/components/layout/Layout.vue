<template>
    <div id="grid">
        <Modal v-show="showModal"/>
        <SettingsModal v-show="showSettingsModal" />

        <div>
          <Demo />
        </div>

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
import SettingsModal from '../settings/SettingsModal.vue'
import Demo from './Demo.vue'

export default {
  name: 'Layout',
  components: {
      Header,
      HeaderAuth,
      Menu,
      FlashMessage,
      Modal,
      SettingsModal,
      Demo
  },
  computed: {
      ...mapState(["authenticated", "showMenu", "showFlashMessage", "showModal", "showSettingsModal"])
  }
}
</script>

<style>
html { box-sizing: border-box; }
* { box-sizing: inherit; }

body {
    margin: 0;
    font-size: 100%;
    font-family: Helvetica, sans-serif;
    line-height: 1.3;
    background-color:rgb(245, 245, 245);
}
#grid {
    display: grid;
    grid-template-rows: 1fr 1fr auto;
    grid-template-areas: 
        "demo"
        "header"
        "main";
}

#demo {
    grid-area: demo;
    position: fixed;
    width: 100%;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 30px;
    background-color: #1b4e8c;
    color: white;
    font-weight: 1000;
}

#header {
    grid-area: header;
    margin: 0;
    padding: 15px;
}

header {
    position: fixed;
    top: 30px;
    width: 100%;
    margin: 0;
    padding: 0;
    display: flex;
    background-color: white;
    box-shadow: 4px 4px 10px rgb(230, 230, 230);
}

#header-title {
    display: flex;
    margin: auto;
}

.header-nav-right {
    display: flex;
    width: 200px;
    justify-content: right;
}

.header-nav-right-menu {
    display: flex;
    width: 75px;
    justify-content: right;
}

.header-nav-left {
    display: flex;
    width: 75px;
    justify-content: left;
}

.header-item {
    margin: auto 5px;
    padding: 5px;
    color: black;
    text-decoration: none;
    font-size: 0.8em;
    font-weight: 550;
}

.hamburger-menu {
    width: 20px;
    height: 2px;
    margin: 4px 0;
    background-color: black;
}

#menu {
    background-color: white;
    color: black;
}
.menu-list {
    margin: 0;
    padding: 0;
    list-style-type: none;
    display: flex;
    flex-direction: column;
}
.menu-item {
    margin: 5px;
    padding: 0 5px;
}
.menu-text {
    color: black;
    text-decoration: none;
    font-size: 0.8em;
    font-weight: 400;
}

#main{
    grid-area: main;
    margin: 0;
    margin-top: 100px;
    padding: 0;
}

#index {
    text-align: center;
}

.index-story {
    display: flex;
    justify-content: center;
    margin: 10px;
}

.index-benefits {
    width: 500px;
    padding: 10px;
    margin: 5px 5px;
    background-color: white;
    border-radius: 5%;
}

.index-benefits-img {
    width: 300px;
    border-radius: 5%;
    margin: 5px 5px;
}

.attribute-link {
    font-size: 0.5em;
}

.wrap {
    flex-wrap: wrap;
}

.wrap-reverse {
    flex-wrap: wrap-reverse;
}

.settings-account {
    margin: 10px;
    display: flex;
    flex-direction: column;
}

#settings-categories {
    min-width: 600px;
}

.settings-categories {
    display: flex;
    flex-direction: row;
}

.category-settings {
    margin: 10px;
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

.card-grey {
  background-color: rgb(245, 245, 245);
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

.input, .margin-3-padding-3, .input-title {
  margin: 3px;
  padding: 3px;
}

.input-narrow {
  width: 150px;
}

.input-large {
  padding: 5px;
}

.textarea {
  min-width: 300px;
  min-height: 300px;
}

h4, h5 {
  margin: 2px;
}

.flash-message {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background-color: white;
    padding: 20px;
    border: 1px solid rgb(109, 109, 109);
    border-radius: 3px;
}

.button {
  background-color: #1b4e8c;
  color: white;
  font-weight: 600;
  font-size: 0.8em;
  padding: 10px;
  margin: 5px;
  border: 0;
  border-radius: 3px;
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

a:hover {
  color: black;
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
    max-width: 350px;
    background-color: white;
    z-index: 999
}

.journal-entry, .todo-entry, .habit-entry, .home-text {
    width: 95%;
}

.habit-column {
  width: 20px
}

p {
  margin: 0;  
}

.background-red {
  background-color: #ce2316;
}

.background-green {
  background-color: green;
}

.small-font {
  font-size: 0.8em;
}

.medium-font {
  font-size: 1em;
}

.text-grey {
  color: rgb(50, 50, 50);
}

.text-center {
  text-align: center;
}

.margin-10 {
    margin: 10px;
}

.margin-top-5 {
  margin-top: 5px;
}

.margin-right-10 {
  margin-right: 10px;
}

.margin-left-3 {
  margin-left: 3px;
}

.margin-right-auto {
  margin-right: auto;
}

.margin-left-auto {
  margin-left: auto;
}

.w-200 {
  width: 200px;
}

.load-spinner {
    animation: spin 1s infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media screen and (max-width: 800px) {
    .index-benefits {
        width: 300px;
    }

    .index-benefits-img {
        width: 300px;
    }
}

</style>