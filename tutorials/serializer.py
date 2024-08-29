import logging


logger = logging.getLogger(__name__)

def serialize_users(users_mapping):
    serialized_users = []
    # users_mapping.forEach(userId, userData):
    for user_id, user_info in users_mapping.items():
        # user_info = entry.value; 
        logger.info(user_info)
        serialized_users.append({
            'id': user_id,
            # 'bio': user_info['bio'],
            'username': user_info['username'],
            'profile_pic':user_info['profile_pic'],
        })
    return serialized_users 

def serialize_quiz(questions):
    serialize_quiz = []
    logger.info(len(questions))
    for question in questions:
        serialize_quiz.append({
            'id': question.id,
            'text': question.question_text,
            'image_1': question.image_1,
            'image_2': question.image_2,
            'image_3': question.image_3,
            'image_4': question.image_4,
            'answer' : question.answer,
            'quiz_level' : question.quiz_level_id
            # 'quiz_level_details' : {
            #     'id': str(question.quiz_level_id.id),  # Convert UUID to string
            #     'level_desc': question.quiz_level_id.level_desc,
            #     'difficulty_rating': question.quiz_level_id.dificulty_rating,
            # }
        })
    logger.debug(serialize_quiz)    
    return serialize_quiz

def serialize_leaderboard(leaderboard):
    serialize_leaderboard = []
    for position in leaderboard:
        serialize_leaderboard.append({
            'xp' : position.xp,
            'user_id' : str(position.user_id.user_id),
            'username' : position.user_id.username
        })
    return serialize_leaderboard    

def serialize_generated_questions(questions):
    serialize_questions = []
    for question in questions:
        serialize_questions.append({
            'question': question['question'],
            'text': question['question'],
            'instruction': question.get('instruction', ""),
            'difficulty_rating': question.get('difficulty_rating', ""),
            'category' : question.get('category', ""),
            'answer' : question['answer'],
        }) 
    return serialize_questions

def serialize_questions(questions):
    serialize_questions = []
    logger.info(len(questions))
    for question in questions:
        serialize_questions.append({
            'question_id': question.question_id,
            'text': question.question_text,
            'option_1': question.option_1,
            'option_2': question.option_2,
            'option_3': question.option_3,
            'option_4': question.option_4,
            'difficulty_rating': question.difficulty_rating,
            'question_type': question.question_type,
            'answer' : question.answer,
            'file_path' : question.file_path,
            'category_id' : question.category_id
        })
    logger.debug(serialize_questions)    
    return serialize_questions


def serialize_user_dict(users_dict):
    serialize_users_dict = {}
    for user_id, user_info in users_dict.items():
        logger.info(user_info)
        serialize_users_dict[str(user_id)] = {
            'username': user_info['username'],
            'profile_pic': user_info['profile_pic'],
        }
    return serialize_users_dict


