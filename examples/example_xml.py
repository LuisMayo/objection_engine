from objection_engine.xml_parser import parse_script
from objection_engine.ace_attorney_scene import AceAttorneyDirector
from os.path import dirname, realpath, join
from time import time
from rich import print

pages = parse_script(join(dirname(realpath(__file__)), "test_script.xml"))

director = AceAttorneyDirector()
director.set_current_pages(pages)
director.render_movie(output_filename=f'example-xml-{int(time())}.mp4')