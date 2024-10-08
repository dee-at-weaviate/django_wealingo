from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("question/<uuid:question_id>/", views.question, name="question"),
    path("question/view/<uuid:question_id>/", views.questionView, name="question_view"),
    path("questions/all/<str:query>", views.questionsForCategory, name="questions_all"),
    path("questions/create", views.generate_questions, name="generate_questions"),
    path("questions/search/<str:query>", views.search, name="search"),
    path("questions/view/all", views.questionsAllView, name="question_all_view"),
    path("quiz/level/<int:level>", views.quizForLevel, name="quiz_for_level" ),
    path('quiz/score', views.submitScore, name='submit_score'),
    path('user/new', views.createUser, name='create_user'),
    path('leaderboard', views.showLeaderBoard, name='show_leaderboard')
]