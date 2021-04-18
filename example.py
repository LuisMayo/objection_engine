import anim

# mocks PRAW objects
class MockRedditAuthor:
    
    def __init__(self, name):
        self.name = name

class MockRedditComment:
    
    def __init__(self, username: str, text: str, score: int = 0):
        self.author = MockRedditAuthor(username)
        self.body = text
        self.score = score
        self.evidence = "evidence_test.png"


most_common = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'] # usernames in order of freq
characters = anim.get_characters(most_common) # returns a dict where key = character, val = username
comments = [
    MockRedditComment('a', 'Hello as I am the most common I will be Phoenix'),
    MockRedditComment('b', 'wassup I\'m edgyboy'),
    MockRedditComment('c', 'I\'m someone random and I\'m angry'),
    # MockRedditComment('c', 'Bonjour, je m\'appelle Louis'),
    # MockRedditComment('c', ':('),
    # MockRedditComment('d', 'Ti odio, mi sento male'),
    # MockRedditComment('e', 'Ich hasse dich, ich fühle mich schlecht'),
    # MockRedditComment('f', 'Te odio, no me encuentro bien'),
    # MockRedditComment('g', 'Estoy triste'),
    # MockRedditComment('h', 'sono triste'),
    # MockRedditComment('i', 'im so happy'),
    # MockRedditComment('j', 'im so happy'),
    # MockRedditComment('k', 'im so happy'),
    # MockRedditComment('l', 'im so happy'),
    # MockRedditComment('m', 'im so happy'),
    # MockRedditComment('n', 'im so happy'),
    # MockRedditComment('n', 'im so happy'),
    # MockRedditComment('n', 'im so happy')
]  *  1
anim.comments_to_scene(comments, characters, output_filename="hello.mp4")