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


most_common = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'] # usernames in order of freq
characters = anim.get_characters(most_common) # returns a dict where key = character, val = username
comments = [
    MockRedditComment('a', 'Hello as I am the most common I will be Phoenix'),
    MockRedditComment('b', 'wassup I\'m edgyboy'),
    MockRedditComment('c', 'I\'m someone random and I\'m angry', score=-1),
    MockRedditComment('d', 'd', score=-1),
    MockRedditComment('e', 'e', score=-1),
    MockRedditComment('f', 'f', score=-1),
    MockRedditComment('g', 'g', score=-1),
    MockRedditComment('h', 'h', score=-1),
    MockRedditComment('i', 'i', score=-1),
    MockRedditComment('j', 'j', score=-1),
    MockRedditComment('k', 'k', score=-1),
    MockRedditComment('l', 'l', score=-1),
    MockRedditComment('m', 'm', score=-1),
    MockRedditComment('n', 'n', score=-1),
    MockRedditComment('n', 'n', score=-1)
]  *  1
anim.comments_to_scene(comments, characters, output_filename="hello.mp4")