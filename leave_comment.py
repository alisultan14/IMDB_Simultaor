import random

InsertComment = """
                    INSERT INTO mutable.comments(movie_id, review_author_id, user_id, comment)
                    VALUES (%s, %s, %s, %s);
                    """
Sentences = [
    "Greetings from the real universe.",
    "Today is the day I'll finally know what brick tastes like.",
    "Jenny made the announcement that her baby was an alien.",
    "She had that tint of craziness in her soul that made her believe she could actually make a difference.",
    "The crowd yells and screams for more memes.",
    "The body piercing didn't go exactly as he expected.",
    "This made him feel like an old-style rootbeer float smells.",
    "I received a heavy fine but it failed to crush my spirit.",
    "I ate a sock because people on the Internet told me to.",
    "The view from the lighthouse excited even the most seasoned traveler.",
    "Martha came to the conclusion that shake weights are a great gift for any occasion.",
    "She did not cheat on the test, for it was not the right thing to do.",
    "For oil spots on the floor, nothing beats parking a motorbike in the lounge.",
    "Mary realized if her calculator had a history, it would be more embarrassing than her computer browser history.",
    "The sight of his goatee made me want to run and hide under my sister-in-law's bed.",
    "They say that dogs are man's best friend, but this cat was setting out to sabotage that theory.",
    "The glacier came alive as the climbers hiked closer.",
    "He set out for a short walk, but now all he could see were mangroves and water were for miles.",
    "He walked into the basement with the horror movie from the night before playing in his head.",
    "On each full moon,He decided to fake his disappearance to avoid jail.",
    "You're good at English when you know the difference between a man eating chicken and a man-eating chicken.",
    "It dawned on her that others could make her happier, but only she could make herself happy.",
    "She was sad to hear that fireflies are facing extinction due to artificial light, habitat loss, and pesticides.",
    "Just go ahead and press that button.",
    "Check back tomorrow; I will see if the book has arrived.",
    "Eating eggs on Thursday for choir practice was recommended.",
    "All they could see was the blue water surrounding their sailboat.",
    "The near-death experience brought new ideas to light.",
    "He never understood why what, when, and where left out who.",
    "He learned the hardest lesson of his life and had the scars, both physical and mental, to prove it.",
    "Best friends are like old tomatoes and shoelaces.",
    "I hear that Nancy is very pretty.",
    "The elderly neighborhood became enraged over the coyotes who had been blamed for the poodle’s disappearance.",
    "She folded her handkerchief neatly.",
    "He picked up trash in his spare time to dump in his neighbor's yard.",
    "Kevin embraced his ability to be at the wrong place at the wrong time.",
    "The child’s favorite Christmas gift was the large box her father’s lawnmower came in.",
    "The door slammed on the watermelon.",
    "She could hear him in the shower singing with a joy she hoped he'd retain after she delivered the news.",
    "There was no ice cream in the freezer, nor did they have money to go to the store.",
    "Shakespeare was a famous 17th-century diesel mechanic.",
    "I'm not a party animal, but I do like animal parties.",
    "You've been eyeing me all day and waiting for your move like a lion stalking a gazelle in a savannah.",
    "It's important to remember to be aware of rampaging grizzly bears.",
    "Today I dressed my unicorn in preparation for the race.",
    "His confidence would have bee admirable if it wasn't for his stupidity.",
    "It would have been a better night if the guys next to us weren't in the splash zone.",
    "The door swung open to reveal pink giraffes and red elephants.",
    "Dan ate the clouds like cotton candy.",
    "She thought there'd be sufficient time if she hid her watch.",
    "The furnace repairman indicated the heating system was acting as an air conditioner.",
    "As the years pass by, we all know owners look more and more like their dogs.",
    "In that instant, everything changed.",
    "His son quipped that power bars were nothing more than adult candy bars.",
    "It's a skateboarding penguin with a sunhat!",
    "You're unsure whether or not to trust him, but very thankful that you wore a turtle neck.",
    "The doll spun around in circles in hopes of coming alive.",
    "Honestly, I didn't care much for the first season, so I didn't bother with the second.",
    "Gwen had her best sleep ever on her new bed of nails.",
    "She was the type of girl that always burnt sugar to show she cared.",
    "Getting up at dawn is for the birds.",
    "They called out her name time and again, but were met with nothing but silence.",
    "They say that dogs are man's best friend, but this cat was setting out to sabotage that theory.",
    "The water flowing down the river didn’t look that powerful from the car.",
    "I'll have you know I've written over fifty novels.",
    "A purple pig and a green donkey flew a kite in the middle of the night and ended up sunburnt.",
    "The irony of the situation wasn't lost on anyone in the room.",
    "All you need to do is pick up the pen and begin.",
    "At that moment he wasn't listening to music, he was living an experience.",
    "His mind was blown that there was nothing in space except space itself.",
    "The tart lemonade quenched her thirst, but not her longing.",
    "They ran around the corner to find that they had traveled back in time.",
    "I like to leave work after my eight-hour tea-break.",
    "It took me too long to realize that the ceiling hadn't been painted to look like the sky.",
    "The shooter says goodbye to his love.",
    "Siri became confused when we reused to follow her directions.",
    "Poison ivy grew through the fence they said was impenetrable.",
    "The Guinea fowl flies through the air with all the grace of a turtle.",
    "She hadn't had her cup of coffee, and that made things all the worse.",
    "There's a message for you if you look up.",
    "He excelled at firing people nicely.",
    "The best part of marriage is animal crackers with peanut butter.",
    "My uncle's favorite pastime was building cars out of noodles.",
    "Jeanne wished she has chosen the red button.",
    "Excitement replaced fear until the final moment.",
    "His get rich quick scheme was to grow a cactus farm.",
    "The mysterious diary records the voice.",
    "The underground bunker was filled with chips and candy.",
    "Jason lived his life by the motto,Anything worth doing is worth doing poorly.",
    "It was her first experience training a rainbow unicorn.",
    "Jenny made the announcement that her baby was an alien.",
    "Instead of a bachelorette party.",
    "Lightning Paradise was the local hangout joint where the group usually ended up spending the night.",
    "Garlic ice-cream was her favorite.",
    "It must be five o'clock somewhere.",
    "The fog was so dense even a laser decided it wasn't worth the effort.",
    "Edith could decide if she should paint her teeth or brush her nails.",
    "Boulders lined the side of the road foretelling what could come next.",
    "I would be delighted if the sea were full of cucumber juice."
]


