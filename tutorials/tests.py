from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from .models import Questions_Inventory, Questions_Type, QuizLevel, Quiz
from django.urls import reverse
import json
import uuid

class QuestionsInventoryTests(TestCase):

    def setUp(self):
        self.qIDType = uuid.uuid4()
        self.qID = uuid.uuid4()  
        self.quizLevelID = uuid.uuid4()
        self.quizID = uuid.uuid4()
        self.factory = RequestFactory()    
        self.questionType = Questions_Type.objects.create(question_type_id=self.qIDType,
                                                          question_type_desc="check")
        self.question = Questions_Inventory.objects.create(question_id=self.qID, 
                                                           answer=2, 
                                                           image_1="yes",
                                                           image_2="yes",
                                                           image_3="yes",
                                                           image_4="yes",
                                                           question_text="Good Morning",
                                                           question_type_id=self.qIDType)
        self.quizLevel = QuizLevel.objects.create(id=self.quizLevelID,
                                                  dificulty_rating="3", level_desc="Basic")
        self.quiz = Quiz.objects.create(id=self.quizID, 
                                        question_text="Text", image_1="ans 1", image_2="ans 2",
                                        image_3="ans 3", image_4="ans 4", answer=2,
                                        quiz_level_id= self.quizLevelID)

    def test_get_question_success(self):
        question = Questions_Inventory.objects.get(
            question_id=self.qID)
        # print(question.question_text)
        # q2 = question.getQuestion(id=self.qID)
        # print(question.getQuestion(id=self.qID))
        self.assertEqual(self.question.answer, 2)

# class QuestionsViewTests(TestCase):
    def test_question_response(self):
        url = reverse('question', args=[self.qID])
        # print(url)
        response = self.client.get(url)
        self.assertEqual(response['Content-Type'], 'application/json')
        # print(response.content)
        try:
            response_data = json.loads(response.content)
            self.assertEqual(response_data['answer'], 2)
        except json.JSONDecodeError as e:
            self.fail(f"JSON decode error: {e}")

    def test_questions_all_response(self):
        url = reverse('questions_all', args=[self.qIDType])
        print(url)
        response = self.client.get(url)
        self.assertEqual(response['Content-Type'], 'application/json')
        # print(response.content)
        try:
            response_data = json.loads(response.content)
            print(response_data)
            # self.assertEqual(response_data['answer'], 2)
        except json.JSONDecodeError as e:
            self.fail(f"JSON decode error: {e}")   

    def test_quiz_level(self):
        url = reverse("quiz_for_level", args=[self.quizLevelID])
        print(url)
        response = self.client.get(url)
        self.assertEqual(response['Content-Type'], 'application/json')  
        try:
            response_data = json.loads(response.content)
            print(response_data)
            # self.assertEqual(response_data['answer'], 2)
        except json.JSONDecodeError as e:
            self.fail(f"JSON decode error: {e}")              
