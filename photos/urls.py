from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    
    
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),

    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('', views.gallery, name='gallery'),
    
    path('photo/delete/<int:photo_id>/', views.delete_photo, name='delete-photo'),
    
    path('albums/', views.album_list, name='album-list'),
    
    path('album/<int:album_id>/', views.album_detail, name='album-detail'),

    path('album/create/', views.create_album, name='create-album'),
    
    path('album/delete/<int:album_id>/', views.delete_album, name='delete-album'),
    
    path("bin/", views.view_bin, name="view-bin"),
    
    path('photo/restore/<int:photo_id>/', views.restore_photo, name='restore-photo'),
    
    path('photo/delete-permanently/<int:photo_id>/', views.delete_photo_permanently, name='delete-photo-permanently'),
    
    path('favourites/', views.view_favourites, name='view-favourites'),
    
    path('photo/favourite/<int:photo_id>/', views.toggle_favourite, name='toggle-favourite'),
    
    path('recently-added/', views.recently_added, name='recently-added'),

    path('search/', views.search_view, name='search'),
    
    path('videos/', views.view_videos, name='view-videos'),
    
    path('video/delete/<int:video_id>/', views.delete_video, name='delete-video'),
    
    path('video/restore/<int:video_id>/', views.restore_video, name='restore-video'),
    
    path('video/delete-permanently/<int:video_id>/', views.delete_video_permanently, name='delete-video-permanently'),
]