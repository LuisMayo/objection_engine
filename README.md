## Objection! rendering engine 👨🏼‍⚖️

Code that allows you to convert chains of comments into ace attorney scenes. It's meant to be used by bots or other apps.
List of users:
- [Twiitter Bot](https://github.com/LuisMayo/ace-attorney-twitter-bot)
- [Telegram Bot](https://github.com/LuisMayo/ace-attorney-telegram-bot)
- [Discord Bot](https://github.com/LuisMayo/ace-attorney-discord-bot)

This is a fork of a wonderful [Reddit bot](https://github.com/micah5/ace-attorney-reddit-bot)

## Getting Started

### Prerequisites

 - Python 3
 - Ace Attorney data. Download it [here](https://drive.google.com/drive/folders/1jNpnB3pjHFvOyrfZ-WxlOXNaZ-XH4INx?usp=sharing) and put them in `./assets/`
 - FFMPEG instalation. In most Linux distros it should be available in the default package manager, although it may have some caveats (more info on faq.md). In Windows systems it'd include downloading a [pre-compiled zip folder](https://ffmpeg.org/download.html#build-windows), extracting it and adding the /bin folder into the [system path](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/)

#### Optional
 - [Google Translation API Credentials](https://cloud.google.com/translate/docs/setup): These are needed for language support other than English. Other languages may work even without this credentials as the system will fallback to TextBlob's translation system.
 
### Installing

Clone the repository

```
git clone https://github.com/LuisMayo/objection_engine
```
Install dependencies (in case any problems are encountered please check faq.md)
``` bash
python -m pip install -r requirements.txt
```

Install OpenCV if you are on Windows (if you're on Linux and you don't have a working installation check faq.md)
`pip install opencv-python`

In case you want language support outside English install polyglot and its dependencies:
(if on windows check faq.md)

```bash
pip install pyICU pycld2 morfessor polyglot
python -m polyglot download TASK:sentiment2
```

Check the exmaple
`python example.py`

### Using it as a library
 - Add it as a library with 
`git submodule add https://github.com/LuisMayo/objection_engine.git`

 - Import it into your python file
``` python
import sys
sys.path.append('objection_engine/')
import objection_engine
```
 - Create a list of comments
``` python
foo = [objection_engine.comment.Comment(), objection_engine.comment.Comment(text_content='Second comment',  user_name="Second user")]
```
 - Render the list
``` python
objection_engine.renderer.render_comment_list(foo)
```
For a list of arguments to the class and method check both https://github.com/LuisMayo/objection_engine/blob/main/renderer.py and https://github.com/LuisMayo/objection_engine/blob/main/beans/comment.py

There is a complete example in https://github.com/LuisMayo/objection-engine-testing

## Contributing
Since this is a tiny project we don't have strict rules about contributions. Just open a Pull Request to fix any of the project issues or any improvement you have percieved on your own. Any contributions which improve or fix the project will be accepted as long as they don't deviate too much from the project objectives. If you have doubts about whether the PR would be accepted or not you can open an issue before coding to ask for my opinion

