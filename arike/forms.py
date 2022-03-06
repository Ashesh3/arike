from django.forms import ModelForm
from .models import (
    FAMILY_RELATIONS,
    GENDER_CHOICES,
    FamilyDetail,
    Patient,
    PatientDisease,
    Treatment,
    UserProfile,
    Facility,
    FACILITY_CHOICES,
    Ward,
)
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class ProfileEditForm(ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(), label="Previous Password", required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput(), label="New Password", required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password", required=False)

    def clean(self):
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("Password not matched")
            if not self.instance.check_password(old_password):
                raise forms.ValidationError("Incorrect current Password")
        return self.cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        if password:
            self.instance.set_password(password)
        if commit:
            self.instance.save()
        return self.instance

    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "email", "phone"]


class DistAdminFacilityCreateUpdateForm(ModelForm):
    kind = forms.ChoiceField(choices=FACILITY_CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(DistAdminFacilityCreateUpdateForm, self).__init__(*args, **kwargs)
        self.fields["ward"].queryset = Ward.objects.filter(
            is_deleted=False, local_body__district__name=self.request.user.district.name
        )

    class Meta:
        model = Facility
        fields = ["kind", "name", "address", "ward", "pincode", "phone"]


class NursePatientCreateUpdateForm(ModelForm):
    class Meta:
        model = Patient
        fields = ["full_name", "date_of_birth", "phone", "emergency_phone_number", "address", "landmark", "gender"]


class NursePatientFamilyCreateUpdateForm(ModelForm):
    class Meta:
        model = FamilyDetail
        fields = [
            "full_name",
            "phone",
            "date_of_birth",
            "gender",
            "email",
            "relation",
            "address",
            "education",
            "occupation",
            "is_primary",
            "remarks",
        ]


class NursePatientTreatmentCreateUpdateForm(ModelForm):
    class Meta:
        model = Treatment
        fields = [
            "name",
            "dosage",
            "note",
        ]


class NursePatientDiseaseCreateUpdateForm(ModelForm):
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.patient_id = kwargs.pop("patient_id", None)
        self.treatment_name = kwargs.pop("treatment_name", None)
        super(NursePatientDiseaseCreateUpdateForm, self).__init__(*args, **kwargs)
        self.fields["treatment"].queryset = Treatment.objects.filter(is_deleted=False, patient__id=self.patient_id)
        if self.treatment_name:
            self.initial["name"] = self.treatment_name

    class Meta:
        model = PatientDisease
        fields = ["note", "treatment"]


class VerifiedAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _(),
                code="inactive",
            )
        if not user.is_verified:
            raise forms.ValidationError(
                _(),
                code="unverified",
            )
