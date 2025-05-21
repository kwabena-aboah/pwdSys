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
                                  <div class="autocomplete-container" @keydown.down.prevent="moveDown" @keydown.up.prevent="moveUp" @keydown.enter.prevent="selectActive">
                                    <input
                                      type="text"
                                      v-model="form.pwd_id"
                                      @input="debouncedFetchSuggestions"
                                      placeholder="Start typing a record name..."
                                      @focus="isFocused = true"
                                      @blur="hideSuggestionsWithDelay"
                                      autocomplete="off"
                                      class="form-control"
                                      />
                                      <ul v-if="isFocused && suggestions.length && form.pwd_id" class="ul">
                                        <li
                                          v-for="(name, index) in suggestions"
                                          :key="name.id"
                                          :class="{ active: index === activeIndex }"
                                          @mousedown.prevent="selectPWD(name)">
                                            {{ name.id }}. {{ name.full_name }}
                                          </li>
                                      </ul>
                                      <p v-if="selectedPWD">Selected: {{ selectedPWD.full_name }}</p>
                                  </div>
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
                       <input type="text" name="search" class="form-control" v-model="searchQuery" placeholder="Search doctor's name..." @input="this.updateRouteQuery()">
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
                            <td>{{ mrecord.last_checkup_date }}</td>
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
            activeIndex: -1,
            isFocused: false,
            loading: false,
            selectedPWD: null,
            debouceTimeout: null,
            modalTitle: '',
            modalAction: '',
            pagination: {
                next: null,
                prev: null,
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
        async fetchRecords() {
          if(this.form.pwd_id.length < 2) {
            this.suggestions = []
            this.activeIndex = -1
            return
           }
           await instance.get('/pwd_records/', {
                headers: {
                'Authorization': `Bearer ${this.$store.state.accessToken}`,
              },
              params: {
                q: this.form.pwd_id,
              }
            })
           .then((response) => {
            this.suggestions = response.data.results;
            this.activeIndex = -1;
           })
           .catch((error) => {
            toast.error("Error fetching pwd record name!");
            console.error(error)
           })
        },
        debouncedFetchSuggestions() {
            clearTimeout(this.debouceTimeout)
            this.debouceTimeout = setTimeout(() => {
              this.fetchRecords()
            }, 300)
          },
          selectPWD(name) {
            this.form.pwd_id = name.pwd_id
            this.selectedPWD = name
            this.suggestions = []
            this.activeIndex = -1
          },
          moveDown() {
            if(this.activeIndex < this.suggestions.length - 1) {
              this.activeIndex++
            }
          },
          moveUp() {
            if(this.activeIndex > 0) {
              this.activeIndex--
            }
          },
          selectActive() {
            if(this.activeIndex >= 0) {
              this.selectPWD(this.suggestions[this.activeIndex])
            }
          },
          hideSuggestionsWithDelay() {
            setTimeout(() => {
              this.isFocused = false
            }, 100)
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
                formData.append('pwd_id', this.form.pwd_id || this.selectedPWD.id);
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
                formData.append('pwd_id', this.form.pwd_id || this.selectedPWD.id);
                formData.append('diagnosis', this.form.diagnosis || "");
                formData.append('doctor_name', this.form.doctor_name || "");
                formData.append('hospital_name', this.form.hospital_name || "");
                formData.append('last_checkup_date', this.form.last_checkup_date || "");

                 if (!this.selectedPWD) {
                  toast.warn('Please select a record name from suggestions')
                  return
                }

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