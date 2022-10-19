## Objection! rendering engine 👨🏼‍⚖️

Code that allows you to convert chains of comments into ace attorney scenes. It's meant to be used by bots or other apps.
List of users:
- [Twiitter Bot](https://github.com/LuisMayo/ace-attorney-twitter-bot)
- [Telegram Bot](https://github.com/LuisMayo/ace-attorney-telegram-bot)
- [Discord Bot](https://github.com/LuisMayo/ace-attorney-discord-bot)

This is a fork of a wonderful [Reddit bot](https://github.com/micah5/ace-attorney-reddit-bot)

## Getting Started

### Prerequisites
 - Python 3. Python 3.8 and 3.9 and 3.10 have been proven to work.
 - FFMPEG instalation. In most Linux distros it should be available in the default package manager. In Windows systems it'd include downloading a [pre-compiled zip folder](https://ffmpeg.org/download.html#build-windows), extracting it and adding the /bin folder into the [system path](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/)

#### Optional
 - [Google Translation API Credentials](https://cloud.google.com/translate/docs/setup): These are needed for language support other than English. Other languages may work even without this credentials as the system will fallback to TextBlob's translation system.
 - Libraqm: Improves text rendering on right-to-left languages. In windows refer to the faq.md

### Installing

Clone the repository

```
git clone https://github.com/LuisMayo/objection_engine
```

Install dependencies (in case any problems are encountered please check faq.md)
You can use either pip
``` bash
python -m pip install .
```
Or poerty
``` bash
poetry install
```



(optional) In case you want language support outside English install polyglot and its dependencies:
(if on windows check faq.md)

```bash
pip install pyICU pycld2 morfessor polyglot
python -m polyglot download TASK:sentiment2
```

Check the exmaple
`python example.py`

### Using it as a library
 - Add this git repository as a library:
`pip install objection_engine`

 - Import it into your python file
``` python
import objection_engine
# You can also import the components like this
from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment
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

### Rendering a video using Docker

``` bash
cp example.py docker-entrypoint.py

docker build --tag objection-engine .
docker run --rm \
  --volume $(pwd)/docker-entrypoint.py:/app/entrypoint.py:ro \
  --volume $(pwd)/assets:/app/assets \
  --volume $(pwd)/outputs:/app/outputs \
  objection-engine
```

The video will be in the `/outputs` directory.

You can download Polyglot models by setting `oe_polyglot_models` environment variable and preserve the data by mounting `/root/polyglot_data`:

``` bash
docker run --rm \
  --volume $(pwd)/docker-entrypoint.py:/app/entrypoint.py:ro \
  --volume $(pwd)/assets:/app/assets \
  --volume $(pwd)/outputs:/app/outputs \
  --volume $(pwd)/polyglot_data:/root/polyglot_data \
  --env oe_polyglot_models="de fr" \
  objection-engine
```

#### Settings
The following environment variables are honored by objection_engine:
- oe_bypass_sentiment: If on any value other than the empty string, the sentiment analysis is bypassed
- oe_stats_server: If present, it will be used as the URL to post statistics to. The server responsible should be similar to https://github.com/LuisMayo/simple-server-counter
- oe_polyglot_models: (docker only) If on polyglot model(s), the data for the model will be downloaded when starting the container.
- OE_DIRECT_H264_ENCODING: If "true" then it will directly encode the videos in H264 with OpenCV, instead of encoding in mp4v and re-encoding later. This is faster than the default, but it requires running on windows or having a self-compiled OpenCV build in your system. If you don't know what any of this means, don't enable it.
## Contributing
Since this is a tiny project we don't have strict rules about contributions. Just open a Pull Request to fix any of the project issues or any improvement you have percieved on your own. Any contributions which improve or fix the project will be accepted as long as they don't deviate too much from the project objectives. If you have doubts about whether the PR would be accepted or not you can open an issue before coding to ask for my opinion.

