from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


admin.site.site_title = 'Student Management'
admin.site.site_header = 'Lesson Report'
admin.site.index_title = 'Menu'

urlpatterns = [
    path('teacher-admin/', admin.site.urls),
    path('', include('students.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)