<template>
    <div>
        <Navbar />
        <Sidebar />
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <div class="container-fluid">
                <nav aria-label="breadcrumb" class="container-fluid">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><RouterLink to="/dashboard">Dashboard Report</RouterLink></li>
                        <li class="breadcrumb-item active" aria-current="page">Overview</li>
                    </ol>
                </nav>
            </div>
            <div class="container-fluid">
                <div class="row">
                    <div class="col-md-4">
                        <div class="card text-white bg-danger mb-3">
                            <div class="card-header">Total Members</div>
                            <div class="card-body">
                                <h5 class="card-title">{{ totalPWDs }}</h5>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card text-white bg-warning mb-3">
                            <div class="card-header">Total Males</div>
                            <div class="card-body">
                                <h5 class="card-title">{{ totalMales }}</h5>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card text-white bg-success mb-3">
                            <div class="card-header">Total Females</div>
                            <div class="card-body">
                                <h5 class="card-title">{{ totalFemales }}</h5>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <hr>
            <br>
            <div class="filters">
                <label class="form-label">
                    From:
                    <input type="date" v-model="filters.startDate" name="startDate" class="form-control">
                </label>
                <label class="form-label">
                    To:
                    <input type="date" v-model="filters.endDate" name="endDate" class="form-control">
                </label>
            </div>
            <div class="chart-grid">
                <PWDCountChart :filters="filters" />
                <VerifiedPWDChart :filters='filters' />
            </div>
            <hr>
            <br>
            <div class="container-fluid">
                <PWDByDisabilityChart :filters='filters' />
            </div>
        </main>
    </div>
</template>

<script>
    import instance from '@/api/axios';
    import { toast } from "vue3-toastify";
    import "vue3-toastify/dist/index.css";
    import PWDCountChart from '@/components/PWDCountChart.vue'
    import PWDByDisabilityChart from '@/components/PWDByDisabilityChart.vue'
    import VerifiedPWDChart from '@/components/VerifiedPWDChart.vue'
    import Navbar from "@/components/Navbar.vue"
    import Sidebar from "@/components/Sidebar.vue"

    export default {
        components: {
            Navbar,
            Sidebar,
            PWDCountChart,
            PWDByDisabilityChart,
            VerifiedPWDChart,
        },
        name: 'DashboardPage',
        data() {
            return {
                totalMembers: 0,
                totalMales: 0,
                totalFemales: 0,
                filters: {
                    startDate: '',
                    endDate: '',
                }
            }
        },
        methods: {
            async fetchPWDReport(){
                try{
                    await instance.get("/pwd/report/", {
                     headers: {
                         'Authorization': `Bearer ${this.$store.state.accessToken}`,
                     },
                }).then((res) => {
                    this.totalPWDs = res.data.total_record;
                    this.totalMales = res.data.total_males;
                    this.totalFemales = res.data.total_females;
                });
                
                }catch (error){
                    toast.error("Error fetching report:", error);
                    console.error("Error fetching report:", error);
                }
            },
        },
        mounted() {
             this.fetchPWDReport();
         },
    }
</script>

<style scoped>
    .chart-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
    }
    .filters {
        margin-bottom: 2rem;
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
</style>