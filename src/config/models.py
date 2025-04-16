"""
    Sergio Gabriel Pérez
    23-EISN-2-028

    Configuración para los modelos de la API de OpenAI utilizados en la aplicación StoryCraft.
    Se utilizan Enums, dataclasses y anotaciones de tipo para una mejor estructura de código.
"""

import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv

from config.music import ASSETS_DIR  # type: ignore[import]

# Cargar variables de entorno una sola vez
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class ModelName(Enum):
    """Enumeración para los nombres de modelos de OpenAI"""

    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"
    DALL_E_3 = "dall-e-3"


class ImageSize(Enum):
    """Enumeración para los tamaños de imágenes de DALL-E"""

    SMALL = "1024x1024"  # Tamaño pequeño (cuadrado)
    MEDIUM = "1792x1024"  # Tamaño mediano (horizontal)
    LARGE = "1024x1792"  # Tamaño grande (vertical)


@dataclass
class ModelConfig:
    """Configuración para los ajustes de modelos"""

    # Modelo para generación de historias
    STORY_MODEL: ModelName = ModelName.GPT_4O_MINI

    # Modelo para optimización de prompts
    PROMPT_MODEL: ModelName = ModelName.GPT_4O_MINI

    # Modelo para generación de imágenes
    IMAGE_MODEL: ModelName = ModelName.DALL_E_3

    # Modelo para evaluación del contexto musical
    MUSIC_MODEL: ModelName = ModelName.GPT_4O_MINI

    # Tamaño de imagen para DALL-E
    IMAGE_SIZE: ImageSize = ImageSize.SMALL

    # Formato de respuesta predeterminado
    RESPONSE_FORMAT_JSON: Optional[Dict[str, str]] = None

    # Imagen de avatar
    AVATAR_IMAGE: Path = ASSETS_DIR / Path("images/bot.png")

    def __post_init__(self):
        """Inicializa los valores que dependen de otros atributos tras la creación"""
        if self.RESPONSE_FORMAT_JSON is None:
            self.RESPONSE_FORMAT_JSON = {"type": "json_object"}

    @property
    def story_model_name(self) -> str:
        """Obtiene el nombre del modelo de historias como string"""
        return self.STORY_MODEL.value

    @property
    def prompt_model_name(self) -> str:
        """Obtiene el nombre del modelo de prompts como string"""
        return self.PROMPT_MODEL.value

    @property
    def image_model_name(self) -> str:
        """Obtiene el nombre del modelo de imágenes como string"""
        return self.IMAGE_MODEL.value

    @property
    def music_model_name(self) -> str:
        """Obtiene el nombre del modelo de música como string"""
        return self.MUSIC_MODEL.value

    @property
    def image_size_value(self) -> str:
        """Obtiene el tamaño de imagen como string"""
        return self.IMAGE_SIZE.value


# Crear una instancia de la configuración para usar en toda la aplicación
CONFIG = ModelConfig()

# Para compatibilidad con versiones anteriores
STORY_MODEL = CONFIG.story_model_name
PROMPT_MODEL = CONFIG.prompt_model_name
IMAGE_MODEL = CONFIG.image_model_name
MUSIC_MODEL = CONFIG.music_model_name
AVATAR_IMAGE = CONFIG.AVATAR_IMAGE
IMAGE_SIZE = CONFIG.image_size_value
RESPONSE_FORMAT_JSON = CONFIG.RESPONSE_FORMAT_JSON
