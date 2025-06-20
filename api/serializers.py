from .models import Gender, Work, Mediator, Action, Spouse, Opponent, Representative, Case, Applicant, Title, Nationality, EmploymentStatus, MaritalStatus, BeneficiaryType, CourtRoom, CourtType, EmployerType, Job, Language, Party, Representative, CaseType, IdType
from rest_framework import serializers
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom user data to the response
        data['user'] = {
            'username': self.user.username,
            'id': self.user.id,
            'email': self.user.email,
        }

        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']
    
class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'
        
class MediatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mediator
        fields = '__all__'

class IdTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdType
        fields = '__all__'

class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'
        
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class CourtTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtType
        fields = '__all__'

class CourtRoomSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.name', read_only=True)

    class Meta:
        model = CourtRoom
        fields = '__all__'

class EmployerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerType
        fields = '__all__'

class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = '__all__'

class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaritalStatus
        fields = '__all__'

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
        
class CaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseType
        fields = '__all__'
        
class BeneficiaryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeneficiaryType
        fields = '__all__'
        
class EmploymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentStatus
        fields = '__all__'
        
class RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representative
        fields = '__all__'
        
class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'
        
class ActionSerializer(serializers.ModelSerializer):
    
    completed_by_id = serializers.PrimaryKeyRelatedField(
        source='completed_by', queryset=User.objects.all(),
        write_only=True, required=False, allow_null=True
    )
    mediator_id = serializers.PrimaryKeyRelatedField(
        source='mediator', queryset=Mediator.objects.all(),
        write_only=True, required=False, allow_null=True
    )
    
    completed_by = UserSerializer(read_only=True)
    mediator = MediatorSerializer(read_only=True)
    class Meta:
        model = Action
        fields = '__all__'

class SpouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spouse
        fields = '__all__'

class OpponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opponent
        fields = '__all__'

