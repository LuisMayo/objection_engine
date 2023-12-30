from objection_engine.parse_tags import DialogueAction

def compose_verdict(
    text: str,
    slam_group: str = "letter",
    color: str = "white",
    slam_delay: float = 0.0,
    finish_wait_time: float = 2.0,
):
    if slam_group not in ["letter", "word"]:
        raise ValueError(
            f'slam_group "{slam_group}" is not valid; must be "letter" or "word"'
        )
    if color not in ["black", "white"]:
        raise ValueError(f'color "{color}" is not valid; must be "black" or "white"')

    output = []
    output.append(DialogueAction(f'verdict set "{text}" {color}', 0))

    slam_delay_command = f"wait {slam_delay}"
    if slam_group == "letter":
        for i in range(len(text)):
            output.extend(
                [
                    DialogueAction(f"verdict show {i}", 0),
                    DialogueAction("wait 0.2", 0),
                    DialogueAction("sound guilty", 0),
                    DialogueAction("shake 4 0.1", 0),
                ]
            )
            if i != len(text) - 1:
                output.append(DialogueAction(slam_delay_command, 0))

    elif slam_group == "word":
        for i in range(len(text)):
            output.append(DialogueAction(f"verdict show {i}", 0))
            if text[i].isspace():
                output.extend(
                    [
                        DialogueAction("wait 0.2", 0),
                        DialogueAction("sound guilty", 0),
                        DialogueAction("shake 4 0.1", 0),
                        DialogueAction(slam_delay_command, 0),
                    ]
                )
        output.extend(
            [
                DialogueAction("wait 0.2", 0),
                DialogueAction("sound guilty", 0),
                DialogueAction("shake 4 0.1", 0),
            ]
        )

    output.append(DialogueAction(f"wait {finish_wait_time}", 0))
    output.append(DialogueAction("verdict clear", 0))
    return output