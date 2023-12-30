from objection_engine.parse_tags import DialogueAction


def compose_gavel_slam(
    num_slams: int = 3,
    delay_between_slams: float = 0.17,
    finish_wait_time: float = 0.766,
):
    if num_slams <= 0:
        return []

    if num_slams == 1:
        return [
            DialogueAction("hidebox", 0),
            DialogueAction("cut gavel", 0),
            DialogueAction("gavel 0", 0),
            DialogueAction("wait 0.3", 0),
            DialogueAction("gavel 1", 0),
            DialogueAction("wait 0.04", 0),
            DialogueAction("gavel 2", 0),
            DialogueAction("wait 0.04", 0),
            DialogueAction("gavel 3", 0),
            DialogueAction("sound gavel", 0),
            DialogueAction("shake 3 0.2", 0),
            DialogueAction(f"wait {finish_wait_time}", 0),
        ]

    commands = [
        DialogueAction("hidebox", 0),
        DialogueAction("cut gavel", 0),
        DialogueAction("gavel 0", 0),
        DialogueAction("wait 0.300", 0),
        DialogueAction("gavel 1", 0),
        DialogueAction("wait 0.04", 0),
        DialogueAction("gavel 3", 0),
        DialogueAction("sound gavel", 0),
        DialogueAction("shake 3 0.2", 0),
        DialogueAction(f"wait {delay_between_slams}", 0),
    ]

    # First and last slams have different duration
    for _ in range(num_slams - 2):
        commands.extend(
            [
                DialogueAction("gavel 2", 0),
                DialogueAction("wait 0.04", 0),
                DialogueAction("gavel 1", 0),
                DialogueAction("wait 0.17", 0),
                DialogueAction("gavel 3", 0),
                DialogueAction("sound gavel", 0),
                DialogueAction("shake 3 0.2", 0),
                DialogueAction(f"wait {delay_between_slams}", 0),
            ]
        )

    # Last slam
    commands.extend(
        [
            DialogueAction("gavel 2", 0),
            DialogueAction("wait 0.04", 0),
            DialogueAction("gavel 1", 0),
            DialogueAction("wait 0.17", 0),
            DialogueAction("gavel 2", 0),
            DialogueAction("wait 0.04", 0),
            DialogueAction("gavel 3", 0),
            DialogueAction("sound gavel", 0),
            DialogueAction("shake 3 0.2", 0),
            DialogueAction(f"wait {finish_wait_time}", 0),
        ]
    )

    return commands
