import { createApp } from 'vue'
import { createPinia } from 'pinia'
import '@coreui/coreui/dist/css/coreui.min.css'
import './styles/index.scss'


import App from './App.vue'
import router from './router'

import { CIcon } from '@coreui/icons-vue';

import {

    cibNetflix,
    cibAmazon,
    cibCrunchyroll,
    cibYoutube
    
} from '@coreui/icons'

const icons = {
    cibNetflix,
    cibAmazon,
    cibCrunchyroll,
    cibYoutube
    
}

const app = createApp(App)

app.provide('icons', icons)
app.component('CIcon', CIcon)

app.use(createPinia())
app.use(router)

app.mount('#app')
