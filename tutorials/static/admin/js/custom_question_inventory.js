document.addEventListener('DOMContentLoaded', function() {
    const questionTypeField = document.getElementById('id_question_type');
    const questionTypeDescField = document.getElementById('id_question_type_desc');

    if (questionTypeField) {
        questionTypeField.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            
            if (selectedOption.value) {
                fetch(`/admin/get-question-type-desc/${selectedOption.value}/`)
                    .then(response => response.json())
                    .then(data => {
                        questionTypeDescField.value = data.question_type_desc;
                    })
                    .catch(error => console.error('Error fetching question type description:', error));
            } else {
                questionTypeDescField.value = ''; 
            }
        });
    }
});
