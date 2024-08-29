from django.db.models import Count
from django.template import Library
from ..models import Post, Tag, Comment


register = Library()


@register.inclusion_tag("includes/sidebar.html", takes_context=True)
def sidebar_view(context, tag=None):
    user = context["request"].user
    categories = Tag.objects.all()
    top_posts = (
        Post.objects.annotate(likes_count=Count("likes"))
        .filter(likes_count__gt=0)
        .order_by("-likes_count")
    )
    top_comments = (
        Comment.objects.annotate(likes_count=Count("likes"))
        .filter(likes_count__gt=0)
        .order_by("-likes_count")
    )

    return {
        "tag": tag,
        "user": user,
        "categories": categories,
        "top_posts": top_posts,
        "top_comments": top_comments,
    }
