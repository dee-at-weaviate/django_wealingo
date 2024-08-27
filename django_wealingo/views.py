from django.http import JsonResponse
from tutorials.models import Questions_Type
import logging

logger = logging.getLogger(__name__)

def get_question_type_desc(request, question_type_id):
    logger.debug(request)
    try:
        question_type = Questions_Type.objects.get(pk=question_type_id)
        data = {
            'question_type_desc': question_type.question_type_desc
        }
    except Questions_Type.DoesNotExist:
        data = {
            'question_type_desc': ''
        }
    return JsonResponse(data)