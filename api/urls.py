from django.urls import path
from .views import MyTokenObtainPairView, app_count, case_count, action_count, update_case, get_actions, create_action, get_mediators, create_mediator, get_genders, get_idtypes, get_cases, get_applications, create_application, create_idtype, create_title, get_titles, get_beneficiarytypes, get_nationalities, get_courtrooms, get_employmentstatus, get_courttypes, get_employmertypes, create_gender, get_courtrooms_by_courttype, create_nationality, get_jobs, create_employmentstatus, get_languages, get_parties, create_beneficiarytype, create_courtroom, get_maritalstatus, create_maritalstatus, create_courttype, create_employmertype, create_job, create_language, create_party, create_representative, get_representatives, create_casetype, get_casetypes
from rest_framework_simplejwt.views import TokenRefreshView
# TokenObtainPairView, 

urlpatterns = [
    path('genders/', get_genders, name='get_genders'),
    path('genders/create/', create_gender, name='create_gender'),
    path('jobs/', get_jobs, name='get_jobs'),
    path('jobs/create/', create_job, name='create_job'),
    path('employertypes/', get_employmertypes, name='get_employmertypes'),
    path('employertypes/create/', create_employmertype, name='create_employmertype'),
    path('courttypes/', get_courttypes, name='get_courttypes'),
    path('courttypes/create/', create_courttype, name='create_courttype'),
    path('beneficiarytypes/', get_beneficiarytypes, name='get_beneficiarytypes'),
    path('beneficiarytypes/create/', create_beneficiarytype, name='create_beneficiarytype'),
    path('employmentstatus/', get_employmentstatus, name='get_employmentstatus'),
    path('employmentstatus/create/', create_employmentstatus, name='create_employmentstatus'),
    path('nationalities/', get_nationalities, name='get_nationalities'),
    path('nationalities/create/', create_nationality, name='create_nationality'),
    path('courtrooms/', get_courtrooms, name='get_courtrooms'),
    path('courtrooms/create/', create_courtroom, name='create_courtroom'),
    path('courtrooms/courttype/<int:courttype_id>/', get_courtrooms_by_courttype, name='get_courtrooms_by_courttype'),
    path('maritalstatus/', get_maritalstatus, name='get_maritalstatus'),
    path('maritalstatus/create/', create_maritalstatus, name='create_maritalstatus'),
    path('languages/', get_languages, name='get_languages'),
    path('languages/create/', create_language, name='create_language'),
    path('parties/', get_parties, name='get_parties'),
    path('parties/create/', create_party, name='create_party'),
    path('representatives/', get_representatives, name='get_representatives'),
    path('representatives/create/', create_representative, name='create_representative'),
    path('casetypes/', get_casetypes, name='get_casetypes'),
    path('casetypes/create/', create_casetype, name='create_casetype'),
    path('titles/', get_titles, name='get_titles'),
    path('titles/create/', create_title, name='create_title'),
    path('idtypes/', get_idtypes, name='get_idtypes'),
    path('idtypes/create/', create_idtype, name='create_idtype'),
    path('applications/', get_applications, name='get_applications'),
    path('applications/create/', create_application, name='create_application'),
    path('cases/', get_cases, name='get_cases'),
    path('cases/<int:pk>/update/', update_case, name='update_case'),
    path('mediators/', get_mediators, name='get_mediators'),
    path('mediators/create/', create_mediator, name='create_mediator'),
    path('actions/', get_actions, name='get_actions'),
    path('actions/create/', create_action, name='create_action'),
    path('applications/count/', app_count, name='app_count'),
    path('cases/count/', case_count, name='case_count'),
    path('actions/count/', action_count, name='action_count'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # 👈 Refresh token
    path('signin/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

# from django.core.cache import cache
# cache.clear()
