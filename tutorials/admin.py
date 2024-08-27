from django.contrib import admin

from .models import Questions_Inventory, User_Profile, Leaderboard, QuizLevel, Quiz, Questions_Category, Questions_Type
from .adminforms import QuestionsInventoryForm

import logging

logger = logging.getLogger(__name__)

class QuestionsInventoryAdmin(admin.ModelAdmin):
    form = QuestionsInventoryForm
    # Display fields from Questions_Inventory and related Questions_Type
    list_display = (
        'question_id', 
        'question_type', 
        'category',
        'question_category_desc',  # Foreign key field from Questions_Category
    )

    def question_category_desc(self, obj):
        # logger.info(obj)
        return obj.category.category_desc 

    # question_category_desc.admin_order_field = 'question_type__name'

    class Media:
        js = ('admin/js/custom_question_inventory.js',)

admin.site.register(Questions_Inventory, QuestionsInventoryAdmin)
admin.site.register(User_Profile)
admin.site.register(Questions_Type)
admin.site.register(Questions_Category)
admin.site.register(QuizLevel)
admin.site.register(Quiz)
admin.site.register(Leaderboard)