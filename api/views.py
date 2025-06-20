from venv import logger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Gender, Nationality, Action, Mediator, Applicant, Title, CourtRoom, EmploymentStatus, BeneficiaryType, CourtType, EmployerType, Job, Language, MaritalStatus, Party, Representative, CaseType, IdType, Case
from .serializers import GenderSerializer, ActionSerializer, ApplicationSerializer, MediatorSerializer, IdTypeSerializer, MyTokenObtainPairSerializer, TitleSerializer, NationalitySerializer, EmploymentStatusSerializer, MaritalStatusSerializer, BeneficiaryTypeSerializer, PartySerializer, LanguageSerializer, CourtRoomSerializer, CourtTypeSerializer, EmployerTypeSerializer, JobSerializer, RepresentativeSerializer, CaseTypeSerializer, CaseSerializer
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
import time
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models.functions import Cast
from django.db.models import CharField
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from django.db.models.functions import ExtractYear, ExtractMonth

# from django.core.cache import cache
# cache.clear()
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# applicant
@receiver(post_save, sender=Applicant)
@receiver(post_delete, sender=Applicant)
def clear_applicant_cache(sender, **kwargs):
    cache.delete('all_applicants')


# Create applicant (POST)
@api_view(['POST'])
# def create_applicantion(request):
#     serializer = ApplicantSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         cache.delete('all_applicants')  # Clear cache to refresh GET view
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def create_application(request):  # Fixed typo in function name
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
        try:
            applicant = serializer.save()
            cache.delete('all_applicants')  # Clear cache
            
            # Return success with created applicant data
            response_serializer = ApplicationSerializer(applicant)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to create application: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get all applicants (GET) with Redis cache
@api_view(['GET'])
# def get_applications(request):
#     try:
#         cached_applications = cache.get('all_applicants')
#         if cached_applications is not None:
#             print("Returned applicants from Redis cache")
#             return Response(cached_applications)

#         applications = Applicant.objects.select_related(
#             'title', 'gender', 'nationality', 'id_type', 'language',
#             'employment_status', 'marital_status',
#             'case', 'case__case_type', 'case__court_room',
#             'case__court_room__court_type', 'case__beneficiary_type',
#             'case__case_relation', 'case__opponent',
#             'case__opponent__gender', 'case__opponent__party'
#         ).prefetch_related(
#             'spouse', 'spouse__gender', 'spouse__job',
#             'work', 'work__job', 'work__employer_type',
#             'representative', 'representative__gender'
#         ).order_by('-case__created_at')
#         # ('-id')

#         serialized_data = ApplicationSerializer(applications, many=True).data
#         cache.set('all_applicants', serialized_data, timeout=None)
#         print("Fetched applicants from DB and cached in Redis")
#         return Response(serialized_data)

#     except Exception as e:
#         import traceback
#         print("Error fetching applications:", str(e))
#         traceback.print_exc()
#         return Response({'error': str(e)}, status=500)
    
