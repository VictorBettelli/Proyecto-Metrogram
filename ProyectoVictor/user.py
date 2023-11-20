
class User:
    def __init__(self, id, firstName, lastName, email, username, user_type, following=None, followers=None):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.username = username
        self.user_type = user_type
        self.solicitudes_seguimiento=[]
        self.following =  []
        self.followers = []
        self.administrator = False

    def to_dict(self):
        user_dict = {
            "id": self.id,
            "name": self.firstName,
            "last_name": self.lastName,
            "email": self.email,
            "username": self.username,
            "user_type": self.user_type
        }
        return user_dict


    def follow(self, user_id):
        self.following.append(user_id)

    def dejar_de_seguir(self, user_id):
        if user_id in self.following:
            self.following.remove(user_id)
            print(f"Dejaste de seguir al usuario con ID: {user_id}")
        else:
            print(f"No estás siguiendo al usuario con ID: {user_id}")

    def agregar_solicitud_seguimiento(self, user_id):
        self.solicitudes_seguimiento.append(user_id)
        print(f"Solicitud de seguimiento enviada al usuario con ID: {user_id}")
    


    


    