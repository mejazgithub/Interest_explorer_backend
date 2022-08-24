from django.core.exceptions import PermissionDenied


def permission_required(perm):
    def inner(function):
        def wrapper(self, *args, **kwargs):
            if self.request.user.is_owner == False:
                if self.request.user.user_role:     
                    perm_store=self.request.user.user_role.permission.values_list('code', flat=True)
                    if isinstance(perm,list):
                        for p in perm:
                            if p in perm_store:
                                has_perm=True
                                break
                            else:
                                has_perm=False
                    else:
                        has_perm = perm in self.request.user.user_role.permission.values_list('code', flat=True)
                    if has_perm:
                        return function(self, *args, **kwargs)
                    else:
                        raise PermissionDenied
                else:
                    raise PermissionDenied
            else:
                return function(self, *args, **kwargs)
        return wrapper
    return inner