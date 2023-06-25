from objection_engine.ace_attorney_scene import AceAttorneyDirector
from objection_engine.parse_tags import DialoguePage
from objection_engine.parse_tags_v2 import parse_line
from rich import print

script = """
[music start pwr/trial]

[sprite judge assets/characters/judge/judge-normal-talk.gif][nametag "Judge"][cut judge][showbox][evidence clear]
[startblip male]Court is now in session for the[br]trial of Larry Butz.[sprite judge assets/characters/judge/judge-normal-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[sprite left assets/characters/phoenix/phoenix-normal-talk.gif][nametag "Phoenix"][cut left][showbox][evidence clear]
[startblip male]The defense is ready,[stopblip][sprite left assets/characters/phoenix/phoenix-normal-idle.gif][wait 0.2][sprite left assets/characters/phoenix/phoenix-normal-talk.gif][startblip male][br]Your Honor.[sprite left assets/characters/phoenix/phoenix-normal-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[hidebox][pan right][sprite right assets/characters/edgeworth/edgeworth-normal-idle.gif][nametag "Edgeworth"][wait 0.6]
[showbox][sprite right assets/characters/edgeworth/edgeworth-normal-talk.gif]
[startblip male]The prosecution is ready,[stopblip][sprite right assets/characters/edgeworth/edgeworth-normal-idle.gif][wait 0.2][sprite right assets/characters/edgeworth/edgeworth-normal-talk.gif][startblip male][br]Your Honor.[sprite right assets/characters/edgeworth/edgeworth-normal-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[sprite judge assets/characters/judge/judge-normal-talk.gif][nametag "Judge"][cut judge][showbox][evidence clear]
[startblip male]Please present the charges[br]against Mr. Butz.[sprite judge assets/characters/judge/judge-normal-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[sprite right assets/characters/edgeworth/edgeworth-normal-talk.gif][nametag "Edgeworth"][cut right][showbox][evidence clear]
[startblip male]Certainly,[stopblip][sprite right assets/characters/edgeworth/edgeworth-normal-idle.gif][wait 0.2][sprite right assets/characters/edgeworth/edgeworth-normal-talk.gif][startblip male] Your Honor.[sprite right assets/characters/edgeworth/edgeworth-normal-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[hidebox][pan left][sprite left assets/characters/phoenix/phoenix-sweating-idle.gif][nametag "Phoenix"][wait 0.6]
[showbox][sprite left assets/characters/phoenix/phoenix-sweating-talk.gif]
[startblip male]Uh oh,[stopblip][sprite left assets/characters/phoenix/phoenix-sweating-idle.gif][wait 0.2][sprite left assets/characters/phoenix/phoenix-sweating-talk.gif][startblip male] here we go...[sprite left assets/characters/phoenix/phoenix-sweating-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[hidebox][pan center][sprite center assets/characters/larry/larry-nervous-idle.gif][nametag "Larry"][wait 0.6]
[showbox][sprite center assets/characters/larry/larry-nervous-talk.gif]
[startblip male]I swear, man, [sound smack][shake 4 0.4]I didn't do it![sprite center assets/characters/larry/larry-nervous-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[showbox][sprite center assets/characters/larry/larry-nervous-talk.gif]
[startblip male]I was [sound smack][shake 4 0.4]framed! I'm tellin' ya![sound smack][shake 4 0.4][sprite center assets/characters/larry/larry-nervous-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[sprite right assets/characters/edgeworth/edgeworth-thinking-talk.gif][nametag "Edgeworth"][cut right][showbox][evidence clear]
[startblip male]Would the defendant please be[br]quiet?[sprite right assets/characters/edgeworth/edgeworth-thinking-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[showbox][cut center][sprite center assets/characters/larry/larry-thumbsup-talk.gif]
[startblip male]S-[shake 4 0.4]sure, yeah, I'll try![sprite center assets/characters/larry/larry-thumbsup-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[music start pwr/cross-moderato]

[sprite right assets/characters/edgeworth/edgeworth-document-talk.gif][nametag "Edgeworth"][cut right][showbox][evidence clear]
[startblip male]At 9:68 AM on September 43rd,[stopblip][sprite right assets/characters/edgeworth/edgeworth-document-idle.gif][wait 0.2][sprite right assets/characters/edgeworth/edgeworth-document-talk.gif][startblip male][br]Mr. Butz brutally murdered[br]Linda Lorba with a knife twice.[sprite right assets/characters/edgeworth/edgeworth-document-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[sprite judge assets/characters/judge/judge-warning-talk.gif][nametag "Judge"][cut judge][showbox][evidence clear]
[startblip male]Hmmm...[stopblip][sprite judge assets/characters/judge/judge-warning-idle.gif][wait 0.2][sprite judge assets/characters/judge/judge-warning-talk.gif][startblip male] That does seem[br]rather incriminating.[sprite judge assets/characters/judge/judge-warning-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[hidebox][music stop][bubble objection phoenix][wait 1][music start pwr/objection]

[sprite left assets/characters/phoenix/phoenix-pointing-talk.gif][nametag "Phoenix"][cut left][showbox][evidence clear]
[startblip male]There's a lot of [shake 4 0.4]holes in the[br]prosecution's claims![sprite left assets/characters/phoenix/phoenix-pointing-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[sprite judge assets/characters/judge/judge-warning-talk.gif][nametag "Judge"][cut judge][showbox][evidence clear]
[startblip male]Are there,[stopblip][sprite judge assets/characters/judge/judge-warning-idle.gif][wait 0.2][sprite judge assets/characters/judge/judge-warning-talk.gif][startblip male] Mr. Wright?[sprite judge assets/characters/judge/judge-warning-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[sprite right assets/characters/edgeworth/edgeworth-confident-talk.gif][nametag "Edgeworth"][cut right][showbox][evidence clear]
[startblip male]Please,[stopblip][sprite right assets/characters/edgeworth/edgeworth-confident-idle.gif][wait 0.2][sprite right assets/characters/edgeworth/edgeworth-confident-talk.gif][startblip male] Mr. Wright.[stopblip][sprite right assets/characters/edgeworth/edgeworth-confident-idle.gif][wait 0.4][sprite right assets/characters/edgeworth/edgeworth-confident-talk.gif][startblip male] Show us[br]these supposed holes.[sprite right assets/characters/edgeworth/edgeworth-confident-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[hidebox][bubble takethat phoenix][wait 1]

[sprite left assets/characters/phoenix/phoenix-document-talk.gif][nametag "Phoenix"][cut left][showbox][evidence clear]
[startblip male]For one thing,[stopblip][sprite left assets/characters/phoenix/phoenix-document-idle.gif][wait 0.2][sprite left assets/characters/phoenix/phoenix-document-talk.gif][startblip male] there's no such[br]time as 9:68 AM.[stopblip][sprite left assets/characters/phoenix/phoenix-document-idle.gif][wait 0.4][sprite left assets/characters/phoenix/phoenix-document-talk.gif][startblip male] And September[br]43rd doesn't exist either![sprite left assets/characters/phoenix/phoenix-document-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[sprite right assets/characters/edgeworth/edgeworth-damage.gif][nametag "Edgeworth"][cut right][shake 5 0.5][sound stab]!!![wait 0.8][sprite right assets/characters/edgeworth/edgeworth-strained-idle.gif][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[sprite left assets/characters/phoenix/phoenix-confident-talk.gif][nametag "Phoenix"][cut left][showbox][evidence clear]
[startblip male]And,[stopblip][sprite left assets/characters/phoenix/phoenix-confident-idle.gif][wait 0.2][sprite left assets/characters/phoenix/phoenix-confident-talk.gif][startblip male] Mr. Edgeworth...[stopblip][sprite left assets/characters/phoenix/phoenix-confident-idle.gif][wait 0.3][sprite left assets/characters/phoenix/phoenix-confident-talk.gif][startblip male] How do[br]you suppose my client[music start pwr/press][flash 0.21][wait 0.2][cut leftzoom][sprite leftzoom assets/characters/phoenix/phoenix-zoom-talk.gif] murdered[br]Mrs. Lorba twice?[flash 0.15][shake 5 0.3][sound objection][sprite leftzoom assets/characters/phoenix/phoenix-zoom-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[sprite right assets/characters/edgeworth/edgeworth-strained-talk.gif][nametag "Edgeworth"][cut right][shake 5 0.5]
[startblip male]Gah...[stopblip][sprite right assets/characters/edgeworth/edgeworth-strained-idle.gif][shake 4 0.4][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[sprite judge assets/characters/judge/judge-surprised-talk.gif][nametag "Judge"][cut judge][showbox][evidence clear]
[startblip male]Those are some very good[br]points,[stopblip][sprite judge assets/characters/judge/judge-surprised-idle.gif][wait 0.2][sprite judge assets/characters/judge/judge-surprised-talk.gif][startblip male] Mr. Wright![sprite judge assets/characters/judge/judge-surprised-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[sprite left assets/characters/phoenix/phoenix-confident-talk.gif][nametag "Phoenix"][cut left][showbox][evidence clear]
[startblip male]Thank you, Your Honor.[stopblip][sprite left assets/characters/phoenix/phoenix-confident-idle.gif][wait 0.4][sprite left assets/characters/phoenix/phoenix-confident-talk.gif][startblip male] I rest[br]my case.[sprite left assets/characters/phoenix/phoenix-confident-idle.gif][stopblip][showarrow][wait 2]
[hidearrow][sound pichoop][wait 0.3]

[music start pwr/trial]

[sprite judge assets/characters/judge/judge-normal-talk.gif][nametag "Judge"][cut judge][showbox][evidence clear]
[startblip male]I hereby declare the defendant,[stopblip][sprite judge assets/characters/judge/judge-normal-idle.gif][wait 0.2][sprite judge assets/characters/judge/judge-normal-talk.gif][startblip male][br]Larry Butz...[sprite judge assets/characters/judge/judge-normal-idle.gif][stopblip][showarrow][wait 2]
[hidebox][music stop][hidearrow][sound pichoop][wait 1]

[verdict set "Not Guilty" white]
[verdict show 0][verdict show 1][verdict show 2]
[verdict show 3][wait 0.2][sound guilty][shake 4 0.1][wait 0.8]
[verdict show 4][verdict show 5][verdict show 6][verdict show 7][verdict show 8][verdict show 9]
[verdict show 3][wait 0.2][sound guilty][shake 4 0.1]
[wait 2]
[verdict clear]

[sprite judge assets/characters/judge/judge-normal-talk.gif][nametag "Judge"][cut judge][showbox][evidence clear]
[startblip male]Court is adjourned![sprite judge assets/characters/judge/judge-normal-idle.gif][stopblip][showarrow][wait 2]
[hidebox][hidearrow][sound pichoop][wait 1]
"""

pages = [
    DialoguePage(parse_line(line)) for line in script.strip().split("\n") if len(line) > 0
]

director = AceAttorneyDirector()
director.set_current_pages(pages)
director.render_movie()