from django.shortcuts import get_object_or_404,render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.http import Http404
from django.views import View
from django.db.models import F
from .models import Questions_Inventory, QuizLevel, Quiz, Leaderboard, User_Profile, Questions_Category
from django.db import IntegrityError, DatabaseError
from .serializer import serialize_questions, serialize_quiz, serialize_leaderboard, serialize_generated_questions
from .weaviate import perform_search, generate_text_with_prompt
from .util import create_prompt

import logging
import json

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


@csrf_exempt 
def createUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            logger.info('error')
            return JsonResponse({"error": "Invalid JSON"}, status=400)        
        username = data.get('username')   
        email = data.get('email') 
        if username is None or email is None:
            return JsonResponse({"error": "username and email are required"}, status=400)

        try:
            user_profile, created = User_Profile.objects.get_or_create(username=username, email=email)

            return JsonResponse({"message": "User updated successfully", 
                                 "username": user_profile.username,
                                 "email": user_profile.email,
                                 'user_id': user_profile.user_id}, status=200)
        
        except DatabaseError as e:
            logger.error(f"DatabaseError while creating user : {str(e)}")
            return JsonResponse({"error": "DB error when creating user"})
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return JsonResponse({"error": "Exception when creating user"})
    else:
        logger.info('error method')
    return HttpResponse(status=405) 

@csrf_exempt 
def submitScore(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # logger.info(data)
        except json.JSONDecodeError:
            logger.info('error')
            return JsonResponse({"error": "Invalid JSON"}, status=400)        
        user_id = data.get('user_id')
        new_score = data.get('totalScore')
        logger.info(user_id)
        logger.info(new_score)
        if user_id is None or new_score is None:
            return JsonResponse({"error": "user_id and totalScore are required"}, status=400)
        
        user_profile = get_object_or_404(User_Profile, pk=user_id)
        logger.info(user_profile)

        leaderboard_entry, created = Leaderboard.objects.get_or_create(
                                        user_id=user_profile,
                                        defaults={'xp': new_score} 
                                    )

        if not created:
            leaderboard_entry.xp = F('xp') + new_score
            leaderboard_entry.save()
            leaderboard_entry.refresh_from_db()

        if created:
            leaderboard_entry.save()

        logger.info(leaderboard_entry)
        logger.info('response')
        return JsonResponse({"message": "Score updated successfully", "new_total_xp": leaderboard_entry.xp})
    else:
        logger.info('error method')
    return HttpResponse(status=405) 

def showLeaderBoard(request):
    logger.debug('in show leaderbaoard')
    # latest_leaderboard = Leaderboard.objects.order_by("-xp")[:15]
    latest_leaderboard = Leaderboard.objects.select_related('user_id').order_by('-xp')[:15]
    logger.debug(latest_leaderboard)
    results = {
        "leaderboard" : serialize_leaderboard(latest_leaderboard)
    }
    logger.debug('in shooooow leaderbaoard')
    logger.debug(results)
    return JsonResponse(results, status=200)

def generate_questions(request, category):
    logger.debug('in generate ques')
    questions = [
        {
            "category": "Order in a restaurant",
            "question_text": "For the first course, I'd like a pasta",
            "translation": "Per primo, vorrei una pasta",
            "difficulty": "3"
        },
        {
            "category": "Navigate a city",
            "question_text": "Is there a pharmacy nearby?",
            "translation": "C'è una farmacia nelle vicinanze?",
            "difficulty": "2"
        }
    ]
    prompt = create_prompt(questions, category)    
    try:
        questions = generate_text_with_prompt(prompt, category, "")
        results = {
            "questions" : serialize_generated_questions(questions)
        }
        # logger.debug(results)
        return JsonResponse(results, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def search(request, query):    
    try:
        questions = perform_search(query, near_text="")
        results = {
            "questions" : serialize_generated_questions(questions)
        }
        return JsonResponse(results)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ----------- html views

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