from rest_framework.permissions import BasePermission

class IsTeacherOfClass(BasePermission):
    def has_permission(self, request, view, obj):
        return request.user.userprofile in obj.teacher.all()