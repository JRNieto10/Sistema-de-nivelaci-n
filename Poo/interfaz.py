# interfaz.py
import os
from estructura.AlmacenamietoUsuarios import Almacenamiento_Usuarios
from estructura.Autenticacion import Autenticacion  # Pon el nombre del archivo de tu clase Autenticacion si difiere
from vista_login import VentanaLogin

def inicializar_entorno():
    if not os.path.exists("Datos"):
        os.makedirs("Datos")
        
    ruta_json = "Datos/users.json"
    if not os.path.exists(ruta_json) or os.path.getsize(ruta_json) == 0:
        with open(ruta_json, "w", encoding="utf-8") as f:
            f.write("[]")
        print("[Sistema] Archivo 'users.json' verificado/inicializado.")

def iniciar_aplicacion():
    inicializar_entorno()
    
    # Acoplamiento de tu Backend de persistencia y controladores
    almacenamiento = Almacenamiento_Usuarios()
    servicio_auth = Autenticacion(almacenamiento)
    
    # Lanzamiento controlado del Login
    print("[Sistema] Abriendo ventana de inicio de sesión...")
    app = VentanaLogin(servicio_auth)
    app.mainloop()

if __name__ == "__main__":
    iniciar_aplicacion()