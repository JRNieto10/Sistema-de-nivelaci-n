# interfaz.py
import os
import json
from estructura.AlmacenamietoUsuarios import Almacenamiento_Usuarios
from estructura.Autenticacion import Autenticacion  # Pon el nombre del archivo de tu clase Autenticacion si difiere
from vista_login import VentanaLogin

def inicializar_entorno():
    if not os.path.exists("Datos"):
        os.makedirs("Datos")
        
    ruta_json = "Datos/users.json"
    if not os.path.exists(ruta_json) or os.path.getsize(ruta_json) == 0:
        admin_inicial = [{
            "cedula": "0000000000",
            "nombre": "Administrador",
            "apellido": "Principal",
            "correo": "admin@nivelacion.com",
            "contraseña": "admin1234",
            "rol": "Personal"
        }]
        with open(ruta_json, "w", encoding="utf-8") as f:
            json.dump(admin_inicial, f, indent=4, ensure_ascii=False)
        print("[Sistema] Usuario administrador inicial creado: admin@nivelacion.com / admin1234")

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