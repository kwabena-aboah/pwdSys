<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <nav aria-label="breadcrumb" class="container-fluid">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><RouterLink to="/certificates">Medical Certificate</RouterLink></li>
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

            <!-- Add Service Type Modal -->
             <div class="modal fade" id="medicalCertificateModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="medicalCertificateModalLabel">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title fs-5" id="medicalCertificateModalLabel">{{ modalTitle }}</h5>
                            <button class="btn-close" type="button" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <form @submit.prevent="handleSubmit">
                            <div class="modal-body">
                                <div class="mb-3">
                                  <label for="pwd_id" class="form-label">PWD Name</label>
                                  <Multiselect
                                    v-model="form.pwd_id"
                                    :options="suggestions"
                                    label="full_name"
                                    value-prop="id"
                                    track-by="id"
                                    searchable
                                    :filter-results="false"
                                    @search-change="fetchRecords"
                                    placeholder="Search PWD by name..."
                                    class="form-control p-0"
                                    />
                                </div>
                                <div class="mb-3">
                                    <label for="medical_certificate" class="form-label">Diagnosis</label>
                                    <input type="file" 
                                            id="picture" 
                                            name="picture" 
                                            class="form-control"
                                            @change="handleFileChange($event)"
                                            accept="image/*" />
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

             <!-- Search filter & Ordering -->
             <div class="container-fluid">
                 <div class="row mb-3">
                     <div class="col-sm-12 col-md-8 col-lg-8">
                       <input type="text" name="search" class="form-control" v-model="searchQuery" placeholder="Search pwd's name..." @input="this.updateRouteQuery()">
                   </div>
                   <div class="col-sm-12 col-md-4 col-lg-4">
                       <select v-model="ordering" @change="this.updateRouteQuery()" class="form-select">
                         <option value="created_at">Created Date (Asc)</option>
                         <option value="-created_at">Created Date (Desc)</option>
                       </select>
                   </div>
                 </div>
             </div>

            <!-- Service Type list -->
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>PWD Name</th>
                            <th>Medical Certificate</th>
                            <th>Created Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody v-if="this.medicalCertificate?.length > 0">
                        <tr v-for="mrecord in medicalCertificate" :key="mrecord.id">
                            <td>{{ mrecord.id }}</td>
                            <td>{{ mrecord.pwd_name }}</td>
                            <td><img :src="mrecord.medical_certificate" :alt="mrecord.pwd_name" class="rounded-circle img-fluid" style="width:50px; height:50px;"/></td>
                            <td>{{ formatDate(mrecord.created_at) }}</td>
                            <td>
                                <button class="btn btn-sm btn-warning me-2" @click="openModal('edit', mrecord)">Edit</button>
                                <button class="btn btn-sm btn-danger" @click="deleteMedicalCertificate(mrecord.id)">Delete</button>
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
              <b-pagination
                v-if="pagination.count > 0"
                v-model="page"
                :total-rows="pagination.count"
                :per-page="pagination.perPage"
                align="center"
                @update:model-value="changePage" 
              />
               <!-- <nav aria-label="Page navigation">
                <ul class="pagination justify-content-center">
                    <li 
                        class="page-item"
                        :class="{ disabled: !pagination.prev }"
                        >
                        <a href="#" class="page-link" @click.prevent="changePage(pagination.prev)">Previous</a>
                    </li>
                    <li 
                        class="page-item"
                        :class="{ disabled: !pagination.next }"
                        >
                        <a href="#" class="page-link" @click.prevent="changePage(pagination.next)">Next</a>
                    </li>
                </ul>
               </nav> -->
        </main>
    </div>
</template>

<script>
import instance from '@/api/axios';
import { Modal } from "bootstrap";
import { BPagination } from 'bootstrap-vue-next';
import Navbar from '@/components/Navbar.vue';
import Sidebar from "@/components/Sidebar.vue"
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import Multiselect from "@vueform/multiselect";
import "@vueform/multiselect/themes/default.css";

