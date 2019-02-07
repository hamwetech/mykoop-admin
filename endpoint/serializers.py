from rest_framework import serializers
from django.utils import timezone
from coop.models import *
from product.models import ProductVariation, Supplier
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
            
            member = CooperativeMember.objects.filter(phone_number=phone_number)
            if member.exists():
                raise serializers.ValidationError("The phone number.'%s' is arleady in use. Please provide another number" % phone_number)
        
        if other_phone_number:
            try:
                other_phone_number = internationalize_number(other_phone_number)
                data['other_phone_number'] = other_phone_number
            except ValueError:
                raise serializers.ValidationError("Please enter a valid phone number.'%s' is not valid" % other_phone_number)
        return data

class CooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperative
        fields = ['id', 'name']


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ['product', 'name', 'id']


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        exclude = ['create_date', 'update_date']


class CollectionListSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)
    product = ProductVariationSerializer(read_only=True)
    cooperative = CooperativeSerializer(read_only=True)
    class Meta:
        model = Collection
        fields = ['id', 'collection_date', 'is_member', 'name', 'phone_number', 'collection_reference', 'quantity', 'unit_price', 'total_price', 'cooperative', 'member', 'product', 'created_by']

        
class TrainingModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingModule
        fields = ['thematic_area', 'topic', 'descriprion']
        
        
class TrainingSessionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TrainingSession
        exclude = ['training_module','created_by', 'create_date', 'update_date']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ['create_date', 'update_date']
        
        
class ItemSerializer(serializers.ModelSerializer):
    supplier  = SupplierSerializer(read_only=True)
    
    class Meta:
        model = Item
        fields = ['name', 'supplier', 'price']
        

class MemberOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberOrder
        exclude = ['update_date']
        

class OrderItemSerializer(serializers.ModelSerializer):
    order = MemberOrderSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['order', 'item', 'quantity', 'price', 'create_date']
        

class OrderItemSerializer_(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['update_date']
