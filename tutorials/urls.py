from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("question/<uuid:question_id>/", views.question, name="question"),
    path("question/view/<uuid:question_id>/", views.questionView, name="question_view"),
    path("questions/all", views.questionsAllView, name="question_all_view"),

]