from django.urls import path
from .views import *


urlpatterns = [
    path("", profile_view, name="profile"),
    path("edit/", profile_edit_view, name="profile-edit"),
    path("delete/", profile_delete_view, name="profile-delete"),
    path("onboarding/", profile_edit_view, name="profile-onboarding"),
    path("settings/", profile_settings_view, name="profile-settings"),
    path("verify_email/", profile_verify_email, name="profile-verify-email"),
    path("link/<provider>/", link_social_account, name="link-social-account"),
    path("<username>/", profile_view, name="user-profile"),
]
