class Comment:
    def __init__(self,
    user_id: str,
    evidence_path: str,
    user_name = 'Prosecutor',
    text_content = '...',
    score = 0
    ):
        self.user_name = user_name
        self.user_id = user_id
        self.text_content = text_content
        self.score = score
        self.evidence_path = evidence_path