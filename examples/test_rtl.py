from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment
from time import time

comments = [
    Comment(user_name = 'Edgeworth', text_content="Here is some English LTR text"),
    Comment(user_name = 'فينيكس', text_content="هذا نص عربي. أنا أستخدم مترجمًا ، لذلك ربما يكون الأمر سيئًا للغاية."),
    Comment(user_name="فينيكس", text_content="الكلمة الأخيرة في هذه الجملة هي <red> أحمر </red>.")
]

render_comment_list(comments, f'test-rtl-{str(int(time()))}.mp4', resolution_scale=2)