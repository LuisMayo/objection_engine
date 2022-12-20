# DialogueAction Commands
Objection 4 allows for fine control of the way that dialogue plays out. This
document describes all of the currently-supported `DialogueAction` commands.

## Character control
### `sprite <position> <path>`
Sets the sprite at the given `position` to the file found at `path`.

#### Valid positions
The valid `position` values are:
- `left` for the left side of the courtroom, i.e. where Phoenix stands
- `center` for the center of the courtroom, i.e. where the witnesses stand
- `right` for the right side of the courtroom, i.e. where the prosecutor stands
- `judge` for the judge's seat
- `leftzoom` for the "action lines" background moving left
- `rightzoom` for the "action lines" background moving right

## Displaying elements
### `showarrow`
Shows the "next dialogue" arrow in the corner of the dialogue box.

### `hidearrow`
Hides the "next dialogue" arrow in the corner of the dialogue box.

### `showbox`
Shows the dialogue box.

### `hidebox`
Hides the dialogue box.

### `nametag <name>`
Sets the text in the nametag of the dialogue box to `name`.

### `evidence <side> <path>`
Shows or hides evidence.

If `side` is `clear`, whatever evidence is currently shown on-screen is hidden.

Otherwise, `side` must be `left` or `right`; the evidence will appear on that
side of the screen. The argument `path` specifies the path to the image file
in the evidence "bubble".

## Visual effects
### `shake <magnitude> <duration>`
Shakes the screen with a given `magnitude` for `duration` seconds.

### `flash <duration>`
Turns the screen white for `duration` seconds.

### `bubble <type> <character>`
Animates an exclamation bubble of a given `type`, with a given `character`'s
voice.

The `type` may be one of the following:
- `objection` for "Objection!"
- `holdit` for "Hold it!"
- `takethat` for "Take that!"

The `character` should be the ID of the character making the exclamation, i.e.
the name of their folder in the `characters` folder. If they don't have an audio
file that corresponds to the bubble, a generic sound will be used instead.


## Music and sound
### `music start <path>`
Starts playing the music track. inside the assets "music" folder
titled `<path>.mp3`. By including slashes in `path`, you can reference a file
in subfolders of the "music" folder. For example, the command to start playing
the *Objection!* theme from *Phoenix Wright: Ace Attorney* would be
`music start pwr/objection`.

### `music stop`
Stops the currently-playing music.

### `sound <name>`
Plays the sound effect inside the assets "sound" folder titled
`sfx-<name>.wav`. For example, the command to play the sound file titled
`sfx-bang.wav` would be `sound bang`.

### `startblip <gender>`
Starts playing the voice "blip" sound effect on loop. It should be canceled
with the `stopblip` command. The `gender` argument can be `male` or `female`.

### `stopblip`
Stops playing the currently-playing voice "blip" sound effect.

## Camera control
### `cut <position>`
Immediately moves the camera to the specified `position`.

See the documentation for the `sprite` command for valid `position` values.

### `pan <position>`
Performs the "courtroom pan" animation from the camera's current position
to the specified `position`. The animation takes `0.5` seconds,
**but this command does not block execution of later commands.** If you want to
wait for the animation to finish before executing subsequent commands, include
a `wait 0.5` command after this command.

See the documentation for the `sprite` command for valid `position` values.

## Scene flow
### `wait <duration>`
Pauses execution of commands for `duration` seconds.