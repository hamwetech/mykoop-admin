from rest_framework import routers, serializers, viewsets
from system.models import CooperativeMember


# Serializers define the API representation.
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CooperativeMember
        fields = ['first_name', 'surname', 'other_name', 'phone_number', 'id_number', 'date_of_birth']