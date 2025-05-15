<template>
    <main class="container-fluid vh-100">
        <div class="row h-100">
          <!-- Banner Section -->
          <div class="col-lg-6 d-none d-lg-flex align-items-center justify-content-center bg-dark text-white">
            <img src="@/assets/banner.jpeg" alt="Login Logo" class="img-fluid rounded shadow" />
          </div>

          <!-- Login Form Section -->
          <div class="col-lg-6 d-flex align-items-center justify-content-center bg-light">
            <div class="card shadow-lg p-4" style="min-width: 350px; max-width: 400px; width: 100%">
              <div class="card-body">
                <h3 class="card-title text-center mb-4">Sign In</h3>
                <form @submit.prevent="loginUser">
                  <!-- Username -->
                    <div class="mb-3">
                        <input v-model="form.username" type="text" class="form-control" id="username" placeholder="Enter username" required />
                        <label for="username" class="form-label">Username</label>
                    </div>
                    <!-- Password -->
                    <div class="mb-3 position-relative">
                        <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="form-control" id="password" placeholder="Enter password" required />
                        <label for="password" class="form-label">Password</label>
                        <!-- Toggle password -->
                        <button
                          type="button"
                          class="btn btn-sm btn-outline-secondary position-absolute top-25 end-0 translate-middle-y me-2" @click="togglePassword">
                          {{ showPassword ? 'Hide' : 'Show' }}
                        </button>
                    </div>
                    <!-- Submit button -->
                    <div class="d-grid mt-4">
                      <button type="submit" class="w-100 btn btn-lg btn-primary">Sign in</button>
                    </div>
                    <!-- Additional links -->
                    <div class="text-center mt-3">
                        <a href="#" class="text-decoration-none">Forgot Password?</a>
                        <br>
                        <span class="text-muted">Don't have an account?</span>
                        <a href="#" class="text-decoration-none">Register</a>
                    </div>
                </form>
                <!-- <p class="mt-5 mb-3 text-muted">&copy; 2025–2026</p> -->
              </div>
            </div>
          </div>
        </div>
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
            showPassword: false,
        };
    },
    methods: {
        ...mapActions(["saveTokens"]),
        togglePassword() {
          this.showPassword = !this.showPassword;
        },
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
.card {
  border-radius: 10px;
}

.top-25 {
  top: 25%;
}
@media (max-width: 991.98px) {
  .row {
    flex-direction: column;
  }
}
</style>