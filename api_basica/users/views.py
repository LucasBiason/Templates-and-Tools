from rest_framework import mixins, viewsets, authentication, permissions
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class ManageUserView(viewsets.GenericViewSet,
                                        mixins.ListModelMixin,
                                        mixins.RetrieveModelMixin,
                                        mixins.DestroyModelMixin,
                                        mixins.CreateModelMixin,
                                        mixins.UpdateModelMixin):
    ''' Manage the authenticated user '''
    serializer_class = UserSerializer
    authentication_classes =(authentication.TokenAuthentication,)
    permission_classes =(permissions.IsAuthenticated,)
    queryset = User.objects.all()
    
    def get_queryset(self, *args, **kwargs):
        return User.get_queryset(**kwargs)
        
    def retrieve(self, request, *args, **kwargs):
        user = User.retrieve(kwargs.get('pk'))
        return Response(self.serializer_class(user).data)
        
    def destroy(self, request, *args, **kwargs):
        user = User.retrieve(kwargs.get('pk'))
        user.is_active = False
        user.save()
        return Response({
            'user': kwargs.get('pk'),
            'status': 'success'
        })
        
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        user = User.perform_create(data, self.request.user)
        return Response(self.serializer_class(user).data)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        user = User.retrieve(kwargs.get('pk'))
        user.perform_update(data, self.request.user)
        return Response(self.serializer_class(user).data)
    
    
