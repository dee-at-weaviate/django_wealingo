from django import forms
from .models import Questions_Inventory, User_Profile

class QuestionsInventoryForm(forms.ModelForm):
    # Include related model fields in the form
    question_type_desc = forms.CharField(label='Category Type Desc', max_length=500, required=False, disabled=True)

    class Meta:
        model = Questions_Inventory
        fields = ['question_text', 'category', 'options', 'answer', 'difficulty_rating', 'file_path']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            if self.instance.category_id:
                self.fields['category_desc'].initial = self.instance.category.category_desc

    def save(self, commit=True):
        # Save the primary model (Questions_Inventory)
        instance = super().save(commit=False)

        # if instance.category_id:
        #     instance.category.category_desc = self.cleaned_data['question_type_desc']
        #     instance.category.save() 
        
        if commit:
            instance.save()

        return instance
