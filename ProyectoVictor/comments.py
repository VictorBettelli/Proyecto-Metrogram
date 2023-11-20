import uuid
from datetime import datetime 
class Comment:
    def __init__(self, user_id, post_id, comentario):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.post_id = post_id
        self.comentario = comentario
        self.fecha_publicacion = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def __str__(self):
        return f"Comentario - ID: {self.id}, Usuario ID: {self.user_id}, Post ID: {self.post_id}, Comentario: {self.comentario}, Fecha: {self.fecha_publicacion}"