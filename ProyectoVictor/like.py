class Like:
    def __init__(self, user_id):
        self.user_id = user_id

    def to_dict(self):
        return {
            'user_id': self.user_id
        }
        