class User:
    def __init__(self,
                 user_id: str,
                 tg_tag: str,
                 notify: bool
                 ):
        self.user_id = user_id
        self.tg_tag = tg_tag
        self.notify = notify
