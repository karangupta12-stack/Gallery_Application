# Username: karangupta , Pass: karan@21
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.views import PasswordResetView
from .models import Photo, Album, Video
from django.contrib import messages
from collections import OrderedDict
from datetime import datetime
# Create your views here.

def signup(request):
    # Handle user registration using a custom user creation form.
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the new user in immediately after signup
            login(request, user)
            return redirect('gallery')
    else:
        form = CustomUserCreationForm()
    return render(request, 'photos/signup.html', {'form': form}) 


@login_required
def gallery(request):
    """
    Main gallery view:
    - Handles media upload (images/videos) and optional assignment to an album.
    - Renders grouped photos by upload date for the logged-in user.
    """
    if request.method == 'POST':
        # Get uploaded files (could be multiple)
        media_files = request.FILES.getlist('media_files')
        album_id = request.POST.get('album_select')

        # Resolve album if an album_id was provided and belongs to the user
        album_instance = None
        if album_id:
            try:
                album_instance = Album.objects.get(id=album_id, owner=request.user)
            except Album.DoesNotExist:
                # If album does not exist or doesn't belong to user, ignore and save without an album
                pass
        
        # Create Photo or Video objects depending on content type
        for file in media_files:
            if file.content_type.startswith('image'):
                Photo.objects.create(
                    user=request.user, image=file, album=album_instance
                )
            elif file.content_type.startswith('video'):
                Video.objects.create(
                    user=request.user, video_file=file, album=album_instance
                )
        
        return redirect('gallery')
        
    # Fetch active photos for the user and order newest first
    all_photos = Photo.objects.filter(user=request.user, is_active=True).order_by('-uploaded_at')
    
    # Group photos by upload date for display (OrderedDict preserves insertion order)
    grouped_photos = OrderedDict()
    
    for photo in all_photos:
        upload_date = photo.uploaded_at.date()
        
        if upload_date not in grouped_photos:
            grouped_photos[upload_date] = []
            
        grouped_photos[upload_date].append(photo)
    
    # Fetch albums owned by the user for album-related UI
    albums = Album.objects.filter(owner=request.user)
    
    context = {'grouped_photos': grouped_photos, 'albums': albums}
    
    return render(request, 'photos/gallery.html', context)


def login_view(request):
    # Handle user login using Django's AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('gallery')
    else:
        form = AuthenticationForm()
    return render(request, 'photos/login.html', {'form': form})


def logout_view(request):
    # Log the user out and redirect to login page
    logout(request)
    return redirect('login')


class CustomPasswordResetView(PasswordResetView):
    # Use custom email templates for password reset emails
    email_template_name = "registration/password_reset_email.txt"
    html_email_template_name = "registration/password_reset_email.html"
    

@login_required
def delete_photo(request, photo_id):
    # Soft-delete a photo by marking is_active=False if the request.user is the owner.
    photo = get_object_or_404(Photo, id=photo_id)
    
    # Check if the logged-in user is the owner
    if photo.user == request.user:
        photo.is_active = False
        photo.save()
        messages.success(request, 'Photo deleted successfully!')
        return redirect('gallery')
    else:
        # Do not reveal details—just show a permission error
        messages.error(request, 'You do not have permission to delete this photo.')
    
    return redirect('gallery')


# --------------------------------- Collection page---------------------------------
# photos/views.py

@login_required
def album_list(request):
    # List all albums owned by the logged-in user.
    albums = Album.objects.filter(owner=request.user)

    # Optional debug: count photos per album (kept commented)
    for album in albums:
        photo_count = album.photos.filter(is_active=True).count()
        # print(f"Album '{album.title}' has {photo_count} photos")
        # if album.cover_photo:
        #     print(f"  Cover photo URL: {album.cover_photo.image.url}")
        # else:
        #     print(f"  No cover photo found")

    context = {'albums': albums}
    return render(request, 'photos/albums.html', context)


@login_required
def album_detail(request, album_id):
    # Fetch the specific album by its ID, ensuring it belongs to the user
    album = get_object_or_404(Album, id=album_id, owner=request.user)

    # Handle file uploads if the form is submitted
    if request.method == 'POST':
        image_files = request.FILES.getlist('image_files')
        for image_file in image_files:
            Photo.objects.create(
                user=request.user, 
                album=album, 
                image=image_file
            )
        # Redirect back to the same album page to see the newly uploaded photos
        return redirect('album-detail', album_id=album.id)

    # Fetch all active photos in the album
    photos = Photo.objects.filter(album=album, is_active=True)
    context = {
        'album': album,
        'photos': photos,
    }
    return render(request, 'photos/album_detail.html', context)


