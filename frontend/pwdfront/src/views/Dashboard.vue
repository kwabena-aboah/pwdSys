<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <h1>Welcome to PWD Records Dashboard</h1>
            <!-- <p>Manage your financial transactions, budget, and more!</p> -->

            <!-- Floating button -->
             <button 
                class="btn btn-primary rounded-circle position-fixed"
                style="bottom: 30px; right: 30px; width: 60px; height: 60px;"
                >
                <i class="bi bi-currency-dollar"></i>
            </button>
        </main>
    </div>
</template>

<script>
// import instance from '@/api/axios';
import Navbar from "@/components/Navbar.vue"
import Sidebar from "@/components/Sidebar.vue"
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

export default {
    components: {
        Navbar,
        Sidebar,
    },
    name: 'DashboardPage',
    created() {
        toast.success("Login successful!", {
          autoClose: 8000,
        });
    },
};
</script>
<style scoped>
.position-fixed {
    z-index: 1050;
}
</style>