"""
Test script to compare performance of the v3 engine and v4 engine
on identical comment chains.
"""
from timeit import default_timer as timer
from time import time
from objection_engine.beans.comment import Comment
from rich import print
import cProfile

comments = [
    Comment(
        user_name="first guy",
        text_content="Hello it's me, the first guy. Because I talk so much, I'm Phoenix.",
    ),
    Comment(
        user_name="first guy",
        text_content="I am going to say a few more sentences. This is a lot of fun.",
        evidence_path="examples/puppies.jpeg",
    ),
    Comment(
        user_name="فينيكس",
        text_content="هذا نص عربي. أنا أستخدم مترجمًا ، لذلك ربما يكون الأمر سيئًا للغاية.",
    ),
    Comment(
        user_name="first guy",
        text_content="Here's a few more lines, because why not. This is a second sentence. And, last but not least, here's a third sentence.",
    ),
    Comment(
        user_name="second guy",
        text_content="I have the second most comments, so I must be Edgeworth.",
        evidence_path="examples/cats.jpeg",
    ),
    Comment(
        user_name="second guy", text_content="Why don't I do a little talking as well?"
    ),
    Comment(
        user_name="someone random",
        text_content="I have very few lines, so I'm just some random person.",
    ),
    Comment(user_name="someone else random", text_content="I'm also a random person!"),
    Comment(
        user_name="someone random", text_content="Hey it's me, the first random person."
    ),
    Comment(
        user_name="first guy",
        text_content="And last but not least, it's Phoenix again.",
    ),
]

current_time = int(time())

# # Test importing and rendering with v3 engine
before_v3 = timer()
from objection_engine.renderer import render_comment_list as render_comment_list_v3
render_comment_list_v3(comment_list=comments, output_filename=f"output_3vs4_v3-{current_time}.mp4")
after_v3 = timer()

print(f"v3 done, took {after_v3 - before_v3:.2f} s")

# Do initialization stuff ahead of time (especially loading the sentiment
# analysis model)
from objection_engine.v4.ace_attorney_scene import DialogueBoxBuilder
builder = DialogueBoxBuilder()

# Test importing and rendering with v4 engine
pr = cProfile.Profile()
before_v4 = timer()
pr.enable()
builder.render(
    comments=comments,
    output_filename=f"output_3vs4_v4-{current_time}.mp4",
)
pr.disable()
after_v4 = timer()
pr.dump_stats(f"output_3vs4_4profile-{current_time}")



print("Time for v3:", f"{after_v3 - before_v3:.2f} s")
print("Time for v4:", f"{after_v4 - before_v4:.2f} s")
