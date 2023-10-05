import './plugins/axios';
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import Toaster from "@meforma/vue-toaster";
import './assets/css/theme.scss'
import langService from './services/langService';

const app = createApp(App);
app.config.globalProperties.$t = langService.translate;
app.use(router);
app.use(Toaster, {
    duration: "1000",
});
app.mount("#app");