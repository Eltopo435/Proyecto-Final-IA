"""
Sergio Gabriel Pérez
23-EISN-2-028

Módulo para evaluar el contexto musical de las escenas y seleccionar
música apropiada según el contenido narrativo.
"""

import json
import random
from typing import Dict, List, Optional

import openai

# Importar configuraciones
from config.models import CONFIG, OPENAI_API_KEY, ModelConfig  # type: ignore
from config.music import (
    MOOD_TO_CATEGORY_MAP,
    MUSIC_DIR,  # type: ignore
    MUSIC_LIBRARY,
    MusicCategory,
    MusicLibrary,
    assign_default_categories,
)
from config.prompts import PromptTemplates  # type: ignore[import]

# Establecer la clave API - usando la clave centralizada de models.py
openai.api_key = OPENAI_API_KEY


class MusicContextEvaluator:
    def __init__(self, music_folder: str = MUSIC_DIR) -> None:
        """Inicializar el evaluador de contexto musical"""
        self.music_folder: str = music_folder
        self.current_music: Optional[str] = None
        self.music_library: MusicLibrary = MUSIC_LIBRARY
        self.config: ModelConfig = CONFIG

        # Actualizar la biblioteca musical para asegurarnos de tener los archivos más recientes
        self.music_library.refresh()

        # Asignar categorías predeterminadas a todos los archivos de música
        assign_default_categories()

        # Si no existen archivos de música, aún necesitaremos las descripciones para posibles coincidencias
        self.music_descriptions: Dict[str, List[str]] = {}
        self._prepare_music_descriptions()

    def _prepare_music_descriptions(self) -> None:
        """Preparar descripciones musicales de la biblioteca o crearlas si es necesario"""
        # Limpiar descripciones existentes
        self.music_descriptions.clear()

        # Si tenemos archivos de música en la biblioteca, usar sus categorías
        if not self.music_library.is_empty:
            for music_file in self.music_library.get_all_files():
                self.music_descriptions[music_file.absolute_path] = (
                    music_file.category_values
                )
        else:
            # No hay archivos de música en la biblioteca todavía, por lo que no hay descripciones que preparar
            pass

    def evaluate_scene_for_music(
        self, scene: str, current_music: Optional[str] = None
    ) -> Optional[str]:
        """Evaluar si la música actual es apropiada para la escena, o seleccionar nueva música"""
        music_files = self.music_library.get_all_paths()

        if not music_files:
            return None

        if not current_music and music_files:
            # Si no se está reproduciendo música, seleccionar una aleatoria para comenzar
            return random.choice(music_files)

        # Solo evaluar con la API si tenemos archivos de música y música actual
        if not current_music or not music_files:
            return random.choice(music_files) if music_files else None

        # Formatear el prompt con la escena y las categorías de música actual
        prompt = PromptTemplates.format_music_evaluation(
            scene=scene,
            categories=self.music_descriptions.get(current_music, ["unknown"]),
        )

        try:
            # Realizar la consulta al modelo de IA para evaluar la adecuación musical
            response = openai.chat.completions.create(
                model=self.config.music_model_name,
                response_format=self.config.RESPONSE_FORMAT_JSON,
                messages=[
                    {
                        "role": "system",
                        "content": PromptTemplates.MUSIC_SYSTEM_PROMPT.content,
                    },
                    {"role": "user", "content": prompt},
                ],
            )

            # Analizar el JSON del contenido de respuesta
            content = response.choices[0].message.content
            if content is not None:
                result = json.loads(content)
            else:
                # Manejar el caso cuando el contenido es None
                result = {"is_appropriate": True}

            if result.get("is_appropriate", True):
                # Mantener la música actual
                return current_music
            else:
                # Seleccionar nueva música basada en categorías recomendadas
                recommended_categories = result.get("recommended_categories", [])
                return self._select_music_by_categories(
                    recommended_categories, current_music
                )
        except Exception as e:
            print(f"Error al evaluar el contexto musical: {e}")
            # Si hay un error, simplemente mantener la música actual
            return current_music

    def _select_music_by_categories(
        self, target_categories: List[str], current_music: Optional[str] = None
    ) -> Optional[str]:
        """Seleccionar un archivo de música basado en categorías"""
        music_files = self.music_library.get_all_paths()

        if not music_files:
            return None

        # No seleccionar la música actual nuevamente
        available_files = [file for file in music_files if file != current_music]
        if not available_files:
            return current_music  # Si solo hay un archivo, seguir usándolo

        # Encontrar el archivo con mejor coincidencia
        best_match = None
        best_match_score = -1

        for file in available_files:
            file_categories = self.music_descriptions.get(file, [])
            # Contar cuántas categorías objetivo coinciden con este archivo
            match_score = sum(
                1
                for cat in target_categories
                if cat.lower() in [fc.lower() for fc in file_categories]
            )

            if match_score > best_match_score:
                best_match = file
                best_match_score = match_score

        # Si no se encuentra una buena coincidencia, simplemente elegir un archivo aleatorio
        if best_match is None or best_match_score == 0:
            return random.choice(available_files)

        return best_match

    def get_all_music_files(self) -> List[str]:
        """Obtener todos los archivos de música disponibles"""
        return self.music_library.get_all_paths()

    def get_categories_for_mood(self, mood: str) -> List[str]:
        """Obtener categorías musicales apropiadas para un estado de ánimo/tipo de escena dado"""
        if mood in MOOD_TO_CATEGORY_MAP:
            return [category.value for category in MOOD_TO_CATEGORY_MAP[mood]]
        # Si el estado de ánimo no está mapeado, devolver categorías aleatorias
        return [category.value for category in random.sample(list(MusicCategory), 2)]
