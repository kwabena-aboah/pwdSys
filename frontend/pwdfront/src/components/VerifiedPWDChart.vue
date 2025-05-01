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
    PieController,
    ArcElement,
} from "chart.js";

ChartJS.register(Title, Tooltip, Legend, BarController, BarElement, CategoryScale, LinearScale, DoughnutController, ArcElement, BubbleController, PointElement, PieController,);

export default {
    name: 'VerifiedPWDChart',
    props: ['filters'],
    data () {
        return {
            chart: null,
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
    methods: {
        async loadChart() {
            const res = await instance.get('/pwd/verified-report/', {
                headers: {
                        'Authorization': `Bearer ${this.$store.state.accessToken}`,
                    },
                params: this.filters,
            })
            const { verified, total } = res.data
            const unverified = total - verified

            if (this.chart) this.chart.destroy()

                this.chart = new ChartJS(this.$refs.chartCanvas, {
                    type: 'pie',
                    data: {
                        labels: ['verified', 'unverified'],
                        datasets: [{
                            label: 'Verification Status',
                            data: [verified, unverified],
                            backgroundColor: ['#10b981', '#f87171']
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Total Verified vs Unverified PWDs'
                            }
                        }
                    }
                })
        }
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