from guardian.shortcuts import get_perms
from rest_framework import exceptions
from rest_framework.viewsets import ModelViewSet


class ObjectPermissionMixin(ModelViewSet):
    def check_object_permissions(self, request, obj):
        print(self.action)
        action = self.map_action_to_permission()
        print(action)
        perms = get_perms(request.user, obj)
        print(perms)

        if action not in perms:
            raise exceptions.PermissionDenied()

    def map_action_to_permission(self):
        action_map = {
            "list": "view",
            "retrieve": "view",
            "create": "add",
            "update": "change",
            "partial_update": "change",
            "destroy": "delete",
        }

        singular = self.queryset.model._meta.verbose_name
        return "{}_{}".format(action_map[self.action], singular)
