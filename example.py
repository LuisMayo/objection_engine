from renderer import render_comment_list
from beans.comment import Comment
from time import time
import anim

comments = [
    Comment(user_name = 'a', text_content='Hello as I am the most common I will be Phoenix'),
    Comment(user_name = 'b', text_content='wassup I\'m edgyboy', user_id='id1'),
    Comment(user_name = 'c', text_content='I\'m someone random and I\'m angry', score=-1),
    Comment(user_name = 'جالكسي', text_content='حاب أذكركم انه باقي كم يوم وينتهي عرض الطلب المسبق على جالكسي Z فليب', user_id="id2"),
    Comment(user_name = 'd', text_content='Bonjout mâ fìlle. Coment ça-va'),
    Comment(user_name = 'e', text_content='Türkiye Türkçesi, dil ailesi sınıflandırmasında, Doğu Avrupa, Orta Asya ve Sibirya’da konuşulan 30 kadar yaşayan dili kapsayan'),
    Comment(user_name = 'f', text_content='気やすく呼ぶんじゃないよ!このギザギザ男がッ!アンタのせいで、オバチャンまた、ワルモノにされちまったョ!'),
    Comment(user_name = 'g', text_content='검사 따위는 때려 치고 말겠다!'),
    Comment(user_name = 'h', text_content='б, г, ґ, д, ж, з, к, л, м, н, п, р, с, т, ф, х, ц, ч, ш, щ), ten vowels (а, е, є, и, і, ї, о, у, ю, я), and two semivowels (й/yot, and в'),
    Comment(user_name = 'i', text_content='Hello OwO'),
    Comment(user_name = 'j', text_content='Hello OwO'),
    Comment(user_name = 'k', text_content='Hello OwO'),
    Comment(user_name = 'l', text_content='Hello OwO'),
    Comment(user_name = 'm', text_content='Hello OwO'),
    Comment(user_name = 'n', text_content='Hello OwO'),
    Comment(user_name = 'o', text_content='《长征》第1集 The Long March 01震惊世界的二万五千里长征（唐国强/陈道明）【CCTV电视剧】Highlights：毛泽东针对奔袭湘江的作战命令会给数万红军带来的严重损失，连夜找“三人团”请示复议作战计划，李德不耐烦地指责毛泽东是在危言耸听。'),    
    Comment(user_name = 'o', text_content='Hello OwO')
]  *  1
render_comment_list(comments, f'output-{str(int(time()))}.mp4')
