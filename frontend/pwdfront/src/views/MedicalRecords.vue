<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <nav aria-label="breadcrumb" class="container-fluid">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><RouterLink to="/medical_records">Medical Records</RouterLink></li>
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
             <div class="modal fade" id="medicalRecordsModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="medicalRecordsModalLabel">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title fs-5" id="medicalRecordsModalLabel">{{ modalTitle }}</h5>
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
                                    <label for="diagnosis" class="form-label">Diagnosis</label>
                                    <textarea name="diagnosis" id="diagnosis" rows="3" v-model="form.diagnosis" class="form-control" required></textarea>
                                </div>
                                <div class="mb-3">
                                    <label for="doctor_name" class="form-label">Doctor's Name</label>
                                    <input type="text" name="doctor_name" id="doctor_name" placeholder="Doctor's Name..." v-model="form.doctor_name" class="form-control">
                                </div>
                                <div class="mb-3">
                                    <label for="hospital_name" class="form-label">Hospital Name</label>
                                    <input type="text" name="hospital_name" id="hospital_name" placeholder="Hospital Name..." v-model="form.hospital_name" class="form-control">
                                </div>
                                <div class="mb-3">
                                    <label for="last_checkup_date" class="form-label">Last Checkup Date</label>
                                    <input type="date" name="last_checkup_date" id="last_checkup_date" v-model="form.last_checkup_date" class="form-control">
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
                       <input type="text" name="search" class="form-control" v-model="searchQuery" placeholder="Search medical record..." @input="this.updateRouteQuery()">
                   </div>
                   <div class="col-sm-12 col-md-4 col-lg-4">
                       <select v-model="ordering" @change="this.updateRouteQuery()" class="form-select">
                         <option value="last_checkup_date">Last Checkup Date (Asc)</option>
                         <option value="-last_checkup_date">Last Checkup Date (Desc)</option>
                       </select>
                   </div>
                 </div>
             </div>

            <!-- Service Type list -->
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>PWD Name</th>
                            <th>Diagnosis</th>
                            <th>Doctor's Name</th>
                            <th>Hospital Name</th>
                            <th>Last Checkup Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody v-if="this.medicalRecord?.length > 0">
                        <tr v-for="mrecord in medicalRecord" :key="mrecord.id">
                            <td>{{ mrecord.id }}</td>
                            <td>{{ mrecord.pwd_name }}</td>
                            <td>{{ mrecord.diagnosis }}</td>
                            <td>{{ mrecord.doctor_name }}</td>
                            <td>{{ mrecord.hospital_name }}</td>
                            <td>{{ formatDate(mrecord.last_checkup_date) }}</td>
                            <td>
                                <button class="btn btn-sm btn-warning me-2" @click="openModal('edit', mrecord)">Edit</button>
                                <button class="btn btn-sm btn-danger" @click="deleteMedicalRecord(mrecord.id)">Delete</button>
                            </td>
                        </tr>
                    </tbody>
                    <tbody v-else>
                        <tr>
                            <td colspan="7">Loading...</td>
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
    name: "MedicalRecordPage",
    data() {
        return {
            medicalRecord: [],
            form: {
                id: null,
                pwd_id: "",
                // pwd_name: "",
                diagnosis: "",
                doctor_name: "",
                hospital_name: "",
                last_checkup_date: ""
            },
            page: 1,
            suggestions: [],
            searchQuery: "",
            ordering: "last_checkup_date",
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
          this.ordering = query.ordering || 'last_checkup_date';
          this.fetchMedicalRecords(query.page || 1);
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
        async fetchMedicalRecords(page = this.page) {
            try {
                this.loading = true;
                let url = `/medical_records/?search=${this.searchQuery}&page=${page}&ordering=${this.ordering}`;
                const response = await instance.get(url, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                }
                });
                this.medicalRecord = response.data.results;
                this.pagination.next = response.data.next;
                this.pagination.prev = response.data.previous;
                console.log(response.data);
            } catch (error) {
                toast.error("Error fetching Medical Records!");
                console.error("Error fetching Medical Records:", error);
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
                this.modalTitle = 'Add Medical Record';
                this.modalAction = 'Create';
                this.form = { id: null, pwd_id: "", diagnosis: "", doctor_name: "", hospital_name: "", last_checkup_date: "" };
            } else if (action === 'edit') {
                this.modalTitle = 'Edit Medical Record';
                this.modalAction = 'Update';
                this.form = { ...mrecord };
            }
            const modal = new Modal(document.getElementById('medicalRecordsModal'));
            modal.show();
        },
        handleSubmit() {
            if (this.modalAction === 'Create') {
                this.createMedicalRecord();
            } else {
                this.updateMedicalRecord();
            }
        },
        async createMedicalRecord() {
            try {
                let formData = new FormData();
                // Append form fields
                formData.append('pwd_id', this.form.pwd_id || "");
                formData.append('diagnosis', this.form.diagnosis || "");
                formData.append('doctor_name', this.form.doctor_name || "");
                formData.append('hospital_name', this.form.hospital_name || "");
                formData.append('last_checkup_date', this.form.last_checkup_date || "");

                 if (!this.selectedPWD) {
                  toast.warn('Please select a record name from suggestions')
                  return
                }
                const response = await instance.post("/medical_records/", formData, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    'Content-Type': 'multipart/form-data',
                    }
                });
                this.medicalRecord = response.data; // Add new medical record to the  list
                toast.success("Medical Record created successfully!");
                this.fetchMedicalRecords();    // Reset form
                this.closeModal();
            } catch (error) {
                // console.error("Error adding medical record:", error);
                toast.error("Failed to create medical record.", error);
            }
        },
        async updateMedicalRecord() {
            try {
                let formData = new FormData();
                // Append form fields
                formData.append('pwd_id', this.form.pwd_id || "");
                formData.append('diagnosis', this.form.diagnosis || "");
                formData.append('doctor_name', this.form.doctor_name || "");
                formData.append('hospital_name', this.form.hospital_name || "");
                formData.append('last_checkup_date', this.form.last_checkup_date || "");

                const response = await instance.put(`/medical_records/${this.form.id}/`, formData, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    'Content-Type': 'multipart/form-data',
                    }
                });
                this.medicalRecord = response.data;
                toast.success("Medical Record updated successfully!");
                this.fetchMedicalRecords();    // Reset form
                this.closeModal();
            } catch (error) {
                toast.error("Error updating medical record!", error);
                // console.error("Error updating medical record:", error);
            }
        },
        async deleteServiceType(id) {
            if(confirm('Are you sure you want to delete this medical record?')){
                await instance.delete(`/medical_records/${id}/`, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    }
                })
                .then(() => this.fetchMedicalRecords(), toast.success("Medical Record deleted successfully!"))
                .catch(error => //console.error(error); 
                    toast.error("Error deleting medical record!", error)
                );
            }
        },
        closeModal() {
            const modal = Modal.getInstance(document.getElementById('medicalRecordsModal'));
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
        this.loadFromQuery();
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