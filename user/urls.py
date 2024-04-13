from django.urls import path
from rest_framework.authtoken import views

from user.views import CreateUserView, RetrieveUserView, ManageUserView, LoginUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("<int:pk>/", RetrieveUserView.as_view(), name="retrieve"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user"

