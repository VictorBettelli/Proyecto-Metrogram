
import uuid

from like import Like
class Post:
    def __init__(self, date, publisher_id: str, multimedia_type: str, multimedia_url: str,caption: str, hashtag: str):
        self.id = str(uuid.uuid4())
        self.publisher_id = publisher_id
        self.type = multimedia_type
        self.multimedia_url = multimedia_url
        self.caption = caption
        self.hashtag = hashtag
        self.date = date
        self.comments = []
        self.likes = []

    def to_dict(self):
        return {
            'id': self.id,
            'publisher_id': self.publisher_id,
            'caption': self.caption,
            'date': self.date,
            'multimedia_url': self.multimedia_url,
            'comments': [comment.to_dict() for comment in self.comments],
            'likes': [like.to_dict() for like in self.likes]
        }
       

    def add_comment(self, comment):
        self.comments.append(comment)
    
    def eliminar_comentario1(self, user_id, comentario_id):
        comentario = next((comentario for comentario in self.comments if comentario.id == comentario_id and comentario.user_id == user_id), None)
        if comentario:
            self.comments.remove(comentario)
            
    def quitar_like(self, user_id):
        likes_usuario = [like for like in self.likes if like.user_id == user_id]
        
        if likes_usuario:
            # Suponemos que solo hay un like por usuario, pero podrías ajustarlo si eso cambia
            like_a_quitar = likes_usuario[0]
            self.likes.remove(like_a_quitar)
            print("Like quitado con éxito.")
        else:
            print("El usuario no había dado like anteriormente.")


    def add_like(self, user_id):
        if user_id not in [like.user_id for like in self.likes]:
            like = Like(user_id)
            self.likes.append(like)


    def get_comentario_by_id(self, comentario_id):
            return next((comentario for comentario in self.comments if comentario.id == comentario_id), None)
    def cargar_comentarios(self, comentarios):
        self.comentarios = [comentario for comentario in comentarios if comentario.post_id == self.id]
    

    def __str__(self):
        return f"Post - Fecha: {self.date}, Publisher ID: {self.publisher_id}, Multimedia: {self.multimedia_url}, Caption: {self.caption}, Hashtag: {self.hashtag}, Likes: {len(self.likes)}, Comentarios: {len(self.comments)}"
    

    