<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <div class="container-fluid">
              <h2 class="text-center">PWD Records</h2>

              <!-- Floating button -->
             <button 
                class="btn btn-primary rounded-circle position-fixed"
                style="bottom: 30px; right: 30px; width: 60px; height: 60px;"
                @click="openModal('create')"
                >
                <i class="bi bi-plus-lg"></i>
            </button>

             <!-- Search filter -->
             <div class="mb-3">
                 <input type="text" name="search" class="form-control" v-model="searchQuery" placeholder="Search name or contact number..." @input="fetchRecords(1)">
             </div>

             <!-- Add PWDRecord Modal -->
             <div class="modal fade" id="PWDModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="PWDModalLabel">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title fs-5" id="PWDModalLabel">{{ modalTitle }}</h5>
                            <button class="btn-close" type="button" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <form @submit.prevent="handleSubmit">
                            <div class="modal-body">
                                <div class="mb-3">
                                    <label for="full_name" class="form-label">Full Name</label>
                                    <input type="text" id="full_name" name="full_name" v-model="form.full_name" class="form-control" required />
                                </div>
                                <div class="mb-3">
                                    <label for="date_of_birth" class="form-label">Date of Birth</label>
                                    <input type="date" id="date_of_birth" name="date_of_birth" v-model="form.date_of_birth" class="form-control" required />
                                </div>
                                <div class="mb-3">
                                    <label for="gender" class="form-label">Gender</label>
                                    <select name="gender" id="gender" v-model="form.gender" class="form-select" required>
                                        <option value="" disabled>Select gender</option>
                                        <option value="male">Male</option>
                                        <option value="female">Female</option>
                                        <option value="other">Other</option>
                                    </select>
                                </div>
                                <div class="mb-3">
                                  <label for="disability_type" class="form-label">Disability Type</label>
                                  <select name="disability_type" id="disability_type" class="form-select" v-model="form.disability_type" required>
                                     <option value="" disabled>Select Disability Type</option>
                                     <option v-for="dtype in disability" :key="dtype.id" :value="dtype.id">
                                         {{ dtype.id }}. {{ dtype.disability_type }}
                                     </option>
                                 </select>
                                   <div class="container">
                                    <p>Click on the "Next" option to select other disability type not listed.</p>
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
                                  <label for="id_photo" class="form-label">Select Passport Picture</label>
                                  <input type="file" 
                                      id="id_photo" 
                                      name="id_photo" 
                                      class="form-control"
                                      @change="handleFileChange"
                                      accept="image/*" />
                              </div>
                              <div class="mb-3">
                                    <label for="address" class="form-label">Address</label>
                                    <input type="text" id="address" name="address" v-model="form.address" class="form-control" autocomplete="true" required />
                                </div>
                                <div class="mb-3">
                                    <label for="contact_number" class="form-label">Contact Number</label>
                                    <input type="text" id="contact_number" name="contact_number" v-model="form.contact_number" class="form-control" required />
                                </div>
                                <div class="mb-3">
                                    <label for="emergency_contact_name" class="form-label">Emergency Contact Name</label>
                                    <input type="text" id="emergency_contact_name" name="emergency_contact_name" v-model="form.emergency_contact_name" class="form-control" required />
                                </div>
                                <div class="mb-3">
                                    <label for="emergency_phone" class="form-label">Emergency Phone</label>
                                    <input type="text" id="emergency_phone" name="emergency_phone" v-model="form.emergency_phone" class="form-control" required />
                                </div>
                                <div class="mb-3">
                                  <div class="form-check form-switch">
                                        <label for="is_verified" class="form-check-label">Verified?</label>
                                        <input type="checkbox" id="is_verified" name="is_verified" v-model="form.is_verified" class="form-check-input" value="is_verified" />
                                    </div>
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

             <!-- PWDRecords list -->
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>Full Name</th>
                    <th>Disability Type</th>
                    <th>Gender</th>
                    <th>Verified?</th>
                    <th>Registration Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody v-if="this.records?.length > 0">
                  <tr v-for="record in records" :key="record.id">
                    <td>{{ record.full_name }}</td>
                    <td>{{ record.disability_name }}</td>
                    <td>{{ record.gender }}</td>
                    <td>{{ record.is_verified }}</td>
                    <td>{{ record.registration_date }}</td>
                    <td>
                      <button class="btn btn-sm btn-warning me-2" @click="openModal('edit', record)">Edit</button>
                      <button class="btn btn-sm btn-danger" @click="deleteRecord(record.id)">Delete</button>
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

            </div>

        </main>
    </div>
</template>

<script>
import instance from '@/api/axios';
import { Modal } from "bootstrap";
import Navbar from "@/components/Navbar.vue"
import Sidebar from "@/components/Sidebar.vue"
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

