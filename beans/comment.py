from constants import Character

"""
All arguments are optional
user_id: An unique identifier to tell users appart
evidence_path: Path pointing to an image to be used as evidence
user_name: Name of the user
text_content: Text to display
score: Positiveness of a comentary (negative below zero, positive avobe zero)
"""
class Comment:
    def __init__(self,
    user_id: str = None,
    user_name = 'Prosecutor',
    text_content = '...',
    evidence_path: str = None,
    score = 0
    ):
        self.user_name = user_name
        self.user_id = user_id
        self.text_content = text_content
        self.score = score
        self.evidence_path = evidence_path
        self.effective_user_id = self.user_id or self.user_name
        self.character: Character = None
