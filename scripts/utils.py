from os.path import join
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from allauth.account.models import EmailAddress
from a_posts.models import Tag
from a_rtchat.models import ChatGroup


def create_superuser(username="ad", email="admin@gmail.com", password="admin"):
    if not User.objects.filter(is_superuser=True).exists():
        user = User.objects.create_superuser(username, email, password)
        EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)


def create_chatrooms():
    for group_name in ("public-chat", "online-status"):
        if not ChatGroup.objects.filter(group_name=group_name).exists():
            ChatGroup.objects.create(group_name=group_name)


def create_tags():
    STATIC_PATH = join("static", "images")

    def create_tag(file_name, name, slug, order):
        if not Tag.objects.filter(name=name).exists():
            with open(join(STATIC_PATH, file_name), mode="rb") as file_data:
                file = File(file=file_data, name=file_name)
                Tag.objects.create(image=file, name=name, slug=slug, order=order)

    create_tag("icon_landscape.svg", "Landscape", "landscape", 1)
    create_tag("icon_people.svg", "People", "people", 2)
    create_tag("icon_animals.svg", "Animals", "animals", 3)
    create_tag("icon_urban.svg", "Urban", "urban", 4)
    create_tag("icon_blackandwhite.svg", "Black & White", "black-and-white", 5)


def update_site():
    Site.objects.filter(id=1).update(domain="awesome.com", name="Awesome")


def load_data():
    create_superuser()
    create_chatrooms()
    create_tags()
    update_site()
