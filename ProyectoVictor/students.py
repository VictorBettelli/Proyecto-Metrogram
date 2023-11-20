from user import User

class Student(User):
    def __init__(self, id, firstName, lastName, email, username, major, user_type="student", following=[], followers=None):
        super().__init__(id, firstName, lastName, email, username, user_type, following, followers)
        self.major = major

    def __str__(self):
        return f"Student: {self.firstName} {self.lastName},Email:{self.email} , Major: {self.major},ID: {self.id}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'firstName': self.firstName,
            'lasName' : self.lastName,
            'major': self.major,
            'following': self.following
        }
    