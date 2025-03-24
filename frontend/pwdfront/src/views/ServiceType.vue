<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <h2 class="text-center">Service Type</h2>

            <!-- Floating button -->
             <button 
                class="btn btn-primary rounded-circle position-fixed"
                style="bottom: 30px; right: 30px; width: 60px; height: 60px;"
                @click="openModal('create')"
                >
                <i class="bi bi-plus-lg"></i>
            </button>

            <!-- Add Service Type Modal -->
             <div class="modal fade" id="serviceTypeModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="serviceTypeModalLabel">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title fs-5" id="serviceTypeModalLabel">{{ modalTitle }}</h5>
                            <button class="btn-close" type="button" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <form @submit.prevent="handleSubmit">
                            <div class="modal-body">
                                <div class="mb-3">
                                    <label for="service_name" class="form-label">Service Name</label>
                                    <input type="text" id="service_name" v-model="form.service_name" class="form-control" required />
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

            <!-- Service Type list -->
              <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Service Name</th>
                        <th>Description</th>
                        <th>Created Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody v-if="this.serviceType?.length > 0">
                    <tr v-for="stype in serviceType" :key="stype.id">
                        <td>{{ stype.id }}</td>
                        <td>{{ stype.service_name }}</td>
                        <td>{{ stype.description }}</td>
                        <td>{{ stype.created_on }}</td>
                        <td>
                            <button class="btn btn-sm btn-warning me-2" @click="openModal('edit', stype)">Edit</button>
                            <button class="btn btn-sm btn-danger" @click="deleteServiceType(stype.id)">Delete</button>
                        </td>
                    </tr>
                </tbody>
                <tbody v-else>
                    <tr>
                        <td colspan="5">Loading...</td>
                    </tr>
                </tbody>
              </table>

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
    name: "ServiceTypePage",
    data() {
        return {
            serviceType: [],
            form: {
                id: null,
                service_name: "",
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
        async fetchServiceType(url = `/service_type/?page=${this.page}`) {
            try {
                const response = await instance.get(url, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                }
                });
                this.serviceType = response.data.results;
                this.pagination.next = response.data.next;
                this.pagination.prev = response.data.previous;
                console.log(response.data);
            } catch (error) {
                toast.error("Error fetching Service Type!");
                console.error("Error fetching Service Type:", error);
            }
        },
        changePage(url) {
            if (url) {
                this.fetchServiceType(url);
            }
        },
        openModal(action, stype = null) {
            if (action === 'create') {
                this.modalTitle = 'Add Service Type';
                this.modalAction = 'Create';
                this.form = { id: null, service_name: '', description: '' };
            } else if (action === 'edit') {
                this.modalTitle = 'Edit Service Type';
                this.modalAction = 'Update';
                this.form = { ...stype };
            }
            const modal = new Modal(document.getElementById('serviceTypeModal'));
            modal.show();
        },
        handleSubmit() {
            if (this.modalAction === 'Create') {
                this.createServiceType();
            } else {
                this.updateServiceType();
            }
        },
        async createServiceType() {
            try {
                const response = await instance.post("/service_type/", this.form, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    }
                });
                this.serviceType = response.data; // Add new service type to the  list
                toast.success("Service Type created successfully!");
                this.fetchServiceType();    // Reset form
                this.closeModal();
            } catch (error) {
                // console.error("Error adding service type:", error);
                toast.error("Failed to create service type.", error);
            }
        },
        async updateServiceType() {
            try {
                const response = await instance.put(`/service_type/${this.form.id}/`, this.form, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    'Content-Type': 'application/json',
                    }
                });
                this.serviceType = response.data;
                toast.success("Service Type updated successfully!");
                this.fetchServiceType();    // Reset form
                this.closeModal();
            } catch (error) {
                toast.error("Error updating service type!", error);
                // console.error("Error updating service type:", error);
            }
        },
        async deleteServiceType(id) {
            if(confirm('Are you sure you want to delete this service type?')){
                await instance.delete(`/service_type/${id}/`, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    }
                })
                .then(() => this.fetchServiceType(), toast.success("Service type deleted successfully!"))
                .catch(error => //console.error(error); 
                    toast.error("Error deleting service type!", error)
                );
            }
        },
        closeModal() {
            const modal = Modal.getInstance(document.getElementById('serviceTypeModal'));
            modal.hide();
        },
    },
    created() {
        this.fetchServiceType();
    },
};
</script>

<style scoped>
.position-fixed {
    z-index: 1050;
}
</style>