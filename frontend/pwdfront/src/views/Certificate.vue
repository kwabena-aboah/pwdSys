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
                            <td>{{ mrecord.created_at }}</td>
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
            activeIndex: -1,
            isFocused: false,
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
    methods: {
        async fetchMedicalCertificate(url = `/certificates/?page=${this.page}`) {
            try {
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
            }
        },
        changePage(url) {
            if (url) {
                this.fetchMedicalCertificate(url);
            }
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
                if (!this.selectedPWD) {
                  toast.warn('Please select a record name from suggestions')
                  return
                }

                let formData = new FormData();
                // Append form fields
                formData.append('pwd_id', this.form.pwd_id || this.selectedPWD.id);
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
                // if (!this.selectedPWD) {
                //   toast.warn('Please select a record name from suggestions')
                //   return
                // }

                let formData = new FormData();
                // Append form fields
                formData.append('pwd_id', this.form.pwd_id || this.selectedPWD.id);
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