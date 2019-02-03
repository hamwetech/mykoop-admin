from rest_framework import serializers
from django.utils import timezone
from coop.models import *
from conf.utils import internationalize_number, log_debug, log_error
from activity.models import ThematicArea, TrainingSession, TrainingModule

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)


class CooperativeMemberBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = CooperativeMemberBusiness
        exclude = ['create_date', 'update_date']
        

class CooperativeMemberSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CooperativeMemberSupply
        exclude = ['create_date', 'update_date']
      

class CooperativeMemberProductDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CooperativeMemberProductDefinition
        exclude = ['create_date', 'update_date']
      

class CooperativeMemberProductQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CooperativeMemberProductQuantity
        exclude = ['create_date', 'update_date']
   
        
class MemberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CooperativeMember
        exclude = ['create_date', 'update_date']
        
    
    def validate(self, data):
        phone_number = data.get('phone_number')
        other_phone_number = data.get('other_phone_number')
        
        date_of_birth = data.get('date_of_birth')
        if date_of_birth:
            if date_of_birth > timezone.now().date():
                raise serializers.ValidationError("Error! Date of Birth cannot be in the Future")
        
        if phone_number:
            try:
                phone_number = internationalize_number(phone_number)
                data['phone_number'] = phone_number
            except ValueError:
                raise serializers.ValidationError("Please enter a valid phone number.'%s' is not valid" % phone_number)
        if other_phone_number:
            try:
                other_phone_number = internationalize_number(other_phone_number)
                data['other_phone_number'] = other_phone_number
            except ValueError:
                raise serializers.ValidationError("Please enter a valid phone number.'%s' is not valid" % other_phone_number)
        return data


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        exclude = ['create_date', 'update_date']
        
        
class TrainingModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingModule
        fields = ['thematic_area', 'topic', 'descriprion']
        
        
class TrainingSessionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TrainingSession
        exclude = ['training_module','created_by', 'create_date', 'update_date']