from django.core.management.base import BaseCommand
from ...views import generate_questions, questionsForCategory

class Command(BaseCommand):
    help = 'Add to database'

    def handle(self, *args, **kwargs):
        # generate_questions(request="", category="Navigate a city")   
        questionsForCategory(request="", query="Talk about family and friends")     
        self.stdout.write(self.style.SUCCESS('Successfully ran the method'))
        # self.stdout.write(str(result)) 
