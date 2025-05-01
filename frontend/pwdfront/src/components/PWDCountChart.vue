<template>
    <div class="chart-container">
        <canvas ref="chartCanvas"></canvas>
    </div>
</template>
<script>
import instance from '@/api/axios';

import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarController,
    BarElement,
    CategoryScale,
    LinearScale,
    DoughnutController,
    BubbleController,
    PointElement,
    LineController, 
    LineElement,
    PieController,
    ArcElement,
} from "chart.js";

ChartJS.register(Title, Tooltip, Legend, BarController, BarElement, CategoryScale, LinearScale, DoughnutController, LineController, LineElement, ArcElement, BubbleController, PointElement, PieController);

export default {
    props: ['filters'],
    data () {
        return {
            chart: null,
        };
    },
    watch: {
        filters: {
            deep: true,
            handler() {
                this.fetchPWDReport()
            }
        }
    },
    methods: {
        async fetchPWDReport(){
           const res = await instance.get("/pwd/report/", {
                 headers: {
                     'Authorization': `Bearer ${this.$store.state.accessToken}`,
                 },
                 params: this.filters,
            })
           const data = res.data
           if (this.chart) this.chart.destroy()

            this.chart = new ChartJS(this.$refs.chartCanvas, {
                type: 'bar',
                data: {
                    labels: ['Males', 'Females', 'Total'],
                    datasets: [{
                        label: 'PWD Gender Count',
                        data: [data.total_males, data.total_females, data.total_record],
                        backgroundColor: ['#3b82f6', '#f472b6', '#10b981']
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Gender Distribution of PWDs'
                        }
                    }
                }   
            })
        }

    },
    mounted() {
         this.fetchPWDReport();
     },
};
</script>
<style scoped>
.chart-container {
    position: relative;
    height: 400px;
    width: 100%;
}
</style>