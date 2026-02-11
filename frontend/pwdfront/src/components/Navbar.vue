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
        
        
        <div class="navbar-nav">
            <div class="navbar-item text-nowrap">
                <div :class="['badge', online ? 'bg-success' : 'bg-danger']"> {{ online ? 'Online' : 'Offline' }}</div>
                <button type="button" class="btn btn-text btn-sm" data-bs-toggle="modal" data-bs-target="#searchModal">
                        Global Search
                </button>
                <a class="btn btn-text btn-sm" @click="logout">Sign Out</a>
            </div>
        </div>
    </header>

    <!-- Search Modal -->
    <div class="container">
        <div class="modal fade" id="searchModal" tabindex="-1" aria-labelledby="searchModalLabel" aria-hidden="true" role="dialog">
            <div class="modal-dialog modal-fullscreen">
                <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title fs-5" id="exampleModalLabel">Global PWD Record Search</h3>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <!-- Import Search Component -->
                  <SearchPage />
                </div>
              </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions } from 'vuex';
import SearchPage from '@/components/Search.vue';

export default {
    components: SearchPage,
    name: "NavBar",
    data(){
      return { online: navigator.online }
    },
    mounted() {
      window.addEventListener('online', () => this.online = true)
      window.addEventListener('offline', () => this.online = false)
    },
    methods: {
        ...mapActions(["logout"]),
        logout() {
            // toast.success("See you later!");
            // alert("See you later!")
            this.$router.push({ name: "LoginComponent" });
        },
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