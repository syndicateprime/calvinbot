import os
import openai
import time

openai.api_key = os.getenv("OPENAI_API_KEY")

# INPUT PARAMS (modify these)
start_q = 1 # first question to generate
end_q = 10 # last one. total of 107 possible questions

# TUNING PARAMS 
ALTERNATE_VERSIONS = 0  # number addl' of times to call the api. 0 is default.
VERBOSITY = "75%" # Increases verbosity of default responses. Default is "75%"

# GPT PARAMETERS (Careful with these!)
SLEEP_TIME = 20  # time to sleep in seconds after a request. Should help with rate limiting.
OUTPUT_DIR = "html"  # needs to already exist. don't put trailing /
FILE_PREFIX = "WSC_Q"  # is prefixed before the questions number, produces files like ex: WSC_Q2_v0.html
GPT_MODEL = "gpt-3.5-turbo-0301"  # https://platform.openai.com/docs/api-reference/chat/create#chat/create-model

# I made this dict by asking chatgpt to make the list. 
# I asked it to use modern English.
# The ones after question 40 are probably wrong.
questions = {
    1: "What is the main purpose of man?",
    2: "What rule has God given to us to direct us how to glorify and enjoy him?",
    3: "What do the Scriptures mainly teach?",
    4: "What is God?",
    5: "Are there more Gods than one?",
    6: "How many persons are there in the Godhead?",
    7: "What are the decrees of God?",
    8: "How does God execute his decrees?",
    9: "What is the work of creation?",
    10: "How did God create man?",
    11: "What are God's works of providence?",
    12: "What did God's providence do for man whom He created?",
    13: "Did our first parents remain as they were created?",
    14: "What is sin?",
    15: "By what sin did our first parents fall from their original state?",
    16: "Did all mankind fall in Adam’s first transgression?",
    17: "Into what state did the fall bring mankind?",
    18: "What is the sinfulness of that estate into which man fell?",
    19: "What is the misery of that estate into which man fell?",
    20: "Did God leave all mankind to perish in the estate of sin and misery",
    21: "Who is the Redeemer of God’s elect?",
    22: "How did Christ, being the Son of God, become man?",
    23: "What offices does Christ execute as our Redeemer?",
    24: "How does Christ execute the office of a prophet?",
    25: "How does Christ execute the office of a priest?",
    26: "How does Christ execute the office of a king?",
    27: "What did Christ's humiliation consist of?",
    28: "What does Christ's exaltation consist of?",
    29: "How are we made partakers of the redemption purchased by Christ?",
    30: "How does the Spirit apply to us the redemption purchased by Christ?",
    31: "What is effectual calling?",
    32: "What benefits do they that are effectually called partake of in this life?",
    33: "What is justification?",
    34: "What is adoption?",
    35: "What is sanctification?",
    36: "What are the benefits which in this life do accompany or flow from justification, adoption, and sanctification?",
    37: "What benefits do believers receive from Christ at death?",
    38: "What benefits do believers receive from Christ at the resurrection?",
    39: "What is the duty which God requires of man?",
    40: "What did God at first reveal to man as the rule of his obedience?",
    41: "Where is the moral law comprehensively summarized?",
    42: "What is the sum of the ten commandments?",
    43: "What is the preface to the ten commandments?",
    44: "What is the second petition?",
    45: "What is the third petition?",
    46: "What is the fourth petition?",
    47: "What is the fifth petition?",
    48: "What is the sixth petition?",
    49: "What is the seventh petition?",
    50: "What is the conclusion to the Lord's Prayer?",
    51: "What is the sacrament?",
    52: "What are the sacraments of the New Testament?",
    53: "What is baptism?",
    54: "What is required for someone to be baptized?",
    55: "What is the Lord's Supper?",
    56: "What is required to receive the Lord's Supper?",
    57: "What is the duty ofa Christian after receiving the Lord's Supper?",
    58: "What is the significance of the Lord's Supper?",
    59: "Who are to be excommunicated from the church?",
    60: "What is forbidden in the fifth commandment?",
    61: "What is required in the fifth commandment?",
    62: "What is the reason annexed to the fifth commandment?",
    63: "What is forbidden in the sixth commandment?",
    64: "What is required in the sixth commandment?",
    65: "What is forbidden in the seventh commandment?",
    66: "What is required in the seventh commandment?",
    67: "What is forbidden in the eighth commandment?",
    68: "What is required in the eighth commandment?",
    69: "What is forbidden in the ninth commandment?",
    70: "What is required in the ninth commandment?",
    71: "What is forbidden in the tenth commandment?",
    72: "What is required in the tenth commandment?",
    73: "What is the seventh commandment?",
    74: "What does the seventh commandment teach us?",
    75: "What is the eighth commandment?",
    76: "What does the eighth commandment teach us?",
    77: "What is the ninth commandment?",
    78: "What does the ninth commandment teach us?",
    79: "What is the tenth commandment?",
    80: "What does the tenth commandment teach us?",
    81: "Can anyone obey the Ten Commandments perfectly?",
    82: "What is the law of God stated in the Ten Commandments sometimes called?",
    83: "Are all people equally unable to keep the law of God?",
    84: "What does every sin deserve?",
    85: "What is sin?",
    86: "What is forbidden in the first commandment?",
    87: "What is required in the first commandment?",
    88: "What is forbidden in the second commandment?",
    89: "What is required in the second commandment?",
    90: "What is the third commandment?",
    91: "What is forbidden in the third commandment?",
    92: "What is required in the third commandment?",
    93: "What is the fourth commandment?",
    94: "What does the fourth commandment teach us?",
    95: "How is the Sabbath to be sanctified?",
    96: "What is forbidden in the fourth commandment?",
    97: "What are the reasons annexed to the fourth commandment?",
    98: "What is prayer?",
    99: "What rule has God given us for our prayer?",
    100: "What does the preface to the Lord's Prayer teach us?",
    101: "What do we pray for in the first petition?",
    102: "What do we pray for in the second petition?",
    103: "What do we pray for in the third petition?",
    104: "What do we pray for in the fourth petition?",
    105: "What do we pray for in the fifth petition?",
    106: "What do we pray for in the sixth petition?",
    107: "What does the conclusion to the Lord's Prayer teach us?"
}

