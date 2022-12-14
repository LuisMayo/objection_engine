from objection_engine.v4.make_movie import render_comment_list
from objection_engine.beans.comment import Comment

comments = [
    Comment(user_name = 'first guy', text_content = "Hello it's me, the first guy. Because I talk so much, I'm Phoenix."),
    Comment(user_name = 'first guy', text_content = "I am going to say a few more sentences. This is a lot of fun."),
    Comment(user_name = 'first guy', text_content = "Here's a few more lines, because why not. This is a second sentence. And, last but not least, here's a third sentence."),
    Comment(user_name = 'second guy', text_content= "I have the second most comments, so I must be Edgeworth."),
    Comment(user_name = 'second guy', text_content= "Why don't I do a little talking as well?"),
    Comment(user_name = 'someone random', text_content= "I have very few lines, so I'm just some random person."),
    Comment(user_name = 'someone else random', text_content= "I'm also a random person!"),
    Comment(user_name = 'someone random', text_content= "Hey it's me, the first random person."),
    Comment(user_name = 'first guy', text_content = "And last but not least, it's Phoenix again."),
]
render_comment_list(comments)