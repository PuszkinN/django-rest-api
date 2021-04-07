from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User, FollowRequest
from accounts.serializers import UserSerializer, RegisterUserSerializer, VisitedUserProfileSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from content.models import Movie
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.authtoken.models import Token

class UserView(APIView):
    @permission_classes(IsAuthenticated)
    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @permission_classes(IsAuthenticated,)
    def patch(self, request, format=None):
        user = request.user
        serializer = RegisterUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@permission_classes(IsAuthenticated)
@api_view(['GET'])
def visited_user(request, pk):
    try:
        user = User.objects.get(id=pk)
        serializer = VisitedUserProfileSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes(IsAuthenticated)
@api_view(['PUT'])
def follow_user(request, pk):
    try:
        user = User.objects.get(id=pk)
        if request.user not in user.profile.followers:
            if user.profile.is_private:
                if not FollowRequest.objects.filter(receiver=user).filter(sender=request.user).first():
                    follow_request = FollowRequest.objects.create(
                        sender=request.user,
                        receiver=user,
                        is_active=True
                    )
                    follow_request.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                user.profile.followers.add(request.user)
                return Response(status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes(IsAuthenticated)
@api_view(['PUT'])
def decline_follow(request, pk):
    try:
        follow_request = FollowRequest.objects.get(id=pk)
        follow_request.is_active = False
        follow_request.save()
        return Response(status=status.HTTP_200_OK)
    except FollowRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes(IsAuthenticated)
@api_view(['PUT'])
def accept_follow(request, pk):
    try:
        follow_request = FollowRequest.objects.get(id=pk)
        follow_request.is_active = False
        follow_request.receiver.profile.followers.add(follow_request.sender)
        follow_request.receiver.profile.save()
        follow_request.save()
        return Response(status=status.HTTP_200_OK)
    except FollowRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes(IsAuthenticated)
@api_view(['PUT'])
def add_to_favorite_movies(request, pk):
    try:
        movie = Movie.objects.get(id=pk)
        request.user.profile.favorite_movies.add(movie)
        return Response(status=status.HTTP_200_OK)
        
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() 
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)