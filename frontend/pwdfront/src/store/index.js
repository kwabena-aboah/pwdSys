import { createStore } from "vuex";
import { jwtDecode } from "jwt-decode";

const store = createStore({
    state: {
        accessToken: localStorage.getItem("access_token") || null,
        refreshToken: localStorage.getItem("refresh_token") || null,
        tokenExpiry: localStorage.getItem("token_expiry") || null,
        user: null,
    },
    mutations: {
        SET_TOKENS(state, { accessToken, refreshToken }){
            const decoded = jwtDecode(accessToken);
            const expiry = decoded.exp * 1000; // convert expiry to miliseconds

            state.accessToken = accessToken;
            state.refreshToken = refreshToken;
            state.tokenExpiry = expiry;

            // Persist tokens in localStorage for session continuity
            localStorage.setItem("access_token", accessToken);
            localStorage.setItem("refresh_token", refreshToken);
            localStorage.setItem("token_expiry", expiry);
        },
        CLEAR_TOKENS(state) {
            state.accessToken = null;
            state.refreshToken = null;
            state.tokenExpiry = null;

            // Reemove token from localStorage
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            localStorage.removeItem("token_expiry");
        },
        SET_USER(state, user) {
            state.user = user;
        },
    },
    actions: {
        saveTokens({ commit }, { accessToken, refreshToken }) {
            commit("SET_TOKENS", { accessToken, refreshToken });
        },
        fetchUser({ commit }){
            const user = JSON.parse(localStorage.getItem("user"));
            if (user) commit("SET_USER", user);
        },
        logout({ commit }){
            commit("CLEAR_TOKENS");
        },
    },
    getters: {
        isAuthenticated: (state) => !!state.accessToken,
        accessToken: (state) => state.accessToken,
        refreshToken: (state) => state.refreshToken,
        tokenExpiry: (state) => state.tokenExpiry,
    },
});

export default store;