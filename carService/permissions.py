from rest_framework.permissions import BasePermission, SAFE_METHODS

admin = "Admin"
serviceman = "Tamirci"
accountant = "Muhasebe"
customer = "Customer"


def get_user_group(user):
    return user.groups.values_list('name', flat=True)[0]


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        group = get_user_group(request.user)
        return (group == admin)


class IsServiceman(BasePermission):
    def has_permission(self, request, view):
        group = get_user_group(request.user)
        return (group == serviceman)


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        group = get_user_group(request.user)
        return (group == customer)


class IsAccountant(BasePermission):
    def has_permission(self, request, view):
        group = get_user_group(request.user)
        return (group == accountant)


class IsServicemanOrAdmin(BasePermission):
    def has_permission(self, request, view):
        group = get_user_group(request.user)
        return (group == serviceman or group == admin)


class IsCustomerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        group = get_user_group(request.user)
        return (group == customer or group == admin)


class IsAccountantOrAdmin(BasePermission):
    def has_permission(self, request, view):
        group = get_user_group(request.user)
        return (group == accountant or group == admin)


class IsAll(BasePermission):
    def has_permission(self, request, view):
        group = get_user_group(request.user)
        return group == serviceman or group == admin or group == customer


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            # this call is needed for request permissions
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)

        return decorated_func

    return decorator