export default {
    components: {
        Navbar,
        Sidebar,
        Multiselect,
        BPagination
    },
    name: "CertificatePage",
    data() {
        return {
            medicalCertificate: [],
            form: {
                id: null,
                pwd_id: "",
                // pwd_name: "",
                medical_certificate: ""
            },
            page: 1,
            suggestions: [],
            searchQuery: "",
            ordering: "created_at",
            loading: false,
            modalTitle: '',
            modalAction: '',
            pagination: {
              count: 0,
              perPage: 10,
          },
        };
    },
    watch: {
        '$route.query': {
          handler() {
            this.loadFromQuery();
          },
          deep: true
        }
      },
    methods: {
        loadFromQuery() {
          const query = this.$route.query;

          this.searchQuery = query.search || '';
          this.ordering = query.ordering || 'created_at';
          this.fetchMedicalCertificate(query.page || 1);
        },
        updateRouteQuery() {
          this.$router.push({
            path: this.$route.path,
            query: {
              search: this.searchQuery || undefined,
              ordering: this.ordering || undefined,
              page: 1,
            },
          });
        },
        async fetchMedicalCertificate(page = this.page) {
            try {
                this.loading = true;

                let url = `/certificates/?search=${this.searchQuery}&page=${page}&ordering=${this.ordering}`;

                const response = await instance.get(url, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                }
                });
                this.medicalCertificate = response.data.results;
                this.pagination.next = response.data.next;
                this.pagination.prev = response.data.previous;
                console.log(response.data);
            } catch (error) {
                toast.error("Error fetching Medical Certificate!");
                console.error("Error fetching Medical Certificate:", error);
            } finally {
                this.loading = false;
            }
        },
        changePage(url) {
            if (!url) return;
            const pageParam = new URLSearchParams(url.split('?')[1]).get('page');
            this.$router.push({
              path: this.$route.path,
              query: { ...this.$route.query, pageParam },
            });
        },
        async fetchRecords(query) {
          if (!query || query.length < 2){
            this.suggestions = [];
            return;
          }
           await instance.get('/pwd_records/', {
                headers: {
                'Authorization': `Bearer ${this.$store.state.accessToken}`,
              },
              params: { search: query }
            })
           .then((response) => {
            this.suggestions = response.data.results ?? response.data;
           })
           .catch((error) => {
            toast.error("Error fetching pwd record name!");
            console.error(error)
           })
        },
        openModal(action, mrecord = null) {
            if (action === 'create') {
                this.modalTitle = 'Add Medical Certificate';
                this.modalAction = 'Create';
                this.form = { id: null, pwd_id: "", medical_certificate: null };
            } else if (action === 'edit') {
                this.modalTitle = 'Edit Medical Certificate';
                this.modalAction = 'Update';
                this.form = { ...mrecord };
            }
            const modal = new Modal(document.getElementById('medicalCertificateModal'));
            modal.show();
        },
        handleFileChange(event){
            console.log(event.target.files[0]);
            const file = event.target.files[0];
            if(!file) return;

            this.form.medical_certificate = file;
            this.createBase64Image(file);
        },
        createBase64Image(fileObject){
            // converts image to a text file for backend to read
            const reader = new FileReader();

            reader.onChange = (event) => {
                this.form.medical_certificate = event.target.result;
                // this.handleSubmit();
            };
            reader.readAsDataURL(fileObject);
        },
        handleSubmit() {
            if (this.modalAction === 'Create') {
                this.createMedicalCertificate();
            } else {
                this.updateMedicalCertificate();
            }
        },
        async createMedicalCertificate() {
            try {
                let formData = new FormData();
                // Append form fields
                formData.append('pwd_id', this.form.pwd_id || "");
                // formData.append('medical_certificate', this.form.medical_certificate || "");

                if (this.form.medical_certificate instanceof File){
                    formData.append('medical_certificate', this.form.medical_certificate);
                } else {
                    toast.warn('Pleass upload a valid medical certificate image');
                    return;
                }

                const response = await instance.post("/certificates/", formData, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    'Content-Type': 'multipart/form-data',
                    }
                });
                this.medicalCertificate = response.data; // Add new medical certificate to the  list
                toast.success("Medical Certificate created successfully!");
                this.fetchMedicalCertificate();    // Reset form
                this.closeModal();
            } catch (error) {
                // console.error("Error adding medical certificate:", error);
                toast.error("Failed to create medical certificate.", error);
            }
        },
        async updateMedicalCertificate() {
            try {
                let formData = new FormData();
                // Append form fields
                formData.append('pwd_id', this.form.pwd_id || "");
                // formData.append('medical_certificate', this.form.medical_certificate || "");

                if (this.form.medical_certificate instanceof File){
                    formData.append('medical_certificate', this.form.medical_certificate)
                }
                const response = await instance.patch(`/certificates/${this.form.id}/`, formData, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    }
                });
                this.medicalCertificate = response.data;
                toast.success("Medical Certificate updated successfully!");
                this.fetchMedicalCertificate();    // Reset form
                this.closeModal();
            } catch (error) {
                toast.error("Error updating medical certificate!", error);
                // console.error("Error updating medical certificate:", error);
            }
        },
        async deleteMedicalCertificate(id) {
            if(confirm('Are you sure you want to delete this medical certificate?')){
                await instance.delete(`/certificates/${id}/`, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    'Content-Type': 'multipart/form-data',
                    }
                })
                .then(() => this.fetchMedicalCertificate(), toast.success("Medical Certificate deleted successfully!"))
                .catch(error => //console.error(error); 
                    toast.error("Error deleting medical certificate!", error)
                );
            }
        },
        closeModal() {
            const modal = Modal.getInstance(document.getElementById('medicalCertificateModal'));
            modal.hide();
        },
        formatDate(dateStr){
            const d = new Date(dateStr)
            return d.toLocaleString('en-GB', {
              day: '2-digit',
              month: 'short',
              year: 'numeric',
              hour: '2-digit',
              minute: '2-digit'
            })
          },
    },
    created() {
        this.fetchMedicalCertificate();
        this.fetchRecords();
    },
};
</script>

<style scoped>
.position-fixed {
    z-index: 1050;
}
.ul {
list-style: none;
margin: 0;
padding: 0;
background: #fff;
border: 1px solid #ccc;
max-height: 150px;
overflow-y: auto;
position: absolute;
width: 100%;
z-index: 1000;
}
.ul li {
padding: 8px;
cursor: pointer;
}
.ul li.active {
background-color: #007BFF;
color: white;
}
.ul li.hover {
background-color: #f0f0f0;
}
</style>