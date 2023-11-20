import json 
import requests
from datetime import datetime
import uuid
from typing import Dict,Union,List  


from timeline import Timeline 
from professor import Professor
from students import Student
from administrator import Administrator
from comments import Comment 
from post import Post
from like import Like


 
class App:
    def __init__(self):
        """Inicializa la aplicación con listas vacías para usuarios, posts, comentarios, e información del usuario conectado.
        #Carga usuarios y posts desde las APIs proporcionadas al crear una instancia de la aplicación."""
        
        self.users = []
        self.posts = []
        self.comments = []
        self.logged_user_id = None
        self.cargar_usuarios_desde_api(api_url)
        self.cargar_post_desde_api(url_post)
 

    def iniciar_sesion(self):
        print("Iniciar Sesión")
        username = input("Ingrese su username: ")
        password = input("Ingrese su contraseña: ")

        user_id = self.obtener_user_id_por_username(username)

        if user_id:
            self.logged_user_id = user_id
            self.logged_user_administrator = self.es_administrador(username)  # Nueva propiedad para el usuario administrador
            print(f"Sesión iniciada como {username} (ID: {self.logged_user_id})")
            self.seguir_usuarios_auto(self.logged_user_id)

            return self.logged_user_id

        else:
            print("Usuario no encontrado. Verifique su username e intente nuevamente.")
            return None
 
    def es_administrador(self, username):
        usuario = next((user for user in self.users if user.username == username), None)

        if usuario and usuario.administrator:
            return True
        else:
            return False
    
