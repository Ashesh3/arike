from django.db import models
from datetime import date

from django.contrib.auth.models import AbstractUser
from sqlalchemy import false

LOCAL_BODY_CHOICES = (
    (1, "Grama Panchayath"),
    (2, "Block Panchayath"),
    (3, "District Panchayath"),
    (4, "Nagar Panchayath"),
    (10, "Municipality"),
    (20, "Corporation"),
    (50, "Others"),
)

FACILITY_CHOICES = (
    ("phc", "PHC"),
    ("chc", "CHC"),
)

ROLE_CHOICES = (
    ("district_admin", "District Admin"),
    ("primary_nurse", "Primary Nurse"),
    ("secondary_nurse", "Secondary Nurse"),
)

GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
)

FAMILY_RELATIONS = (
    ("brother", "Brother"),
    ("sister", "Sister"),
    ("husband", "Husband"),
    ("wife", "Wife"),
    ("mother", "Mother"),
    ("son", "Son"),
    ("daughter", "Daughter"),
    ("uncle", "Uncle"),
    ("aunt", "Aunt"),
    ("nephew", "Nephew"),
    ("niece", "Niece"),
    ("cousin", "Cousin"),
    ("other", "Other"),
)


class RecordModel(models.Model):

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


class State(RecordModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(RecordModel):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class LocalBody(RecordModel):
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=100)
    lsg_body_code = models.IntegerField(choices=LOCAL_BODY_CHOICES)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Ward(RecordModel):
    local_body = models.ForeignKey(LocalBody, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    number = models.IntegerField()

    def __str__(self):
        return self.name


class Facility(RecordModel):
    kind = models.CharField(max_length=100, choices=FACILITY_CHOICES)
    name = models.CharField(max_length=100)
    address = models.TextField()
    pincode = models.IntegerField()
    phone = models.IntegerField()
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    phone = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=False, blank=False)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)

    REQUIRED_FIELDS = ["full_name", "role", "phone", "district"]

    def __str__(self):
        return self.first_name + " " + self.last_name


class Patient(RecordModel):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.TextField()
    landmark = models.CharField(max_length=100)
    phone = models.IntegerField()
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    emergency_phone_number = models.IntegerField()
    expired_time = models.DateTimeField(blank=True, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, blank=False, null=False)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, blank=False, null=False)

    def get_age(self):
        return date.today().year - self.date_of_birth.year

    def __str__(self) -> str:
        return self.full_name


class FamilyDetail(RecordModel):
    full_name = models.CharField(max_length=100)
    phone = models.IntegerField()
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    email = models.EmailField(max_length=100)
    relation = models.CharField(max_length=100, choices=FAMILY_RELATIONS)
    address = models.TextField()
    education = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    remarks = models.TextField()
    is_primary = models.BooleanField(default=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class Disease(RecordModel):
    name = models.CharField(max_length=100)
    icds_code = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class VisitSchedule(RecordModel):
    date = models.DateField()
    time = models.TimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    visitor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.full_name + " " + self.visitor.full_name


class VisitDetails(RecordModel):
    palliative_phase = models.CharField(max_length=100)
    blood_pressure = models.CharField(max_length=100)
    pulse = models.CharField(max_length=100)
    general_random_blood_sugar = models.CharField(max_length=100)
    personal_hygiene = models.CharField(max_length=100)
    mouth_hygiene = models.CharField(max_length=100)
    pubic_hygiene = models.CharField(max_length=100)
    systemic_examination = models.CharField(max_length=100)
    patient_at_peace = models.BooleanField(default=False)
    pain = models.BooleanField(default=False)
    symptoms = models.CharField(max_length=100)
    note = models.CharField(max_length=100)
    visit_details = models.ForeignKey(VisitSchedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.visit_details.patient.full_name + " " + self.visit_details.visitor.full_name


class Treatment(RecordModel):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    note = models.TextField()
    visit_details = models.ForeignKey(VisitDetails, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TreatmentNotes(RecordModel):
    note = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    visit = models.ForeignKey(VisitDetails, on_delete=models.CASCADE, null=True, blank=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)

    def __str__(self):
        return self.treatment.name


class PatientDisease(RecordModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, null=True, blank=True)
    note = models.TextField(max_length=100)

    def __str__(self):
        return self.patient.full_name + " " + self.disease.name
