from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework import status
from .permission_decorator import permission_required


# Create your views here.
class UserListCreateView(generics.CreateAPIView):
    permission_classes  = [HasAPIKey]
    serializer_class    = UserListCreateSerializer
    queryset            = User.objects.all().order_by('-id')

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class SigninView(generics.GenericAPIView):
    permission_classes      = [HasAPIKey]
    serializer_class        = SigninSerializer
    queryset                = User.objects.all().order_by('-id')

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class   = UserListCreateSerializer
    queryset           = User.objects.all().order_by("-id")

    @permission_required('view_user')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class   = UserListCreateSerializer
    queryset           = User.objects.all()



class UserPermissionsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        user_id = request.data['id']
        if user_id:
            try:
                userobj=User.objects.get(id=int(user_id))
                permissions = userobj.get_permissions_by_role()
                return Response({"permission":permissions})
            except Exception as e:
                return Response({"message":"Requested user have no or is_owner True"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"user_id":"User id is required"},status=status.HTTP_400_BAD_REQUEST)
                
class PermissionListView(generics.ListAPIView):
    permission_classes  = [permissions.IsAuthenticated]
    serializer_class    = UserPermissionSerializer
    queryset            = UserPermission.objects.all()
    pagination_class    = None
    
    permission_required('view_user_permission')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UserRoleListView(generics.ListCreateAPIView):
    permission_classes  = [permissions.IsAuthenticated]
    serializer_class    = UserRoleListSerializer
    queryset = UserRole.objects.all().order_by('-id')

    @permission_required('view_user_role')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @permission_required('add_user_role')
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserRoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes  = [permissions.IsAuthenticated]
    serializer_class    = UserRoleDetailSerializer
    queryset            = UserRole.objects.all().order_by('-id')


    @permission_required('view_user_role')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @permission_required('update_user_role')
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @permission_required('update_user_role')
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    @permission_required('delete_user_role')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)