from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from ..serializers_dir.permissionSerializers import PermissionSerializer,GroupSerializer
from django.contrib.auth.models import Permission,Group
from rest_framework.permissions import IsAuthenticated
from ..permission import IsCompanyOwner
from django.shortcuts import get_object_or_404


class RoleApiView(APIView):
    permission_classes = [IsAuthenticated,IsCompanyOwner]
    def get(self,request):
        roles = Group.objects.all()
        serializer = GroupSerializer(roles,many = True)
        return Response(serializer.data)

class PermissionApiview(APIView):
    permission_classes = [IsAuthenticated,IsCompanyOwner]

    def get(self,request,group_id):
        group = get_object_or_404(Group,id=group_id)

        assigned_permission_id = group.permissions.values_list('id',flat=True)
        all_permissions = Permission.objects.filter(content_type__model__in=["customer", "expense", "product", "productcategory"])


        serializer = PermissionSerializer(all_permissions,many = True,context={'assigned_ids': assigned_permission_id})
        return Response({
            "role":group.name,
            "permissions":serializer.data
        })
    
    def patch(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        permission_ids = request.data.get("permission_ids", [])

        perms = Permission.objects.filter(id__in=permission_ids)

        # permissions exactly
        group.permissions.set(perms)

        # Serialize all permissions with checked status
        all_perms = Permission.objects.filter(content_type__model__in=["customer", "expense", "product", "productcategory"])
        serializer = PermissionSerializer(
            all_perms,
            many=True,
            context={"assigned_ids": group.permissions.values_list("id", flat=True)}
        )

        return Response({
            "message": "Permissions updated successfully",
            "role": group.name,
            "permissions": serializer.data
        }, status=status.HTTP_200_OK)