class CaseSerializer(serializers.ModelSerializer):
    # WRITE: Accept IDs
    case_type_id = serializers.PrimaryKeyRelatedField(
        source='case_type', queryset=CaseType.objects.all(),
        write_only=True, required=False, allow_null=True
    )
    case_relation_id = serializers.PrimaryKeyRelatedField(
        source='case_relation', queryset=Party.objects.all(),
        write_only=True, required=False, allow_null=True
    )
    court_room_id = serializers.PrimaryKeyRelatedField(
        source='court_room', queryset=CourtRoom.objects.all(),
        write_only=True, required=False, allow_null=True
    )
    beneficiary_type_id = serializers.PrimaryKeyRelatedField(
        source='beneficiary_type', queryset=BeneficiaryType.objects.all(),
        write_only=True, required=False, allow_null=True
    )

    # READ: Return nested objects
    case_type = CaseTypeSerializer(read_only=True)
    case_relation = PartySerializer(read_only=True)
    court_room = CourtRoomSerializer(read_only=True)
    beneficiary_type = BeneficiaryTypeSerializer(read_only=True)
    
    opponent = OpponentSerializer(required=False, allow_null=True)

    class Meta:
        model = Case
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
 # WRITE: Accept ID
    gender_id = serializers.PrimaryKeyRelatedField(
        source='gender', queryset=Gender.objects.all(), write_only=True, required=False, allow_null=True
    )
    nationality_id = serializers.PrimaryKeyRelatedField(
        source='nationality', queryset=Nationality.objects.all(), write_only=True, required=False, allow_null=True
    )
    id_type_id = serializers.PrimaryKeyRelatedField(
        source='id_type', queryset=IdType.objects.all(), write_only=True, required=False, allow_null=True
    )
    language_id = serializers.PrimaryKeyRelatedField(
        source='language', queryset=Language.objects.all(), write_only=True, required=False, allow_null=True
    )
    employment_status_id = serializers.PrimaryKeyRelatedField(
        source='employment_status', queryset=EmploymentStatus.objects.all(), write_only=True, required=False, allow_null=True
    )
    marital_status_id = serializers.PrimaryKeyRelatedField(
        source='marital_status', queryset=MaritalStatus.objects.all(), write_only=True, required=False, allow_null=True
    )
    title_id = serializers.PrimaryKeyRelatedField(
        source='title', queryset=Title.objects.all(), write_only=True, required=False, allow_null=True
    )

    # READ: Return full object
    gender = GenderSerializer(read_only=True)
    nationality = NationalitySerializer(read_only=True)
    id_type = IdTypeSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    employment_status = EmploymentStatusSerializer(read_only=True)
    marital_status = MaritalStatusSerializer(read_only=True)
    title = TitleSerializer(read_only=True)

    case = CaseSerializer(required=False, allow_null=True)
    spouse = SpouseSerializer(required=False, allow_null=True)
    work = WorkSerializer(required=False, allow_null=True)
    representative = RepresentativeSerializer(required=False, allow_null=True)

    class Meta:
        model = Applicant
        fields = '__all__'
        read_only_fields = ['created_at']  # auto-handled by model

        
    def create(self, validated_data):
        try:
            with transaction.atomic():
                # Extract nested data
                case_data = validated_data.pop('case', None)
                spouse_data = validated_data.pop('spouse', None)
                work_data = validated_data.pop('work', None)
                rep_data = validated_data.pop('representative', None)

                # Handle case creation with opponent
                case = None
                if case_data:
                    opponent_data = case_data.pop('opponent', None)
                    opponent = None
                    
                    if opponent_data and any(v for v in opponent_data.values() if v not in [None, '']):
                        opponent = Opponent.objects.create(**opponent_data)
                        case_data['opponent'] = opponent

                    case = Case.objects.create(**case_data)
                    validated_data['case'] = case

                # Create main applicant
                applicant = Applicant.objects.create(**validated_data)

                # Create related records only if they contain meaningful data
                if spouse_data and any(v for v in spouse_data.values() if v not in [None, '']):
                    Spouse.objects.create(applicant=applicant, **spouse_data)

                if work_data and any(v for v in work_data.values() if v not in [None, '']):
                    Work.objects.create(applicant=applicant, **work_data)

                if rep_data and any(v for v in rep_data.values() if v not in [None, '']):
                    Representative.objects.create(applicant=applicant, **rep_data)

                return applicant
                
        except Exception as e:
            import traceback
            print(f"Applicant creation error: {e}")
            traceback.print_exc()
            raise serializers.ValidationError(f"Failed to create applicant: {str(e)}")
        
# from django.core.cache import cache
# cache.clear()

        
    # def create(self, validated_data):
    #     case_data = validated_data.pop('case', None)
    #     spouse_data = validated_data.pop('spouse', None)
    #     work_data = validated_data.pop('work', None)
    #     rep_data = validated_data.pop('representative', None)

    # # 🔹 Handle opponent inside case
    #     case = None
    #     if case_data:
    #         opponent_data = case_data.pop('opponent', None)
    #         opponent = None
    #         if opponent_data and any(v is not None for v in opponent_data.values()):
    #             opponent = Opponent.objects.create(**opponent_data)
    #             case_data['opponent'] = opponent

    #         case = Case.objects.create(**case_data)
    #         validated_data['case'] = case

    # # 🔹 Create the main applicant
    #     applicant = Applicant.objects.create(**validated_data)

    # # 🔹 Related sub-records (only create if they have meaningful data)
    #     if spouse_data and any(v is not None for v in spouse_data.values()):
    #         Spouse.objects.create(applicant=applicant, **spouse_data)

    #     if work_data and any(v is not None for v in work_data.values()):
    #         Work.objects.create(applicant=applicant, **work_data)

    #     if rep_data and any(v is not None for v in rep_data.values()):
    #         Representative.objects.create(applicant=applicant, **rep_data)

    #     return applicant