@login_required
def albums_view(request):
    # Alias to list albums; kept for possible separate route usage
    albums = Album.objects.filter(owner=request.user)
    context = {'albums': albums}
    return render(request, 'photos/albums.html', context)


@login_required
def create_album(request):
    # Create a new album for the logged-in user if a title is provided.
    # print("--- create_album function was called ---") # Breadcrumb 1

    if request.method == 'POST':
        # print("Inside POST request block.") # Breadcrumb 2

        album_title = request.POST.get('album_title')
        # print(f"Album title found in POST data: '{album_title}'") # Breadcrumb 3

        if album_title:
            # print("Album title is not empty. Attempting to create album...") # Breadcrumb 4
            Album.objects.create(title=album_title, owner=request.user)
            # print("Album created successfully!") # Breadcrumb 5

    # print("Redirecting to album list.") # Breadcrumb 6
    return redirect('album-list')


@login_required
def delete_album(request, album_id):
    # Permanently delete an album (only allowed for owner). Uses POST for action.
    album =  get_object_or_404(Album, id = album_id, owner= request.user)
    
    if request.method == 'POST':
        album.delete()
        return redirect('album-list')
    
    return redirect('album-list')
    

@login_required
def view_bin(request):
    # Show soft-deleted (is_active=False) photos and videos so user can restore or permanently delete.
    binned_photos = Photo.objects.filter(user=request.user, is_active = False)
    binned_videos = Video.objects.filter(user=request.user, is_active=False)
    context = {
        'photos':binned_photos,
        'videos': binned_videos,
    }
    return render(request, 'photos/bin.html', context)


@login_required
def restore_photo(request, photo_id):
    # Restore a previously soft-deleted photo.
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)
    
    if request.method == 'POST':
        photo.is_active = True
        photo.save()
    return redirect('view-bin')


@login_required
def delete_photo_permanently(request, photo_id):
    # Permanently delete a photo from the database (irreversible).
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)
    
    if request.method == 'POST':
        photo.delete()
    return redirect('view-bin')


@login_required
def toggle_favourite(request, photo_id):
    # Toggle the is_favourite flag for a photo and return user to the referring page.
    photo = get_object_or_404(Photo, id=photo_id, user=request.user)
    
    if request.method == 'POST':
        photo.is_favourite = not photo.is_favourite
        photo.save()
        
        return redirect(request.META.get('HTTP_REFERER', 'gallery'))
    return redirect('gallery')


@login_required
def view_favourites(request):
    # Show all active photos marked as favourite by the user.
    favourite_photos = Photo.objects.filter(user=request.user, is_favourite = True, is_active = True)
    context = {'photos': favourite_photos}
    return render(request, 'photos/favourites.html', context)


@login_required
def recently_added(request):
    # Show photos ordered by most recently uploaded.
    recent_photos = Photo.objects.filter(user=request.user, is_active=True).order_by('-uploaded_at')
    context = {'photos': recent_photos}
    return render(request, 'photos/recently_added.html', context)


@login_required
def search_view(request):
    """
    Search photos by upload date.
    - Expects 'query_date' in GET parameters in YYYY-MM-DD format.
    - If parsing fails, returns an empty list.
    """
    found_photos = None
    query_date_str = ""
    if 'query_date' in request.GET:
        query_date_str = request.GET.get('query_date')
        
        if query_date_str:            
            try:
                query_date = datetime.strptime(query_date_str, '%Y-%m-%d').date()
                found_photos = Photo.objects.filter(
                    user=request.user,
                    uploaded_at__date=query_date,
                )
            except ValueError:
                # Invalid date format; show no results
                found_photos = []
    context = {
        'photos': found_photos,
        'query_date': query_date_str,
    }
    return render(request, 'photos/search.html', context)


@login_required
def view_videos(request):
    # Fetch active videos for the user and render a videos page.
    videos = Video.objects.filter(user=request.user, is_active=True).order_by('-uploaded_at')
    context = {'videos': videos}
    return render(request, 'photos/videos.html', context)


@login_required
def delete_video(request, video_id):
    # Soft-delete a video by marking is_active=False
    video = get_object_or_404(Video, id=video_id, user=request.user)
    if request.method == 'POST':
        video.is_active = False  # Mark video inactive (move to Bin)
        video.save()
    return redirect('view-videos')


@login_required
def restore_video(request, video_id):
    # Restore a soft-deleted video
    video = get_object_or_404(Video, id=video_id, user=request.user)
    
    if request.method == 'POST':
        video.is_active = True
        video.save()
    return redirect('view-bin')


@login_required
def delete_video_permanently(request, video_id):
    # Permanently remove a video from the database
    video = get_object_or_404(Video, id=video_id, user=request.user)
    
    if request.method == 'POST':
        video.delete()
    return redirect('view-bin')