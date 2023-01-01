import random

QUES1 = ["What is money to you?",
         "What do you try to do to make the world a little better?",
         "What activity do you do where your mind wanders in thoughts the most?",
         "What have you recently found to be ironic?",
         "If you had to name one thing that makes you stand out from others,What would that be?",
         "If you were handed $500 at this moment, how would you spend it?",
         "Is there any place that you have no desire to visit? Why?",
         "Have you ever been punished for something you didn't do?",
         "On any given day, What do you think you spend the most time doing?",
         "If you could choose the way you became a hero, What would the circumstances be?",
         "Have you ever had to complain to management? Why?",
         "Is there a personality trait that you'd like to adopt from one of your friends?",
         "What sound will instantly melt your heart?",
         "Is there anything that makes you far angrier than it should?",
         "What's the worst piece of advice you ever got from someone?",
         "What situation is sure to make you cry?",
         "What doesn't exist, but should?",
         "What is the most selfish thing you do that you're okay with?",
         "What's something about you today that the old you would find surprising?",
         "What's something interesting about you that few people know?",
         "Have you ever let someone else get punished for something you did?",
         "Which of your past teachers would you like to sit down with and talk to today?",
         "Do you have any secret hobbies?",
         "In emergency situations, how do you react?",
         "What's something that you believe you'll never be able to do well?",
         "What was a situation where you literally did a doubletake?",
         "What recent situation was nearly a disaster, but you were able to prevent it?",
         "What thing have you been procrastinating about that you will begin doing today?",
         "How often do you find yourself daydreaming?",
         "What recent event have you seen that restored your faith in humankind?",
         "What is the next skill that you'd like to learn really well?",
         "What did you recently learn the hard way?",
         "Do you have a favorite brand?",
         "How far back can you trace your family tree?",
         "Have you ever done something embarrassing around a former crush?",
         "What app or website completely changed your life?",
         "What do you see happening in your future?",
         "Are you currently going through any type of phase?",
         "What's the last thing that you broke and how did it happen?",
         "If everyone here was a color, What color would each person be?",
         "What food have you never tried?",
         "If you were to devote your life to art, What type of art would that be?",
         "What's stopping you?",
         "If you could play a prank on any historical figure, who would you pick and What prank would you do?",
         "What types of things do you doodle?",
         "Where's the next place you want to visit?",
         "What's a situation when you look back you should have gone ahead and done it?",
         "What's your favorite form of entertainment?",
         "If each person had a warning label, What would yours say?",
         "What's your most recent passion?",
         "What song currently speaks to you the most?",
         "What's your biggest first world problem?",
         "Have you ever done something embarrassing around a former crush?",
         "What do you consider the best decision you've made thus far in your life?",
         "What is your current favorite TV show? What was it 5 years ago?",
         "If it's raining outside, what activity do you most want to do?",
         "What's the biggest wager you've ever made?",
         "What is the strangest way you met one of your friends?",
         "Would the world be better or worse if superheroes existed?",
         "What's a food you vow never to eat?",
         "If you could change the length of each day to make it perfect for you, how many hours would it be?",
         "If you had the choice to go back in time or into the future, which would you choose?",
         "If you knew you could live forever, how would you spend your days differently?",
         "What's the story behind why you replaced the last phone you had?",
         "What food combination do you eat that makes others cringe?",
         "How do you usually react if you receive bad service?",
         "How do you think your reality differs from others you know?",
         "What's your favorite room in your house and why?",
         "Did you ever have a huge rival? Was the rivalry friendly or fierce?",
         "What's your favorite ritual?",
         "What recent situation was nearly a disaster, but you were able to prevent it?",
         "What's your famous person story?",
         "If you had to walk away from one technology in your life, what would it be?",
         "What's the most difficult thing that you still do each day?",
         "On any given day, what do you think you spend the most time doing?",
         "Who was the last person you made happy and what did you do to do it?",
         "What's something in your fridge right now that should probably be thrown out?",
         "What weird thing do you do when nobody else is around?",
         "What's your opinion on tipping?",
         "How do you make decisions?"
         ]


def make_Question():
    questions = []
    num_questions = random.randint(1, 10)

    for _ in range(0, num_questions):
        questions.append(random.choice(QUES1))
    return questions


def insert_survey_questions(cursor, survey_id):
    surveyQuestions = make_Question()
    for question in surveyQuestions:
        cursor.execute("""INSERT INTO mutable.survey_questions (survey_id, question) VALUES (%s, %s)""",
                       (survey_id, question))