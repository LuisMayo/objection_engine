"""
Test script to compare performance of the v3 engine and v4 engine
on identical comment chains, but using the v4 API.
"""

from timeit import default_timer as timer
from time import time
from objection_engine.beans.comment import Comment
from rich import print

# Using same comments as a previous test
from .example_compare_v3_and_v4 import comments

current_time = int(time())


from objection_engine.ace_attorney_scene import DialogueBoxBuilder

# In here, the sprite data 
box_builder = DialogueBoxBuilder()
