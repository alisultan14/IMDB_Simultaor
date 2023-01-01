import random

# SQL Statement for the insertion of Actor news into the actor_news table

import view_actor
import view_director

InsertComment_Actor = """
                  INSERT INTO mutable.actor_news (actor_id, title, clicks)
                  VALUES (%s, %s, %s);
                  """
# SQL Statement for the insertion of Director news into the actor_news table
InsertComment_Director = """INSERT INTO mutable.director_news (director_id, title,clicks)
VALUES (%s, %s, %s);
"""
# names that are used to name an article - 296 in total
ARTICLE_NAMES = ["The Untold Secret To Mastering ??? In Just 3 Days", "How To Become Better With ??? In 10 Minutes",
                 "Your Key To Success: ???",
                 "How To Make Your Product Stand Out With ???",
                 "Sexy ???",
                 "Using 7 ??? Strategies Like The Pros",
                 "??? Is Essential For Your Success. Read This To Find Out Why",
                 "In 10 Minutes, I'll Give You The Truth About ???",
                 "Do ??? Better Than Barack Obama",
                 "Wondering How To Make Your ??? Rock? Read This!",
                 "Find Out How I Cured My ??? In 2 Days",
                 "Rules Not To Follow About ???",
                 "??? Is Bound To Make An Impact In Your Business",
                 "You Can Thank Us Later - 3 Reasons To Stop Thinking About ???",
                 "The Secret Of ???",
                 "Can You Really Find ??? (on the Web)",
                 "10 Funny ??? Quotes",
                 "??? : An Incredibly Easy Method That Works For All",
                 "Get Better ??? Results By Following 3 Simple Steps",
                 "Cracking The ??? Code",
                 "Make Your ??? A Reality",
                 "How ??? Made Me A Better Salesperson",
                 "The Ultimate Secret Of ???",
                 "Open The Gates For ??? By Using These Simple Tips",
                 "5 Secrets: How To Use ??? To Create A Successful Business(Product)",
                 "Believe In Your ??? Skills But Never Stop Improving",
                 "The Number One Reason You Should (Do) ???",
                 "SuperEasy Ways To Learn Everything About ???",
                 "Why Everything You Know About ??? Is A Lie",
                 "How I Improved My ??? In One Easy Lesson",
                 "Warning: These 9 Mistakes Will Destroy Your ???",
                 "5 Incredibly Useful ??? Tips For Small Businesses",
                 "How To Earn $398/Day Using ???",
                 "Improve(Increase) Your ??? In 3 Days",
                 "Should Fixing ??? Take 60 Steps?",
                 "How To Make More ??? By Doing Less",
                 "Why ??? Succeeds",
                 "Learn Exactly How We Made ??? Last Month",
                 "3 Ways Twitter Destroyed My ??? Without Me Noticing",
                 "The Ultimate Guide To ???",
                 "??? An Incredibly Easy Method That Works For All",
                 "??? Expert Interview",
                 "Why ??? Is No Friend To Small Business",
                 "Find Out Now, What Should You Do For Fast ???",
                 "Are You Making These ??? Mistakes",
                 "2 Ways You Can Use ??? To Become Irresistible To Customers",
                 "??? And The Chuck Norris Effect",
                 "How To Make Your ??? Look Like A Million Bucks",
                 "Apply These 5 Secret Techniques To Improve ???",
                 "15 Tips For ??? Success",
                 "??? : The Samurai Way",
                 "Essential ??? Smartphone Apps",
                 "The Next 3 Things To Immediately Do About ???",
                 "If You Want To Be A Winner, Change Your ??? Philosophy Now!",
                 "Being A Star In Your Industry Is A Matter Of ???",
                 "How To Find The Right ??? For Your Specific Product(Service).",
                 "The ??? That Wins Customers",
                 "5 Brilliant Ways To Teach Your Audience About ???",
                 "3 Things Everyone Knows About ??? That You Don't",
                 "How To Turn Your ??? From Zero To Hero",
                 "Top 25 Quotes On ???",
                 "Top 10 Tips With ???",
                 "Fast-Track Your ???",
                 "Little Known Ways to ???",
                 "5 Romantic ??? Ideas",
                 "101 Ideas For ???",
                 "What Make ??? Don't Want You To Know",
                 "What You Should Have Asked Your Teachers About ???",
                 "How To Win Clients And Influence Markets with ???",
                 "Picture Your ??? On Top. Read This And Make It So",
                 "10 Tips That Will Make You Influential In ???",
                 "How To Teach ??? Like A Pro",
                 "Little Known Ways To Rid Yourself Of ???",
                 "??? Strategies For Beginners",
                 "What Everyone Ought To Know About ???",
                 "??? And Love - How They Are The Same",
                 "22 Tips To Start Building A ??? You Always Wanted",
                 "5 Things To Do Immediately About ???",
                 "A Surprising Tool To Help You ???",
                 "The Secret of ???",
                 "This Study Will Perfect Your ??? : Read Or Miss Out",
                 "Top 10 Tips To Grow Your ???",
                 "3 Easy Ways To Make ??? Faster",
                 "What Can You Do About ??? Right Now",
                 "How To Deal With(A) Very Bad ???",
                 "Fall In Love With ???",
                 "Remarkable Website ??? Will Help You Get There",
                 "5 Reasons ??? Is A Waste Of Time",
                 "The Truth Is You Are Not The Only Person Concerned About ???",
                 "3 Ways To Have (A) More Appealing ???    Take 10 Minutes to Get Started With ???",
                 "Want A Thriving Business? Focus On ??? !",
                 "These 5 Simple ??? Tricks Will Pump Up Your Sales Almost Instantly",
                 "Read This Controversial Article And Find Out More About ???",
                 "??? : Do You Really Need It? This Will Help You Decide!",
                 "At Last, The Secret To ??? Is Revealed",
                 "Now You Can Have The ??? Of Your Dreams Cheaper/Faster Than You Ever Imagined",
                 "Learn Exactly How I Improved ??? In 2 Days",
                 "The Hidden Mystery Behind ???",
                 "Secrets To ???  Even In This Down Economy",
                 "Why Some People Almost Always Make/Save Money With ???",
                 "7 Rules About ??? Meant To Be Broken",
                 "3 Ways You Can Reinvent ??? Without Looking Like An Amateur",
                 "Never Suffer From ??? Again",
                 "Why Most People Will Never Be Great At ???",
                 "13 Myths About ???",
                 "How To Win Friends And Influence People with ???",
                 "The Untapped Gold Mine Of ??? That Virtually No One Knows About",
                 "3 Simple Tips For Using ??? To Get Ahead Your Competiti",
                 "The A  Z Guide Of ???",
                 "5 Problems Everyone Has With ??? How To Solved Them",
                 "Are You Embarrassed By Your ??? Skills? Here's What To D",
                 "If ??? Is So Terrible, Why Don't Statistics Show It?",
                 "I Don't Want To Spend This Much Time On ??? . How About You?",
                 "3 Ways To Master ??? Without Breaking A Sweat",
                 "Savvy|Smart|Sexy People Do ??? :)",
                 "What Everyone Must Know About ???",
                 "Where Is The Best ????",
                 "Beware The ??? Scam",
                 "Proof That ??? Really Works",
                 "Avoid The Top 10 ??? Mistakes",
                 "Death, ??? And Taxes",
                 "How To Win Buyers And Influence Sales with ???",
                 "The Secrets To ???",
                 "A Guide To ??? At Any Age",
                 "How To Learn ???",
                 "Find A Quick Way To ???",
                 "??? Adventures",
                 "Here Is A Quick Cure For ???",
                 "The Lazy Man's Guide To ???",
                 "Listen To Your Customers. They Will Tell You All About ???",
                 "??? Is Crucial To Your Business. Learn Why!",
                 "How To Take The Headache Out Of ???",
                 "14 Days To A Better ???",
                 "How You Can (Do) ??? Almost Instantly",
                 "5 Ways ??? Will Help You Get More Business",
                 "Get The Most Out of ??? and Facebook",
                 "Who Else Wants To Know The Mystery Behind ???",
                 "Need More Time? Read These Tips To Eliminate ???",
                 "Take The Stress Out Of ???",
                 "How To Buy (A) ??? On A Tight Budget",
                 "Never Changing ??? Will Eventually Destroy You",
                 "How To Turn ??? Into Success",
                 "The Quickest & Easiest Way To ???",
                 "Here's A Quick Way To Solve A Problem with ???",
                 "Proof That ??? Is Exactly What You Are Looking For",
                 "What Is ??? and How Does It Work?",
                 "??? Iphone Apps",
                 "Have You Heard? ??? Is Your Best Bet To Grow",
                 "10 Unforgivable Sins Of ???",
                 "OMG! The Best ??? Ever!",
                 "Don't Be Fooled By ???",
                 "Never Lose Your ??? Again",
                 "How To Make Your ??? Look Amazing In 5 Days",
                 "Master (Your) ??? in 5 Minutes A Day",
                 "How To Start A Business With ???",
                 "Everything You Wanted to Know About ??? and Were Too Embarrassed to Ask",
                 "7 Ways To Keep Your ??? Growing Without Burning The Midnight Oil",
                 "Old School ???",
                 "??? - So Simple Even Your Kids Can Do It",
                 "Guaranteed No Stress ???",
                 "Does ??? Sometimes Make You Feel Stupid",
                 "How To Sell ???",
                 "Best Make ??? You Will Read This Year (in 2015)",
                 "How To Improve At ??? In 60 Minutes",
                 "The Best Way To ???",
                 "4 Ways You Can Grow Your Creativity Using ???",
                 "What Your Customers Really Think About Your ???",
                 "Congratulations! Your ??? Is (Are) About To Stop Being Relevant",
                 "Quick and Easy Fix For Your ???",
                 "Sick And Tired Of Doing ??? The Old Way? Read This",
                 "The Biggest Lie In ???",
                 "??? Smackdown!",
                 "Get Rid of ??? Once and For All",
                 "Turn Your ??? Into A High Performing Machine",
                 "Why You Really Need (A) ???",
                 "2 Things You Must Know About ???",
                 "5 Ways You Can Get More ??? While Spending Less",
                 "10 Things You Have In Common With ???",
                 "Ho To (Do) ??? Without Leaving Your Office(House).",
                 "The ??? Mystery Revealed",
                 "How You Can (Do) ??? In 24 Hours Or Less For Free",
                 "Now You Can Buy An App That is Really Made For ???",
                 "Here Is A Method That Is Helping ???",
                 "11 Methods Of ??? Domination",
                 "Marriage And ??? Have More In Common Than You Think",
                 "Stop Wasting Time And Start ???",
                 "Who Else Wants To Be Successful With ???",
                 "Learn How To Start ???",
                 "Revolutionize Your ??? With These Easy-peasy Tips",
                 "No More Mistakes With ???",
                 "9 Ridiculous Rules About ???",
                 "Want To Step Up Your ???? You Need To Read This First",
                 "3 Mistakes In ??? That Make You Look Dumb",
                 "Everything You Wanted to Know About ??? and Were Afraid To Ask",
                 "Here Is What You Should Do For Your ???",
                 "??? Made Simple Even Your Kids Can Do It",
                 "5 Brilliant Ways To Use ???",
                 "10 Secret Things You Didn't Know About ???",
                 "The Ultimate Deal On ???",
                 "7 and a Half Very Simple Things You Can Do To Save ???",
                 "Now You Can Have Your ??? Done Safely",
                 "How To Start ??? With Less Than $100",
                 "10 Best Practices For ???",
                 "Best ??? Android/iPhone App",
                 "Don't Fall For This ??? Scam",
                 "12 Questions Answered About ???",
                 "10 Warning Signs Of Your ??? Demise"
                 "If You Do Not (Do)??? Now, You Will Hate Yourself Later",
                 "Some People Excel At ??? And Some Don't - Which One Are You?",
                 "15 Lessons About ??? You Need To Learn To Succeed",
                 "5 Ways Of ??? That Can Drive You Bankrupt - Fast!",
                 "15 Unheard Ways To Achieve Greater ???",
                 "Succeed With ??? In 24 Hours",
                 "The Death Of ??? And How To Avoid It",
                 "Why Ignoring ??? Will Cost You Time and Sales",
                 "3 ??? Secrets You Never Knew",
                 "You Don't Have To Be A Big Corporation To Start ???",
                 "The Lazy Way To ???",
                 "How We Improved Our ??? In One Week(Month, Day)",
                 "Want More Money? Start ???",
                 "The Secret of Successful ???",
                 "5 Simple Steps To An Effective ??? Strategy",
                 "??? : This Is What Professionals Do",
                 "How I Improved My ??? In One Day",
                 "What Alberto Savoia Can Teach You About ???",
                 "The Ugly Truth About ???",
                 "Boost Your ??? With These Tips",
                 "Don't Just Sit There! Start ???",
                 "The Ultimate Guide To ???",
                 "How To Save Money with ????",
                 "Top 3 Ways To Buy A Used ???",
                 "Clear And Unbiased Facts About ??? (Without All the Hype)",
                 "The Untold Secret To ??? In Less Than Ten Minutes",
                 "The Single Most Important Thing You Need To Know About ???",
                 "Got Stuck? Try These Tips To Streamline Your ???",
                 "How To Handle Every ??? Challenge With Ease Using These Tips",
                 "9 Ways ??? Can Make You Invincibl",
                 "Fear% Not If You Use ??? The Right Way!",
                 "7 Easy Ways To Make ??? Faster",
                 "How To Get (A) Fabulous ??? On A Tight Budget",
                 "Who Else Wants To Enjoy ???",
                 "World Class Tools Make ??? Push Button Easy",
                 "??? Works Only Under These Conditions",
                 "5 Sexy Ways To Improve Your ???",
                 "What You Can Learn From Bill Gates About ???",
                 "Interesting Facts I Bet You Never Knew About ???",
                 "The Truth About ??? In 3 Minutes",
                 "17 Tricks About ??? You Wish You Knew Before",
                 "10 Ways To Immediately Start Selling ???",
                 "Best 50 Tips For ???",
                 "The Philosophy Of ???",
                 "You Will Thank Us 10 Tips About ??? You Need To Know",
                 "It's All About (The) ???",
                 "5 Best Ways To Sell ???",
                 "How To Use ??? To Desire",
                 "Can You Pass The ??? Test?",
                 "Is ??? Worth [$] To You?",
                 "Why I Hate ???",
                 "??? Shortcuts  The Easy Way",
                 "??? Your Way To Success",
                 "Winning Tactics For ???",
                 "52 Ways To Avoid ??? Burnout",
                 "Answered: Your Most Burning Questions About ???",
                 "The Secrets To Finding World Class Tools For Your ??? Quickly",
                 "How To Lose Money With ???",
                 "??? And Love Have 4 Things In Common",
                 "Double Your Profit With These 5 Tips on ???",
                 "10 Ways To Reinvent Your ???",
                 "Short Story: The Truth About ???",
                 "5 Surefire Ways ??? Will Drive Your Business Into The Ground",
                 "Get Rid of ??? For Good",
                 "What Can You Do To Save Your ??? From Destruction By Social Media?",
                 "Why Most ??? Fail",
                 "How To Teach ??? Better Than Anyone Else",
                 "Avoid The Top 10 Mistakes Made By Beginning ???",
                 "Why My ??? Is Better Than Yours",
                 "Lies And Damn Lies About ???",
                 "Use ??? To Make Someone Fall In Love With You",
                 "To People That Want To Start ??? But Are Affraid To Get Started",
                 "Secrets To Getting ??? To Complete Tasks Quickly And Efficiently",
                 "Could This Report Be The Definitive Answer To Your ????",
                 "What Can Instagramm Teach You About ???",
                 "What Zombies Can Teach You About ???",
                 "Why You Never See ??? That Actually Works",
                 "Why ??? Is The Only Skill You Really Need",
                 "How To Quit ??? In 5 Days",
                 "Fascinating ??? Tactics That Can Help Your Business Grow",
                 "At Last, The Secret To ??? Is Revealed",
                 "3 Ways Create Better ??? With The Help Of Your Dog",
                 "3 Tips About ??? You Can't Afford To Miss",
                 "5 Easy Ways You Can Turn ??? Into Success",
                 "???? It's Easy If You Do It Smart",
                 "Where Can You Find Free ??? Resources",
                 "The Anthony Robins Guide To ???",
                 "Learn To (Do) ??? Like A Professional",
                 "27 Ways To Improve ???",
                 "5 Actionable Tips on ??? And Twitter."]


