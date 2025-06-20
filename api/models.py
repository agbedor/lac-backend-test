from django.db import models
from django.contrib.auth.models import User

class Gender(models.Model):
    name = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name
    
class Title(models.Model):
    name = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name
    
class IdType(models.Model):
    name = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name
    
class Nationality(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class MaritalStatus(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
    
class Job(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class EmploymentStatus(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class CaseType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
class CourtType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class CourtRoom(models.Model):
    name = models.CharField(max_length=20, unique=True)
    court_type = models.ForeignKey(CourtType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class EmployerType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Party(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
class BeneficiaryType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
class Opponent(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=10)
    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Case(models.Model):
    case_type = models.ForeignKey(CaseType, on_delete=models.SET_NULL, null=True, blank=True)
    main_charge = models.CharField(max_length=100)
    suit_no = models.CharField(max_length=20, null=True, blank=True)
    court_room = models.ForeignKey(CourtRoom, on_delete=models.SET_NULL, null=True, blank=True)
    case_pending_duration = models.CharField(max_length=20, null=True, blank=True)
    beneficiary_type = models.ForeignKey(BeneficiaryType, on_delete=models.SET_NULL, null=True, blank=True)
    number_of_times = models.IntegerField(null=True, blank=True)
    previous_case_number = models.CharField(max_length=20, null=True, blank=True)
    case_relation = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, blank=True)
    # changed opponent to onetoone
    opponent = models.OneToOneField(Opponent, on_delete=models.SET_NULL, null=True, blank=True) 
    case_summary = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        default="pending",        # ← here’s your default
        choices=[
            ("pending", "Pending"),
            ("action taken", "Action Taken"),
            ("closed", "Closed"),
        ]                         # ← optional but recommended
    )
    # declaration = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Applicant(models.Model):
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    dob = models.DateField()
    age = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=100)
    period_of_stay = models.CharField(max_length=20)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, blank=True)
    id_type = models.ForeignKey(IdType, on_delete=models.SET_NULL, null=True, blank=True)
    id_number = models.CharField(max_length=50)
    contact = models.CharField(max_length=10)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    children = models.IntegerField(null=True, blank=True)
    employment_status = models.ForeignKey(EmploymentStatus, on_delete=models.SET_NULL, null=True, blank=True)
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.SET_NULL, null=True, blank=True)
    case = models.OneToOneField(Case, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Spouse(models.Model):
    applicant = models.OneToOneField(Applicant, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=10, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Work(models.Model):
    applicant = models.OneToOneField(Applicant, on_delete=models.SET_NULL, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)
    qualification = models.CharField(max_length=50, null=True, blank=True)
    working_period = models.CharField(max_length=20, null=True, blank=True)
    employer = models.CharField(max_length=50, null=True, blank=True)
    employer_type = models.ForeignKey(EmployerType, on_delete=models.SET_NULL, null=True, blank=True)
    employer_address = models.CharField(max_length=100, null=True, blank=True)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    asset = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class Representative(models.Model):
    applicant = models.OneToOneField(Applicant, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    reason = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    

class Mediator(models.Model):
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)

    
class Action(models.Model):
    case = models.OneToOneField(Case, on_delete=models.SET_NULL, null=True, blank=True)
    action_taken = models.CharField(max_length=100)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    mediator = models.ForeignKey(Mediator, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    
# from django.core.cache import cache
# cache.clear()

