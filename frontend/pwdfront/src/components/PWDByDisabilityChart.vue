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
    ArcElement,
} from "chart.js";

ChartJS.register(Title, Tooltip, Legend, BarController, BarElement, CategoryScale, LinearScale, DoughnutController, ArcElement, BubbleController, PointElement);

export default {
    name: "PWDByDisabilityChart",
    props: ['filters'],
    data() {
        return {
            chart: null
        }
    },
    watch: {
        filters: {
            deep: true,
            handler() {
                this.loadChart()
            }
        }
    },
    mounted() {
        this.loadChart()
    },
    methods : {
        async loadChart() {
            const res = await instance.get('/pwd/disability-report/', {
                headers: {
                        'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    },
                params: this.filters,
            })
            const data = res.data
            const labels = Object.keys(data)
            const males = labels.map(label => data[label].male || 0)
            const females = labels.map(label => data[label].female || 0)

            if (this.chart) {
                this.chart.destroy()
                this.chart = null
            }
                this.chart = new ChartJS(this.$refs.chartCanvas, {
                    type: 'bar',
                    data: {
                        labels,
                        datasets: [
                            {
                                label: 'Males',
                                data: males,
                                backgroundColor: '#3b82f6'
                            },
                            {
                                label: 'Females',
                                data: females,
                                backgroundColor: '#f472b6'
                            },
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'PWDs by Gender and Disability Type'
                            }
                        },
                    },
                })
        },
    }
}
</script>
<style scoped>
.chart-container {
    position: relative;
    height: 400px;
    width: 100%;
}
</style>