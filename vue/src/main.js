import { createApp } from 'vue'
import Markdown from 'vue3-markdown-it';
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faGear, faSpinner } from '@fortawesome/free-solid-svg-icons'

import App from './App.vue'
import store from './store/store'
import router from './router/router'

library.add(faGear)
library.add(faSpinner)

const app = createApp(App).component('font-awesome-icon', FontAwesomeIcon)
app.use(store)
app.use(router)
app.use(Markdown)
app.mount('#app')


