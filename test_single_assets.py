import anim
import constants


item = constants.Character().KLAVIER
for thing in constants.character_emotions[item]:
    for emotion in constants.character_emotions[item][thing]:
        scene = [
            {
                "location": constants.character_location_map[item],
                "audio": "03 - Turnabout Courtroom - Trial",
                "scene": [
                    {
                        "action": constants.Action.TEXT,
                        "character": item,
                        "emotion" : emotion,
                        "text": f"TESTING ASSETS {item}: Emotion : {emotion}"
                    }
                ]
            }
        ]
        anim.ace_attorney_anim(scene, output_filename=f"asset_test_{item}_{emotion}.mp4")
