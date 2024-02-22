from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home,
    register,
    question_detail,
    QuestionCreateView,
    post_answer,
    upvote_question,
    upvote_answer,
    profile,
)

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="main/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="main/logout.html"),
        name="logout",
    ),
    path("profile/", profile, name="profile"),
    path("question/new/", QuestionCreateView.as_view(), name="create-question"),
    path("question/<int:id>/", question_detail, name="question"),
    # Fix post-answer url
    # Done
    path("question/<int:qid>/answer/", post_answer, name="answer"),
    # upvoke -> upvote
    # Done
    path("upvote-question/<int:qid>/", upvote_question, name="upvote-question"),
    path("upvote-answer/<int:aid>/", upvote_answer, name="upvote-answer"),
]
