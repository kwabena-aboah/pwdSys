<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <nav aria-label="breadcrumb" class="container-fluid">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><RouterLink to="/verify-upload">Upload & Verify Document</RouterLink></li>
                    <li class="breadcrumb-item active" aria-current="page">Overview</li>
                </ol>
            </nav>

            <div class="container mt-5">
                <form @submit.prevent="uploadAndVerify">
                    <div class="mb-3">
                        <input type="file" name="certificate" @change="onFileChange" class="form-control" required>
                    </div>
                    <button class="btn btn-primary">Upload & Verify</button>
                </form>
            </div>
            <br>
            <hr>
            <div v-if="result">
                <div class="mt-2">
                    <h5>Extracted Text:</h5>
                    <pre>{{ result.text_extracted }}</pre>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
import instance from '@/api/axios';
import Navbar from '@/components/Navbar.vue';
import Sidebar from "@/components/Sidebar.vue"
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

export default {
    components: {
        Navbar,
        Sidebar,
    },
    name: 'VerifyUpload',
    data() {
        return {
            file: null,
            result: null
        };
    },
    methods: {
        onFileChange(e) {
            this.file = e.target.files[0];
        },
        async uploadAndVerify(){
            const formData = new FormData();
            formData.append("file", this.file);

            const res = await instance.post('/pwd/upload-and-verify/', formData, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    'Content-Type': 'multipart/form-data',
                }
            });
            this.result = res.data;
            console.log(res.data)
            toast.success(this.result.result);
        }
    }
};
</script>

<style scoped>
.position-fixed {
    z-index: 1050;
}
</style>