from user import User

class Administrator(User):
    def __init__(self, id, firstName, lastName, email, username):
        super().__init__(id, firstName, lastName, email, username, user_type="administrator")

    def __str__(self):
        return f"Administrador: {self.firstName} {self.lastName}, Email: {self.email}, ID: {self.id}"

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict["user_type"] = self.user_type
        return user_dict