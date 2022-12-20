# Structure of a Scene
The Objection 4 engine introduces a more transparent, editable structure
for scenes than was present in Objection 3.

In short:
- A scene is made up of a list of `DialoguePage` objects.
    - Each `DialoguePage` has a list of objects inheriting from `BaseDialogueItem`:
        - A `DialogueTextChunk` displays a snippet of text in the text box.
        - A `DialogueTextLineBreak` causes subsequent text to be displayed
        on the next line down.
        - A `DialogueAction` causes some action to be performed. For more
        information on what actions can be triggered, see
        [DialogueAction Commands](DialogueActionCommands.md).

The engine will move through all of the `DialoguePage`s in sequence, and within
them, all of the `BaseDialogueItem`s in sequence. Once all of the
`DialoguePage`s have been completed, the engine will stop rendering frames and
begin compositing them into the finished video.
