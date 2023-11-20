from user import User

class Professor(User):
    def __init__(self, id, firstName, lastName, email, username, department, user_type="professor", following= [], followers=None):
        super().__init__(id, firstName, lastName, email, username, user_type, following, followers)
        self.department = department

    def __str__(self):
        return f"Professor: {self.firstName} {self.lastName},Email:{self.email}, Department: {self.department},ID: {self.id}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'firstName': self.firstName,
            'lasName' : self.lastName,
            'department': self.department,
            'following': self.following
        }