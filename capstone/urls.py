from arike.views import (
    DistAdminDashboardView,
    DistAdminProfileView,
    UserLoginView,
    UserLogoutView,
    index_page,
    DistAdminFacilityList,
    DistAdminFacilityCreate,
    DistAdminFacilityView,
    DistAdminFacilityUpdate,
    DistAdminFacilityDelete,
    NurseDashboardView,
    NurseProfileView,
    NursePatientList,
    NursePatientCreate,
    NursePatientCreate,
    NursePatientView,
    NursePatientUpdate,
    NursePatientFamilyList,
    NursePatientFamilyCreate,
    NursePatientFamilyUpdate,
    NursePatientFamilyDelete,
    NursePatientTreatmentList,
    NursePatientTreatmentCreate,
    NursePatientTreatmentUpdate,
    NursePatientTreatmentDelete,
    NursePatientDiseaseList,
    NursePatientDiseaseCreate,
    NursePatientDiseaseUpdate,
    NursePatientDiseaseDelete,
)

from arike.forms import VerifiedAuthenticationForm

from django.contrib import admin
from django.urls import include, path

dist_admin_urls = [
    path("dist_admin/dashboard/", DistAdminDashboardView.as_view(), name="dashboard"),
    path("dist_admin/profile/", DistAdminProfileView.as_view(), name="profile"),
    path("dist_admin/facility/", DistAdminFacilityList.as_view(), name="facility"),
    path("dist_admin/facility/create/", DistAdminFacilityCreate.as_view(), name="facility"),
    path("dist_admin/facility/view/<int:pk>/", DistAdminFacilityView.as_view(), name="facility"),
    path("dist_admin/facility/update/<int:pk>/", DistAdminFacilityUpdate.as_view(), name="facility"),
    path("dist_admin/facility/delete/<int:pk>/", DistAdminFacilityDelete.as_view(), name="facility"),
]

nurse_urls = [
    path("nurse/dashboard/", NurseDashboardView.as_view(), name="dashboard"),
    path("nurse/profile/", NurseProfileView.as_view(), name="profile"),
    path("nurse/patient/", NursePatientList.as_view(), name="patient"),
    path("nurse/patient/create/", NursePatientCreate.as_view(), name="patient"),
    path("nurse/patient/view/<int:pk>/", NursePatientView.as_view(), name="patient"),
    path("nurse/patient/update/<int:pk>/", NursePatientUpdate.as_view(), name="patient"),
]

patient_details_urls = [
    # family
    path("nurse/patient/<int:pk>/family/", NursePatientFamilyList.as_view(), name="patient"),
    path("nurse/patient/<int:pk>/family/create/", NursePatientFamilyCreate.as_view(), name="patient"),
    path("nurse/patient/<int:pk>/family/update/<int:subpk>/", NursePatientFamilyUpdate.as_view(), name="patient"),
    path("nurse/patient/<int:pk>/family/delete/<int:subpk>/", NursePatientFamilyDelete.as_view(), name="patient"),
    # disease
    path("nurse/patient/<int:pk>/disease/", NursePatientDiseaseList.as_view(), name="patient"),
    path("nurse/patient/<int:pk>/disease/create/", NursePatientDiseaseCreate.as_view(), name="patient"),
    path("nurse/patient/<int:pk>/disease/update/<int:subpk>/", NursePatientDiseaseUpdate.as_view(), name="patient"),
    path("nurse/patient/<int:pk>/disease/delete/<int:subpk>/", NursePatientDiseaseDelete.as_view(), name="patient"),
    # visit
    # path("nurse/patient/<int:pk>/visit/", NursePatientList.as_view(), name="patient"),
    # path("nurse/patient/<int:pk>/visit/create/", NursePatientList.as_view(), name="patient"),
    # path("nurse/patient/<int:pk>/visit/update/<int:subpk>/", NursePatientList.as_view(), name="patient"),
    # path("nurse/patient/<int:pk>/visit/delete/<int:subpk>/", NursePatientList.as_view(), name="patient"),
    # treatment
    path("nurse/patient/<int:pk>/treatment/", NursePatientTreatmentList.as_view(), name="patient"),
    path("nurse/patient/<int:pk>/treatment/create/", NursePatientTreatmentCreate.as_view(), name="patient"),
    path(
        "nurse/patient/<int:pk>/treatment/update/<int:subpk>/",
        NursePatientTreatmentUpdate.as_view(),
        name="patient",
    ),
    path(
        "nurse/patient/<int:pk>/treatment/delete/<int:subpk>/",
        NursePatientTreatmentDelete.as_view(),
        name="patient",
    ),
]

urlpatterns = (
    [
        path("__reload__/", include("django_browser_reload.urls")),
        path("admin/", admin.site.urls),
        path("login/", UserLoginView.as_view(), {"authentication_form": VerifiedAuthenticationForm}, name="login"),
        path("logout/", UserLogoutView.as_view(), name="logout"),
        path("", index_page, name="index"),
    ]
    + dist_admin_urls
    + nurse_urls
    + patient_details_urls
)
