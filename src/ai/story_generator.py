"""
Sergio Gabriel Pérez
23-EISN-2-028
Generador de historias interactivas utilizando la API de OpenAI
"""

import openai
import json
from typing import Dict, List, Tuple, Optional, Any

# Importar configuraciones
from config.models import ModelConfig, CONFIG, OPENAI_API_KEY  # type: ignore
from config.prompts import PromptTemplates  # type: ignore

# Establecer la clave de API - usando la clave centralizada desde models.py
openai.api_key = OPENAI_API_KEY


class StoryGenerator:
    def __init__(self) -> None:
        """Inicializa el generador de historias con la configuración predeterminada"""
        self.story_history: List[Dict[str, Optional[str]]] = []  # Historial de la historia
        self.current_scene: str = ""  # Escena actual
        self.options: List[str] = []  # Opciones disponibles para el usuario
        self.config: ModelConfig = CONFIG  # Configuración del modelo

    def start_story(self) -> Tuple[str, List[str]]:
        """Genera la escena inicial de la historia y las opciones disponibles"""
        response = self._get_completion(
            PromptTemplates.STORY_START_PROMPT.template)

        # Actualizar el estado
        self.current_scene = response["scene"]
        self.options = response["options"]
        self.story_history.append(
            {"scene": self.current_scene, "choice": None})

        return self.current_scene, self.options

    def continue_story(self, choice_index: int) -> Tuple[str, List[str]]:
        """Continúa la historia basándose en la elección del usuario
        
        Args:
            choice_index: Índice de la opción seleccionada por el usuario
            
        Returns:
            Tupla con la nueva escena y las nuevas opciones disponibles
        """
        choice = self.options[choice_index]

        # Añadir la elección del usuario al historial
        self.story_history[-1]["choice"] = choice

        # Crear un contexto a partir del historial de la historia
        context = self._build_context()

        # Formatear la petición con el contexto y la elección
        prompt = PromptTemplates.format_story_continue(context, choice)

        response = self._get_completion(prompt)

        # Actualizar el estado
        self.current_scene = response["scene"]
        self.options = response["options"]
        self.story_history.append(
            {"scene": self.current_scene, "choice": None})

        return self.current_scene, self.options

    def _build_context(self) -> str:
        """Construye una cadena de contexto a partir del historial de la historia
        
        Returns:
            Cadena con el historial formateado para el contexto de la IA
        """
        context = "Story history:\n"

        for i, entry in enumerate(self.story_history):
            context += f"Scene {i+1}: {entry['scene']}\n"
            if entry['choice']:
                context += f"User chose: {entry['choice']}\n"

        return context

    def _get_completion(self, prompt: str) -> Dict[str, Any]:
        """Obtiene una respuesta de la API de OpenAI y la analiza como JSON
        
        Args:
            prompt: El texto de petición para enviar al modelo
            
        Returns:
            Diccionario con la respuesta parseada del modelo
        """
        try:
            response = openai.chat.completions.create(
                model=self.config.story_model_name,
                response_format=self.config.RESPONSE_FORMAT_JSON,
                messages=[
                    {"role": "system",
                        "content": PromptTemplates.STORY_SYSTEM_PROMPT.content},
                    {"role": "user", "content": prompt}
                ]
            )
            # Analizar el JSON del contenido de la respuesta
            content = response.choices[0].message.content
            if content is None:
                raise ValueError("Se recibió un contenido nulo de la API")
            return json.loads(content)
        except Exception as e:
            print(f"Error al obtener la respuesta: {e}")
            # Devolver una respuesta predeterminada si la llamada a la API falla
            return {
                "scene": "Ha ocurrido un error en la generación de la historia.",
                "options": ["Intentar de nuevo", "Comenzar de nuevo", "Continuar lo mejor posible"]
            }

    def get_current_state(self) -> Dict[str, Any]:
        """Obtiene el estado actual de la historia
        
        Returns:
            Diccionario con la escena actual, opciones e historial completo
        """
        return {
            "current_scene": self.current_scene,
            "options": self.options,
            "history": self.story_history
        }
