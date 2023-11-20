
from app import App

        
    
def main():
    app = App()
    api_url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/08d4d2ce028692d71e9f8c32ea8c29ae24efe5b1/users.json"
    url_post= "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/main/posts.json"
    app.cargar_post_desde_api(url_post)
    app.cargar_usuarios_desde_api(api_url)
    app.menu()
main( )
    


   
    