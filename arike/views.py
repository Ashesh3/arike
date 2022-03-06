from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import (
    FACILITY_CHOICES,
    Disease,
    FamilyDetail,
    Patient,
    PatientDisease,
    Treatment,
    UserProfile,
    Facility,
    Ward,
)
from .forms import (
    ProfileEditForm,
    DistAdminFacilityCreateUpdateForm,
    NursePatientCreateUpdateForm,
    NursePatientFamilyCreateUpdateForm,
    NursePatientTreatmentCreateUpdateForm,
    NursePatientDiseaseCreateUpdateForm,
)
from django.db.models import Q


def index_page(request):
    if request.user.is_authenticated:
        if request.user.role == "district_admin":
            return HttpResponseRedirect("/dist_admin/dashboard/")
        if request.user.role == "primary_nurse":
            return HttpResponseRedirect("/nurse/dashboard/")
    else:
        return HttpResponseRedirect("/login/")

    return HttpResponseRedirect("/404/")


class DistrictAdminAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if (
            not request.user.is_authenticated
            or not request.user.role == "district_admin"
            or not request.user.is_verified
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class NurseAccessMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if (
            not request.user.is_authenticated
            or request.user.role not in ("primary_nurse", "secondary_nurse")
            or not request.user.is_verified
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = "/"


class UserLogoutView(LoginRequiredMixin, LogoutView):
    redirect_authenticated_user = True
    success_url = "/"


class DistAdminDashboardView(DistrictAdminAccessMixin, TemplateView):
    template_name = "dist_admin/dashboard.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class DistAdminProfileView(DistrictAdminAccessMixin, UpdateView):
    model = UserProfile
    form_class = ProfileEditForm
    template_name = "dist_admin/profile.html"
    success_url = "/dist_admin/profile/"

    def get_object(self):
        return UserProfile.objects.filter(username=self.request.user.get_username()).first()


class DistAdminFacilityList(DistrictAdminAccessMixin, ListView):
    model = Facility
    context_object_name = "facilities"
    template_name = "dist_admin/facility/list.html"

    def get_context_data(self, **kwargs):
        context = super(DistAdminFacilityList, self).get_context_data(**kwargs)
        context["wards"] = Ward.objects.filter(
            is_deleted=False, local_body__district__name=self.request.user.district.name
        )
        context["kinds"] = FACILITY_CHOICES
        return context

    def get_queryset(self):
        facilities = Facility.objects.filter(
            is_deleted=False, ward__local_body__district__name=self.request.user.district.name
        )

        ward = self.request.GET.get("ward")
        if ward:
            facilities = facilities.filter(ward__name=ward)

        kind = self.request.GET.get("kind")
        if kind:
            facilities = facilities.filter(kind=kind)

        search = self.request.GET.get("query")
        if search:
            facilities = facilities.filter(
                Q(kind__icontains=search)
                | Q(name__icontains=search)
                | Q(address__icontains=search)
                | Q(pincode__icontains=search)
                | Q(phone__icontains=search)
                | Q(ward__name__icontains=search)
            )

        return facilities


class DistAdminFacilityCreate(DistrictAdminAccessMixin, CreateView):
    form_class = DistAdminFacilityCreateUpdateForm
    template_name = "dist_admin/facility/create.html"
    success_url = "/dist_admin/facility/"

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(DistAdminFacilityCreate, self).get_form_kwargs(*args, **kwargs)
        kwargs["request"] = self.request
        return kwargs


class DistAdminFacilityView(DistrictAdminAccessMixin, ListView):
    model = Facility
    context_object_name = "facilities"
    template_name = "dist_admin/facility/view.html"

    def get_queryset(self):
        return Facility.objects.filter(id=self.kwargs["pk"], is_deleted=False).first()


class DistAdminFacilityUpdate(DistrictAdminAccessMixin, UpdateView):
    model = Facility
    form_class = DistAdminFacilityCreateUpdateForm
    template_name = "dist_admin/facility/update.html"

    def get_object(self):
        return Facility.objects.filter(id=self.kwargs["pk"], is_deleted=False).first()

    def get_success_url(self):
        return f"/dist_admin/facility/view/{self.kwargs['pk']}/"

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(DistAdminFacilityUpdate, self).get_form_kwargs(*args, **kwargs)
        kwargs["request"] = self.request
        return kwargs


class DistAdminFacilityDelete(DistrictAdminAccessMixin, DeleteView):
    model = Facility
    context_object_name = "facilities"
    template_name = "dist_admin/facility/delete.html"

    def get_object(self):
        return Facility.objects.filter(id=self.kwargs["pk"], is_deleted=False).first()

    def delete(self, request, *args, **kwargs):
        facility = self.get_object()
        if facility:
            facility.soft_delete()
        return HttpResponseRedirect("/dist_admin/facility/")


# ===================


class NurseDashboardView(NurseAccessMixin, TemplateView):
    template_name = "nurse/dashboard.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class NurseProfileView(NurseAccessMixin, UpdateView):
    model = UserProfile
    form_class = ProfileEditForm
    template_name = "nurse/profile.html"
    success_url = "/nurse/profile/"

    def get_object(self):
        return UserProfile.objects.filter(username=self.request.user.get_username()).first()


class NursePatientList(NurseAccessMixin, ListView):
    model = Patient
    context_object_name = "patients"
    template_name = "nurse/patient/list.html"

    def get_queryset(self):
        patients = Patient.objects.filter(is_deleted=False, facility=self.request.user.facility)

        search = self.request.GET.get("query")
        if search:
            patients = patients.filter(
                Q(full_name__icontains=search)
                | Q(landmark__icontains=search)
                | Q(address__icontains=search)
                | Q(gender__icontains=search)
                | Q(phone__icontains=search)
                | Q(ward__name__icontains=search)
            ).all()

        return patients


class NursePatientCreate(NurseAccessMixin, CreateView):
    form_class = NursePatientCreateUpdateForm
    template_name = "nurse/patient/create.html"
    success_url = "/nurse/patient/"

    def form_valid(self, form):
        form.instance.facility = self.request.user.facility
        form.instance.ward = self.request.user.facility.ward
        return super().form_valid(form)


class NursePatientView(NurseAccessMixin, ListView):
    model = Patient
    context_object_name = "patient"
    template_name = "nurse/patient/view.html"

    def get_queryset(self):
        return Patient.objects.filter(
            id=self.kwargs["pk"], is_deleted=False, facility=self.request.user.facility
        ).first()


class NursePatientUpdate(NurseAccessMixin, UpdateView):
    model = Patient
    form_class = NursePatientCreateUpdateForm
    template_name = "nurse/patient/update.html"

    def get_object(self):
        return Patient.objects.filter(
            id=self.kwargs["pk"], is_deleted=False, facility=self.request.user.facility
        ).first()

    def get_success_url(self):
        return f"/nurse/patient/view/{self.kwargs['pk']}/"


# patient family


class NursePatientFamilyList(NurseAccessMixin, ListView):
    model = FamilyDetail
    context_object_name = "families"
    template_name = "nurse/patient/family/list.html"

    def get_queryset(self):
        return FamilyDetail.objects.filter(
            is_deleted=False,
            patient__id=self.kwargs["pk"],
            patient__is_deleted=False,
            patient__facility=self.request.user.facility,
        )

    def get_context_data(self, **kwargs):
        context = super(NursePatientFamilyList, self).get_context_data(**kwargs)
        context["patient"] = Patient.objects.filter(
            id=self.kwargs["pk"], is_deleted=False, facility=self.request.user.facility
        ).first()
        return context


class NursePatientFamilyCreate(NurseAccessMixin, CreateView):
    form_class = NursePatientFamilyCreateUpdateForm
    template_name = "nurse/patient/family/create.html"

    def get_success_url(self):
        return f"/nurse/patient/{self.kwargs['pk']}/family/"

    def form_valid(self, form):
        form.instance.patient = Patient.objects.filter(
            id=self.kwargs["pk"], is_deleted=False, facility=self.request.user.facility
        ).first()
        return super().form_valid(form)


class NursePatientFamilyUpdate(NurseAccessMixin, UpdateView):
    model = FamilyDetail
    form_class = NursePatientFamilyCreateUpdateForm
    template_name = "nurse/patient/family/update.html"

    def get_object(self):
        return FamilyDetail.objects.filter(
            is_deleted=False,
            id=self.kwargs["subpk"],
            patient__id=self.kwargs["pk"],
            patient__is_deleted=False,
            patient__facility=self.request.user.facility,
        ).first()

    def get_success_url(self):
        return f"/nurse/patient/{self.kwargs['pk']}/family/"


class NursePatientFamilyDelete(NurseAccessMixin, DeleteView):
    model = FamilyDetail
    context_object_name = "families"
    template_name = "nurse/patient/family/delete.html"

    def get_object(self):
        return FamilyDetail.objects.filter(
            is_deleted=False,
            id=self.kwargs["subpk"],
            patient__id=self.kwargs["pk"],
            patient__is_deleted=False,
            patient__facility=self.request.user.facility,
        ).first()

    def delete(self, request, *args, **kwargs):
        family = self.get_object()
        if family:
            family.soft_delete()
        return HttpResponseRedirect(f"/nurse/patient/{self.kwargs['pk']}/family/")

    def get_context_data(self, **kwargs):
        context = super(NursePatientFamilyDelete, self).get_context_data(**kwargs)
        context["patient"] = Patient.objects.filter(
            id=self.kwargs["pk"], is_deleted=False, facility=self.request.user.facility
        ).first()
        return context


# patient treatments


class NursePatientTreatmentList(NurseAccessMixin, ListView):
    model = FamilyDetail
    context_object_name = "treatments"
    template_name = "nurse/patient/treatment/list.html"

    def get_queryset(self):
        return Treatment.objects.filter(
            is_deleted=False,
            patient__id=self.kwargs["pk"],
            patient__is_deleted=False,
            patient__facility=self.request.user.facility,
        )

    def get_context_data(self, **kwargs):
        context = super(NursePatientTreatmentList, self).get_context_data(**kwargs)
        context["patient"] = Patient.objects.filter(
            id=self.kwargs["pk"], is_deleted=False, facility=self.request.user.facility
        ).first()
        return context


class NursePatientTreatmentCreate(NurseAccessMixin, CreateView):
    form_class = NursePatientTreatmentCreateUpdateForm
    template_name = "nurse/patient/treatment/create.html"

    def get_success_url(self):
        return f"/nurse/patient/{self.kwargs['pk']}/treatment/"

    def form_valid(self, form):
        form.instance.patient = Patient.objects.filter(
            id=self.kwargs["pk"], is_deleted=False, facility=self.request.user.facility
        ).first()
        return super().form_valid(form)


class NursePatientTreatmentUpdate(NurseAccessMixin, UpdateView):
    model = Treatment
    form_class = NursePatientTreatmentCreateUpdateForm
    template_name = "nurse/patient/treatment/update.html"

    def get_object(self):
        return Treatment.objects.filter(
            is_deleted=False,
            id=self.kwargs["subpk"],
            patient__id=self.kwargs["pk"],
            patient__is_deleted=False,
            patient__facility=self.request.user.facility,
        ).first()

    def get_success_url(self):
        return f"/nurse/patient/{self.kwargs['pk']}/treatment/"


class NursePatientTreatmentDelete(NurseAccessMixin, DeleteView):
    model = Treatment
    context_object_name = "treatments"
    template_name = "nurse/patient/treatment/delete.html"

    def get_object(self):
        return Treatment.objects.filter(
            is_deleted=False,
            id=self.kwargs["subpk"],
            patient__id=self.kwargs["pk"],
            patient__is_deleted=False,
            patient__facility=self.request.user.facility,
        ).first()

    def delete(self, request, *args, **kwargs):
        family = self.get_object()
        if family:
            family.soft_delete()
        return HttpResponseRedirect(f"/nurse/patient/{self.kwargs['pk']}/treatment/")

    def get_context_data(self, **kwargs):
        context = super(NursePatientTreatmentDelete, self).get_context_data(**kwargs)
        context["patient"] = Patient.objects.filter(
            id=self.kwargs["pk"], is_deleted=False, facility=self.request.user.facility
        ).first()
        return context


# patient diseases


class NursePatientDiseaseList(NurseAccessMixin, ListView):
    model = PatientDisease
    context_object_name = "diseases"
    template_name = "nurse/patient/disease/list.html"

    def get_queryset(self):
        return PatientDisease.objects.filter(
            is_deleted=False,
            patient__id=self.kwargs["pk"],
            patient__is_deleted=False,
            patient__facility=self.request.user.facility,
        )

    def get_context_data(self, **kwargs):
        context = super(NursePatientDiseaseList, self).get_context_data(**kwargs)
        context["patient"] = Patient.objects.filter(
            id=self.kwargs["pk"], is_deleted=False, facility=self.request.user.facility
        ).first()
        return context


class NursePatientDiseaseCreate(NurseAccessMixin, CreateView):
    form_class = NursePatientDiseaseCreateUpdateForm
    template_name = "nurse/patient/disease/create.html"

    def get_success_url(self):
        return f"/nurse/patient/{self.kwargs['pk']}/disease/"

    def form_valid(self, form):
        form.instance.patient = Patient.objects.filter(
            id=self.kwargs["pk"], is_deleted=False, facility=self.request.user.facility
        ).first()
        form.instance.disease = Disease.objects.get_or_create(name=form.cleaned_data["name"])[0]
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(NursePatientDiseaseCreate, self).get_form_kwargs(*args, **kwargs)
        kwargs["request"] = self.request
        kwargs["patient_id"] = self.kwargs["pk"]
        return kwargs


class NursePatientDiseaseUpdate(NurseAccessMixin, UpdateView):
    model = PatientDisease
    form_class = NursePatientDiseaseCreateUpdateForm
    template_name = "nurse/patient/disease/update.html"

    def get_object(self):
        return PatientDisease.objects.filter(
            is_deleted=False,
            id=self.kwargs["subpk"],
            patient__id=self.kwargs["pk"],
            patient__is_deleted=False,
            patient__facility=self.request.user.facility,
        ).first()

    def get_success_url(self):
        return f"/nurse/patient/{self.kwargs['pk']}/disease/"

    def form_valid(self, form):
        form.instance.disease = Disease.objects.get_or_create(name=form.cleaned_data["name"])[0]
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(NursePatientDiseaseUpdate, self).get_form_kwargs(*args, **kwargs)
        kwargs["request"] = self.request
        kwargs["patient_id"] = self.kwargs["pk"]
        kwargs["treatment_name"] = self.get_object().disease.name
        return kwargs


class NursePatientDiseaseDelete(NurseAccessMixin, DeleteView):
    model = PatientDisease
    context_object_name = "diseases"
    template_name = "nurse/patient/disease/delete.html"

    def get_object(self):
        return PatientDisease.objects.filter(
            is_deleted=False,
            id=self.kwargs["subpk"],
            patient__id=self.kwargs["pk"],
            patient__is_deleted=False,
            patient__facility=self.request.user.facility,
        ).first()

    def delete(self, request, *args, **kwargs):
        family = self.get_object()
        if family:
            family.soft_delete()
        return HttpResponseRedirect(f"/nurse/patient/{self.kwargs['pk']}/disease/")

    def get_context_data(self, **kwargs):
        context = super(NursePatientDiseaseDelete, self).get_context_data(**kwargs)
        context["patient"] = Patient.objects.filter(
            id=self.kwargs["pk"], is_deleted=False, facility=self.request.user.facility
        ).first()
        return context
