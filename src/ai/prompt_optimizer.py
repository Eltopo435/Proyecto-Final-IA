"""
Sergio Gabriel Pérez
23-EISN-2-028

Optimizador de prompts para generación de imágenes
Este módulo se encarga de optimizar descripciones de escenas para mejorar
la calidad de las imágenes generadas por IA.
"""

import openai
from typing import Optional

# Importación de configuraciones
from config.models import ModelConfig, CONFIG, OPENAI_API_KEY  # type: ignore
from config.prompts import PromptTemplates  # type: ignore[import]

# Establecer la clave API - usando la clave centralizada desde models.py
openai.api_key = OPENAI_API_KEY


class PromptOptimizer:
    def __init__(self) -> None:
        """Inicializa el optimizador de prompts"""
        self.config: ModelConfig = CONFIG

    def optimize_prompt(self, scene: str, choice: Optional[str] = None) -> str:
        """
        Optimiza la descripción de una escena para la generación de imágenes
        
        Args:
            scene (str): Descripción de la escena a optimizar
            choice (Optional[str]): Opción seleccionada por el usuario, si existe
            
        Returns:
            str: Prompt optimizado para la generación de imágenes
        """
        # Combinar la escena y la elección para proporcionar contexto
        context = scene
        if choice:
            context += f"\nEl usuario eligió: {choice}"

        # Formatear el prompt con el contexto
        prompt = PromptTemplates.format_prompt_optimization(context)

        try:
            # Realizar la llamada a la API de OpenAI para optimizar el prompt
            response = openai.chat.completions.create(
                model=self.config.prompt_model_name,
                messages=[
                    {"role": "system",
                        "content": PromptTemplates.PROMPT_OPTIMIZER_SYSTEM_PROMPT.content},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            optimized_prompt = content.strip() if content is not None else ""
            return optimized_prompt
        except Exception as e:
            # Manejo de errores en caso de falla en la llamada a la API
            print(f"Error al optimizar el prompt: {e}")
            # Devolver una versión simplificada si la llamada a la API falla
            return f"Una escena que representa: {scene[:100]}..."
