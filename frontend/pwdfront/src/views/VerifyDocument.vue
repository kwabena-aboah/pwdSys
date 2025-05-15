<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <nav aria-label="breadcrumb" class="container-fluid">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><RouterLink to="/verify-document">Document Verification</RouterLink></li>
                    <li class="breadcrumb-item active" aria-current="page">Overview</li>
                </ol>
            </nav>

            <div class="container mt-5">
                <div class="p-5 mb-4 bg-light rounded-3 text-center">
                    <h1 class="display-4 fw-bold">Important Information!</h1>
                    <p class="lead">Please check the ID of the record at the PWD Records page / Medical Certificate page if you want to verify an ID Card / Certificate</p>
                </div>
                <form @submit.prevent="verifyDocument">
                    <div class="mb-3">
                        <label class="form-label">Document Type</label>
                        <select v-model="form.document_type" class="form-select">
                            <option value="" disabled>Select document type</option>
                            <option value="certificate">Certificate</option>
                            <option value="id_card">ID Card</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Related ID</label>
                        <input type="number" name="related_id" v-model="form.related_id" class="form-control">
                    </div>
                    <button class="btn btn-primary">Verify</button>
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
    name: 'VerifyDocument',
    data() {
        return {
            form: {
                document_type: 'certificate',
                related_id: null
            },
            result: null
        };
    },
    methods: {
        async verifyDocument(){
            const res = await instance.post('/pwd/verify-document/', this.form, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
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