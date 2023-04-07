# Creating a Custom Music Pack
*Objection 4* makes it very easy to add custom music packs. In this tutorial,
I'll walk through the process of creating a music pack for music from
*Phoenix Wright: Ace Attorney ~ Dual Destinies*.

**NOTE:** You'll need access to the `assets` folder of *Objection* in order to
add custom music packs. If you're using the public social media bots, this won't
work.

## Setting up the pack folder
Inside of the `music` folder, create a new folder with an ID for your music
pack. The name can be anything, as long as it is a valid folder name.

For this example, I'll name the folder `dd`.

The folder will also need a `config.toml` file. Copy the file named
`config_template.toml` from the `music` folder into your new folder, and rename
it to `config.toml`. For now, we'll leave it be at that.

## Getting the music
The bulk of the work is finding the music tracks and downloading them. Though
*Objection* doesn't require the tracks to have specific filenames, it's good
practice to use the same names as the existing packs, so others can easily
tell what music corresponds to what phase:
- `cross-moderato.mp3` is usually a game's *Cross-Examination ~ Moderato* theme
- `trial.mp3` is a game's *Trial* theme
- `objection.mp3` is a game's *Objection!* theme
- `press.mp3` is a game's *Pursuit* theme

## Setting up `config.toml`
If you only wanted to use music files with the names above, then congrats -
you're done! The `config_template.toml` file comes with those names pre-written.

If your music files have different names, updating the `config.toml` file to
use them is quite easy. It only consists of two arrays:
- **`relaxed`** is a list of music tracks to start playing at the
beginning of the video, before the conversation gets heated.
- **`tense`**, on the other hand, is a list of tracks to start playing once the
conversation heats up.

## The final product
The finished `dd` folder looks like this:
```
dd
├ config.toml
├ cross-moderato.mp3
├ objection.mp3
├ press.mp3
└ trial.mp3
```

Let's hear it in action!
```python
from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment

comments = [
    Comment(
        user_name="Phoenix",
        text_content="Hello, everyone. My name is Phoenix.",
    ),
    Comment(
        user_name="Phoenix",
        text_content="The defense is ready, Your Honor!"
    ),
    Comment(
        user_name="Phoenix",
        text_content="And here's a little more text! Isn't this cool?",
    )
]
render_comment_list(comments, music_code='dd')
```

<iframe width="560" height="315" src="https://www.youtube.com/embed/3ayAHL5blPA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>