<template>
  <div>
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
      <ul v-if="records.length">
        <li v-for="record in records" :key="record.id">
          <RouterLink :to="{name: 'DashboardPage', params: {id: record.id}}">
              <strong>{{ record.full_name }} {{ record.contact_number }}</strong>
          </RouterLink>
        </li>
      </ul>

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