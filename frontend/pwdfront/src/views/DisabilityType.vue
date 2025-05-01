<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <nav aria-label="breadcrumb" class="container-fluid">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><RouterLink to="/disability-type">Disability Type</RouterLink></li>
                    <li class="breadcrumb-item active" aria-current="page">Overview</li>
                </ol>
            </nav>

            <!-- Floating button -->
             <button 
                class="btn btn-primary rounded-circle position-fixed"
                style="bottom: 30px; right: 30px; width: 60px; height: 60px;"
                @click="openModal('create')"
                >
                <i class="bi bi-plus-lg"></i>
            </button>

            <!-- Add Disability Type Modal -->
             <div class="modal fade" id="disabilityTypeModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="disabilityTypeModalLabel">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title fs-5" id="disabilityTypeModalLabel">{{ modalTitle }}</h5>
                            <button class="btn-close" type="button" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <form @submit.prevent="handleSubmit">
                            <div class="modal-body">
                                <div class="mb-3">
                                    <label for="disability_type" class="form-label">Disability Type</label>
                                    <input type="text" id="disability_type" v-model="form.disability_type" class="form-control" required />
                                </div>
                                <div class="mb-3">
                                    <label for="description" class="form-label">Description</label>
                                    <textarea name="description" id="description" rows="3" v-model="form.description" class="form-control" required></textarea>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="submit" class="btn btn-primary">{{ modalAction }}</button>
                            </div>
                        </form>
                    </div>
                </div>
             </div>

            <!-- Disability Type list -->
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Disability Type</th>
                            <th>Description</th>
                            <th>Created Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody v-if="this.disabilityType?.length > 0">
                        <tr v-for="dtype in disabilityType" :key="dtype.id">
                            <td>{{ dtype.id }}</td>
                            <td>{{ dtype.disability_type }}</td>
                            <td>{{ dtype.description }}</td>
                            <td>{{ dtype.created_on }}</td>
                            <td>
                                <button class="btn btn-sm btn-warning me-2" @click="openModal('edit', dtype)">Edit</button>
                                <button class="btn btn-sm btn-danger" @click="deleteDisabilityType(dtype.id)">Delete</button>
                            </td>
                        </tr>
                    </tbody>
                    <tbody v-else>
                        <tr>
                            <td colspan="5">Loading...</td>
                        </tr>
                    </tbody>
                  </table>
            </div>

              <!-- Pagination controls -->
               <nav aria-label="Page navigation">
                <ul class="pagination justify-content-center">
                    <li 
                        class="page-item"
                        :class="{ disabled: !pagination.prev }"
                        @click="changePage(pagination.prev)">
                        <a href="#" class="page-link">Previous</a>
                    </li>
                    <li 
                        class="page-item"
                        :class="{ disabled: !pagination.next }"
                        @click="changePage(pagination.next)">
                        <a href="#" class="page-link">Next</a>
                    </li>
                </ul>
               </nav>
        </main>
    </div>
</template>

<script>
import instance from '@/api/axios';
import { Modal } from "bootstrap";
import Navbar from '@/components/Navbar.vue';
import Sidebar from "@/components/Sidebar.vue"
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

export default {
    components: {
        Navbar,
        Sidebar,
    },
    name: "DisabilityTypePage",
    data() {
        return {
            disabilityType: [],
            form: {
                id: null,
                disability_type: "",
                description: "",
            },
            page: 1,
            modalTitle: '',
            modalAction: '',
            pagination: {
                next: null,
                prev: null,
            },
        };
    },
    methods: {
        async fetchDisabilityType(url = `/disability_type/?page=${this.page}`) {
            try {
                const response = await instance.get(url, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                }
                });
                this.disabilityType = response.data.results;
                this.pagination.next = response.data.next;
                this.pagination.prev = response.data.previous;
                console.log(response.data);
            } catch (error) {
                toast.error("Error fetching Disability Type!");
                console.error("Error fetching Disability Type:", error);
            }
        },
        changePage(url) {
            if (url) {
                this.fetchDisabilityType(url);
            }
        },
        openModal(action, dtype = null) {
            if (action === 'create') {
                this.modalTitle = 'Add Disability Type';
                this.modalAction = 'Create';
                this.form = { id: null, disability_type: '', description: '' };
            } else if (action === 'edit') {
                this.modalTitle = 'Edit Disability Type';
                this.modalAction = 'Update';
                this.form = { ...dtype };
            }
            const modal = new Modal(document.getElementById('disabilityTypeModal'));
            modal.show();
        },
        handleSubmit() {
            if (this.modalAction === 'Create') {
                this.createDisabilityType();
            } else {
                this.updateDisabilityType();
            }
        },
        async createDisabilityType() {
            try {
                const response = await instance.post("/disability_type/", this.form, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    }
                });
                this.disabilityType = response.data; // Add new disability type to the  list
                toast.success("Disability Type created successfully!");
                this.fetchDisabilityType();    // Reset form
                this.closeModal();
            } catch (error) {
                // console.error("Error adding disability type:", error);
                toast.error("Failed to create disability type.", error);
            }
        },
        async updateDisabilityType() {
            try {
                const response = await instance.put(`/disability_type/${this.form.id}/`, this.form, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    'Content-Type': 'application/json',
                    }
                });
                this.disabilityType = response.data;
                toast.success("Disability Type updated successfully!");
                this.fetchDisabilityType();    // Reset form
                this.closeModal();
            } catch (error) {
                toast.error("Error updating disability type!", error);
                // console.error("Error updating disability type:", error);
            }
        },
        async deleteDisabilityType(id) {
            if(confirm('Are you sure you want to delete this disability type?')){
                await instance.delete(`/disability_type/${id}/`, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    }
                })
                .then(() => this.fetchDisabilityType(), toast.success("Disability type deleted successfully!"))
                .catch(error => //console.error(error); 
                    toast.error("Error deleting disability type!", error)
                );
            }
        },
        closeModal() {
            const modal = Modal.getInstance(document.getElementById('disabilityTypeModal'));
            modal.hide();
        },
    },
    created() {
        this.fetchDisabilityType();
    },
};
</script>

<style scoped>
.position-fixed {
    z-index: 1050;
}
</style>