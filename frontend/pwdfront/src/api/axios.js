import axios from "axios"
import store from "@/store";

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
// axios.defaults.withCredentials = true;

const instance = axios.create({
    baseURL: "http://127.0.0.1:8000/api",
});

let isRefreshing = false; // tracks if token refresh is in progress
let failedQueue = []; // Queue to store requests while refreshing token

const processQueue = (error, token = null) => {
    failedQueue.forEach((prom) => {
        if(token) {
            prom.resolve(token);
        } else {
            prom.reject(error);
        }
    });
    failedQueue = [];
};

instance.interceptors.request.use((config) => {
    const token = store.getters.accessToken;
    if(token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Interceptor for refreshing token on 401 response
instance.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Check if the error is due to an expired  access token
        if(error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            
            if(isRefreshing) {
                // wait for the token to refresh
                return new Promise((resolve, reject) => {
                    failedQueue.push({
                        resolve: (token) => {
                            originalRequest.headers.Authorization = `Bearer ${token}`;
                            resolve(axios(originalRequest));
                        },
                        reject: (err) => {
                            reject(err);
                        },
                    });
                });
            }

            isRefreshing = true;

            try {
                // Refresh the token
                const refreshToken = store.getters.refreshToken;
                const response = await axios.post("http://127.0.0.1:8000/api/token/refresh/", {
                    refresh: refreshToken,
                });

                // save the new access token in vuex
                const { access } = response.data;
                store.dispatch("saveTokens", { accessToken: access, refreshToken });

                processQueue(null, access);

                // Retry the original request with the new access token
                originalRequest.headers.Authorization = `Bearer ${access}`;
                return axios(originalRequest);
            } catch (refreshError) {
                processQueue(refreshError, null);
                // if refreshing fails, log the user out
                store.dispatch("logout");
                return Promise.reject(refreshError);
            } finally {
                isRefreshing = false;
            }
        }
        return Promise.reject(error);
    }
);

export default instance;