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
                <div class="p-5 mb-4 bg-light rounded-3 text-center">
                    <h1 class="display-4 fw-bold">Important Information!</h1>
                    <p class="lead">Select an image file only (i.e., PNG, JPEG and JPG file types). Do not upload any document file or PDF file format</p>
                </div>
                <form @submit.prevent="uploadAndVerify">
                    <div class="mb-3">
                        <input type="file" name="certificate" @change="onFileChange" class="form-control" required accept="image/png, image/jpeg, image/jpg">
                    </div>
                    <button class="btn btn-primary">Upload & Verify</button>
                </form>
            </div>
            <div v-if="result" class="container mt-5">
                <div class="p-5 mb-4 bg-light rounded-4 text-center">
                    <h5 class="display-4 fw-bold">Extracted Text:</h5>
                    <pre class="lead">{{ result.text_extracted }}</pre>
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
            const selectedFile = e.target.files[0];
            if (!selectedFile.type.startsWith("image/")){
                toast.warn("Only image files (PNG, JPG) are allowed.");
                this.file = null;
                return;
            }
            this.file = selectedFile;
        },
        async uploadAndVerify(){
            if (!this.file) {
                toast.warn("Please select an image file.");
                return;
            }
            
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