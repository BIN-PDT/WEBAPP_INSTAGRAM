from a_posts.views import home_view
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # ADMIN.
    path("admin/", admin.site.urls),
    # FEATURE.
    path("accounts/", include("allauth.urls")),
    path("profile/", include("a_users.urls")),
    path("post/", include("a_posts.urls")),
    path("inbox/", include("a_inbox.urls")),
    path("chat/", include("a_rtchat.urls")),
    # HOME.
    path("", home_view, name="home"),
    path("category/<tag>/", home_view, name="category"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
