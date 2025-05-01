<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <nav aria-label="breadcrumb" class="container-fluid">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><RouterLink to="/complaints">Complaints</RouterLink></li>
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

            <!-- Add Complaints Modal -->
             <div class="modal fade" id="complaintsModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="complaintsModalLabel">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title fs-5" id="complaintsModalLabel">{{ modalTitle }}</h5>
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
                                    <label for="location" class="form-label">Location</label>
                                    <input type="text" name="location" v-model="form.location" id="location" class="form-control" placeholder="Enter location...">
                                </div>
                                <div class="mb-3">
                                    <label for="complaint_description" class="form-label">Complaint Description</label>
                                    <textarea name="complaint_description" v-model="form.complaint_description" rows="3" id="complaint_description" class="form-control" placeholder="Enter complaint..."></textarea>
                                </div>
                                <div class="mb-3">
                                    <label for="status" class="form-label">Complaint Status</label>
                                    <select class="form-select" v-model="form.status" required>
                                        <option value="" disabled>Select status</option>
                                        <option value="new">New</option>
                                        <option value="under review">Under Review</option>
                                        <option value="resolved">Resolved</option>
                                    </select>
                                </div>
                                <div class="mb-3">
                                    <label for="reported_at" class="form-label">Reported Date</label>
                                    <input type="datetime-local" name="reported_at" v-model="form.reported_at" id="reported_at" class="form-control">
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
                            <th>ID</th>
                            <th>PWD Name</th>
                            <th>Location</th>
                            <th>Complaint Description</th>
                            <th>Status</th>
                            <th>Reported Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody v-if="this.complaints?.length > 0">
                        <tr v-for="complaint in complaints" :key="complaint.id">
                            <td>{{ complaint.id }}</td>
                            <td>{{ complaint.pwd_name }}</td>
                            <td>{{ complaint.location}}</td>
                            <td>{{ complaint.complaint_description}}</td>
                            <td>{{ complaint.status }}</td>
                            <td>{{ complaint.reported_at }}</td>
                            <td>
                                <button class="btn btn-sm btn-warning me-2" @click="openModal('edit', complaint)">Edit</button>
                                <button class="btn btn-sm btn-danger" @click="deleteComplaint(complaint.id)">Delete</button>
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
    name: "ComplaintPage",
    data() {
        return {
            complaints: [],
            form: {
                id: null,
                pwd_id: "",
                // pwd_name: "",
                location: "",
                complaint_description: "",
                status: "",
                reported_at: ""

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
        async fetchComplaints(url = `/complaints/?page=${this.page}`) {
            try {
                const response = await instance.get(url, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                }
                });
                this.complaints = response.data.results;
                this.pagination.next = response.data.next;
                this.pagination.prev = response.data.previous;
                console.log(response.data);
            } catch (error) {
                toast.error("Error fetching Complaints!");
                console.error("Error fetching Complaints:", error);
            }
        },
        changePage(url) {
            if (url) {
                this.fetchComplaints(url);
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
        openModal(action, complaint = null) {
            if (action === 'create') {
                this.modalTitle = 'Add Complaint';
                this.modalAction = 'Create';
                this.form = { id: null, pwd_id: "", location: "", complaint_description: "", status: "", reported_at: "" };
            } else if (action === 'edit') {
                this.modalTitle = 'Edit Complaint';
                this.modalAction = 'Update';
                this.form = { ...complaint };
            }
            const modal = new Modal(document.getElementById('complaintsModal'));
            modal.show();
        },
        handleSubmit() {
            if (this.modalAction === 'Create') {
                this.createComplaint();
            } else {
                this.updateComplaint();
            }
        },
        async createComplaint() {
            try {
                if (!this.selectedPWD) {
                  toast.warn('Please select a record name from suggestions')
                  return
                }

                let formData = new FormData();
                // Append form fields
                formData.append('pwd_id', this.form.pwd_id || this.selectedPWD.id);
                formData.append('location', this.form.location || "");
                formData.append('complaint_description', this.form.complaint_description || "");
                formData.append('status', this.form.status || "");
                formData.append('reported_at', this.form.reported_at || "")

                const response = await instance.post("/complaints/", formData, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    'Content-Type': 'multipart/form-data',
                    }
                });
                this.medicalCertificate = response.data; // Add new medical certificate to the  list
                toast.success("Complaint created successfully!");
                this.fetchComplaints();    // Reset form
                this.closeModal();
            } catch (error) {
                // console.error("Error adding complaint:", error);
                toast.error("Failed to create complaint.", error);
            }
        },
        async updateComplaint() {
            try {
                // if (!this.selectedPWD) {
                //   toast.warn('Please select a record name from suggestions')
                //   return
                // }

                let formData = new FormData();
                // Append form fields
                formData.append('pwd_id', this.form.pwd_id || this.selectedPWD.id);
                formData.append('location', this.form.location || "");
                formData.append('complaint_description', this.form.complaint_description || "");
                formData.append('status', this.form.status || "");
                formData.append('reported_at', this.form.reported_at || "")

                const response = await instance.patch(`/complaints/${this.form.id}/`, formData, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    }
                });
                this.medicalCertificate = response.data;
                toast.success("Complaint updated successfully!");
                this.fetchComplaints();    // Reset form
                this.closeModal();
            } catch (error) {
                toast.error("Error updating complaint!", error);
                // console.error("Error updating complaint:", error);
            }
        },
        async deleteComplaint(id) {
            if(confirm('Are you sure you want to delete this complaint?')){
                await instance.delete(`/complaints/${id}/`, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    'Content-Type': 'multipart/form-data',
                    }
                })
                .then(() => this.fetchComplaints(), toast.success("Complaint deleted successfully!"))
                .catch(error => //console.error(error); 
                    toast.error("Error deleting complaint!", error)
                );
            }
        },
        closeModal() {
            const modal = Modal.getInstance(document.getElementById('complaintsModal'));
            modal.hide();
        },
    },
    created() {
        this.fetchComplaints();
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