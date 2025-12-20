<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <nav aria-label="breadcrumb" class="container-fluid">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><RouterLink to="/beneficiary-support">Beneficiary Support</RouterLink></li>
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

            <!-- Add Beneficiary Support Modal -->
             <div class="modal fade" id="beneficiarySupportModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="beneficiarySupportModalLabel">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title fs-5" id="beneficiarySupportModalLabel">{{ modalTitle }}</h5>
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
                                    <label for="application_status" class="form-label">Application Status</label>
                                    <select class="form-select" v-model="form.application_status" required>
                                        <option value="" disabled>Select status</option>
                                        <option value="pending">Pending</option>
                                        <option value="approved">Approved</option>
                                        <option value="rejected">Rejected</option>
                                    </select>
                                </div>
                                <div class="mb-3">
                                  <label for="service_type" class="form-label">Service Type</label>
                                  <Multiselect
                                    v-model="form.service_type"
                                    :options="searchQuery"
                                    label="service_name"
                                    value-prop="id"
                                    track-by="id"
                                    searchable
                                    :filter-results="false"
                                    @search-change="fetchServiceBenefit"
                                    placeholder="Search service type..."
                                    class="form-control p-0"
                                    />
                                </div>
                                <div class="mb-3">
                                  <label for="support_name" class="form-label">Support Name</label>
                                  <input type="text" name="support_name" id="support_name" v-model="form.support_name" class="form-control">
                                </div>
                                <div class="mb-3">
                                    <label for="approval_date" class="form-label">Approval Date</label>
                                    <input type="date" name="approval_date" id="approval_date" v-model="form.approval_date" class="form-control">
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
                       <input type="text" name="search" class="form-control" v-model="searchQ" placeholder="Search beneficiary..." @input="this.updateRouteQuery()">
                   </div>
                   <div class="col-sm-12 col-md-4 col-lg-4">
                       <select v-model="ordering" @change="this.updateRouteQuery()" class="form-select">
                         <option value="approval_date">Approval Date (Asc)</option>
                         <option value="-approval_date">Approval Date (Desc)</option>
                       </select>
                   </div>
                 </div>
             </div>

            <!-- Beneficiary Support list -->
              <div class="table-responsive">
                <table class="table table-striped table-hover">
                  <thead>
                      <tr>
                          <th>ID</th>
                          <th>PWD Name</th>
                          <th>Service Type</th>
                          <th>Support Name</th>
                          <th>Application Status</th>
                          <th>Approval Date</th>
                          <th>Actions</th>
                      </tr>
                  </thead>
                  <tbody v-if="this.beneficiarySupport?.length > 0">
                      <tr v-for="bensup in beneficiarySupport" :key="bensup.id">
                          <td>{{ bensup.id }}</td>
                          <td>{{ bensup.pwd_name }}</td>
                          <td>{{ bensup.service_name }}</td>
                          <td>{{ bensup.support_name }}</td>
                          <td>{{ bensup.application_status }}</td>
                          <td>{{ formatDate(bensup.approval_date) }}</td>
                          <td>
                              <button class="btn btn-sm btn-warning me-2" @click="openModal('edit', bensup)">
                                <i class="bi bi-pencil"></i>
                              </button>
                              <button class="btn btn-sm btn-danger" @click="deleteBeneficiarySupport(bensup.id)">
                                <i class="bi bi-trash"></i>
                              </button>
                          </td>
                      </tr>
                  </tbody>
                  <tbody v-else>
                      <tr>
                          <td colspan="6">Loading...</td>
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
import Multiselect from "@vueform/multiselect";
import "@vueform/multiselect/themes/default.css";

