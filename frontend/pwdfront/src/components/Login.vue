<template>
    <main class="form-signin text-center">
        <form @submit.prevent="loginUser">
            <img src="@/assets/logo.jpeg" class="mb-4" alt="logo.jpeg" width="280" height="100">
            <div class="form-floating">
                <input v-model="form.username" type="text" class="form-control" id="username" placeholder="Username" required />
                <label for="username" class="form-label">Username</label>
            </div>
            <div class="form-floating">
                <input v-model="form.password" type="password" class="form-control" id="password" placeholder="Password" required />
                <label for="password" class="form-label">Password</label>
            </div>
            <button type="submit" class="w-100 btn btn-lg btn-primary">Sign in</button>
            <hr>
            <!-- <div class="checkbox mb-3">
                <p class="mt-5 mb-3 text-muted">Don't have an account? Click on the "Register" button below.</p>
              <router-link to="/register"  class="w-100 btn btn-lg btn-default shadow">Register</router-link>
            </div> -->
        </form>
        <p class="mt-5 mb-3 text-muted">&copy; 2025–2026</p>
    </main>
</template>

<script>
import instance from '@/api/axios';
import { mapActions } from 'vuex';
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

export default {
    name: 'LoginComponent',
    data() {
        return {
            form: {
                username: "",
                password: "",
            },
        };
    },
    methods: {
        ...mapActions(["saveTokens"]),
        async loginUser() {
            try {
                const response = await instance.post("/token/", this.form);
                const { access, refresh } = response.data;
                
                // save token in vuex store
                this.saveTokens({ accessToken: access, refreshToken: refresh });
                // alert("Login successful!");
                this.$router.push({ name: "DashboardPage" });
            } catch (error) {
              toast.error("Invalid credentials", error.response.data);
                // console.error(error.response.data);
                // alert("Invalid credentials")
            }
        },
    },
};
</script>

<style scoped>
html,
body {
  height: 100%;
}

body {
  display: flex;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #8b8b8b;
}

.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}

.form-signin .checkbox {
  font-weight: 400;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>