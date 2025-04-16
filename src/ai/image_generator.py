"""
Sergio Gabriel Pérez
23-EISN-2-028

Este módulo proporciona funcionalidades para la generación de imágenes
utilizando la API de OpenAI DALL-E.
"""

import base64
from typing import Optional

import openai

# Importar configuraciones
from config.models import CONFIG, OPENAI_API_KEY, ModelConfig  # type: ignore

# Establecer la clave API - usando la clave centralizada desde models.py
openai.api_key = OPENAI_API_KEY


class ImageGenerator:
    def __init__(self) -> None:
        """Inicializa el generador de imágenes"""
        self.config: ModelConfig = CONFIG

    def generate_image(self, prompt: str) -> Optional[str]:
        """
        Genera una imagen basada en el prompt proporcionado usando DALL-E

        Args:
            prompt (str): Descripción textual para generar la imagen

        Returns:
            Optional[str]: Imagen codificada en base64 o None si hay error
        """
        try:
            response = openai.images.generate(
                model=self.config.image_model_name,
                prompt=prompt,
                n=1,
                size=self.config.image_size_value,
                response_format="b64_json",
            )

            # Obtener la imagen codificada en base64
            image_b64 = response.data[0].b64_json
            return image_b64
        except Exception as e:
            print(f"Error al generar la imagen: {e}")
            # Devolver None si la generación de imagen falla
            return None

    def save_image(
        self, image_b64: Optional[str], filename: str = "scene.png"
    ) -> Optional[str]:
        """
        Guarda una imagen desde codificación base64 a un archivo

        Args:
            image_b64 (Optional[str]): Imagen codificada en base64
            filename (str): Nombre del archivo donde guardar la imagen

        Returns:
            Optional[str]: Ruta del archivo guardado o None si hay error
        """
        if image_b64:
            try:
                image_data = base64.b64decode(image_b64)
                with open(filename, "wb") as f:
                    f.write(image_data)
                return filename
            except Exception as e:
                print(f"Error al guardar la imagen: {e}")
                return None
        return None
        return None
