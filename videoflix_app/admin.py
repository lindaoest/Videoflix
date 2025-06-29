from django.contrib import admin

from videoflix_app.models import Genre, Video

admin.site.register(Video)
admin.site.register(Genre)
