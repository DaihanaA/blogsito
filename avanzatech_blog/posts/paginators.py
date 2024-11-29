from rest_framework.pagination import PageNumberPagination

class PostPagination(PageNumberPagination):
    page_size = 10  # 10 elementos por página
    page_size_query_param = 'page_size'  # Permite que los usuarios cambien el tamaño de la página
    max_page_size = 100  # Tamaño máximo de la página
    

class LikePagination(PageNumberPagination):
    page_size = 20  # 20 elementos por página
    page_size_query_param = 'page_size'  # Permite que los usuarios cambien el tamaño de la página
    max_page_size = 100  # Tamaño máximo de la página
    
class CommentPagination(PageNumberPagination):
    page_size = 10  # Puedes cambiar este número según tus necesidades
    page_size_query_param = 'page_size'
    max_page_size = 100  # El número máximo de comentarios que pueden mostrarse por página
