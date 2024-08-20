from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.http import Http404
from django.views import View

from .models import Questions_Inventory, QuizLevel, Quiz
from .serializer import serialize_questions, serialize_quiz

import logging

# class QuestionsView(View):

logger = logging.getLogger(__name__)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def question(request, question_id):
    # question = get_object_or_404(Questions_Inventory, pk=question_id)
    data = {
        'answer': 2,
        'status': 'success',
    }
    return JsonResponse(data, status=200)

def questions_all(request, course_id):
    logger.debug('in questions all')
    latest_question_list = Questions_Inventory.objects.order_by("-created_at")[:5]
    logger.debug(latest_question_list)
    results = {
        "questions" : serialize_questions(latest_question_list)
    }
    logger.debug(results)
    return JsonResponse(results, status=200)

def quizForLevel(request, level):
    questions = Quiz.objects.filter(quiz_level_id=level)
    # order_by("-created_at")[:5]
    # filter(quiz_level_id=level)
    logger.debug(questions)
    results = {
        "questions" : serialize_quiz(questions)
    }
    logger.debug(results)
    return JsonResponse(results, status=200)

def questionView(request, question_id):
    question = get_object_or_404(Questions_Inventory, pk=question_id)
    return render(request, "tutorials/question.html", {"question": question})

def questionsAllView(request):
    latest_question_list = Questions_Inventory.objects.order_by("-created_at")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "tutorials/index.html", context)

def question_old(request, question_id):
    try:
        question = Questions_Inventory.objects.get(pk=question_id)
    except Questions_Inventory.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "tutorials/question.html", {"question": question})
    # return HttpResponse("You're looking at question %s." % question_id)

def questions_all_old(request):
    latest_question_list = Questions_Inventory.objects.order_by("-created_at")[:5]
    template = loader.get_template("tutorials/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))
    # output = ", ".join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)