import { createApp } from 'vue'
import Markdown from 'vue3-markdown-it';
import CKEditor from '@ckeditor/ckeditor5-vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faGear, faSpinner, faPen, faTrash, faPlus, faCheck, faXmark, faAngleLeft, faAngleRight, faHouse, faFloppyDisk} from '@fortawesome/free-solid-svg-icons'

import App from './App.vue'
import store from './store/store'
import router from './router/router'

library.add(faGear)
library.add(faSpinner)
library.add(faPen)
library.add(faTrash)
library.add(faPlus)
library.add(faCheck)
library.add(faXmark)
library.add(faAngleLeft)
library.add(faAngleRight)
library.add(faHouse)
library.add(faFloppyDisk)

const app = createApp(App).component('font-awesome-icon', FontAwesomeIcon)
app.use(store)
app.use(router)
app.use(Markdown)
app.use(CKEditor)
app.mount('#app')


