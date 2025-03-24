<template>
    <header class="navbar navbar-light sticky-top bg-light flex-md-nowrap p-0 shadow">
        <router-link to="/dashboard" class="navbar-brand col-md-3 col-lg-2 me-0 px-3"><span class="h3" style="color: #2f59a1;">PWD</span><span class="h4" style="color: #ffffff;">Records</span></router-link>
        <button 
            type="button"
            class="navbar-toggler position-absolute d-md-none collapsed"
            data-bs-toggle="collapse"
            data-bs-target="#sidebarMenu"
            aria-controls="sidebarMenu"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <input class="form-control form-control-dark w-100" type="text" name="search" id="search" placeholder="Search" aria-label="Search">
        <div class="navbar-nav">
            <div class="navbar-item text-nowrap">
                <a class="nav-link px-3" @click="logout">Sign Out</a>
            </div>
        </div>
    </header>
</template>

<script>
import { mapActions } from 'vuex';
// import { toast } from "vue3-toastify";
// import "vue3-toastify/dist/index.css";

export default {
    name: "NavBar",
    methods: {
        ...mapActions(["logout"]),
        logout() {
            // toast.success("See you later!");
            // alert("See you later!")
            this.$router.push({ name: "LoginComponent" });
        }
    }
};
</script>

<style scoped>
/*
 * Navbar
 */

.navbar-brand {
  padding-top: .75rem;
  padding-bottom: .75rem;
  font-size: 1rem;
  background-color: rgba(0, 0, 0, .25);
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, .25);
}

.navbar .navbar-toggler {
  top: .25rem;
  right: 1rem;
}

.navbar .form-control {
  padding: .75rem 1rem;
  border-width: 0;
  border-radius: 0;
}

.form-control-dark {
  color: #fff;
  background-color: rgba(255, 255, 255, .1);
  border-color: rgba(255, 255, 255, .1);
}

.form-control-dark:focus {
  border-color: transparent;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, .25);
}
</style>