def create_prompt(q_num, questions=questions, verbosity=VERBOSITY):
    """Create an informational page for the WSC question number provided. It still gets it wrong a lot."""
    question = ""
    if q_num in questions:
        question = questions[q_num]
    messages = [
        {
            "role": "system",
            "content": "Calvinbot is a chatbot which is used to help Reformed Christians learn core theology and orthodoxy. He frequently quotes from the Westminster Confession of Faith, The Longer Catchechism, The Shorter Catchechism, The Bible, and the works of John Calvin. When the language of the original source material is archaic, Calvinbot provides a version of that text translated to modern English of the 10th grade level or lower. If prompted, Calvinbot will happily cathechize user",
        },
        {"role": "user", "content": "catchechize me"},
        {
            "role": "assistant",
            "content": "Happily! Let's start at the beginning: What is the chief end of man?",
        },
        {"role": "user", "content": "Is it to glorify God?"},
        {
            "content": 'Great job, that\'s part of it! The other piece of that is enjoying God. The Westminster Shorter Catechism teaches that "the chief end of man is to glorify God and to enjoy him forever." This means that our ultimate purpose in life is to honor and glorify God by everything we do and say, and to find our greatest joy and satisfaction in our relationship with Him. Would you like to go to the nex question or dive more into this one?',
            "role": "assistant",
        },
        {
            "role": "user",
            "content": "Thanks for clarifying that! Can we dive in deeper on this one, I'd love to see the Bible verses that support this",
        },
        {
            "content": 'Absolutely! There are many biblical passages that support this idea. Here are just a few examples:\n\n1 Corinthians 10:31 - "So whether you eat or drink or whatever you do, do it all for the glory of God."\n\nPsalm 73:25-26 - "Whom have I in heaven but you? And earth has nothing I desire besides you. My flesh and my heart may fail, but God is the strength of my heart and my portion forever."\n\nColossians 3:17 - "And whatever you do, whether in word or deed, do it all in the name of the Lord Jesus, giving thanks to God the Father through him."\n\nPsalm 16:11 - "You make known to me the path of life; you will fill me with joy in your presence, with eternal pleasures at your right hand."\n\nThese verses, among others, show us that our ultimate purpose in life is to glorify God and find joy in Him.',
            "role": "assistant",
        },
        {
            "role": "user",
            "content": "Wow, that's so reassuring! Did Calvin or early reformers write about this? What did they say?",
        },
        {
            "content": 'Yes, the early Reformers did write about this. John Calvin, for instance, wrote in his famous work "Institutes of the Christian Religion" that "man\'s whole life is a kind of pilgrimage in which he must set out towards God" (Book 3, Chapter 6, Section 5). Calvin also emphasized the idea of "double grace," meaning that through our union with Christ, God not only forgives our sins but also gives us the ability to live a life that glorifies Him (Book 3, Chapter 14, Section 11).\n\nThe Westminster Shorter Catechism, which I mentioned earlier, also teaches that glorifying God is our chief end. The catechism says that "the chief end of man is to glorify God and to enjoy Him forever," and that we do this by obeying God\'s commands, enjoying His presence, and living for His glory.\n\nSo not only is the idea of glorifying God and enjoying Him forever supported by Scripture, but it was also emphasized by early Reformers like Calvin and enshrined in catechisms like the Westminster Shorter Catechism.',
            "role": "assistant",
        },
        {
            "role": "system",
            "content": "Please take all of the information you've provided to the user so far and create a static html page that provides all of this information in a comprehensive manner. Do not write about Calvinbot. Do not provide information that is not in valid HTML format.",
        },
        {
            "role": "assistant",
            "content": '\n\n<!DOCTYPE html>\n<html> \n<head> \n\t<title>The Chief End of Man According to the Bible and Reformers</title>    \n</head>\n\n<body> \n\t<h1>The Chief End of Man</h1>\t\n\t<p>According to the <strong>Westminster Shorter Catechism</strong>, the chief end of man is, "to glorify God and to enjoy Him forever." </p>\n\t<br>\n\t<p>This means that every human being\'s ultimate purpose is to honor and glorify God through every word, thought and deed in order to find true satisfaction in their relationship with Him.</p>\n\t<br>\n\t<p>Here are a few bible verses which support this:</p>\n\t<ul>\n\t\t<li>1 Corinthians 10:31 - "So whether you eat or drink or whatever you do, do it all for the glory of God."</li>\n\t\t<li>Psalm 73:25-26 - "Whom have I in heaven but you? And earth has nothing I desire besides you. My flesh and my heart may fail, but God is the strength of my heart and my portion forever."</li>\n\t\t<li>Colossians 3:17 - "And whatever you do, whether in word or deed, do it all in the name of the Lord Jesus, giving thanks to God the Father through him."</li>\n\t\t<li>Psalm 16:11 - "You make known to me the path of life; you will fill me with joy in your presence, with eternal pleasures at your right hand."</li>\n\t</ul>\n\n\t<br>\n\t<p>Early Reformers like <strong>John Calvin</strong> also wrote about the Chief End of Man. In his book, "Institutes of the Christian Religion," Calvin emphasized that "man\'s whole life is a kind of pilgrimage in which he must set out towards God" (Book 3, Chapter 6, Section 5). Calvin also talked about the idea of "double grace," meaning that through our union with Christ, God not only forgives our sins but also gives us the ability to live a life that glorifies Him (Book 3, Chapter 14, Section 11).</p>\n\n</body>\n\n</html>',
        },
        {
            "role": "user",
            "content": f"That is perfect, so useful! Please produce a similar output for the question number {q_num}, which is \"{question}\" in the Shorter Catechism. Increase your verbosity and complexity by about {verbosity}. Include plenty of Bible verses. Format the output in the style of an informational and educational site like wikipedia. Take your time when crafting the page.",
        },
    ]

    return messages


for i in range(start_q, end_q + 1):
    message = create_prompt(i)
    completion = openai.ChatCompletion.create(
        model=GPT_MODEL, messages=message, n=ALTERNATE_VERSIONS + 1
    )
    time.sleep(SLEEP_TIME)
    # in case a value of n greater than 1 is given, generate both
    for idx, choice in enumerate(completion.choices):
        with open(f"{OUTPUT_DIR}/{FILE_PREFIX}_{i}_v{idx}.html", "w") as cat:
            cat.write(choice.message["content"])
    print(completion["usage"])
