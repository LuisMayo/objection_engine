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


most_common = ['a', 'b', 'c'] # usernames in order of freq
characters = anim.get_characters(most_common) # returns a dict where key = character, val = username
comments = [
    MockRedditComment('a', 'Hello as I am the most common I will be Phoenix'),
    MockRedditComment('b', 'wassup I\'m edgyboy'),
    MockRedditComment('c', 'I\'m someone random and I\'m angry', score=-1)
]
anim.comments_to_scene(comments, characters, output_filename="hello.mp4")