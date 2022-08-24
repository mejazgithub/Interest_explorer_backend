from django.urls import path
from .views import *

urlpatterns = [
    path('signup/',                         UserListCreateView.as_view(),           name="list-create-user-view"),
    path('signin/',                         SigninView.as_view(),                   name="sigin-view"),
    path('userlistview/',                   UserListView.as_view(),                 name="user-list-view"),
    path('userdetailview/<pk>/',            UserDetailView.as_view(),               name="user-detail-view"),
    path('userpermissions/',                UserPermissionsView.as_view(),          name='user-permission-list-by-role'),
    path('permissionslistview/',            PermissionListView.as_view(),           name='user-permission-list-view'),
    path('userrolelistview/',               UserRoleListView.as_view(),             name='user-role-list-view'),
    path('userroledetailview/<pk>/',        UserRoleDetailView.as_view(),           name='user-role-detail-view'),
]


from .models import setup_permissions
setup_permissions()