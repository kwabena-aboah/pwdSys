import { createRouter, createWebHistory } from "vue-router";
import LoginComponent from "@/components/Login.vue";
// import RegisterComponent from "@/components/Register.vue";
import store from "@/store";

const routes = [
    {
        path: "/",
        name: "LoginComponent",
        component: LoginComponent
    },
    {
        path: '/dashboard',
        name: 'DashboardPage',
        component: () => import('../views/Dashboard.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/records',
        name: 'PWDRecordList',
        component: () => import('../views/PWDRecordList.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/disability-type',
        name: 'DisabilityTypePage',
        component: () => import('../views/DisabilityType.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/beneficiary-support',
        name: 'BenefitSupport',
        component: () => import('../views/BenefitSupport.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/certificates',
        name: 'CertificatePage',
        component: () => import('../views/Certificate.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/complaints',
        name: 'ComplaintPage',
        component: () => import('../views/Complaints.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/service_type',
        name: 'ServiceTypePage',
        component: () => import('../views/ServiceType.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/medical_records',
        name: 'MedicalRecordPage',
        component: () => import('../views/MedicalRecords.vue'),
        meta: { requiresAuth: true },
    },
];

const router  = createRouter({
    history: createWebHistory(),
    routes,
});

// Navigation guard for protected routes
router.beforeEach((to, from, next) => {
    const isAuthenticated = store.getters.isAuthenticated;
    if (to.meta.requiresAuth && !isAuthenticated) {
        next({ name: "LoginComponent" });
    } else {
        next();
    }
});

export default router;