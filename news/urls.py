from django.urls import path
from .views import NewsList, NewsDetail, PostCreateView, PostDetailedView, PostUpdateView, PostDeleteView # импортируем наше представление
 
 
urlpatterns = [
    # path — означает путь. В данном случае путь ко всем новостям у нас останется пустым, позже станет ясно почему
    path('', NewsList.as_view()), # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', NewsDetail.as_view()),
    path('create/', PostCreateView.as_view(), name='new_post_form'),
    path('<int:pk>/', PostDetailedView.as_view(), name='post_details'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post_form'), # Новый маршрут
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post_form'),
]