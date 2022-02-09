import { createRouter, createWebHistory } from 'vue-router'
import store from '../store/store'

import ManageCategories from '../components/pages/ManageCategories.vue'
import ManageAccount from '../components/pages/ManageAccount.vue'
import Journal from '../components/pages/Journal.vue'
import Todo from '../components/pages/Todo.vue'
import CreateAccount from '../components/pages/CreateAccount.vue'
import Login from '../components/pages/Login.vue'
import Home from '../components/pages/Home.vue'
import NotFound from '../components/pages/NotFound.vue'

function checkExpiration(to, from, next, authRequired) {
  let expiration_time = localStorage.getItem('expires')
  if (Date.now() < expiration_time) {    
    if (authRequired) next()
    else next ('/home')   
  } else {
    if (authRequired) next('/login')
    else next()
    store.state.authenticated = false
  }
}

const routes = [
  { path: '/', 
    redirect: '/home'
   },
  { path: '/topics/journal/:topicId', 
    name: 'journal', 
    component: Journal,
    beforeEnter: (to, from, next) => {
        checkExpiration(to, from, next, true)
    }
  },
  { path: '/topics/todo/:topicId', 
    name: 'todo', 
    component: Todo,
    beforeEnter: (to, from, next) => {
       checkExpiration(to, from, next, true)
    }
  },
  { path: '/join', 
    name: 'createAccount', 
    component: CreateAccount,
    beforeEnter: (to, from, next) => {
       checkExpiration(to, from, next, false)
    }
  },
  { path: '/login', 
    name: 'login', 
    component: Login,
    beforeEnter: (to, from, next) => {
        checkExpiration(to, from, next, false)
    }
  },
  { path: '/home',
    name: 'home',
    component: Home,
    beforeEnter: (to, from, next) => {
        checkExpiration(to, from, next, true)
    }
  },
  { path: '/manage_categories', 
    name: 'manageCategories', 
    component: ManageCategories,
    beforeEnter: (to, from, next) => {
        checkExpiration(to, from, next, true)
    }
  },
  { path: '/manage_account', 
    name: 'manageAccount', 
    component: ManageAccount,
    beforeEnter: (to, from, next) => {
        checkExpiration(to, from, next, true)
  }
},
  { path: '/:pathMatch(.*)*', 
    name: 'notFound', 
    component: NotFound
  } 
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
