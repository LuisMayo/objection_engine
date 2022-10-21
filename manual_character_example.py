from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment
from objection_engine.constants import Character
from time import time

comments = [
    Comment(user_name = "User 1", text_content="I'm Phoenix even though I don't talk much", user_id="a"),
    
    Comment(user_name = "User 4", text_content="No idea who I am, I'm not specified", user_id="d"),
    Comment(user_name = "User 4", text_content="I'm gonna talk a little bit more though", user_id="d"),

    Comment(user_name = "User 2", text_content="I'm Payne instead of Edgeworth, and I talk a little bit.", user_id="b"),
    Comment(user_name = "User 2", text_content="Here I am talking some more.", user_id="b"),
    Comment(user_name = "User 2", text_content="And a little bit more", user_id="b"),
    
    Comment(user_name = "User 3", text_content="I'm Redd White, some random guy, even though I talk the most", user_id="c"),
    Comment(user_name = "User 3", text_content="Lorem ipsum dolor sit amet, consectetur adipiscing elit.", user_id="c"),

    Comment(user_name = "User 5", text_content="Hey don't forget about me! whoever I am", user_id="e"),

    Comment(user_name = "User 3", text_content="Nunc aliquet et justo elementum mollis. Nullam commodo nisl id accumsan gravida.", user_id = "c"),
    Comment(user_name = "User 3", text_content="Vivamus elementum mattis ipsum, ac luctus lacus scelerisque lacinia.", user_id = "c"),
    Comment(user_name = "User 3", text_content="Vivamus elementum mattis ipsum, ac luctus lacus scelerisque lacinia.", user_id = "c")
]

characters = {
    Character.PHOENIX: "a",
    Character.PAYNE: "b",
    Character.REDD: "c"
}

render_comment_list(comments, f'output-manual-character-{str(int(time()))}.mp4', resolution_scale=2, assigned_characters=characters)
