from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment
from time import time

comments = [
    Comment(user_name='Phoenix', text_content='We are in the relaxed music phase right now. happy thoughts :)', score=1),
    Comment(user_name='Edgeworth', text_content="Now we are in tense music!", score=-1),
    Comment(user_name='Phoenix', text_content="The music shouldn't have just changed", score=-1),
    Comment(user_name="Edgeworth", text_content="And again, it shouldn't have changed here either.", score=-1),
    Comment(user_name="Phoenix", text_content="Here are several identical boxes that should keep the music.", score=-1),
    Comment(user_name="Phoenix", text_content="Here are several identical boxes that should keep the music.", score=-1),
    Comment(user_name="Phoenix", text_content="Here are several identical boxes that should keep the music.", score=-1),
    Comment(user_name="Phoenix", text_content="Here are several identical boxes that should keep the music.", score=-1),
    Comment(user_name="Phoenix", text_content="Here are several identical boxes that should keep the music.", score=-1),
    Comment(user_name="Phoenix", text_content="Here are several identical boxes that should keep the music.", score=-1),
    Comment(user_name="Phoenix", text_content="Here are several identical boxes that should keep the music.", score=-1),
    Comment(user_name="Phoenix", text_content="Here are several identical boxes that should keep the music.", score=-1),
    Comment(user_name="Phoenix", text_content="Here are several identical boxes that should keep the music.", score=-1),
    Comment(user_name="Phoenix", text_content="Here are several identical boxes that should keep the music.", score=-1),
    Comment(user_name="Phoenix", text_content="Here are several identical boxes that should keep the music.", score=-1),
    Comment(user_name="Phoenix", text_content="Here are several identical boxes that should keep the music.", score=-1),
]
render_comment_list(comments, f'test-music-switch-{str(int(time()))}.mp4')
