<template>
    <dir class="container-fluid">
        <div class="row">
            <nav id="sidebarMenu" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
                <div class="position-sticky pt-3">
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/records" class="nav-link">PWD Records</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/medical_records" class="nav-link">Medical Records</router-link>
                        </li>
                        <li class="nav-item">
                          <router-link to="/certificates" class="nav-link">Medical Certificates</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/beneficiary-support" class="nav-link">Beneficial Support</router-link>
                        </li>
                        <li class="nav-item">
                          <router-link to="/complaints" class="nav-link">Complaints</router-link>
                        </li>
                    </ul>

                     <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
                      <span>Other Information</span>
                    </h6>

                    <ul class="nav flex-column mb-2">
                        <li class="nav-item">
                            <router-link to="/disability-type" class="nav-link">Disability Type</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/service_type" class="nav-link">Service Type</router-link>
                        </li>
                    </ul>
                </div>
            </nav>
        </div>
    </dir>
</template>
<script>
export default {
    name: "SideBar",
};
</script>

<style scoped>
/*
 * Sidebar
 */

.sidebar {
  position: fixed;
  top: 0;
  /* rtl:raw:
  right: 0;
  */
  bottom: 0;
  /* rtl:remove */
  left: 0;
  z-index: 100; /* Behind the navbar */
  padding: 48px 0 0; /* Height of navbar */
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
}

@media (max-width: 767.98px) {
  .sidebar {
    top: 5rem;
  }
}

.sidebar-sticky {
  position: relative;
  top: 0;
  height: calc(100vh - 48px);
  padding-top: .5rem;
  overflow-x: hidden;
  overflow-y: auto; /* Scrollable contents if viewport is shorter than content. */
}

.sidebar .nav-link {
  font-weight: 500;
  color: #333;
}

.sidebar .nav-link .feather {
  margin-right: 4px;
  color: #727272;
}

.sidebar .nav-link.active {
  color: #2470dc;
}

.sidebar .nav-link:hover .feather,
.sidebar .nav-link.active .feather {
  color: inherit;
}

.sidebar-heading {
  font-size: .75rem;
  text-transform: uppercase;
}

</style>