def get_applications(request):
    try:
        # Extract filter params
        search_id = request.GET.get('id')
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        gender = request.GET.get('gender')
        marital_status = request.GET.get('marital_status')
        employment_status = request.GET.get('employment_status')

        # Apply filters only if any search/filter param exists
        if any([search_id, first_name, last_name, gender, marital_status, employment_status]):
            applications = Applicant.objects.select_related(
                'title', 'gender', 'nationality', 'id_type', 'language',
                'employment_status', 'marital_status',
                'case', 'case__case_type', 'case__court_room',
                'case__court_room__court_type', 'case__beneficiary_type',
                'case__case_relation', 'case__opponent',
                'case__opponent__gender', 'case__opponent__party'
            ).prefetch_related(
                'spouse', 'spouse__gender', 'spouse__job',
                'work', 'work__job', 'work__employer_type',
                'representative', 'representative__gender'
            ).order_by('-case__created_at')

            if search_id:
                applications = applications.filter(id=search_id)

            # if first_name:
            #     applications = applications.filter(first_name__icontains=first_name)
            
            if first_name and last_name:
                applications = applications.filter(
                Q(first_name__icontains=first_name) |
               Q(last_name__icontains=last_name)
            )

            # if last_name:
            #     applications = applications.filter(last_name__icontains=last_name)

            if gender:
                applications = applications.filter(gender__id=gender)

            if marital_status:
                applications = applications.filter(marital_status__id=marital_status)

            if employment_status:
                applications = applications.filter(employment_status__id=employment_status)

            serialized_data = ApplicationSerializer(applications, many=True).data
            print("Returned filtered applicants from DB")
            return Response(serialized_data)

        # No filters: serve from cache if available
        cached_applications = cache.get('all_applicants')
        if cached_applications is not None:
            print("Returned applicants from Redis cache")
            return Response(cached_applications)

        applications = Applicant.objects.select_related(
            'title', 'gender', 'nationality', 'id_type', 'language',
            'employment_status', 'marital_status',
            'case', 'case__case_type', 'case__court_room',
            'case__court_room__court_type', 'case__beneficiary_type',
            'case__case_relation', 'case__opponent',
            'case__opponent__gender', 'case__opponent__party'
        ).prefetch_related(
            'spouse', 'spouse__gender', 'spouse__job',
            'work', 'work__job', 'work__employer_type',
            'representative', 'representative__gender'
        ).order_by('-case__created_at')

        serialized_data = ApplicationSerializer(applications, many=True).data
        cache.set('all_applicants', serialized_data, timeout=None)
        print("Fetched applicants from DB and cached in Redis")
        return Response(serialized_data)

    except Exception as e:
        import traceback
        print("Error fetching applications:", str(e))
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
def app_count(request):
    count = Applicant.objects.count()
    return Response({'count': count})

# @api_view(['GET'])
# def get_applications(request):
#     cached_applications = cache.get('all_applicants')
    
#     if cached_applications is not None:
#         print("Returned applicants from Redis cache")
#         return Response(cached_applications)
    
#     # COMPLETE OPTIMIZED QUERY - All relationships included
#     applications = Applicant.objects.select_related(
#         # ===== APPLICANT'S DIRECT FOREIGN KEYS =====
#         'title',                    # applicant.title_id → title.id
#         'gender',                   # applicant.gender_id → gender.id  
#         'nationality',              # applicant.nationality_id → nationality.id
#         'id_type',                  # applicant.id_type_id → id_type.id
#         'language',                 # applicant.language_id → language.id
#         'employment_status',        # applicant.employment_status_id → employment_status.id
#         'marital_status',           # applicant.marital_status_id → marital_status.id
        
#         # ===== CASE RELATIONSHIPS (through applicant.case) =====
#         'case',                     # applicant.case_id → case.id
#         'case__case_type',          # case.case_type_id → case_type.id
#         'case__court_room',         # case.court_room_id → court_room.id
#         'case__court_room__type',   # court_room.type_id → court_type.id (MISSING!)
#         'case__beneficiary_type',   # case.beneficiary_type_id → beneficiary_type.id
#         'case__case_relation',      # case.case_relation_id → party.id
        
#         # ===== OPPONENT RELATIONSHIPS (through case.opponent) =====
#         'case__opponent',           # case.opponent_id → opponent.id
#         'case__opponent__gender',   # opponent.gender_id → gender.id
#         'case__opponent__party'     # opponent.party_id → party.id
        
#     ).prefetch_related(
#         # ===== SPOUSE RELATIONSHIPS =====
#         'spouse',                   # Get spouse record (OneToOne)
#         'spouse__gender',           # spouse.gender_id → gender.id
#         'spouse__job',              # spouse.job_id → job.id
        
#         # ===== WORK RELATIONSHIPS =====
#         'work',                     # Get work record (OneToOne)
#         'work__job',                # work.job_id → job.id
#         'work__employer_type',      # work.employer_type_id → employer_type.id
        
#         # ===== REPRESENTATIVE RELATIONSHIPS =====
#         'representative',           # Get representative record (OneToOne)
#         'representative__gender'    # representative.gender_id → gender.id
        
#     # ).order_by('-id')  # Order by ID since created_at doesn't exist on Applicant
#     ).order_by('-id')  # Order by ID since created_at doesn't exist on Applicant

