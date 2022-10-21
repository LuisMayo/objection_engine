from ..constants import Character


class Comment:
    def __init__(self,
    user_id: str = None,
    user_name: str = 'Prosecutor',
    text_content: str = '...',
    evidence_path: str = None,
    score: float = 0
    ):
        """
        All arguments are optional
        :param str user_id: An unique identifier to tell users appart
        :param str evidence_path: Path pointing to an image to be used as evidence
        :param str user_name: Name of the user
        :param str text_content: Text to display
        :param float score: Positiveness of a commentary (negative below zero, positive above zero)
        """
        self.user_name = user_name
        self.user_id = user_id
        self.text_content = text_content
        self.score = score
        self.evidence_path = evidence_path
        self.effective_user_id = self.user_id or self.user_name
        self.character: Character = None