#Obtiene el ID de usuario correspondiente a un nombre de usuario dado.
#Retorna el ID si se encuentra el usuario, de lo contrario, retorna None
    
    def obtener_user_id_por_username(self, username):
        user = next((user for user in self.users if user.username == username), None)
        
        if user:
            print(f"Usuario encontrado: {user.username} (ID: {user.id})")
            return user.id
        else:
            print(f"Usuario no encontrado para el username: {username}")
            return None



    

        
    
    def menu(self):
        usuario_id = None

        while True:
            print("\n---- Menú Principal ----")
            print("1. Iniciar Sesión")
            print("2. Registrarse")
            print("3. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                usuario_id = self.iniciar_sesion()
                if usuario_id:
                    self.realizar_acciones_despues_inicio_sesion(usuario_id)
            elif opcion == "2":
                self.crear_user()
            elif opcion == "3":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")
    
    def realizar_acciones_despues_inicio_sesion(self, usuario_id):
        #Realiza acciones específicas después de que un usuario ha iniciado sesión.
        if usuario_id:
            # Cargar posts después de iniciar sesión
            self.cargar_post_desde_api(url_post)
            self.submenu_gestion_multimedia(usuario_id)
        else:
            print("Inicio de sesión fallido. Usuario no encontrado.")
                
   
    def submenu_gestion_multimedia(self, usuario_id):
        while True:
            print("\n---- Submenú Gestión Multimedia ----")
            print("1. Ajustes del Perfil")
            print("2. Ver mis Posts")
            print("3. Buscar Usuario")
            print("4. Buscar Posts")
            print("5. Publicar Post")
            print("6. Ver Timeline")
            print("7. Seguir/Dejar de seguir Usuario")
            if self.logged_user_administrator:  # Mostrar opción de moderación solo si es administrador
                print("8. Moderación")
            print("9. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.submenu_gestion_perfil(usuario_id)
            elif opcion == "2":
                self.ver_posts(usuario_id)
            elif opcion == "3":
                self.buscar_perfiles(usuario_id)
            elif opcion == "4":
                self.buscar_posts(usuario_id)
            elif opcion == "5":
                self.registrar_post(usuario_id)
            elif opcion == "6":
                self.mostrar_timeline(usuario_id)
            elif opcion == "7":
                self.submenu_seguir_usuarios(usuario_id)
            elif opcion == "8" and self.logged_user_administrator:
                self.submenu_moderacion()
            elif opcion == "9":
                print("Volviendo al Menú Principal...")
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")

    def submenu_seguir_usuarios(self, usuario_id):
        while True:
            print("\n---- Submenú Seguir/Dejar de seguir ----")
            print("1. Seguir Usuario")
            print("2. Dejar de seguir Usuario")
            print("3. Volver al Menú Anterior")

            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.seguir_usuario(usuario_id)
            elif opcion == "2":
                self.dejar_de_seguir(usuario_id)
            elif opcion == "3":
                print("Volviendo al Menú Anterior...")
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")

    def submenu_gestion_perfil(self,usuario_id):
        while True:
            print("""
                1. Cambiar informacion personal 
                2. Borrar datos de la cuenta  
                3. salir      
            """)

            accion = input("Por favor seleccione el número de la acción que desea realizar:")

            if accion == "1":
                self.modificar_usuario(usuario_id)

            elif accion == "2":
                self.borrar_datos_usuario(usuario_id)

            elif accion == "3":
                break

    def cargar_usuarios_desde_api(self, api_url):
        #Carga datos de usuarios desde una API y crea instancias de usuarios correspondientes.
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            usuarios_data = response.json()

            for user_data in usuarios_data:
                user_type = user_data.get("type", "")
                user = None

                if user_type == "professor":
                    user = Professor(
                        id=user_data["id"],
                        firstName=user_data["firstName"],
                        lastName=user_data["lastName"],
                        email=user_data["email"],
                        username=user_data["username"],
                        user_type=user_type,
                        department=user_data["department"],
                    )
                elif user_type == "student":
                    user = Student(
                        id=user_data["id"],
                        firstName=user_data["firstName"],
                        lastName=user_data["lastName"],
                        email=user_data["email"],
                        username=user_data["username"],
                        user_type=user_type,
                        major=user_data["major"],
                    )
                else:
                    print(f"Tipo de usuario no válido: {user_type}")
                    continue

                # Obtener la lista de seguimiento desde los datos cargados
                if "following" in user_data:
                    user.following = user_data["following"]

                # Cargar solicitudes de seguimiento
                if "solicitudes_seguimiento" in user_data:
                    user.solicitudes_seguimiento = user_data["solicitudes_seguimiento"]

                self.users.append(user)

        except requests.RequestException as e:
            print(f"Error en la solicitud: {e}")

        # Gestion de Perfil 
    
    def crear_user(self):
        # Permite al usuario crear un nuevo usuario y lo agrega a la lista de usuarios.
        id = str(uuid.uuid4())
        name = input("Por favor ingrese su Nombre: ")
        last_name = input("Por favor ingrese su Apellido: ")
        email = input("Por favor ingrese su Email: ")

        print("Si es un profesor Ingrese P")
        print("Si es alumno Ingrese A")
        print("Si es administrador Ingrese AD")
        options = input(" Ingresa si usted es un profesor, alumno o administrador: ").upper()

        if options == "P":
            department = input("Por favor ingrese el departamento a el que corresponde: ")
            new_user = Professor(id, name, last_name, email, input("Ingrese el nombre de usuario: "), department)
        elif options == "A":
            major = input("Por favor ingrese la carrera que estudia: ")
            new_user = Student(id, name, last_name, email, input("Ingrese el nombre de usuario: "), major)
        elif options == "AD":
            new_user = Administrator(id, name, last_name, email, input("Ingrese el nombre de usuario: "))
            new_user.administrator = True

        else:
            print("Opción no válida.")
            return

        self.users.append(new_user)
        print("Usuario registrado con éxito.")

        # Añadir la información a un archivo
        self.guardar_usuarios_en_archivo()

    def user_to_dict(self, user: Union[Professor, Student]) -> Dict[str, Union[str, int, list]]:
        #Convierte la información del usuario a un formato de diccionario.
       
        user_data = {
            "id": user.id,
            "firstName": user.firstName,  # Cambiado de 'name' a 'firstName'
            "lastName": user.lastName,
            "email": user.email,
            "username": user.username,
            "type": user.user_type,
            "following": user.following
        }

        if isinstance(user, Professor):
            user_data["department"] = user.department
        elif isinstance(user, Student):
            user_data["major"] = user.major

        return user_data


    def find_user(self, criterio, valor):
        #Busca usuarios según un criterio y un valor específicos.
        #Retorna una lista de usuarios que cumplen con el criterio y valor dados.
        resultados = [usuario for usuario in self.users if getattr(usuario, criterio, None) == valor]
        return resultados
    
    def buscar_perfiles(self, usuario_id):
        #Permite al usuario buscar perfiles de otros usuarios según un criterio y un valor.
        criterio = input("Ingrese el criterio de búsqueda (major/departamento/username): ")
        valor = input("Ingrese el valor a buscar: ")

        resultados = self.find_user(criterio, valor)

        if resultados:
            print("Resultados de la búsqueda:")
            for usuario in resultados:
                print(usuario)
        else:
            print("No se encontraron resultados.")

    def modificar_usuario(self,usuario_id):
        #Modifica la información de un usuario específico.
        username = input("Ingrese el username del usuario a modificar: ")
        usuario = next((user for user in self.users if user.username == username), None)

        if usuario:
            print(f"Información actual del usuario con username {username}:")
            print(usuario.__dict__)

            nuevo_name = input("Nuevo nombre: ")
            nuevo_last_name = input("Nuevo apellido: ")
            nuevo_email = input("Nuevo email: ")
            nuevo_username = input("Nuevo username: ")
            

            setattr(usuario, "firstName", nuevo_name)
            setattr(usuario, "lastName", nuevo_last_name)
            setattr(usuario, "email", nuevo_email)
            setattr(usuario, "username", nuevo_username)

            print("Información del usuario actualizada:")
            print(usuario.__dict__)
        else:
            print(f"No se encontró información para el usuario con username {username}.")

    def borrar_datos_usuario(self,usuario_id):
        #Permite al usuario borrar los datos de su cuenta.
        username = input("Ingrese el username del usuario a borrar: ")
        usuario = next((user for user in self.users if user.username == username), None)

        if usuario:
            print(f"Información actual del usuario con nombre {username}:")
            print(usuario.__dict__)

            confirmacion = input("¿Está seguro de que desea borrar los datos de este usuario? (s/n): ").lower()

            if confirmacion == 's':
                # Borrar el usuario
                self.users.remove(usuario)
                print(f"Datos del usuario con nombre {username} borrados.")
            else:
                print("Operación cancelada.")
        else:
            print(f"No se encontró información para el usuario con nombre {username}.")


    # GESTION DE MULTIMEDIA.

    def cargar_post_desde_api(self, url_post):
        #Carga datos de posts desde una API y crea instancias de posts correspondientes.
        try:
            response1 = requests.get(url_post)
            response1.raise_for_status()
            posts_data = response1.json()

            for post_data in posts_data:
                post = Post(
                    date=post_data["date"],
                    publisher_id=post_data["publisher"],
                    multimedia_type=post_data["type"],
                    multimedia_url=post_data["multimedia"]["url"],
                    caption=post_data["caption"],
                    hashtag=post_data["tags"][0] if post_data["tags"] else ""  # Tomamos el primer hashtag si hay alguno
                )

                self.posts.append(post)

        except requests.RequestException as e:
            print(f"Error en la solicitud: {e}")

    def registrar_post(self, usuario_id):
        #Permite a un usuario registrado crear y publicar un nuevo post.
        username = input("Ingrese el username del usuario que sube el post: ")
        usuario = next((user for user in self.users if user.username == username), None)

        if not usuario:
            print(f"No se encontró información para el usuario con username {username}.")
            return

        multimedia_type = input("Ingrese el tipo de multimedia (photo/video): ")
        multimedia_url = input("Ingrese la URL de la foto o video del post: ")
        caption = input("Ingrese la descripción del post (caption): ")
        hashtag = input("Ingrese el hashtag del post: ")

        nuevo_post = Post(
            datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            usuario.id,  
            multimedia_type,
            multimedia_url,
            caption,
            hashtag
        )

        if not multimedia_type or not multimedia_url or not caption or not hashtag:
            print("Por favor, complete todos los campos.")
            return

        self.posts.append(nuevo_post)

        # Añadir el nuevo post a la línea de tiempo del usuario
        user_timeline = Timeline(usuario.id)
        user_timeline.add_post(nuevo_post)

        print("Post registrado exitosamente.")


    

    
#Un usuario (A) puede ver el post de otro usuario (B), siempre que A siga a B: 
# Para ver el post deberá mostrar los datos del mismo con su lista de likes y comentarios.
#Adicionalmente este puede comentar

    
    def mostrar_post(self, post):
        #Muestra detalles de un post específico, incluyendo comentarios y likes.
        print("Detalles del post:")
        print(f"Caption: {post.caption}")
        print(f"Fecha de publicación: {post.date}")
        print(f"Multimedia: {post.multimedia_url}")
        print("Comentarios:")
        
        for comment in post.comments:
            print(f"- {comment.comentario} (Usuario: {comment.user_id})")

        print("Likes:")
        print(f"Cantidad de Likes: {len(post.likes)}")

        if post.likes:
            print("Usuarios que dieron like:")
            for like in post.likes:
                usuario = self.get_user_by_id(like.user_id)
                if usuario:
                    print(f"- {usuario.username}")
        else:
            print("Este post no tiene likes.")

    def ver_posts(self, usuario_id):
        #Muestra los posts de un usuario específico y permite al usuario interactuar con ellos.
        
        for post in self.posts:
            publisher_id = post.publisher_id
            # Comparar con el usuario que ha iniciado sesión (usuario_id), no con el atributo 'id' de la clase Post
            if publisher_id == usuario_id:
                print(f"Fecha de publicación: {post.date}")
                print(f"Multimedia: {post.multimedia_url}")
                print("¿Quieres ver detalles y comentar? (s/n)")
                opcion = input().lower()
                if opcion == 's':
                    self.mostrar_post(post)
                    # Preguntar si el usuario quiere agregar un comentario o like
                    self.interactuar_con_post(post, usuario_id)

    



    def buscar_posts(self, usuario_id):
        # Permite al usuario buscar los posts de otro usuario por su nombre de usuario.
        otro_usuario_username = input("Por favor ingrese el username del usuario: ")

        # Verificar si ya estás siguiendo al usuario
        usuario = self.get_user_by_id(usuario_id)
        otro_usuario = self.obtener_user_por_username(otro_usuario_username)

        if otro_usuario and usuario:
            if otro_usuario.id in usuario.following:
                print(f"Mostrando los posts de {otro_usuario_username}:")
                self.ver_posts(otro_usuario.id)
            else:
                print(f"No estás siguiendo a {otro_usuario_username}. ¿Deseas seguirlo? (s/n)")
                opcion = input().lower()

                if opcion == 's':
                    self.seguir_usuario(usuario_id)
                    print(f"Mostrando los posts de {otro_usuario_username}:")
                    self.ver_posts(otro_usuario.id)
                else:
                    print(f"No estás siguiendo a {otro_usuario_username}. No puedes ver sus posts.")
        else:
            print("Usuario no encontrado.")



#Gestion de Interacciones 
    def obtener_post_por_id(self, post_id):
        # Obtiene un objeto de post por su ID
        post = next((post for post in self.posts if post.id == post_id), None)
        if post:
            # Asegúrate de cargar los comentarios asociados al post
            post.cargar_comentarios(self.comments)
        return post
    
    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def obtener_user_por_username(self, username):
        usuario = next((user for user in self.users if user.username.lower() == username.lower()), None)
        return usuario
    
    def seguir_usuario(self, usuario_id):
        otro_usuario_username = input("Ingrese el username del usuario que desea seguir: ")
        otro_usuario = self.obtener_user_por_username(otro_usuario_username)
        usuario = self.get_user_by_id(usuario_id)

        if usuario and otro_usuario:
            if otro_usuario.id in usuario.following:
                print(f"Ya sigues a {otro_usuario.username}.")
            else:
                # Nueva lógica para seguir automáticamente si estudian la misma carrera
                if isinstance(usuario, Student) and isinstance(otro_usuario, Student) and usuario.major == otro_usuario.major:
                    print(f"Automáticamente sigues a {otro_usuario.username} porque estudian la misma carrera.")
                    usuario.follow(otro_usuario.id)
                else:
                    aprobacion = input(f"¿Quieres seguir a {otro_usuario.username}? (s/n): ")
                    if aprobacion.lower() == 's':
                        usuario.follow(otro_usuario.id)
                        print(f"Ahora sigues a {otro_usuario.username}.")
                    else:
                        print(f"No estás siguiendo a {otro_usuario.username}.")

                        aprobacion_solicitud = input(f"¿Quieres enviar una solicitud de seguimiento a {otro_usuario.username}? (s/n): ")
                        if aprobacion_solicitud.lower() == 's':
                            usuario.agregar_solicitud_seguimiento(otro_usuario.id)
                            print(f"Solicitud de seguimiento enviada a {otro_usuario.username}.")
                        else:
                            print(f"No estás siguiendo a {otro_usuario.username} y no has enviado una solicitud de seguimiento.")
        else:
            print("Usuario no encontrado.")

    def guardar_post_en_archivo(self, post):
        # Lógica para guardar el post en un archivo
        with open('posts.txt', 'a') as file:
            file.write(f"Fecha: {post.date}, Multimedia: {post.multimedia_url}\n")
            
            # Guardar comentarios
            file.write("Comentarios:\n")
            for comment in post.comments:
                file.write(f"- {comment.comentario} (Usuario: {comment.user_id})\n")

            # Guardar likes
            file.write("Likes:\n")
            for like in post.likes:
                file.write(f"- Usuario que dio like: {like.user_id}\n")

    

   

    def dejar_de_seguir(self, usuario_id):
        otro_usuario_username = input("Ingrese el username del usuario que desea dejar de seguir: ")
        otro_usuario = self.obtener_user_por_username(otro_usuario_username)

        usuario = self.get_user_by_id(usuario_id)

        if usuario and otro_usuario:
            usuario.dejar_de_seguir(otro_usuario.id)
            print(f"Ahora no sigues a {otro_usuario.username}.")
        else:
            print("Usuario no encontrado.")


    def comentar_post(self, usuario_id, post_id, comentario_texto):
        usuario = self.get_user_by_id(usuario_id)
        post = self.obtener_post_por_id(post_id)

        if usuario and post:
            comentario = Comment(usuario.id, post.id, comentario_texto)
            post.add_comment(comentario)
            self.guardar_comentario_en_archivo(comentario)
            print("Comentario agregado con éxito.")
        else:
            print("Usuario o post no encontrado.")

    def eliminar_comentario_ofensivo(self, post_id, comentario_id):
        post = self.obtener_post_por_id(post_id)

        if post:
            comentario = post.get_comentario_by_id(comentario_id)
            if comentario:
                # Verificar que el usuario que quiere eliminar el comentario sea el dueño del post
                if comentario.user_id == post.publisher_id:
                    post.eliminar_comentario(comentario)
                    print("Comentario eliminado con éxito.")
                else:
                    print("Solo el dueño del post puede eliminar comentarios.")
            else:
                print("Comentario no encontrado.")
        else:
            print("Post no encontrado.")

    
    def interactuar_con_post(self, post, usuario_id):
        accion = input("¿Quieres agregar un comentario (C) o dar like (L)? (C/L): ").lower()

        if accion == 'c':
            comentario = input("Escribe tu comentario: ")
            self.comentar_post(usuario_id, post.id, comentario)
        elif accion == 'l':
            self.dar_like( post.id) 

    def comentar_post(self, usuario_id, post_id, comentario_texto):
        usuario = self.get_user_by_id(usuario_id)
        post = self.obtener_post_por_id(post_id)

        if usuario and post:
            comentario = Comment(usuario.id, post.id, comentario_texto)
            post.add_comment(comentario)  # Utilizar add_comment en lugar de Post.add_comment
            self.guardar_comentario_en_archivo(comentario)
            print("Comentario agregado con éxito.")
        else:
            print("Usuario o post no encontrado.")
    

    def dar_like(self, post_id):
        post = self.obtener_post_por_id(post_id)

        if post:
            # Verificar si el usuario ya dio like
            if self.logged_user_id not in [like.user_id for like in post.likes]:
                # Agregar el like al post
                like = Like(self.logged_user_id)
                post.likes.append(like)
                
                # Guardar el post actualizado en el archivo o donde lo estás almacenando
                self.guardar_post_en_archivo(post)

                # Mostrar la cantidad de likes
                print(f"Like agregado al post. Cantidad de Likes: {len(post.likes)}")
            else:
                # El usuario ya dio like, ofrecer la opción de retirar el like
                opcion_retirar_like = input("Ya has dado like a este post. ¿Quieres retirar tu like? (s/n): ").lower()

                if opcion_retirar_like == 's':
                    # Retirar el like del post
                    post.likes = [like for like in post.likes if like.user_id != self.logged_user_id]

                    # Guardar el post actualizado en el archivo o donde lo estás almacenando
                    self.guardar_post_en_archivo(post)

                    # Mostrar la cantidad de likes después de retirar el like
                    print(f"Like retirado del post. Cantidad de Likes: {len(post.likes)}")
                else:
                    print("No se ha retirado el like.")
        else:
            print("Post no encontrado.")


    def seguir_usuarios_auto(self, usuario_id):
        usuario = self.get_user_by_id(usuario_id)

        if usuario:
            # Imprimir información de depuración
            print(f"Usuario {usuario.username} - following: {usuario.following}")

            # Obtener la lista de usuarios a seguir automáticamente del usuario que inició sesión
            followings_to_add = usuario.following

            # Iterar sobre la lista de usuarios y seguir automáticamente solo a aquellos a los que no sigues
            for otro_usuario_id in followings_to_add:
                if otro_usuario_id != usuario_id and otro_usuario_id not in usuario.following:
                    otro_usuario = self.get_user_by_id(otro_usuario_id)
                    if otro_usuario:
                        usuario.following.append(otro_usuario_id)
                        print(f"Siguiendo automáticamente a {otro_usuario.username}")

            # Guardar los cambios en el archivo de usuarios
            self.guardar_usuarios_en_archivo()

            print("Proceso de seguimiento automático completado.")
        else:
            print("Usuario no encontrado.")

    def guardar_usuarios_en_archivo(self):
        with open("userss.txt", 'w') as file:
            json.dump([user.to_dict() for user in self.users], file)

            

    def mostrar_likes(self, post):
        print(f"Likes en el post de {post.publisher_username}:")
        for user_id in post.likes:
            user = self.get_user_by_id(user_id)
            if user:
                print(f"- {user.username}")
            else:
                print(f"- Usuario no encontrado")

    def guardar_comentario_en_archivo(self, comentario):
        with open("comments.json", "a", encoding="utf-8") as file:
            json_line = json.dumps({
                "id": comentario.id,
                "user_id": comentario.user_id,
                "post_id": comentario.post_id,
                "comentario": comentario.comentario,
                "fecha_publicacion": comentario.fecha_publicacion
            }, ensure_ascii=False)
            file.write(json_line + "\n")

    def buscar_perfil_por_like(self, post_id):
        post = self.obtener_post_por_id(post_id)

        if post:
            for like in post.likes:
                usuario = self.get_user_by_id(like.user_id)
                print(f"Usuario: {usuario.username}, Carrera: {usuario.major}")
        else:
            print("Post no encontrado.")
    def buscar_perfil_por_comentario(self, post_id):
        post = self.obtener_post_por_id(post_id)

        if post:
            for comentario in post.comments:
                usuario = self.get_user_by_id(comentario.user_id)
                print(f"Usuario: {usuario.username}, Carrera: {usuario.major}")
        else:
            print("Post no encontrado.")

    def get_user_by_id(self, user_id):
        user = next((user for user in self.users if user.id == user_id), None)
        return user

#Gestion Moderacion 

    def submenu_moderacion(self):
        
        #Muestra un menú de moderación con opciones para un usuario administrador.
        
        while True:
            print("\n---- Submenú Moderación ----")
            print("1. Eliminar un post ofensivo")
            print("2. Eliminar un comentario ofensivo")
            print("3. Eliminar un usuario infractor")
            print("4. Volver al Menú Principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.eliminar_post_ofensivo()
            elif opcion == "2":
                self.eliminar_comentario_ofensivo_admin()
            elif opcion == "3":
                self.eliminar_usuario_infractor()
            elif opcion == "4":
                print("Volviendo al Menú Principal...")
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")

    def eliminar_post_ofensivo(self):
   
    #Permite a un usuario administrador eliminar un post que considera ofensivo.
    
        post_id = input("Ingrese el ID del post que desea eliminar: ")
        post = self.obtener_post_por_id(post_id)

        if post:
            # Eliminar el post y sus comentarios
            self.posts.remove(post)
            self.comments = [comment for comment in self.comments if comment.post_id != post_id]
            print("Post eliminado con éxito.")
        else:
            print("Post no encontrado.")

    def eliminar_comentario_ofensivo_admin(self):
        post_id = input("Ingrese el ID del post al que pertenece el comentario: ")
        comentario_id = input("Ingrese el ID del comentario que desea eliminar: ")

        self.eliminar_comentario_ofensivo(post_id, comentario_id)

    def eliminar_usuario_infractor(self):
        """
        Permite a un usuario administrador eliminar a un usuario que ha infringido múltiples veces las reglas.
        """
        usuario_id = input("Ingrese el ID del usuario que desea eliminar: ")
        usuario = self.get_user_by_id(usuario_id)

        if usuario:
            # Eliminar al usuario y sus posts y comentarios
            self.users.remove(usuario)
            self.posts = [post for post in self.posts if post.publisher_id != usuario_id]
            self.comments = [comment for comment in self.comments if comment.user_id != usuario_id]
            print("Usuario eliminado con éxito.")
        else:
            print("Usuario no encontrado.")
        

    
    

        
    

api_url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/08d4d2ce028692d71e9f8c32ea8c29ae24efe5b1/users.json"
url_post=  "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/main/posts.json"

                        

    
    
    

    





               






  