#     serialized_data = ApplicationSerializer(applications, many=True).data
#     cache.set('all_applicants', serialized_data, timeout=None)
#     print("Fetched applicants from DB and cached in Redis")
    
#     return Response(serialized_data)
# def get_applications(request):
#     cached_applications = cache.get('all_applicants')

#     if cached_applications is not None:
#         print("Returned applicants from Redis cache")
#         return Response(cached_applications)

#     applicantions = Applicant.objects.all()
#     serialized_data = ApplicationSerializer(applicantions, many=True).data
#     cache.set('all_applicants', serialized_data, timeout=None)
#     print("Fetched applicants from DB and cached in Redis")
#     return Response(serialized_data)


# Gender
@receiver(post_save, sender=Gender)
@receiver(post_delete, sender=Gender)
def clear_gender_cache(sender, **kwargs):
    cache.delete('all_genders')

@api_view(['POST'])
def create_gender(request):
    serializer = GenderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_genders')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_genders(request):
    cached_genders = cache.get('all_genders')

    if cached_genders is not None:
        print("Returned genders from Redis cache")
        return Response(cached_genders)

    genders = Gender.objects.all()
    serialized_data = GenderSerializer(genders, many=True).data
    cache.set('all_genders', serialized_data, timeout=None)
    print("Fetched genders from DB and cached in Redis")

    return Response(serialized_data)

# Case
# no filter

# @api_view(['GET'])
# def get_cases(request):
#     try:
#         cached_cases = cache.get('all_cases')
#         if cached_cases is not None:
#             print("Returned cases from Redis cache")
#             return Response(cached_cases)

#         cases = Case.objects.select_related(
#             'case_type', 'court_room', 'beneficiary_type', 'case_relation', 'opponent',
#             'opponent__gender', 'opponent__party'
#         ).order_by('-created_at')
#         # ('-id')

#         serialized_data = CaseSerializer(cases, many=True).data
#         cache.set('all_cases', serialized_data, timeout=None)
#         print("Fetched cases from DB and cached in Redis")
#         return Response(serialized_data)

#     except Exception as e:
#         import traceback
#         print("Error fetching cases:", str(e))
#         traceback.print_exc()
#         return Response({'error': str(e)}, status=500)

# filter with cache
# @api_view(['GET'])
# def get_cases(request):
#     try:
#         status = request.GET.get('status')

#         # Build a dynamic cache key
#         cache_key = f"cases_{status}" if status else "all_cases"

#         cached_cases = cache.get(cache_key)
#         if cached_cases is not None:
#             print(f"Returned cases from Redis cache (key={cache_key})")
#             return Response(cached_cases)

#         # Build base queryset
#         cases = Case.objects.select_related(
#             'case_type', 'court_room', 'beneficiary_type', 'case_relation', 'opponent',
#             'opponent__gender', 'opponent__party'
#         ).order_by('-created_at')

#         # Apply filter if status is provided
#         if status:
#             cases = cases.filter(status=status)

#         serialized_data = CaseSerializer(cases, many=True).data
#         cache.set(cache_key, serialized_data, timeout=None)
#         print(f"Fetched cases from DB and cached (key={cache_key})")

#         return Response(serialized_data)

#     except Exception as e:
#         import traceback
#         print("Error fetching cases:", str(e))
#         traceback.print_exc()
#         return Response({'error': str(e)}, status=500)

# filter
# @api_view(['GET'])
# def get_cases(request):
#     try:
#         status = request.GET.get('status')

#         # Use cache only if no filters are applied
#         if not status:
#             cached_cases = cache.get('all_cases')
#             if cached_cases is not None:
#                 print("Returned cases from Redis cache")
#                 return Response(cached_cases)

#         # Build base queryset
#         cases = Case.objects.select_related(
#             'case_type', 'court_room', 'beneficiary_type', 'case_relation', 'opponent',
#             'opponent__gender', 'opponent__party'
#         ).order_by('-created_at')

#         # Apply filter if status is provided
#         if status:
#             cases = cases.filter(status=status)

#         serialized_data = CaseSerializer(cases, many=True).data