def make_comment(sentenceNumber):
    comment = []
    for sentence in range(0, sentenceNumber):
        comment.append(random.choice(Sentences))

    return comment


def insert_comment(conn, movie_id, review_author_id, user_id):
    cursor = conn.cursor()
    sentence_number = random.randint(1, 3)
    comment = ' '.join(make_comment(sentence_number))
    cursor.execute(InsertComment, [movie_id, review_author_id, user_id, comment])
    dismiss_review_invite(conn, movie_id, review_author_id, user_id)
    conn.commit()
    cursor.close()


def make_fullcomment(conn, user_id):
    result = choose_randomHeadCommenter(conn)
    if result is not None:
        (movie_id, review_author_id) = result
        insert_comment(conn, movie_id, review_author_id, user_id)
    return True


SelectAllCommentThreads = """SELECT movie_id, creator_id
                    FROM mutable.reviews
                    ORDER BY RANDOM() LIMIT 1;
                """


def choose_randomHeadCommenter(conn):
    cursor = conn.cursor()
    cursor.execute(SelectAllCommentThreads)
    result = cursor.fetchone()
    if result is None:
        return None

    (movie_id, author_id) = result
    cursor.close()
    return movie_id, author_id


def dismiss_review_invite(conn, movie_id, creator_id, user_id):
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE mutable.review_invites
    SET dismissed = TRUE
    WHERE movie_id = %s AND creator_id = %s AND invitee_id = %s;
    """, (movie_id, creator_id, user_id))

    cursor.close()
