from a_posts.views import *
from a_users.views import *
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # ADMIN.
    path("admin/", admin.site.urls),
    # FEATURE.
    path("accounts/", include("allauth.urls")),
    path("inbox/", include("a_inbox.urls")),
    path("chat/", include("a_rtchat.urls")),
    # HOME.
    path("", home_view, name="home"),
    path("category/<tag>/", home_view, name="category"),
    # POST.
    path("post/create/", post_create_view, name="post-create"),
    path("post/edit/<pk>/", post_edit_view, name="post-edit"),
    path("post/delete/<pk>/", post_delete_view, name="post-delete"),
    path("post/like/<pk>/", post_like, name="like-post"),
    path("post/<pk>/", post_page_view, name="post"),
    # PROFILE.
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", profile_edit_view, name="profile-edit"),
    path("profile/delete/", profile_delete_view, name="profile-delete"),
    path("profile/onboarding/", profile_edit_view, name="profile-onboarding"),
    path("profile/settings/", profile_settings_view, name="profile-settings"),
    path("profile/verify_email/", profile_verify_email, name="profile-verify-email"),
    path("profile/link/<provider>/", link_social_account, name="link-social-account"),
    path("profile/<username>/", profile_view, name="user-profile"),
    # COMMENT.
    path("comment_sent/<pk>/", comment_sent, name="comment-sent"),
    path("comment/delete/<pk>/", comment_delete_view, name="comment-delete"),
    path("comment/like/<pk>/", comment_like, name="like-comment"),
    # REPLY.
    path("reply_sent/<pk>/", reply_sent, name="reply-sent"),
    path("reply/delete/<pk>/", reply_delete_view, name="reply-delete"),
    path("reply/like/<pk>/", reply_like, name="like-reply"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
