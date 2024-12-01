class Student:
    def __init__(self,
                 student_id: str,
                 tg_tag: str,
                 notify: bool
                 ):
        self.student_id = student_id
        self.tg_tag = tg_tag
        self.notify = notify

