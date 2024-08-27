from django import forms
from .models import Questions_Inventory, User_Profile, Questions_Type

class QuestionsInventoryForm(forms.ModelForm):
    # Include related model fields in the form
    question_type_desc = forms.CharField(label='Question Type Desc', max_length=100, required=False, disabled=True)

    class Meta:
        model = Questions_Inventory
        fields = ['question_text', 'question_type_desc', 'question_type', 'image_1', 'image_2', 'image_3', 'image_4', 'answer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            if self.instance.question_type_id:
                self.fields['question_type_desc'].initial = self.instance.question_type.question_type_desc

    def save(self, commit=True):
        # Save the primary model (Questions_Inventory)
        instance = super().save(commit=False)

        if instance.question_type_id:
            instance.question_type.question_type_desc = self.cleaned_data['question_type_desc']
            instance.question_type.save()
        
        if commit:
            instance.save()

        return instance