#         # Cache only unfiltered results
#         if not status:
#             cache.set('all_cases', serialized_data, timeout=None)
#             print("Fetched unfiltered cases from DB and cached in Redis")
#         else:
#             print(f"Fetched filtered cases from DB (status={status})")

#         return Response(serialized_data)

#     except Exception as e:
#         import traceback
#         print("Error fetching cases:", str(e))
#         traceback.print_exc()
#         return Response({'error': str(e)}, status=500)
@receiver(post_save, sender=Case)
@receiver(post_delete, sender=Case)
def clear_case_cache(sender, **kwargs):
    cache.delete('all_cases')
    logger.info("Cleared 'all_cases' cache due to Case save/delete")
# filter & search & pagination
@api_view(['GET'])
# def get_cases(request):
#     try:
#         status = request.GET.get('status')
#         search = request.GET.get('search')

#         # Use cache only if no filters/search are applied
#         if not status and not search:
#             cached_cases = cache.get('all_cases')
#             if cached_cases is not None:
#                 print("Returned cases from Redis cache")
#                 return Response(cached_cases)

#         # Build base queryset
#         cases = Case.objects.select_related(
#             'case_type', 'court_room', 'beneficiary_type', 'case_relation', 'opponent',
#             'opponent__gender', 'opponent__party'
#         ).order_by('id')

#         # Filter by status
#         if status:
#             # cases = cases.filter(status=status)
#             cases = cases.filter(status__iexact=status)

#         # Restrict search fields
#         if search:
#             cases = cases.annotate(
#                 id_str=Cast('id', CharField()),
#                 created_at_str=Cast('created_at', CharField())
#             ).filter(
#                 # Q(id__iexact=search) |
#                 Q(id__icontains=search) |
#                 Q(case_type__name__icontains=search) |
#                 Q(case_relation__name__icontains=search) |
#                 Q(created_at_str__icontains=search)
#             )

#         # Pagination
#         paginator = PageNumberPagination()
#         paginator.page_size = int(request.GET.get('page_size', 10))
#         result_page = paginator.paginate_queryset(cases, request)
#         serialized_data = CaseSerializer(result_page, many=True)

#         # Only cache unfiltered results
#         if not status and not search:
#             cache.set('all_cases', serialized_data.data, timeout=None)
#             logger.info("Fetched unfiltered cases from DB and cached in Redis")
#         else:
#             logger.info(f"Fetched filtered/search cases from DB (status={status}, search={search})")

#         return paginator.get_paginated_response(serialized_data.data)

#     except Exception as e:
#          logger.error("Error fetching cases", exc_info=True)
#          return Response({'error': str(e)}, status=500)
    
def get_cases(request):
    try:
        status = request.GET.get('status')
        search = request.GET.get('search')

        # Use cache only if no filters/search are applied
        if not status and not search:
            cached_cases = cache.get('all_cases')
            if cached_cases is not None:
                print("Returned cases from Redis cache")
                return Response(cached_cases)

        # Build base queryset
        cases = Case.objects.select_related(
            'case_type', 'court_room', 'beneficiary_type', 'case_relation', 'opponent',
            'opponent__gender', 'opponent__party'
        ).order_by('-created_at')

        # Filter by status
        if status:
            cases = cases.filter(status=status)

        # Restrict search fields
        
        if search:
           cases = cases.annotate(
        created_at_str=Cast('created_at', CharField())
    ).filter(
        Q(id__iexact=search) |
        Q(case_type__name__icontains=search) |
        Q(case_relation__name__icontains=search) |
        Q(created_at_str__icontains=search)
    )

        serialized_data = CaseSerializer(cases, many=True).data

        # Cache only if no filter/search applied
        if not status and not search:
            cache.set('all_cases', serialized_data, timeout=None)
            logger.info("Fetched unfiltered cases from DB and cached in Redis")
        else:
            logger.info(f"Fetched filtered/search cases from DB (status={status}, search={search})")

        return Response(serialized_data)

    except Exception as e:
         logger.error("Error fetching cases", exc_info=True)
         return Response({'error': str(e)}, status=500)

