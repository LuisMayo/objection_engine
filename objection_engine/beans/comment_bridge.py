from .comment import Comment
"""
Internal use only, do not use outside here
"""
class CommentBridge:
  def __init__(self, comment: Comment):
    self.author = Author(comment.user_name)
    self.body = comment.text_content
    self.score = comment.score
    self.evidence = comment.evidence_path
    self.character = comment.character

class Author:
    def __init__(self, name):
        self.name = name
