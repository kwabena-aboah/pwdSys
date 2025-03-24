import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import store from './store';
import instance from './api/axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'bootstrap';
import Vue3Toastify from "vue3-toastify";
import "vue3-toastify/dist/index.css";

function scheduleTokenRefresh() {
    const tokenExpiry = store.getters.tokenExpiry;

    if (tokenExpiry) {
        const now = Date.now();
        const timeUntilExpiry = tokenExpiry - now;

        if (timeUntilExpiry > 0) {
            setTimeout(async () => {
                try {
                    const refreshToken = store.getters.refreshToken;
                    const response = await instance.post("http://127.0.0.1:8000/api/token/refresh/", {
                        refresh: refreshToken,
                    });

                    const { access } = response.data;
                    store.dispatch("saveTokens", { accessToken: access, refreshToken });
                    scheduleTokenRefresh();
                } catch (error) {
                    console.error("Token refresh failed:", error);
                    store.dispatch("logout");
                }
            }, timeUntilExpiry - 60000); // Refresh 1 minute before expiry
        }
    }
}

scheduleTokenRefresh();

createApp(App).use(router).use(store, Vue3Toastify).mount('#app')
