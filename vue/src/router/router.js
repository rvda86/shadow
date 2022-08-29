import { createRouter, createWebHistory } from 'vue-router'
import store from '../store/store'

import ManageCategories from '../components/pages/ManageCategories.vue'
import ManageAccount from '../components/pages/ManageAccount.vue'
import Journal from '../components/pages/Journal.vue'
import Todo from '../components/pages/Todo.vue'
import CreateAccount from '../components/pages/CreateAccount.vue'
import Login from '../components/pages/Login.vue'
import Index from '../components/pages/Index.vue'
import Home from '../components/pages/Home.vue'
import NotFound from '../components/pages/NotFound.vue'
import PasswordReset from '../components/pages/PasswordReset.vue'
import RequestPasswordReset from '../components/pages/RequestPasswordReset.vue'
import VerifyEmail from '../components/pages/VerifyEmail.vue'

function checkTokenExpiration(to, from, next, authRequired, routeToHomeIfAuthed) {
  let expiration_time = localStorage.getItem('expires')
  if (Date.now() < expiration_time) {  
    if (routeToHomeIfAuthed) {
      next('/home')
    } else {
      next()  
    }
  } else {
    if (authRequired) {
      next('/login')
    } else {
      next()
    }
    store.state.authenticated = false
  }
}

const routes = [
  { path: '/', 
    redirect: '/index'
   },
  { path: '/index', 
   name: 'index', 
   component: Index,
   beforeEnter: (to, from, next) => {
       checkTokenExpiration(to, from, next, false, false)
   }
 },
  { path: '/topics/journal/:topicId', 
    name: 'journal', 
    component: Journal,
    beforeEnter: (to, from, next) => {
        checkTokenExpiration(to, from, next, true, false)
    }
  },
  { path: '/topics/todo/:topicId', 
    name: 'todo', 
    component: Todo,
    beforeEnter: (to, from, next) => {
       checkTokenExpiration(to, from, next, true, false)
    }
  },
  { path: '/join', 
    name: 'createAccount', 
    component: CreateAccount,
    beforeEnter: (to, from, next) => {
       checkTokenExpiration(to, from, next, false, true)
    }
  },
  { path: '/login', 
    name: 'login', 
    component: Login,
    beforeEnter: (to, from, next) => {
        checkTokenExpiration(to, from, next, false, true)
    }
  },
  { path: '/home',
    name: 'home',
    component: Home,
    beforeEnter: (to, from, next) => {
        checkTokenExpiration(to, from, next, true, false)
    }
  },
  { path: '/manage_categories', 
    name: 'manageCategories', 
    component: ManageCategories,
    beforeEnter: (to, from, next) => {
        checkTokenExpiration(to, from, next, true, false)
    }
  },
  { path: '/manage_account', 
    name: 'manageAccount', 
    component: ManageAccount,
    beforeEnter: (to, from, next) => {
        checkTokenExpiration(to, from, next, true, false)
    }
  },
  { path: '/password_reset', 
  name: 'passwordReset', 
  component: PasswordReset,
  beforeEnter: (to, from, next) => {
      checkTokenExpiration(to, from, next, false, false)
    }
  },
  { path: '/request_password_reset', 
  name: 'requestPasswordReset', 
  component: RequestPasswordReset,
  beforeEnter: (to, from, next) => {
      checkTokenExpiration(to, from, next, false, false)
    }
  },
  { path: '/verify_email', 
  name: 'verifyEmail', 
  component: VerifyEmail,
  beforeEnter: (to, from, next) => {
      checkTokenExpiration(to, from, next, false, false)
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
