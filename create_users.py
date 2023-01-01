import random

# 100 first names x 100 last names --> 10k possible unique names
FIRST_NAMES = ["Lorcan", "Ibrahim", "Nasir", "Dottie", "Aydin", "Yasemin", "Elowen", "Grover", "Alexis", "Gene",
               "Roisin", "Arisha", "Jia", "Kiyan", "Abbas", "Anushka", "Lexie", "Dave", "Darsh", "Neave", "Jedd",
               "Onur", "Mahdi", "Misha", "Hector", "Arlo", "Gaia", "King", "Umer", "Jacqueline", "Catherine", "Neo",
               "Hannah", "Tobi", "Mamie", "Kayley", "Alan", "Millie-Mae", "Konrad", "Kyron", "Kunal", "Dionne",
               "Regina", "Tomasz", "Asif", "Bradley", "Naya", "Keeleigh", "Garin", "Anwar", "Kira", "Maira", "Kacey",
               "Bruno", "Nettie", "Duncan", "Weronika", "Abigail", "Harri", "Jade", "Aston", "Mallory", "Pauline",
               "Sia", "Arlene", "Frankie", "Coby", "Cayson", "Efe", "Hari", "Tarun", "Kia", "Taran", "Jenson",
               "Geraint", "Libbie", "Rhiana", "Jemma", "Kelsi", "Bonnie", "Dimitri", "Martin", "Rosie", "Azra", "Vera",
               "Harlen", "Cobie", "Robin", "Aliya", "Athena", "Tamanna", "Kacper", "Gurpreet", "Murphy", "Zaara",
               "Freddie", "Estelle", "Abid", "Darcie", "Clarence"]
LAST_NAMES = ["Middleton", "Manning", "Dillon", "Donald", "Shannon", "Short", "Phillips", "Ramsey", "Branch", "Gamble",
              "Berry", "Whitfield", "Reid", "Correa", "Leigh", "Wyatt", "Elliott", "Ibarra", "Winter", "Braun",
              "Fleming", "Sandoval", "Barron", "Huynh", "Hogg", "Humphreys", "Archer", "O'Moore", "Mcdougall",
              "Walters", "Wilder", "John", "Walker", "Miller", "Farley", "Liu", "Hunt", "Mays", "Hartman", "Herbert",
              "Shea", "Neville", "Moore", "Schroeder", "Wallace", "Osborn", "Caldwell", "Stott", "Hardin", "Cobb",
              "Brooks", "Edwards", "Harding", "Horn", "Cowan", "Rogers", "Morrow", "Cummings", "Jennings", "Davey",
              "Power", "Hook", "Sears", "Robins", "Johnston", "Livingston", "Greenwood", "Lennon", "Bennett", "Preece",
              "Bautista", "Meyers", "Bush", "Bone", "Jensen", "Hurley", "Healy", "Blackburn", "Castaneda", "Kearney",
              "Ireland", "Whiteley", "Fountain", "Edge", "Galloway", "Preston", "Gonzales", "O'Quinn", "Fitzgerald",
              "Griffin", "Kim", "Holden", "East", "Fletcher", "Harvey", "Whitmore", "Robson", "Winters", "Kinney",
              "Pruitt"]


def insert_users(conn, num_users):
    users = make_users(num_users)

    cursor = conn.cursor()
    cursor.executemany("""
    INSERT INTO mutable.users (first_name, last_name, is_critic, is_hired) VALUES (%s, %s, %s, %s);
    """, users)
    conn.commit()


def make_user():
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    is_hired = bool(random.getrandbits(1))
    is_critic = is_hired or bool(random.getrandbits(1))
    return first_name, last_name, is_critic, is_hired


def make_users(num_users):
    users = []

    for index in range(num_users):
        users.append(make_user())

    return users
