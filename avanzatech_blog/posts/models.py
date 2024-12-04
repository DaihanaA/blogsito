from django.db import models
from django.contrib.auth.models import Group,User


class BlogPost(models.Model):
    PUBLIC = 'public'
    AUTHENTICATED = 'authenticated'
    AUTHOR = 'author'
    TEAM = 'team'

    READ_PERMISSIONS = [
        (PUBLIC, 'Public'),
        (AUTHENTICATED, 'Authenticated'),
        (AUTHOR, 'Author'),
        (TEAM, 'Team'),
       
    ]
    
    EDIT_PERMISSIONS = [
    (PUBLIC, 'Public'),
    (AUTHENTICATED, 'Authenticated'),
    (AUTHOR, 'Author'),
    (TEAM, 'Team'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    excerpt = models.CharField(max_length=200, blank=True)  # Primeros 200 caracteres del post
    timestamp = models.DateTimeField(auto_now_add=True)
    groups = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL)
   
    likes = models.ManyToManyField(
        User,  # Relación con el usuario
        through='Like',  # Usa el modelo intermedio `Like`
        related_name='liked_posts'  # Relación inversa
    )

    # Permisos de lectura y edición
    read_permission = models.CharField(
        max_length=15,
        choices=READ_PERMISSIONS,
        default=PUBLIC,
    )
    edit_permission = models.CharField(
        max_length=15,
        choices=EDIT_PERMISSIONS,
        default=AUTHOR,
    )

    def __str__(self):
        return self.title

    def get_excerpt(self):
        return self.content[:200]  # Solo los primeros 200 caracteres
    
    def can_edit(self, user):
        # Permitir si el usuario es el autor o miembro del equipo
        return self.author == user or self.team.members.filter(id=user.id).exists()
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')  # Relación inversa
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.blog_post.title}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes_given")
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="like_entries")  # Nombre único

    class Meta:
        unique_together = ('user', 'blog_post')  # Evitar likes duplicados por usuario      

    def __str__(self):
        return f"Liked by {self.user.username} on {self.blog_post.title}"  # Cambiar la coma por un return directo
