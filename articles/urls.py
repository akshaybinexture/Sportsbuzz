from django.urls import path
from .views import (
    home, contact, article_details, likeview, categoryview, latest_article
# , article_detail
)
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('article-detail/<int:pk>/', article_details, name='article-detail'),
    path('like/<int:article_id>/', likeview, name='like_article'),
    path('contact/', contact, name='contact'),
    path('article-detail/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('sport/<str:cats>/', categoryview, name='category'),
    path('latest/', latest_article, name='latest-article'),

    # path('article-detail/', article_detail, name='article-detail')

]