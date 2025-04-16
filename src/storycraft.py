"""
Sergio Gabriel Pérez
23-EISN-2-028

Este es el archivo principal de la aplicación StoryCraft,
que inicializa y lanza la interfaz de usuario.
"""

# Importamos nuestra clase de interfaz de usuario
from ui.chat_interface import StoryCraftUI

# Configuramos y lanzamos la aplicación si se ejecuta directamente
if __name__ == "__main__":
    # Creamos una instancia de la interfaz de usuario
    app = StoryCraftUI()
    # Creamos la interfaz gráfica y la lanzamos en el navegador
    app.create_interface().launch()
