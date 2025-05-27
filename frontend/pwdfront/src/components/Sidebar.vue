<template>
    <dir class="container-fluid">
        <div class="row">
            <nav id="sidebarMenu" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
                <div class="position-sticky pt-3">
                  <h6 class="sidebar-heading d-flex flex-column align-items-center px-3 mt-4 mb-1 text-muted" style="height: 40px;">
                      <span>Core Pages</span>
                    </h6>
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <router-link to="/dashboard" class="nav-link d-flex flex-column align-items-center justify-content-center mb-4" style="height: 35px;" data-bs-toggle="tooltip" title="Dashboard">
                              <i class="bi bi-house custom-icon"></i>
                              <span class="label small">Dashboard</span>
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/records" class="nav-link d-flex flex-column align-items-center justify-content-center mb-4" style="height: 35px;" data-bs-toggle="tooltip" title="PWD Records">
                              <i class="bi bi-person-wheelchair custom-icon"></i>
                              <span class="label small">PWD Info</span>
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/medical_records" class="nav-link d-flex flex-column align-items-center justify-content-center mb-4" style="height: 35px;" data-bs-toggle="tooltip" title="Medical Records">
                              <i class="bi bi-journal-medical custom-icon"></i>
                              <span class="label small">Medical Info</span>
                            </router-link>
                        </li>
                        <li class="nav-item">
                          <router-link to="/certificates" class="nav-link d-flex flex-column align-items-center justify-content-center mb-4" style="height: 35px;" data-bs-toggle="tooltip" title="Medical Certificates">
                            <i class="bi bi-image-alt custom-icon"></i>
                            <span class="label small">Medical Certs</span>
                          </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/beneficiary-support" class="nav-link d-flex flex-column align-items-center justify-content-center mb-4" style="height: 35px;" data-bs-toggle="tooltip" title="Beneficial Support">
                              <i class="bi bi-award custom-icon"></i>
                              <span class="label small">Support</span>
                            </router-link>
                        </li>
                        <li class="nav-item">
                          <router-link to="/complaints" class="nav-link d-flex flex-column align-items-center justify-content-center mb-4" style="height: 35px;" data-bs-toggle="tooltip" title="Complaints">
                            <i class="bi bi-receipt custom-icon"></i>
                            <span class="label small">Complaints</span>
                          </router-link>
                        </li>
                    </ul>

                     <h6 class="sidebar-heading d-flex flex-column align-items-center px-3 mt-4 mb-1 text-muted" style="height: 40px;">
                      <span>Other Information</span>
                    </h6>

                    <ul class="nav flex-column mb-2">
                        <li class="nav-item">
                            <router-link to="/disability-type" class="nav-link d-flex flex-column align-items-center justify-content-center mb-4" style="height: 35px;" data-bs-toggle="tooltip" title="Disability Type">
                              <i class="bi bi-person-heart custom-icon"></i>
                              <span class="label small">Disability Type</span>
                            </router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/service_type" class="nav-link d-flex flex-column align-items-center justify-content-center mb-4" style="height: 35px;" data-bs-toggle="tooltip" title="Service Type">
                              <i class="bi bi-box2-heart custom-icon"></i>
                              <span class="label small">Service Type</span>
                            </router-link>
                        </li>
                        <li class="nav-item">
                          <router-link to="/verify-document" class="nav-link d-flex flex-column align-items-center justify-content-center mb-4" style="height: 35px;" data-bs-toggle="tooltip" title="Verify Document">
                            <i class="bi bi-file-check custom-icon"></i>
                            <span class="label small">Verify Docs</span>
                          </router-link>
                        </li>
                        <li class="nav-item">
                          <router-link to="/verify-upload" class="nav-link d-flex flex-column align-items-center justify-content-center mb-4" style="height: 35px;" data-bs-toggle="tooltip" title="Verify Upload">
                            <i class="bi bi-file-arrow-up custom-icon"></i>
                            <span class="label small">Verify Upload</span>
                          </router-link>
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

.custom-icon {
  font-size: 1.6rem;
  color: #0d6efd;
}

.label {
  font-size: 0.7rem;
  text-align: center;
  margin-top: 0.25rem;
  white-space: nowrap;
}

</style>