def insert_news_continuously(conn, stop_evt):
    while not stop_evt.is_set():
        insert_news(conn)


def insert_news(conn):
    cursor = conn.cursor()

    # picking up the title
    title = random.choice(ARTICLE_NAMES)
    choose_which = random.uniform(0.0, 1.0)
    if choose_which > 0.5:
        cursor.execute(InsertComment_Actor, [view_actor.choose_random_actor(conn), title, 0])
    else:
        cursor.execute(InsertComment_Director, [view_director.choose_random_director(conn), title, 0])
    conn.commit()
    cursor.close()


def get_actor_article(conn, actor_id):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT article_id, actor_id FROM mutable.actor_news WHERE actor_id = %s ORDER BY RANDOM() LIMIT 1;
    """, (actor_id,))

    result = cursor.fetchone()
    article_id = None if result is None else result[0]
    cursor.close()
    return article_id


def get_director_article(conn, director_id):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT article_id, director_id, title FROM mutable.director_news WHERE director_id = %s ORDER BY RANDOM() LIMIT 1;
    """, (director_id,))

    result = cursor.fetchone()
    article_id = None if result is None else result[0]
    cursor.close()
    return article_id


def increase_clicks_actor(conn, id):
    if id is None:
        return

    cursor = conn.cursor()
    Update_Actor_Clicks = """
                  UPDATE mutable.actor_news
                  SET clicks = clicks + 1,
                  last_updated = CURRENT_TIMESTAMP
                   WHERE article_id = %s;
                  """
    cursor.execute(Update_Actor_Clicks, (id, ))
    conn.commit()
    cursor.close()


def increase_clicks_director(conn, id):
    if id is None:
        return

    cursor = conn.cursor()
    Update_Director_Clicks = """
                  UPDATE mutable.director_news
                  SET clicks = clicks + 1,
                  last_updated = CURRENT_TIMESTAMP
                  WHERE article_id = %s;
                  """
    cursor.execute(Update_Director_Clicks, (id, ))
    conn.commit()
    cursor.close()


def click_recent_actor_article(conn):
    cursor = conn.cursor()

    cursor.execute("""SELECT article_id FROM mutable.actor_news ORDER BY creation_TS DESC LIMIT 100;""")
    articles = cursor.fetchall()

    if articles is not None and len(articles) > 0:
        (article_id, ) = random.choice(articles)
        increase_clicks_actor(conn, article_id)


def click_recent_director_article(conn):
    cursor = conn.cursor()

    cursor.execute("""SELECT article_id FROM mutable.director_news ORDER BY creation_TS DESC LIMIT 100;""")
    articles = cursor.fetchall()

    if articles is not None and len(articles) > 0:
        (article_id, ) = random.choice(articles)
        increase_clicks_director(conn, article_id)
