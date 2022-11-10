from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment
from time import time

comments = [
    Comment(user_name = 'a', text_content='Hello as I am the most common <red>I will be Phoenix</red>'),
    Comment(user_name = 'b', text_content='wassup I\'m <green>edgyboy</green>', user_id='id1'),
    Comment(user_name = 'c', text_content='I\'m someone <red>random</red> and I\'m <red>angry</red>', score=-1),
    Comment(user_name = 'جالكسي', text_content='حاب <red>أذكركم انه</red> باقي كم يوم وينتهي <green>عرض الطلب المسبق</green> على <blue>جالكسي</blue> Z فليب', user_id="id2"),
    Comment(user_name = 'd', text_content='Bonjout mâ fìlle. <red>Coment ça-va</red>'),
    Comment(user_name = 'e', text_content='Türkiye Türkçesi, dil ailesi sınıflandırmasında, <red>Doğu Avrupa</red>, Orta Asya ve Sibirya’da konuşulan <red>30 kadar</red> yaşayan dili kapsayan'),
    Comment(user_name = 'f', text_content='気やすく呼ぶんじゃないよ!<red>このギザギザ男がッ!</red>アンタのせいで、<green>オバチャンまた</green>、ワルモノにされちまったョ!'),
    Comment(user_name = 'g', text_content='검사 <green>따위는</green> 때려 치고<red>말겠다</red>!'),
    Comment(user_name = 'h', text_content='<blue>б, г, ґ, д, ж, з, к, л, м, н, п, р, с, т, ф, х, ц, ч, ш, щ),</blue> ten vowels <red>(а, е, є, и, і, ї, о, у, ю, я)</red>, and two semivowels (й/yot, and в'),
    Comment(user_name = 'i', text_content='This is a <red>complex sentence</red> made up of <green>several smaller sentences</green>. This sentence should be divided in several different screens, as it <red>clearly does not fit in one alone</red>. So I hope this is long enough for this little test of ours'),
    Comment(user_name = 'j', text_content='Hello OwO'),
    Comment(user_name = 'k', text_content='Hello OwO'),
    Comment(user_name = 'l', text_content='Hello OwO'),
    Comment(user_name = 'm', text_content='Hello OwO'),
    Comment(user_name = 'n', text_content='Hello OwO'),
    Comment(user_name = 'o', text_content='《长征》第1集 <red>The Long March</red> 01震惊世界的二万五千里长征<green>（唐国强/陈道明）</green>【CCTV电视剧】Highlights：毛泽东针对奔袭湘江的作战命令会给数万红军带来的严重损失，连夜找“三人团”请示复议作战计划，李德不耐烦地指责毛泽东是在危言耸听。'),
    Comment(user_name = 'o', text_content='Hello OwO')
]  *  1
render_comment_list(comments, f'output-{str(int(time()))}.mp4')
