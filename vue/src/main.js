import { createApp } from 'vue'
import Markdown from 'vue3-markdown-it';

import App from './App.vue'
import store from './store/store'
import router from './router/router'

const app = createApp(App)
app.use(store)
app.use(router)
app.use(Markdown)
app.mount('#app')

