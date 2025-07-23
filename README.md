# Videoflix – A Django-based Video Streaming Platform

**Videoflix** is a full-stack web application built with Django and Django REST Framework (DRF). It allows users to register, log in, and stream video content using HTTP Live Streaming (HLS). The frontend uses [video.js](https://videojs.com/) to provide a smooth and customizable video player experience.

## Features

- User authentication (login/logout)
- Video streaming using HLS format
- Backend built with Django + DRF
- Frontend video player with video.js
- Automatic database migrations and RQ worker startup
- Email notifications via Django signals
- Dockerized for easy local development

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML/CSS + JavaScript with video.js
- **Queueing**: Redis Queue (RQ) for background tasks
- **Containerization**: Docker, Docker Compose
- **Database**: PostgreSQL
- **Streaming**: HLS (.m3u8 playlist and .ts segments)

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Installation

Clone the repository:

```bash
git clone git@github.com:lindaoest/Videoflix.git
cd videoflix
```

### Build and start the containers:

```bash
docker-compose up --build
```

## Information about the project setup

### Email Notifications via Signals
Django signals are used to send email notifications for key events, such as:

- User registration
- Password resets

### Docker Overview
The docker-compose.yml includes the following services:

- web: Django application
- db: PostgreSQL database
- redis: Redis instance for RQ
- worker: RQ worker for background tasks

### Entrypoint Behavior
The entrypoint.sh handles:

- Applying migrations
- Starting the RQ worker automatically
- Keeping models in sync on container start
- Running `python manage.py rqworker default &` to start the background task worker
- Running `exec gunicorn core.wsgi:application --bind 0.0.0.0:8000` to serve the Django application

### Useful Commands
Run Django management commands in the web container:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```