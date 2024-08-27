from django.contrib import admin

from .models import Questions_Inventory, User_Profile, Questions_Type, QuizLevel, Quiz
from .adminforms import QuestionsInventoryForm


class QuestionsInventoryAdmin(admin.ModelAdmin):
    form = QuestionsInventoryForm
    # Display fields from Questions_Inventory and related Questions_Type
    list_display = (
        'question_id', 
        'question_type', 
        'question_type_desc',  # Foreign key field from Questions_Type
    )

    def question_type_desc(self, obj):
        return obj.question_type.question_type_desc 

    question_type_desc.admin_order_field = 'question_type__name'

    class Media:
        js = ('admin/js/custom_question_inventory.js',)

admin.site.register(Questions_Inventory, QuestionsInventoryAdmin)
admin.site.register(User_Profile)
admin.site.register(Questions_Type)
admin.site.register(QuizLevel)
admin.site.register(Quiz)