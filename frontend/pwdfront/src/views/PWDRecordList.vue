<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <div class="container-fluid">
              <nav aria-label="breadcrumb" class="container-fluid">
                  <ol class="breadcrumb">
                      <li class="breadcrumb-item"><RouterLink to="/records">PWD Records</RouterLink></li>
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
                                        <!-- <option value="other">Other</option> -->
                                    </select>
                                </div>
                                <div class="mb-3">
                                  <label for="disability_type" class="form-label">Disability Type</label>
                                  <div class="autocomplete-container" @keydown.down.prevent="moveDown" @keydown.up.prevent="moveUp" @keydown.enter.prevent="selectActive">
                                    <input
                                      type="text"
                                      v-model="form.disability_type"
                                      @input="debouncedFetchSuggestions"
                                      placeholder="Start typing a disability type..."
                                      @focus="isFocused = true"
                                      @blur="hideSuggestionsWithDelay"
                                      autocomplete="off"
                                      class="form-control"
                                      />
                                      <ul v-if="isFocused && suggestions.length && form.disability_type" class="ul">
                                        <li
                                          v-for="(dtype, index) in suggestions"
                                          :key="dtype.id"
                                          :class="{ active: index === activeIndex }"
                                          @mousedown.prevent="selectDisability(dtype)">
                                            {{ dtype.id }}. {{ dtype.disability_type }}
                                          </li>
                                      </ul>
                                      <p v-if="selectedDisability">Selected: {{ selectedDisability.disability_type }}</p>
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

             <!-- Search filter & Ordering -->
             <div class="container-fluid">
                 <div class="row mb-3">
                     <div class="col-sm-12 col-md-4 col-lg-4">
                       <input type="text" name="search" class="form-control" v-model="searchQuery" placeholder="Search name or contact number..." @input="this.updateRouteQuery()">
                   </div>
                   <div class="col-sm-12 col-md-4 col-lg-4">
                       <select v-model="ordering" @change="this.updateRouteQuery()" class="form-select">
                         <option value="registration_date">Registration Date (Asc)</option>
                         <option value="-registration_date">Registration Date (Desc)</option>
                       </select>
                   </div>
                   <div class="col-sm-12 col-md-4 col-lg-4">
                       <select v-model="filters.is_verified" @change="this.updateRouteQuery()" class="form-select">
                         <option value="">All Verification Status</option>
                         <option :value="true">Verified</option>
                         <option :value="false">Not Verified</option>
                       </select>
                   </div>
                 </div>
             </div>

             <!-- Export options -->
             <div class="container-fluid">
               <div class="row mb-3">
                 <div class="col-sm-12 col-md-1 col-lg-1">
                   <div class="text-end">
                     <button class="btn btn-outline-primary me-2" @click="exportRecords('csv')">Export CSV</button>
                   </div>
                 </div>
                 <div class="col-sm-12 col-md-1 col-lg-1">
                   <div>
                     <button class="btn btn-outline-danger mb-3" @click="exportToPDF()">Export PDF</button>
                   </div>
                 </div>
               </div>
             </div>
             
             <!-- PWDRecords list -->
             <div class="table-responsive">
               <table class="table table-striped">
                  <thead>
                    <tr>
                      <th>#.Full Name</th>
                      <th>Disability Type</th>
                      <th>Gender</th>
                      <th>ID Card</th>
                      <th>Verified?</th>
                      <th>Registration Date</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody v-if="this.records?.length > 0">
                    <tr v-for="record in records" :key="record.id">
                      <td>{{ record.id }}. {{ record.full_name }}</td>
                      <td>{{ record.disability_name }}</td>
                      <td>{{ record.gender }}</td>
                      <td><img :src="record.id_photo" :alt="record.full_name" class="rounded-circle img-fluid" style="width:50px; height:50px;"/></td>
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
             </div>

              <!-- Pagination controls -->
               <nav aria-label="Page navigation">
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
    name: 'PWDRecordList',
  data() {
    return {
      records: [],
      form: {
          id: null,
          full_name: "",
          date_of_birth: "",
          gender: "",
          disability_type: "",
          id_photo: null, // Store base64 or file object
          address: "",
          contact_number: "",
          emergency_contact_name: "",
          emergency_phone: "",
          is_verified: false,
      },
      suggestions: [],
      searchQuery: "",
      ordering: "registration_date",
      filters: {
        is_verified: "",
      },
      activeIndex: -1,
      isFocused: false,
      selectedDisability: null,
      debouceTimeout: null,
      loading: false,
      page: 1,
      modalTitle: '',
      modalAction: '',
      pagination: {
          next: null,
          prev: null,
      },
    };
  },
  created() {
    this.loadFromQuery();
    this.fetchDisabilityType();
  },
  watch: {
    '$route.query': {
      handler() {
        this.loadFromQuery();
      },
      deep: true,
      // immediate: true,
    }
  },
  methods: {
    loadFromQuery() {
      const query = this.$route.query;

      this.searchQuery = query.search || '';
      this.ordering = query.ordering || 'registration_date';
      this.filters.is_verified = query.is_verified ?? '';

      this.fetchRecords(query.page || 1);
    },
    updateRouteQuery() {
      this.$router.push({
        path: this.$route.path,
        query: {
          search: this.searchQuery || undefined,
          ordering: this.ordering || undefined,
          is_verified: this.filters.is_verified !== '' ? this.filters.is_verified : undefined,
          page: 1,
        },
      });
    },
    async fetchRecords(page = this.page) {
      try {
        this.loading = true;

        let url = `/pwd_records/?search=${this.searchQuery}&page=${page}&ordering=${this.ordering}`;

        if (this.filters.is_verified !== ''){
          url += `&is_verified=${this.filters.is_verified}`;
        }

        const response = await instance.get(url, {
            headers: {
            'Authorization': `Bearer ${this.$store.state.accessToken}`,
          }
        });
        this.records = response.data.results;
        this.pagination.next = response.data.next;
        this.pagination.prev = response.data.previous;
        console.log(response.data);
      } catch (error) {
        const status = error.response?.status;
        const message = error.response?.data || error.message;

        toast.error(`Error fetching records ${status ? ' (${status})' : ''}!`);
        console.error("Error fetching records:", message);
        // this.records = [];
      } finally {
        this.loading = false;
      }
    },
    changePage(url) {
        if (!url) return;
        const pageParam = new URLSearchParams(url.split('?')[1]).get('page');
        if (!pageParam || pageParam === this.$route.query.page) return;
        this.$router.push({
          path: this.$route.path,
          query: { ...this.$route.query, page: pageParam },
        });
    },
    async fetchDisabilityType() {
       if(this.form.disability_type.length < 2) {
        this.suggestions = []
        this.activeIndex = -1
        return
       }
       await instance.get('/disability_type/', {
            headers: {
            'Authorization': `Bearer ${this.$store.state.accessToken}`,
          },
          params: {
            q: this.form.disability_type,
          }
        })
       .then((response) => {
        this.suggestions = response.data.results;
        this.activeIndex = -1;
       })
       .catch((error) => {
        toast.error("Error fetching disability type!");
        console.error(error)
       })
      },
      debouncedFetchSuggestions() {
        clearTimeout(this.debouceTimeout)
        this.debouceTimeout = setTimeout(() => {
          this.fetchDisabilityType()
        }, 300)
      },
      selectDisability(dtype) {
        this.form.disability_type = dtype.disability_type
        this.selectedDisability = dtype
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
          this.selectDisability(this.suggestions[this.activeIndex])
        }
      },
      hideSuggestionsWithDelay() {
        setTimeout(() => {
          this.isFocused = false
        }, 100)
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
        if (file && file.type.startsWith("image/")){
          this.form.id_photo = file; // store the file object
          return;
        } else {
        toast.warn("Only image files are allowed (e.g., PNG, JPG, etc.)");
        this.form.id_photo = null;
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
        formData.append('disability_type', this.form.disability_type ? this.selectedDisability.id : "");
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

        if (!this.selectedDisability) {
          toast.warn('Please select a disability type from suggestion')
          return
        }

        const response = await instance.post("/pwd_records/", formData, {
            headers: {
            'Authorization': `Bearer ${this.$store.state.accessToken}`,
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
        let formData = new FormData();
        // Append form fields
        formData.append('full_name', this.form.full_name);
        formData.append('date_of_birth', this.form.date_of_birth);
        formData.append('gender', this.form.gender);
        formData.append('disability_type', this.form.disability_type ? this.selectedDisability.id : "");
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

        if (!this.selectedDisability) {
          toast.warn('Please select a disability type from suggestion')
          return
        }

        const response = await instance.put(`/pwd_records/${this.form.id}/`, formData, {
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
  exportRecords(format) {
    const query = { ...this.$route.query };
    const queryString = new URLSearchParams(query).toString();

    const url = `/pwd/export/?${queryString}`;

    const token = this.$store.state.accessToken;
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.setAttribute('target', '_blank');
    anchor.setAttribute('download', `pwd_records.${format}`);
    anchor.setAttribute('Authorization', `Bearer ${token}`);

    // To actually include the token in headers, use fetch
    instance.get(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      responseType: 'blob'
    })
    // .then(res => res.blob())
    .then(res => {
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(new Blob([res.data]));
      link.setAttribute('download', `pwd_records.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    })
    .catch(error => 
      toast.error("Export failed", error)
      // console.error(error)
      );
  },
  async exportToPDF() {
    try {
      const params = new URLSearchParams();

      if (this.searchQuery) params.append('search', this.searchQuery);
      if(this.filters.is_verified !== '') params.append('is_verified', this.filters.is_verified);

      const response = await instance.get(`/pwd/export/pdf/?${params.toString()}`, {
        responseType: 'blob',
      });

      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'PWD_Records_Report.pdf');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (error) {
      toast.error('Failed to export PDF');
    }
  },
},
}
</script>
<style scoped>
  /*.autocomplete-container {
    position: relative;
    width: 100px;
  }*/
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