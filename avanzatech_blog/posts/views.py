from .paginators import PostPagination, LikePagination, CommentPagination 
from .filters import CommentFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth.models import User
from .models import BlogPost, Comment, Like
from .serializers import BlogPostSerializer,CommentSerializer, LikeSerializer

from .permissions import IsAuthorOrReadOnly,IsAuthorOrAdmin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.exceptions import PermissionDenied


class PostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny, IsAuthorOrReadOnly,IsAuthenticated]  # Solo autenticados pueden modificar los posts
    pagination_class = PostPagination # Aplicar el paginador personalizado para los posts
    
    
    def perform_create(self, serializer):
        """Aseguramos que el autor del post es el usuario autenticado"""
        serializer.save(author=self.request.user)
        
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # Todos pueden ver posts
        elif self.action in ['destroy', 'update', 'partial_update']:
            return [IsAuthorOrAdmin()]  # Solo el autor o admin puede modificarlos
        else:
            return [IsAuthenticated()]  # Requiere autenticación para otras acciones
        
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated],serializer_class=LikeSerializer)
    def toggle_like(self, request, pk=None):
        """
        Acción personalizada para alternar entre like y dislike en un post.
        """
        user = request.user
        post = self.get_object()

        # Verificar si el usuario ya dio like al post
        existing_like = Like.objects.filter(user=user, blog_post=post).first()

        if existing_like:
            # Si existe un like, eliminarlo (dislike)
            existing_like.delete()
            return Response({"message": "Dislike realizado"}, status=status.HTTP_200_OK)
        else:
            # Si no existe, crear un nuevo like
            Like.objects.create(user=user, blog_post=post)
            return Response({"message": "Like realizado"}, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['get'],serializer_class=LikeSerializer)
    def likes(self, request, pk=None):
        """Obtenemos los likes de un post específico"""
        post = self.get_object()
        user_id = request.query_params.get('user')
        # Obtener todos los likes relacionados con el post
        likes = post.like_entries.all()
        
        
        if user_id:
            try:
                user = User.objects.get(pk=user_id)  # Verifica si el usuario existe
                likes = likes.filter(user=user)  # Filtra los likes por usuario
            except User.DoesNotExist:
                raise NotFound(f"No existe un usuario con ID {user_id}")
            
            
        # Usar el paginador para la lista de likes
        paginator = LikePagination()
        paginated_likes = paginator.paginate_queryset(likes, request)    

        # Serializar los likes paginados
        serializer = LikeSerializer(paginated_likes, many=True)
        
        # Devolver la respuesta paginada
        return paginator.get_paginated_response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], serializer_class=CommentSerializer)
    def add_comment(self, request, pk=None):
        """Agregar un comentario a un post"""
        post = self.get_object()  # Obtener el post correspondiente

        # Validar y serializar el comentario
        serializer = CommentSerializer(data=request.data,context={'post': post})
        if serializer.is_valid():
            # Establecer el autor del comentario como el usuario autenticado
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'],serializer_class=CommentSerializer)
    def comments(self, request, pk=None):
        """Obtenemos los comentarios de un post específico con paginación y filtros"""
        post = self.get_object()
        comments = post.comments.all()

        # Aplicar filtro
        filtered_comments = CommentFilter(request.query_params, queryset=comments)

        # Verificar si el filtro es válido
        if filtered_comments.is_valid():
            comments = filtered_comments.qs
        else:
            comments = comments.none()  # O puedes manejarlo de otra manera

        # Paginación
        paginator = CommentPagination()
        paginated_comments = paginator.paginate_queryset(comments, request)

        # Serialización
        serializer = CommentSerializer(paginated_comments, many=True)

        # Retornar los comentarios paginados
        return paginator.get_paginated_response(serializer.data)
    
    
    
    @action(detail=True, methods=['delete'], url_path='comments/(?P<comment_id>\d+)/delete',serializer_class=CommentSerializer)
    def delete_comment(self, request, pk=None, comment_id=None):
        """Eliminar un comentario de un post específico"""
        post = self.get_object()
        comment = post.comments.filter(id=comment_id).first()

        if not comment:
            return Response({"detail": "Comentario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if comment.user != request.user:
            raise PermissionDenied("No tienes permiso para eliminar este comentario.")

        comment.delete()
        return Response({"detail": "Comentario eliminado exitosamente."}, status=status.HTTP_204_NO_CONTENT)
    


