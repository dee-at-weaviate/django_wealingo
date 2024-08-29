
from django.template import Context
from django.template.loader import get_template

def create_prompt(questions, query):
    template = get_template('prompts/generate_prompt.html')
    context = {
        'questions': questions,
        'query':query
    }
    rendered_output = template.render(context)
    return rendered_output