from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (home,
    register,
    question_detail,
    QuestionCreateView,
    post_answer,
    upvoke_question,
    upvoke_answer,
    profile
)

urlpatterns = [
    path('', home, name="home"),
    path('register/', register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'),name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'),name="logout"),
    path('profile/',profile,name='profile'),
    path('question/new/', QuestionCreateView.as_view(),name='create-question'),
    path('question/<int:id>',question_detail,name='question'),
    path('post-answer/<int:qid>',post_answer,name='post-answer'),
    path('upvoke-question/<int:qid>',upvoke_question,name='upvoke-question'),
    path('upvoke-answer/<int:aid>',upvoke_answer,name='upvoke-answer')
]
