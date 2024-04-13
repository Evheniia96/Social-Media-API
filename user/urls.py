from django.urls import path

from user.views import CreateUserView, RetrieveUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("<int:pk>/", RetrieveUserView.as_view(), name="retrieve"),
]

app_name = "user"

