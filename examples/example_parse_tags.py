from objection_engine.ace_attorney_scene import AceAttorneyDirector
from objection_engine.parse_tags import DialoguePage
from objection_engine.parse_tags_v2 import parse_line
from rich import print

script = """
[music start pwr/cross-moderato]
[sprite left assets/characters/phoenix/phoenix-normal-idle.gif][nametag "Phoenix"][cut left][showbox][evidence clear][startblip male][sprite left assets/characters/phoenix/phoenix-normal-talk.gif]Hello.[stopblip][sprite left assets/characters/phoenix/phoenix-normal-idle.gif][wait 0.6][startblip male][sprite left assets/characters/phoenix/phoenix-handsondesk-talk.gif] My name is Phoenix. This[br]box is really really long so it[br]should go on multiple lines.[sprite left assets/characters/phoenix/phoenix-handsondesk-idle.gif][stopblip][showarrow][wait 2.0][hidearrow][sound pichoop][wait 0.3]"""

pages = [DialoguePage(parse_line(line)) for line in script.strip().split("\n")]

director = AceAttorneyDirector()
director.set_current_pages(pages)
director.render_movie()