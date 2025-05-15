<template>
  <div class="container-fluid">
    <form @submit.prevent class="form-inline mb-3">
      <input
      type="text"
      name="search" 
      id="search"
      class="form-control form-control-dark w-100"
      v-model="searchQuery"
      placeholder="Search pwd by name or phone"
      @input="fetchSuggestions"
      aria-label="Search"
      />
      <!-- <button class="btn btn-primary" type="submit">Search</button> -->
    </form>
    <!-- Autocomplete Suggestions -->
     <ul v-if="suggestions.length && searchQuery" class="list-group">
        <li 
        class="list-group-item"
        v-for="suggestion in suggestions"
        :key="suggestion.id"
        @click="selectSuggestion(suggestion.full_name)">
          {{ suggestion.full_name }} {{ suggestion.contact_number }}
        </li>
     </ul>

     <!-- Search Results -->
      <div v-if="records.length" class="list-group">
        <div v-for="record in records" :key="record.id" class="list-group-item list-group-item-action list-group-flush">
          <div class="p-5 mb-4 bg-light rounded-4">
              <img :src="record.id_photo" :alt="record.full_name" class="img-fluid" style="max-width: 200px;"/>
              <p class="display-4 fw-bold"><em>Full Name:</em> {{ record.full_name }}</p>
              <p class="lead fw-bold"><em>Phone Number:</em> {{ record.contact_number }}</p>
              <p class="lead fw-bold"><em>Date of Birth:</em> {{ record.date_of_birth }}</p>
              <p class="lead fw-bold"><em>Gender:</em> {{ record.gender }}</p>
              <p class="lead fw-bold"><em>Disability Type:</em> {{ record.disability_name }}</p>
              <p class="lead fw-bold"><em>Address:</em> {{ record.address }}</p>
              <p class="lead fw-bold"><em>Contact Number:</em> {{ record.contact_number }}</p>
              <p class="lead fw-bold"><em>Emergency Contact Name:</em> {{ record.emergency_contact_name }}</p>
              <p class="lead fw-bold"><em>Emergency Phone:</em> {{ record.emergency_phone }}</p>
              <p class="lead fw-bold"><em>Verified?</em> {{ record.is_verified }}</p>
              <p class="lead fw-bold"><em>Registration Date:</em> {{ record.registration_date }}</p>
          </div>
        </div>
      </div>

      <p v-else-if="!loading && searchQuery">No records found.</p>
      <p v-if="loading">Loading...</p>

      <!-- Pagination Controls -->
       <div v-if="pagination.count > pagination.limit" class="mt-3">
        <button 
          class="btn btn-outline-secondary"
          :disabled="pagination.offset === 0"
          @click="prevPage"
          >
            Previous
          </button>
          <button 
          class="btn btn-outline-secondary"
          :disabled="pagination.offset + pagination.limit >= pagination.count"
          @click="nextPage"
          >
            Next
          </button>
       </div>
  </div>
</template>

<script>
import instance from '@/api/axios';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default {
  name: 'SearchPage',
  data() {
    return {
      searchQuery: "", 
      records: [],
      suggestions: [],
      loading: false,
      pagination: {
        count: 0,
        limit: 10,
        offset: 0,
      },
    };
  },
  methods: {
    async searchRecords() {
      this.loading = true;
      try {
        const response = await instance.get(`/pwd/search`, {
                headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                },
                params: {
                  q: this.searchQuery,
                  limit: this.pagination.limit,
                  offset: this.pagination.offset,
                },
            });
            this.records = response.data.results;
            this.pagination.count = response.data.count;
      } catch (error) {
        toast.error("Error fetching records:", error);
        // console.error("Error fetching records:", error);
      } finally {
        this.loading = false;
      }
    },
    async fetchSuggestions() {
      if (this.searchQuery.trim() === "") {
        this.suggestions = [];
        return;
      }
      try {
        const response = await instance.get(`/pwd/search/`, {
                headers: {
                    'Authorization': `Bearer ${this.$store.state.accessToken}`,
                },
                params: {
                  q: this.searchQuery,
                  limit: 5
                },
            });
            this.suggestions = response.data.results;
      } catch (error) {
        toast.error("Error fetching suggestions:", error);
        // console.error("Error fetching suggestions:", error);
      }
    },
    selectSuggestion(full_name){
      this.searchQuery = full_name;
      this.suggestions = [];
      this.searchRecords();
    },
    nextPage() {
      this.pagination.offset += this.pagination.limit;
      this.searchRecords();
    },
    prevPage() {
      this.pagination.offset -= this.pagination.limit;
      this.searchRecords();
    },
  },
}
</script>

<style scoped>
ul.list-group {
  position: absolute;
  width: 100%;
  z-index: 1000;
}
li.list-group-item {
  cursor: pointer;
}
</style>