@api_view(['PUT', 'PATCH'])
def update_case(request, pk):
    try:
        case = Case.objects.get(pk=pk)
    except Case.DoesNotExist:
        return Response({'error': 'Case not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CaseSerializer(case, data=request.data, partial=True)  # `partial=True` allows partial updates
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_cases')  # Invalidate cache
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def case_count(request):
    count = Case.objects.count()
    return Response({'count': count})

# Action
@receiver(post_save, sender=Action)
@receiver(post_delete, sender=Action)
def clear_action_cache(sender, **kwargs):
    cache.delete('all_actions')

@api_view(['POST'])
def create_action(request):
    serializer = ActionSerializer(data=request.data)
    if serializer.is_valid():
        try:
            action = serializer.save()
            cache.delete('all_actions')  # Clear cache
            
            # Return success with created action data
            response_serializer = ActionSerializer(action)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to create action: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Q


@api_view(['GET'])
def get_actions(request):
    try:
        search_id = request.GET.get('id')
        completed_by = request.GET.get('completed_by')
        mediator = request.GET.get('mediator')
        appointment_date = request.GET.get('appointment_date')
        generic = request.GET.get('generic')  # smart fallback

        actions = Action.objects.select_related(
            'case', 'completed_by', 'mediator'
        ).order_by('-created_at')

        if search_id:
            actions = actions.filter(id=search_id)

        if completed_by:
            actions = actions.filter(
                Q(completed_by__first_name__icontains=completed_by) |
                Q(completed_by__last_name__icontains=completed_by)
            )

        if mediator:
            actions = actions.filter(
                Q(mediator__first_name__icontains=mediator) |
                Q(mediator__last_name__icontains=mediator)
            )

        if appointment_date:
            parts = appointment_date.split("-")
            
            actions = actions.annotate(
                appointment_year=ExtractYear('appointment_date'),
                appointment_month=ExtractMonth('appointment_date'),
            )

            if len(parts) == 1:
                actions = actions.filter(appointment_year=int(parts[0]))

            elif len(parts) == 2:
                actions = actions.filter(
                        appointment_year=int(parts[0]),
                        appointment_month=int(parts[1])
                    )

            elif len(parts) == 3:
                actions = actions.filter(appointment_date=appointment_date)

        if generic:
            actions = actions.filter(
                Q(completed_by__first_name__icontains=generic) |
                Q(completed_by__last_name__icontains=generic) |
                Q(mediator__first_name__icontains=generic) |
                Q(mediator__last_name__icontains=generic)
            )

        if not any([search_id, completed_by, mediator, appointment_date, generic]):
            cached_actions = cache.get('all_actions')
            if cached_actions is not None:
                logger.info("Returned actions from Redis cache")
                return Response(cached_actions)

            serialized_data = ActionSerializer(actions, many=True).data
            cache.set('all_actions', serialized_data, timeout=None)
            logger.info("Fetched actions from DB and cached in Redis")
            return Response(serialized_data)

        serialized_data = ActionSerializer(actions, many=True).data
        logger.info("Returned filtered actions from DB")
        return Response(serialized_data)

    except Exception as e:
        logger.exception("Error fetching actions")
        return Response({'error': str(e)}, status=500)


# @api_view(['GET'])
# def get_actions(request):
#     try:
#         cached_actions = cache.get('all_actions')
#         if cached_actions is not None:
#             print("Returned actions from Redis cache")
#             return Response(cached_actions)

#         actions = Action.objects.select_related(
#                         'case', 'completed_by', 'mediator'
#         ).order_by('-created_at')
#         # ('-id')

#         serialized_data = ActionSerializer(actions, many=True).data
#         cache.set('all_actions', serialized_data, timeout=None)
#         print("Fetched actions from DB and cached in Redis")
#         return Response(serialized_data)

#     except Exception as e:
#         import traceback
#         print("Error fetching cases:", str(e))
#         traceback.print_exc()
#         return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def action_count(request):
    count = Action.objects.count()
    return Response({'count': count})

# Job
@receiver(post_save, sender=Job)
@receiver(post_delete, sender=Job)
def clear_job_cache(sender, **kwargs):
    cache.delete('all_jobs')

@api_view(['POST'])
def create_job(request):
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_jobs')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_jobs(request):
    cached_jobs = cache.get('all_jobs')

    if cached_jobs is not None:
        print("Returned jobs from Redis cache")
        return Response(cached_jobs)

    jobs = Job.objects.all()
    serialized_data = JobSerializer(jobs, many=True).data
    cache.set('all_jobs', serialized_data, timeout=None)
    print("Fetched jobs from DB and cached in Redis")

    return Response(serialized_data)



# Idtype
@receiver(post_save, sender=IdType)
@receiver(post_delete, sender=IdType)
def clear_job_cache(sender, **kwargs):
    cache.delete('all_idtypes')

@api_view(['POST'])
def create_idtype(request):
    serializer = IdTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_idtypes')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_idtypes(request):
    cached_idtypes = cache.get('all_idtypes')

    if cached_idtypes is not None:
        print("Returned idtypes from Redis cache")
        return Response(cached_idtypes)

    idtypes = IdType.objects.all()
    serialized_data = IdTypeSerializer(idtypes, many=True).data
    cache.set('all_idtypes', serialized_data, timeout=None)
    print("Fetched idtypes from DB and cached in Redis")

    return Response(serialized_data)


# MaritalStatus
@receiver(post_save, sender=MaritalStatus)
@receiver(post_delete, sender=MaritalStatus)
def clear_maritalstatus_cache(sender, **kwargs):
    cache.delete('all_maritalstatus')

@api_view(['POST'])
def create_maritalstatus(request):
    serializer = MaritalStatusSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_maritalstatus')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_maritalstatus(request):
    cached_maritalstatus = cache.get('all_maritalstatus')

    if cached_maritalstatus is not None:
        print("Returned maritalstatus from Redis cache")
        return Response(cached_maritalstatus)

    maritalstatus = MaritalStatus.objects.all()
    serialized_data = MaritalStatusSerializer(maritalstatus, many=True).data
    cache.set('all_maritalstatus', serialized_data, timeout=None)
    print("Fetched maritalstatus from DB and cached in Redis")

    return Response(serialized_data)


# Nationality
@receiver(post_save, sender=Nationality)
@receiver(post_delete, sender=Nationality)
def clear_nationality_cache(sender, **kwargs):
    cache.delete('all_nationalities')

@api_view(['POST'])
def create_nationality(request):
    serializer = NationalitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_nationalities')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_nationalities(request):
    cached_nationalities = cache.get('all_nationalities')

    if cached_nationalities is not None:
        print("🔁 Returned items from Redis cache")
        return Response(cached_nationalities)

    nationalities = Nationality.objects.all()
    serialized_data = NationalitySerializer(nationalities, many=True).data
    cache.set('all_nationalities', serialized_data, timeout=None)
    print("🆕 Fetched nationalities from DB and cached in Redis")

    return Response(serialized_data)


# CourtRoom
@receiver(post_save, sender=CourtRoom)
@receiver(post_delete, sender=CourtRoom)
def clear_courtroom_cache(sender, **kwargs):
    cache.delete('all_courtrooms')

@api_view(['POST'])
def create_courtroom(request):
    serializer = CourtRoom(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_courtrooms')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_courtrooms(request):
    cached_courtrooms = cache.get('all_courtrooms')

    if cached_courtrooms is not None:
        print("🔁 Returned courtrooms from Redis cache")
        return Response(cached_courtrooms)

    courtrooms = CourtRoom.objects.all()
    serialized_data = CourtRoomSerializer(courtrooms, many=True).data
    cache.set('all_courtrooms', serialized_data, timeout=None)
    print("🆕 Fetched courtrooms from DB and cached in Redis")

    return Response(serialized_data)

@api_view(['GET'])
def get_courtrooms_by_courttype(request, courttype_id):
    cache_key = f'courtrooms_courttype_{courttype_id}'
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        print("🔁 Returned courtrooms from Redis cache")
        return Response(cached_data)

    start = time.time()
    courtrooms = CourtRoom.objects.filter(court_type_id=courttype_id)
    serialized_data = CourtRoomSerializer(courtrooms, many=True).data
    end = time.time()

    cache.set(cache_key, serialized_data, timeout=None)
    print("🆕 Fetched courtrooms from DB and cached in Redis")
    print(f"⏱️ Time to get courtrooms: {end - start:.3f} seconds")

    return Response(serialized_data)


# def get_courtrooms_by_type(request, type_id):
#     courtrooms = CourtRoom.objects.filter(court_type_id=type_id)
#     serialized_data = CourtRoomSerializer(courtrooms, many=True).data
#     return Response(serialized_data)

# CourtType
@receiver(post_save, sender=CourtType)
@receiver(post_delete, sender=CourtType)
def clear_courttype_cache(sender, **kwargs):
    cache.delete('all_courttype')

@api_view(['POST'])
def create_courttype(request):
    serializer = CourtTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_courttype')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_courttypes(request):
    cached_courttypes = cache.get('all_courttype')

    if cached_courttypes is not None:
        print("🔁 Returned courttype from Redis cache")
        return Response(cached_courttypes)

    courttypes = CourtType.objects.all()
    serialized_data = CourtTypeSerializer(courttypes, many=True).data
    cache.set('all_courttype', serialized_data, timeout=None)
    print("🆕 Fetched courttype from DB and cached in Redis")

    return Response(serialized_data)


# Language
@receiver(post_save, sender=Language)
@receiver(post_delete, sender=Language)
def clear_languages_cache(sender, **kwargs):
    cache.delete('all_languages')
    
@api_view(['POST'])
def create_language(request):
    serializer = LanguageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_languages')  # Invalidate cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_languages(request):
    cached_languages = cache.get('all_languages')

    if cached_languages is not None:
        print("🔁 Returned languages from Redis cache")
        return Response(cached_languages)

    languages = Language.objects.all()
    serialized_data = LanguageSerializer(languages, many=True).data
    cache.set('all_languages', serialized_data, timeout=None)
    print("🆕 Fetched languages from DB and cached in Redis")

    return Response(serialized_data)

# Party
@receiver(post_save, sender=Party)
@receiver(post_delete, sender=Party)
def clear_parties_cache(sender, **kwargs):
    cache.delete('all_parties')

@api_view(['POST'])
def create_party(request):
    serializer = PartySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_parties')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_parties(request):
    cached_parties = cache.get('all_parties')

    if cached_parties is not None:
        print("Returned parties from Redis cache")
        return Response(cached_parties)

    parties = Party.objects.all()
    serialized_data = PartySerializer(parties, many=True).data
    cache.set('all_parties', serialized_data, timeout=None)
    print("Fetched parties from DB and cached in Redis")

    return Response(serialized_data)

# EmploymentStatus
@receiver(post_save, sender=EmploymentStatus)
@receiver(post_delete, sender=EmploymentStatus)
def clear_employmentstatus_cache(sender, **kwargs):
    cache.delete('all_employmentstatus')

@api_view(['POST'])
def create_employmentstatus(request):
    serializer = EmploymentStatusSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_employmentstatus')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_employmentstatus(request):
    cached_employmentstatus = cache.get('all_employmentstatus')

    if cached_employmentstatus is not None:
        print("Returned employmentstatus from Redis cache")
        return Response(cached_employmentstatus)

    employmentstatus = EmploymentStatus.objects.all()
    serialized_data = EmploymentStatusSerializer(employmentstatus, many=True).data
    cache.set('all_employmentstatus', serialized_data, timeout=None)
    print("Fetched employmentstatus from DB and cached in Redis")

    return Response(serialized_data)


# EmployerType
@receiver(post_save, sender=EmployerType)
@receiver(post_delete, sender=EmployerType)
def clear_employertype_cache(sender, **kwargs):
    cache.delete('all_employertypes')

@api_view(['POST'])
def create_employmertype(request):
    serializer = EmployerType(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_employertypes')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_employmertypes(request):
    cached_employmertypes = cache.get('all_employertypes')

    if cached_employmertypes is not None:
        print("Returned employertypes from Redis cache")
        return Response(cached_employmertypes)

    employmertypes = EmployerType.objects.all()
    serialized_data = EmployerTypeSerializer(employmertypes, many=True).data
    cache.set('all_employertypes', serialized_data, timeout=None)
    print("Fetched employertypes from DB and cached in Redis")

    return Response(serialized_data)


# BeneficiaryType
@receiver(post_save, sender=BeneficiaryType)
@receiver(post_delete, sender=BeneficiaryType)
def clear_beneficiarytypes_cache(sender, **kwargs):
    cache.delete('all_beneficiarytypes')

@api_view(['POST'])
def create_beneficiarytype(request):
    serializer = BeneficiaryTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_beneficiarytypes')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_beneficiarytypes(request):
    cached_beneficiarytypes = cache.get('all_beneficiarytypes')

    if cached_beneficiarytypes is not None:
        print("Returned beneficiarytypes from Redis cache")
        return Response(cached_beneficiarytypes)

    beneficiarytypes = BeneficiaryType.objects.all()
    serialized_data = BeneficiaryTypeSerializer(beneficiarytypes, many=True).data
    cache.set('all_beneficiarytypes', serialized_data, timeout=None)
    print("Fetched beneficiarytypes from DB and cached in Redis")

    return Response(serialized_data)

# Representative
@receiver(post_save, sender=Representative)
@receiver(post_delete, sender=Representative)
def clear_representative_cache(sender, **kwargs):
    cache.delete('all_representatives')

@api_view(['POST'])
def create_representative(request):
    serializer = RepresentativeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_representatives')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_representatives(request):
    cached_representatives = cache.get('all_representatives')

    if cached_representatives is not None:
        print("Returned representatives from Redis cache")
        return Response(cached_representatives)

    representatives = Representative.objects.all()
    serialized_data = RepresentativeSerializer(representatives, many=True).data
    cache.set('all_representatives', serialized_data, timeout=None)
    print("Fetched representatives from DB and cached in Redis")

    return Response(serialized_data)

# CaseType
@receiver(post_save, sender=CaseType)
@receiver(post_delete, sender=CaseType)
def clear_casetype_cache(sender, **kwargs):
    cache.delete('all_casetypes')

@api_view(['POST'])
def create_casetype(request):
    serializer = CaseTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_casetypes')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_casetypes(request):
    cached_casetypes = cache.get('all_casetypes')

    if cached_casetypes is not None:
        print("Returned casetypes from Redis cache")
        return Response(cached_casetypes)

    casetypes = CaseType.objects.all()
    serialized_data = CaseTypeSerializer(casetypes, many=True).data
    cache.set('all_casetypes', serialized_data, timeout=None)
    print("Fetched casetypes from DB and cached in Redis")

    return Response(serialized_data)

# Title
@receiver(post_save, sender=Title)
@receiver(post_delete, sender=Title)
def clear_title_cache(sender, **kwargs):
    cache.delete('all_titles')

@api_view(['POST'])
def create_title(request):
    serializer = TitleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_titles')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_titles(request):
    cached_titles = cache.get('all_titles')

    if cached_titles is not None:
        print("Returned titles from Redis cache")
        return Response(cached_titles)

    titles = Title.objects.all()
    serialized_data = TitleSerializer(titles, many=True).data
    cache.set('all_titles', serialized_data, timeout=None)
    print("Fetched titles from DB and cached in Redis")

    return Response(serialized_data)

# Mediator
@receiver(post_save, sender=Mediator)
@receiver(post_delete, sender=Mediator)
def clear_mediator_cache(sender, **kwargs):
    cache.delete('all_mediators')

@api_view(['POST'])
def create_mediator(request):
    serializer = MediatorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        cache.delete('all_mediators')  # Invalidate the cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_mediators(request):
    cached_mediators = cache.get('all_mediators')

    if cached_mediators is not None:
        print("Returned mediators from Redis cache")
        return Response(cached_mediators)

    mediators = Mediator.objects.all()
    serialized_data = MediatorSerializer(mediators, many=True).data
    cache.set('all_mediators', serialized_data, timeout=None)
    print("Fetched mediators from DB and cached in Redis")

    return Response(serialized_data)