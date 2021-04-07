from rest_framework.response import Response
from rest_framework import status
from content.models import Movie, Comment, Photo
from accounts.models import User, FollowRequest
from content.serializers import ( 
    MovieSerializer, 
    CommentSerializer,
    MovieCreateSerializer,
    CreateCommentSerializer,
    ImageCreateSerializer,
    ImageSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from rest_framework.generics import UpdateAPIView

class MovieView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_movie(self, pk):
        try:
            return Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        movie = self.get_movie(kwargs['pk'])
        if not movie.is_premium or request.user.has_paid():
            serializer = MovieSerializer(movie, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)     
    
    def post(self, request, **kwargs):
        serializer = MovieCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        movie = self.get_movie(kwargs['pk'])        
        if movie.author == request.user:
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    def patch(self, request, **kwargs):
        movie = self.get_movie(kwargs['pk'])
        if movie.author == request.user:
            serializer = MovieCreateSerializer(movie, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response(status=status.HTTP_403_FORBIDDEN)


class ImageView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_user_photos(self, request, **kwargs):
        try:
            user = User.objects.get(id=kwargs['pk'])
            return Photo.objects.filter(author=user)
        except User.DoesNotExist:
            raise Http404
    
    def photo_detail(self, request, **kwargs):
        try:
            return Photo.objects.get(id=kwargs['id'])
        except Photo.DoesNotExist:
            raise Http404
    
    def get(self, request, **kwargs):
        photo = Photo.objects.get(id=kwargs['pk'])
        serializer = ImageSerializer(photo, many=False)
        return Response(serializer.data)

    def post(self, request, **kwargs):
        serializer = ImageCreateSerializer(context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def delete(self, request, **kwargs):
        photo = Photo.objects.get(id=kwargs['id'])
        if photo.author == request.user:
            photo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CommentsList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    serializer_class = CommentSerializer
    def get_queryset(self, **kwargs):
        try:
            post = Post.objects.get(id=self.kwargs['pk'])
            comments = Comment.objects.filter(post=self.kwargs['pk'])
            return comments
        except:
            raise Http404()


class CommentView(APIView):
    permission_classes = (IsAuthenticated,)
    def get_movie(self, pk):
        try:
            return Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get_comment(self, pk):
        try:
            return Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            raise Http404

    def post(self, request, **kwargs):
        movie = self.get_movie(kwargs['pk'])
        serializer = CreateCommentSerializer(data=request.data, context={'request': request, 'movie': movie})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        comment = self.get_comment(kwargs['pk'])
        if comment.author == request.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, **kwargs):
        comment = self.get_comment(kwargs['pk'])
        if comment.author == request.user:
            serializer = CreateCommentSerializer(data=request.data, instance=comment)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)



class LikeMovie(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self, request, **kwargs):
        try:
            movie = Movie.objects.get(id=kwargs['pk'])
            option = request.data['option']
            if option == 'like':
                if request.user in movie.likes.all():
                    movie.likes.remove(request.user)
                else:
                    movie.likes.add(request.user)
                    movie.dis_likes.remove(request.user)           
            elif option == 'dislike':
                if request.user in movie.dis_likes.all():
                    movie.dis_likes.remove(request.user)
                else:    
                    movie.dis_likes.add(request.user)
                    movie.likes.remove(request.user)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class LikePhoto(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    def put(self, request, **kwargs):
        try:
            photo = Photo.objects.get(id=kwargs['pk'])
            if request.user in photo.likes.all():
                photo.likes.remove(request.user)
            else:
                photo.likes.add(request.user)
            return Response(status=status.HTTP_200_OK)       
        except Photo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)