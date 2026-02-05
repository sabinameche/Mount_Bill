from rest_framework import serializers
from django.contrib.auth.models import Permission,Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id","name"]

class PermissionSerializer(serializers.ModelSerializer):
    checked = serializers.SerializerMethodField()
    class Meta:
        model = Permission
        fields = ["id","codename","name","checked"]
        read_only_fields = ["codename","name"]

        
    def get_checked(self,obj):
        assigned_ids = self.context.get('assigned_ids',[])
        return obj.id in assigned_ids
