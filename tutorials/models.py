from django.db import models
import uuid

class User_Profile(models.Model):
    user_id = models.UUIDField(
        primary_key=True,  
        default=uuid.uuid4,  
        editable=False  
    )
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=100)

class Questions_Type(models.Model):
    # question_type_id = models.UUIDField(primary_key=True)
    question_type_id = models.UUIDField(
        primary_key=True,  
        default=uuid.uuid4,  
        editable=False  
    )
    question_type_desc = models.CharField(max_length=100)
    type_image = models.ImageField(upload_to="questiontypes")
    image_url = models.CharField(max_length=100)

class Questions_Inventory(models.Model):
    question_id = models.UUIDField(
        primary_key=True,  
        default=uuid.uuid4,  
        editable=False  
    )
    question_type = models.ForeignKey(Questions_Type, on_delete=models.DO_NOTHING)
    question_text = models.CharField(max_length=200)
    image_1 = models.CharField(max_length=100)
    image_2 = models.CharField(max_length=100)
    image_3 = models.CharField(max_length=100)
    image_4 = models.CharField(max_length=100)
    answer = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def getQuestion(self, id):
        return self.question_id

class User_Questions(models.Model):
    user_question_id = models.UUIDField(
        primary_key=True,  
        default=uuid.uuid4,  
        editable=False  
    )
    question_id = models.ForeignKey(Questions_Inventory, on_delete=models.DO_NOTHING)
    chosen_answer = models.IntegerField()
    actual_answer = models.IntegerField()

class QuizLevel(models.Model):
    id = models.UUIDField(
        primary_key=True,  
        default=uuid.uuid4,  
        editable=False  
    )
    level_desc = models.CharField(max_length=100)
    dificulty_rating = models.IntegerField()

class Quiz(models.Model):
    id = models.UUIDField(
        primary_key=True,  
        default=uuid.uuid4,  
        editable=False  
    )
    quiz_level = models.ForeignKey(QuizLevel, on_delete=models.DO_NOTHING)
    question_text = models.CharField(max_length=200)
    image_1 = models.CharField(max_length=100)
    image_2 = models.CharField(max_length=100)
    image_3 = models.CharField(max_length=100)
    image_4 = models.CharField(max_length=100)
    answer = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserQuiz(models.Model):
    id = models.UUIDField(
        primary_key=True,  
        default=uuid.uuid4,  
        editable=False  
    )
    quiz_id = models.ForeignKey(Quiz, on_delete=models.DO_NOTHING)
    points = models.IntegerField()
    attempts = models.IntegerField()   

class Leaderboard(models.Model):
    id = models.UUIDField(
        primary_key=True,  
        default=uuid.uuid4,  
        editable=False  
    )
    user_id=models.ForeignKey(User_Profile, on_delete=models.DO_NOTHING)
    xp=models.IntegerField()