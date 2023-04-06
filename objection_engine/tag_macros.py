from .ace_attorney_scene import get_sprite_tag
B_M = "<startblip male/>"
B_F = "<startblip female/>"
B_ST = "<stopblip/>"

SPR_PHX_NORMAL_T = B_M + get_sprite_tag('left', 'phoenix', 'normal-talk')
SPR_PHX_NORMAL_I = B_ST + get_sprite_tag('left', 'phoenix', 'normal-idle')
SPR_PHX_SWEAT_T = B_M + get_sprite_tag('left', 'phoenix', 'sweating-talk')
SPR_PHX_SWEAT_I = B_ST + get_sprite_tag('left', 'phoenix', 'sweating-idle')

SPR_EDW_NORMAL_T = B_M + get_sprite_tag('right', 'edgeworth', 'normal-talk')
SPR_EDW_NORMAL_I = B_ST + get_sprite_tag('right', 'edgeworth', 'normal-idle')

SLAM_PHX = B_ST + "<deskslam phoenix/><wait 0.8/>"
SLAM_EDW = B_ST + "<deskslam edgeworth/><wait 0.8/>"

OBJ_PHX = B_ST + "<bubble objection phoenix/><wait 0.8/>"
OBJ_EDW = B_ST + "<bubble objection edgeworth/><wait 0.8/>"
HDI_PHX = B_ST + "<bubble holdit phoenix/><wait 0.8/>"

END_BOX = "<showarrow/><wait 2/><hidearrow/><sound pichoop/><wait 0.3/>"

SHAKE = "<shake 3 0.3/>"
S_DRAMAPOUND = f"<sound dramapound/><flash 0.15/>{SHAKE}"
S_SMACK = f"<sound smack/><flash 0.15/>{SHAKE}"