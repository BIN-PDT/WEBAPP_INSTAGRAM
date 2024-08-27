from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from a_posts.views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", home_view, name="home"),
    path("category/<tag>/", home_view, name="category"),
    path("post/create/", post_create_view, name="post-create"),
    path("post/delete/<pk>/", post_delete_view, name="post-delete"),
    path("post/edit/<pk>/", post_edit_view, name="post-edit"),
    path("post/<pk>/", post_page_view, name="post"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
