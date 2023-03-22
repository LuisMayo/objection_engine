"""
Test script profile performance for the renderer.
"""
import cProfile
from timeit import default_timer as timer
from rich import print
from time import strftime

pr = cProfile.Profile()
pr.enable()
start_time = timer()
from objection_engine.beans.comment import Comment

from objection_engine.ace_attorney_scene import DialogueBoxBuilder

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

current_time = strftime("%Y-%m-%d_%H-%M-%S")

builder = DialogueBoxBuilder()
builder.render(
    comments=comments,
    output_filename=f"output_3vs4_v4-{current_time}.mp4",
)
end_time = timer()
pr.disable()

print("Time for v4:", f"{end_time - start_time:.2f} s")
pr.dump_stats(f"output_3vs4_4profile-{current_time}.prof")