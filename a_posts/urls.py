from django.urls import path
from .views import *


urlpatterns = [
    # POST.
    path("create/", post_create_view, name="post-create"),
    path("edit/<pk>/", post_edit_view, name="post-edit"),
    path("delete/<pk>/", post_delete_view, name="post-delete"),
    path("like/<pk>/", post_like, name="like-post"),
    path("<pk>/", post_page_view, name="post"),
    # COMMENT.
    path("comment_sent/<pk>/", comment_sent, name="comment-sent"),
    path("comment/delete/<pk>/", comment_delete_view, name="comment-delete"),
    path("comment/like/<pk>/", comment_like, name="like-comment"),
    # REPLY.
    path("reply_sent/<pk>/", reply_sent, name="reply-sent"),
    path("reply/delete/<pk>/", reply_delete_view, name="reply-delete"),
    path("reply/like/<pk>/", reply_like, name="like-reply"),
]
