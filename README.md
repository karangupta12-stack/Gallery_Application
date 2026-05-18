<div align="center">

# Gallery Application

### A clean Django media gallery for uploading, organizing, searching, and managing photos and videos.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Local%20DB-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Whitenoise](https://img.shields.io/badge/WhiteNoise-Static%20Files-6B7280?style=for-the-badge)

</div>

---

## Overview

Gallery Application is a Django-based web app that lets users manage their personal photo and video collection. It includes authentication, album management, favourites, soft delete recovery, date-based search, and a clean media browsing experience.

The project is structured as a production-ready Django app with environment-based configuration, static file support through WhiteNoise, and a `Procfile` for deployment platforms that run Gunicorn.

## Features

<table>
  <tr>
    <td><strong>Secure Accounts</strong></td>
    <td>User signup, login, logout, and password reset support.</td>
  </tr>
  <tr>
    <td><strong>Photo Uploads</strong></td>
    <td>Upload and view personal photos grouped by upload date.</td>
  </tr>
  <tr>
    <td><strong>Video Library</strong></td>
    <td>Upload, browse, delete, restore, and permanently remove videos.</td>
  </tr>
  <tr>
    <td><strong>Albums</strong></td>
    <td>Create albums and organize media into user-owned collections.</td>
  </tr>
  <tr>
    <td><strong>Favourites</strong></td>
    <td>Mark important photos as favourites and view them separately.</td>
  </tr>
  <tr>
    <td><strong>Recycle Bin</strong></td>
    <td>Soft-deleted photos and videos can be restored or permanently deleted.</td>
  </tr>
  <tr>
    <td><strong>Date Search</strong></td>
    <td>Find photos by upload date using the built-in search page.</td>
  </tr>
</table>

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Django 5.2 |
| Database | SQLite |
| Authentication | Django Auth |
| Static Files | WhiteNoise |
| Media Handling | Django `ImageField` and `FileField` |
| Deployment Server | Gunicorn |
| Environment Variables | python-dotenv |

## Project Structure

```text
Gallery_Application-main/
|-- gallery_project/        # Main Django project settings and URL configuration
|-- photos/                 # Gallery app: models, views, forms, URLs, templates, static files
|-- media/                  # Uploaded media files for local development
|-- manage.py               # Django management script
|-- requirements.txt        # Python dependencies
|-- Procfile                # Deployment process definition
`-- README.md               # Project documentation
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/karangupta12-stack/Gallery_Application.git
cd Gallery_Application
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DJANGO_SECRET_KEY=your-secret-key
EMAIL_USER=your-email@example.com
EMAIL_PASSWORD=your-email-app-password
```

> Use an app password for SMTP email accounts when required by your email provider.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open the app in your browser:

```text
http://127.0.0.1:8000/
```

## Main Pages

| Page | Route |
| --- | --- |
| Gallery | `/` |
| Login | `/login/` |
| Signup | `/signup/` |
| Albums | `/albums/` |
| Favourites | `/favourites/` |
| Recently Added | `/recently-added/` |
| Search | `/search/` |
| Videos | `/videos/` |
| Bin | `/bin/` |
| Admin Panel | `/admin/` |

## Deployment Notes

The project includes a `Procfile`:

```text
web: gunicorn gallery_project.wsgi
```

Before deploying, review the following settings:

- Set `DEBUG = False` for production.
- Configure `ALLOWED_HOSTS` for your deployed domain.
- Store secrets in environment variables.
- Run `python manage.py collectstatic`.
- Use a production-ready media storage solution if users will upload files in production.

## Environment And Security

This repository is configured to keep sensitive and generated files out of Git:

- `.env`
- `db.sqlite3`
- `media/`
- `staticfiles/`
- virtual environment folders

Never commit real credentials, email passwords, database files, or private uploaded media.

## Future Improvements

- Add cloud media storage for production uploads.
- Add pagination or infinite scrolling for large galleries.
- Add photo captions, tags, and album descriptions.
- Add richer search filters for albums, favourites, and media type.
- Add automated tests for upload, delete, restore, and authentication flows.

## Author

Developed by **Karan Gupta**.

---

<div align="center">
  <strong>Built with Django for simple, organized, and reliable personal media management.</strong>
</div>
