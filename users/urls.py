from django.urls import path

from users.views import SignUpView, LoginView, LikeView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', LoginView.as_view()),
    path('/likes', LikeView.as_view()),
]
