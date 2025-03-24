<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <h2 class="text-center">Medical Records</h2>

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
                                  <select name="pwd_id" id="pwd_id" class="form-select" v-model="form.pwd_id" required>
                                     <option value="" disabled>Select PWD Name</option>
                                     <option v-for="name in records" :key="name.id" :value="name.id">
                                         {{ name.id }}. {{ name.full_name }}
                                     </option>
                                 </select>
                                   <div class="container">
                                    <p>Click on the "Next" for more PWD Record List.</p>
                                     <!-- Pagination controls -->
                                     <nav aria-label="Page navigation">
                                      <ul class="pagination justify-content-center">
                                          <li 
                                              class="page-item"
                                              :class="{ disabled: !paginate.prev }"
                                              @click="changeList(paginate.prev)">
                                              <a href="#" class="page-link">Previous</a>
                                          </li>
                                          <li 
                                              class="page-item"
                                              :class="{ disabled: !paginate.next }"
                                              @click="changeList(paginate.next)">
                                              <a href="#" class="page-link">Next</a>
                                          </li>
                                      </ul>
                                     </nav>
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

            <!-- Service Type list -->
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
            records: [],
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
            modalTitle: '',
            modalAction: '',
            pagination: {
                next: null,
                prev: null,
            },
            paginate: {
                next: null,
                prev: null,
            },
        };
    },
    methods: {
        async fetchMedicalRecords(url = `/medical_records/?page=${this.page}`) {
            try {
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
            }
        },
        changePage(url) {
            if (url) {
                this.fetchServiceType(url);
            }
        },
        async fetchRecords(urls = `/pwd_records/`) {
          try {
            const response = await instance.get(urls, {
                headers: {
                'Authorization': `Bearer ${this.$store.state.accessToken}`,
              }
            });
            this.records = response.data.results;
            this.paginate.next = response.data.next;
            this.paginate.prev = response.data.previous;
            console.log(response.data);
          } catch (error) {
              toast.error("Error fetching records!");
              console.error("Error fetching records:", error);
              // this.records = [];
          }
        },
        changeList(urls) {
            if (urls) {
                this.fetchRecords(urls);
            }
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
                const response = await instance.post("/medical_records/", this.form, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
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
                const response = await instance.put(`/medical_records/${this.form.id}/`, this.form, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    'Content-Type': 'application/json',
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
        this.fetchMedicalRecords();
        this.fetchRecords();
    },
};
</script>

<style scoped>
.position-fixed {
    z-index: 1050;
}
</style>