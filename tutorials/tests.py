from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from .models import Questions_Inventory, User_Profile, Leaderboard, UserQuiz
from .util import create_prompt
from .views import generate_questions
from django.urls import reverse
import json
import uuid

class QuestionsInventoryTests(TestCase):

    def setUp(self):
        # self.qIDType = uuid.uuid4()
        self.qCatergoryID = uuid.uuid4()
        self.qID = uuid.uuid4()  
        # self.quizLevelID = uuid.uuid4()
        self.quizID = uuid.uuid4()
        self.userID = uuid.uuid4()
        self.userID2 = uuid.uuid4()
        self.factory = RequestFactory()    
        # self.category = Questions_Category.objects.create(question_category_id=self.qCatergoryID,
        #                                                   category_desc='Navigate a City')
        # self.questionType = Questions_Type.objects.create(question_type_id=self.qIDType,
        #                                                   question_type_desc="check")
        self.question = Questions_Inventory.objects.create(question_id=self.qID, 
                                                           category='Navigate a City',
                                                           answer="yes no", 
                                                           options="yes",
                                                        #    option_2="no",
                                                        #    option_3="yes",
                                                        #    option_4="yes",
                                                           question_text="Good Morning",
                                                           instruction="instr",
                                                           difficulty_rating=2,
                                                           question_type='fill in the blank')
        self.question2 = Questions_Inventory.objects.create(question_id=uuid.uuid4(), 
                                                           category='Order in a restaurant',
                                                           answer="yes no", 
                                                           options="yes",
                                                        #    option_2="no",
                                                        #    option_3="yes",
                                                        #    option_4="yes",
                                                           question_text="Appetizer",
                                                           instruction="instr",
                                                           difficulty_rating=2,
                                                           question_type='fill in the blank')
        # self.quizLevel = QuizLevel.objects.create(id=self.quizLevelID,
        #                                           dificulty_rating="3", level_desc="Basic")
        # self.quiz = Quiz.objects.create(id=self.quizID, 
        #                                 question_text="Text", image_1="ans 1", image_2="ans 2",
        #                                 image_3="ans 3", image_4="ans 4", answer=2,
        #                                 quiz_level_id= self.quizLevelID)
        self.userProfile = User_Profile.objects.create(user_id=self.userID, 
                                               username="deepT",
                                               email="test.com")
        self.userProfile2 = User_Profile.objects.create(user_id=self.userID2, 
                                               username="deepTrouble",
                                               email="tester.com")
        # self.leaderboardID1 = uuid.uuid4()
        Leaderboard.objects.create(id=uuid.uuid4(), xp=20, user_id_id=self.userID)
        Leaderboard.objects.create(id=uuid.uuid4(), xp=25, user_id_id=self.userID2)

    def test_get_question_success(self):
        question = Questions_Inventory.objects.get(
            question_id=self.qID)
        self.assertEqual(question.answer, "yes no")

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
        url = reverse('questions_all', args=["Order in a restaurant"])
        response = self.client.get(url)
        self.assertEqual(response['Content-Type'], 'application/json')
        try:
            response_data = json.loads(response.content)
            print(response_data)
        except json.JSONDecodeError as e:
            self.fail(f"JSON decode error: {e}")   

    def test_quiz_level(self):
        url = reverse("quiz_for_level", args=[2])
        print(url)
        response = self.client.get(url)
        self.assertEqual(response['Content-Type'], 'application/json')  
        try:
            response_data = json.loads(response.content)
            # print(response_data)
        except json.JSONDecodeError as e:
            self.fail(f"JSON decode error: {e}")   

    def test_create_user(self):
        data = {
            'username': 'deedee',
            'email' : 'test@er.com'
        }
        url = reverse("create_user") 
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response['Content-Type'], 'application/json')  
        try:
            response_data = json.loads(response.content)
            print(response_data)
        except json.JSONDecodeError as e:
            self.fail(f"JSON decode error: {e}")   

    def test_submit_score(self):
        responses = [{'question_id': str(self.qID), 'isCorrect': False}] 
        data = {
            'user_id': str(self.userID),
            'totalScore' : 12,
            'responses' : responses
        }
        url = reverse("submit_score") 
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response['Content-Type'], 'application/json')  
        try:
            response_data = json.loads(response.content)
            print(response_data)
        except json.JSONDecodeError as e:
            self.fail(f"JSON decode error: {e}")    

    def test_show_leaderboard(self):
        url = reverse('show_leaderboard')
        print(url)
        response = self.client.get(url)
        self.assertEqual(response['Content-Type'], 'application/json')  
        try:
            response_data = json.loads(response.content)
            print(response_data)
        except json.JSONDecodeError as e:
            self.fail(f"JSON decode error: {e}")   

    # def test_prompt(self):
    #     questions = [
    #         {
    #             "category": "Order in a restaurant",
    #             "question_text": "For the first course, I'd like a pasta",
    #             "translation": "Per primo, vorrei una pasta",
    #             "difficulty": "3"
    #         },
    #         {
    #             "category": "Navigate a city",
    #             "question_text": "Is there a pharmacy nearby?",
    #             "translation": "C'è una farmacia nelle vicinanze?",
    #             "difficulty": "2"
    #         }
    #     ]
    #     prompt = create_prompt(questions, 'order food')
    #     print(prompt)

    # def test_genAI(self):
    #     UserQuiz.objects.create(question_id=self.qID, category='Navigate a City', correct_answer=False, user_id=self.userID)
    #     url = reverse('generate_questions', args=['Navigate a City', self.userID ])
    #     response = self.client.get(url)
    #     self.assertEqual(response['Content-Type'], 'application/json')
    #     try:
    #         response_data = json.loads(response.content)
    #         print('back in test')
    #         print(response_data)
    #     except json.JSONDecodeError as e:
    #         self.fail(f"JSON decode error: {e}")  
            

    # def test_search(self):
    #     url = reverse('search', args=['Buy hat'])
    #     response = self.client.get(url)
    #     self.assertEqual(response['Content-Type'], 'application/json')
    #     try:
    #         response_data = json.loads(response.content)
    #         print('back in test')
    #         print(response)
    #         # print(response_data[0])
    #     except json.JSONDecodeError as e:
    #         self.fail(f"JSON decode error: {e}")           