export default {
  components: {
        Navbar,
        Sidebar,
    },
  data() {
    return {
      records: [],
      disability: [],
      form: {
          id: null,
          full_name: "",
          date_of_birth: "",
          gender: "",
          disability_type: "",
          id_photo: "", // Store vase64 or file object
          address: "",
          contact_number: "",
          emergency_contact_name: "",
          emergency_phone: "",
          is_verified: false,
          // user: ""
      },
      searchQuery: "",
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
    }
  },
  created() {
    this.fetchRecords();
    this.fetchDisabilityType()
  },
  methods: {
    async fetchDisabilityType(urls = `/disability_type/` ) {
        try {
            const response = await instance.get(urls, {
                headers: {
                'Authorization': `Bearer ${this.$store.state.accessToken}`,
              }
            });
            this.disability = response.data.results;
            this.paginate.next = response.data.next;
            this.paginate.prev = response.data.previous;
            console.log(response.data);
        } catch (error) {
            toast.error("Error fetching Disability Type!");
            console.error("Error fetching Disability Type:", error);
        }
    },
    changeList(urls) {
        if (urls) {
            this.fetchDisabilityType(urls);
        }
    },
    async fetchRecords(url = `/pwd_records/`) {
      try {
        const response = await instance.get(url, {
            headers: {
            'Authorization': `Bearer ${this.$store.state.accessToken}`,
          },
          params: {
            q: this.searchQuery,
            page: this.page
          }
        });
        this.records = response.data.results;
        this.pagination.next = response.data.next;
        this.pagination.prev = response.data.previous;
        console.log(response.data);
      } catch (error) {
          toast.error("Error fetching records!");
          console.error("Error fetching records:", error);
          // this.records = [];
      }
    },
    changePage(url) {
        if (url) {
            this.fetchRecords(url);
        }
    },
    openModal(action, record = null) {
      if (action === 'create') {
          this.modalTitle = 'Add PWD Record';
          this.modalAction = 'Create';
          this.form = { id: null, full_name: "", date_of_birth: "", gender: "", disability_type: "", id_photo: "", address: "", contact_number: "", emergency_contact_name: "", emergency_phone: "", is_verified: false, /*user: ""*/ };
      } else if (action === 'edit') {
          this.modalTitle = 'Edit PWD Record';
          this.modalAction = 'Update';
          this.form = { ...record };
      }
      const modal = new Modal(document.getElementById('PWDModal'));
      modal.show();
    },
    handleFileChange(event){
      const file = event.target.files[0];
      if (file) {
        this.form.id_photo = file // store the file object
        this.convertToBase64(file);
      }
    },
    convertToBase64(file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        this.form.id_photo = event.target.result; // store base64 string
      };
      reader.readAsDataURL(file);
    },
    async handleSubmit(event) {
      event.preventDefault(); // Prevent default form submission behavior

      if (this.modalAction === 'Create') {
        await this.createRecord();
      } else {
          await this.updateRecord();
      }
    },
    async createRecord() {
      // Create new PWD Record Function
      try {
        let formData = new FormData();
        // Append form fields
        formData.append('full_name', this.form.full_name);
        formData.append('date_of_birth', this.form.date_of_birth);
        formData.append('gender', this.form.gender);
        formData.append('disability_type', this.form.disability_type);
        formData.append('address', this.form.address);
        formData.append('contact_number', this.form.contact_number);
        formData.append('emergency_contact_name', this.form.emergency_contact_name);
        formData.append('emergency_phone', this.form.emergency_phone);
        formData.append('is_verified', this.form.is_verified);
        // formData.append('user', this.$store.state.user.id);

        // Append the image file if selected
        if (this.form.id_photo instanceof File) {
          formData.append('id_photo', this.form.id_photo);
        }

        const response = await instance.post("/pwd_records/", formData, {
            headers: {
            'Authorization': `Bearer ${this.$store.state.accessToken}`,
            'Content-Type': 'multipart/form-data',
            }
        });
        this.records = response.data; // Add new record to the  list
        toast.success("Record created successfully!");
        this.fetchRecords();    // Reset form
        this.closeModal();
      } catch (error) {
          console.error("Error adding record:", error);
          toast.error("Failed to create record.", error);
      }
  },
  async updateRecord() {
      try {

        const response = await instance.put(`/pwd_records/${this.form.id}/`, this.form, {
            headers: {
            'Authorization': `Bearer ${this.$store.state.accessToken}`,
            'Content-Type': 'multipart/form-data',
            }
        });
        this.records = response.data;
        toast.success("Record updated successfully!");
        this.fetchRecords();    // Reset form
        this.closeModal();
      } catch (error) {
          toast.error("Error updating record!", error);
          // console.error("Error updating record:", error);
      }
  },
  async deleteRecord(id) {
      if(confirm('Are you sure you want to delete this record?')){
          await instance.delete(`/pwd_records/${id}/`, {
              headers: {
              'Authorization': `Bearer ${this.$store.state.accessToken}`,
              }
          })
          .then(() => this.fetchRecords(), toast.success("Record deleted successfully!"))
          .catch(error => //console.error(error); 
              toast.error("Error deleting record!", error)
          );
      }
  },
  closeModal() {
      const modal = Modal.getInstance(document.getElementById('PWDModal'));
      modal.hide();
  },
  },
}
</script>
