from objection_engine.v4.make_movie import render_comment_list
# from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment
from time import time

comments = [
    Comment(
        user_name="Phoenix",
        text_content="Hello. My name is Phoenix. I am a defense attorney.",
    ),
    Comment(user_name="Phoenix", text_content="thislineofdialogueisreallylongwillitwrapidontknowiguesstheresonlyonewaytofindout"),
    Comment(user_name="Phoenix", text_content="imjustgoingtokeepwritingmoreandmoretextonthislineandhopefullyitshouldwrapbetweenboxesandnotoverflowbutidontknowforsuresothatswhyimdoingthispleaseworkimbeggingyoupythonidontwanttobestuckonthisfortherestofmylifealwaysthinkingabouthowgettinglinebreakstoworkwassohardiwanttobefreeiwanttolivemylifewithouttheseshackles"),
    Comment(user_name="Phoenix", text_content="Here's a little bit of normal text. And heressomelongtextthatwontfitononeline, and back to normal text again."),
    Comment(user_name="Edgeworth", text_content="Anyways, here's some Japanese lorem ipsum I found online."),
    Comment(user_name="Edgeworth", text_content="面かでいッ寺尾3元だむトド霊職こはク用法旦集は多以ラチ的3解ムヱセエ投記テキロ間恭カワナ万切亮凱にどでつ。度サテユセ図富水ょトぱじ図車メソヒモ坂越へのクぴ仕告国ゅだやレ備初リソケ所了いねなあ吉休よぜすた全媛ヨト財前せおんび周見けル告合ヌハレツ送型ゅ著設ぞょそぼ詳些仄伽凹ぞおトる。見僧ユメワリ真毎悩ロ転男けーぴす済歌院ロモア情載そざッえ進入つドれ覧1病治チスオ察旧丸面豊ぎらし。")
]

render_comment_list(comments, output_filename=f"output-{int(time())}.mp4")
