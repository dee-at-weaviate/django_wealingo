
from django.template import Context
from django.template.loader import get_template

def create_prompt(questions, category, query):
    template = get_template('prompts/generate_prompt.html')
    context = {
        'questions': questions,
        'category':category,
        'query': query
    }
    rendered_output = template.render(context)
    return rendered_output