export default {
    components: {
        Navbar,
        Sidebar,
        Multiselect,
    },
    name: 'BenefitSupport',
    data() {
        return {
            beneficiarySupport: [],
            form: {
                id: null,
                pwd_id: "",
                service_type: "",
                support_name: "",
                application_status: "",
                approval_date: "",
            },
            suggestions: [],
            searchQuery: [],
            searchQ: "",
            ordering: "approval_date",
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

          this.searchQ = query.search || '';
          this.ordering = query.ordering || 'approval_date';
          this.fetchBeneficiarySupport(query.page || 1);
        },
        updateRouteQuery() {
          this.$router.push({
            path: this.$route.path,
            query: {
              search: this.searchQ || undefined,
              ordering: this.ordering || undefined,
              page: 1,
            },
          });
        },
        async fetchBeneficiarySupport(page = this.page) {
            try {
              this.loading = true;

                let url = `/support_services/?search=${this.searchQ}&page=${page}&ordering=${this.ordering}`;

                const response = await instance.get(url, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                }
                });
                this.beneficiarySupport = response.data.results;
                this.pagination.next = response.data.next;
                this.pagination.prev = response.data.previous;
                console.log(response.data);
            } catch (error) {
                toast.error("Error fetching Beneficiary!");
                console.error("Error fetching Beneficiary:", error);
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
        openModal(action, bensup = null) {
          if (action === 'create') {
              this.modalTitle = 'Add Beneficiary Support';
              this.modalAction = 'Create';
              this.form = { id: null, pwd_id: "", service_type: "", support_name: "", application_status: "", approval_date: "",};
          } else if (action === 'edit') {
              this.modalTitle = 'Edit Beneficiary Support';
              this.modalAction = 'Update';
              this.form = { ...bensup };
          }
          const modal = new Modal(document.getElementById('beneficiarySupportModal'));
          modal.show();
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
        fetchServiceBenefit(query) {
          if (!query || query.length < 2){
            this.searchQuery = [];
            return;
          }

          instance.get('/service_type/', {
              headers: {
                'Authorization': `Bearer ${this.$store.state.accessToken}`,
              },
              params: { search: query },
          })
         .then((response) => {
          this.searchQuery = response.data.results ?? response.data;
         })
         .catch((error) => {
          toast.error("Error fetching service type!");
          console.error(error)
         });
      },
    handleSubmit() {
            if (this.modalAction === 'Create') {
                this.createBenefitSupport();
            } else {
                this.updateBenefitSupport();
            }
        },
    async createBenefitSupport() {
            try {
                let formData = new FormData();
                // Append form fields
                formData.append('pwd_id', this.form.pwd_id || "");
                formData.append('service_type', this.form.service_type);
                formData.append('support_name', this.form.support_name || "");
                formData.append('application_status', this.form.application_status || "");
                formData.append('approval_date', this.form.approval_date || "");

                const response = await instance.post("/support_services/", formData, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    'Content-Type': 'multipart/form-data',
                    }
                });
                this.beneficiarySupport = response.data; // Add new medical record to the  list
                toast.success("Beneficiary support created successfully!");
                this.fetchBeneficiarySupport();    // Reset form
                this.closeModal();
            } catch (error) {
                // console.error("Error adding beneficiary support:", error);
                toast.error("Failed to create beneficiary support.", error);
            }
        },
    async updateBenefitSupport() {
            try {
                let formData = new FormData();
                // Append form fields
                formData.append('pwd_id', this.form.pwd_id || "");
                formData.append('service_type', this.form.service_type);
                formData.append('support_name', this.form.support_name || "");
                formData.append('application_status', this.form.application_status || "");
                formData.append('approval_date', this.form.approval_date || "");

                const response = await instance.put(`/support_services/${this.form.id}/`, formData, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    'Content-Type': 'multipart/form-data',
                    }
                });
                this.beneficiarySupport = response.data;
                toast.success("Beneficiary support updated successfully!");
                this.fetchBeneficiarySupport();    // Reset form
                this.closeModal();
            } catch (error) {
                toast.error("Error updating beneficiary support!", error);
                // console.error("Error updating beneficiary support:", error);
            }
        },
    async deleteBeneficiarySupport(id) {
            if(confirm('Are you sure you want to delete this beneficiary support?')){
                await instance.delete(`/support_services/${id}/`, {
                    headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    }
                })
                .then(() => this.fetchBeneficiarySupport(), toast.success("Beneficiary support deleted successfully!"))
                .catch(error => //console.error(error); 
                    toast.error("Error deleting beneficiary support!", error)
                );
            }
        },
        closeModal() {
            const modal = Modal.getInstance(document.getElementById('beneficiarySupportModal'));
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
        this.fetchBeneficiarySupport();
        this.fetchRecords();
        this.fetchServiceBenefit();
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