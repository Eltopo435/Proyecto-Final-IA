"""
Sergio Gabriel Pérez
23-EISN-2-028

Interfaz de usuario principal basada en chat para la aplicación StoryCraft.
Usando anotaciones tipadas para una mejor estructura del código.
"""

import base64
import os
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import gradio as gr
from PIL import Image

from ai.image_generator import ImageGenerator
from ai.music_context_evaluator import MusicContextEvaluator
from ai.prompt_optimizer import PromptOptimizer

# Importar componentes de IA
from ai.story_generator import StoryGenerator

# Importar configuraciones
from config.models import AVATAR_IMAGE
from ui.web import (
    AUDIO_CONFIG,
    AUDIO_HANDLER_JS,
    CHATBOT_CONFIG,
    CLEAR_BUTTON_TEXT,
    CONTINUE_BUTTON_TEXT,
    CUSTOM_CSS,
    FORMAT_STORY_RESPONSE,
    START_BUTTON_TEXT,
    UI_DESCRIPTION,
    UI_HEADER,
    UI_INPUT_PLACEHOLDER,
    UI_TITLE,
    WELCOME_MESSAGE,
    CSSClass,
)


class StoryCraftUI:
    def __init__(self) -> None:
        """Inicializar la interfaz de StoryCraft con los componentes de IA"""
        # Inicializar componentes de IA
        self.story_generator: StoryGenerator = StoryGenerator()
        self.prompt_optimizer: PromptOptimizer = PromptOptimizer()
        self.image_generator: ImageGenerator = ImageGenerator()
        self.music_evaluator: MusicContextEvaluator = MusicContextEvaluator()

        # Inicializar estado
        self.current_scene: str = ""
        self.current_options: List[str] = []
        self.current_image_b64: Optional[str] = None
        self.current_music: Optional[str] = None
        self.story_started: bool = False
        self.temp_dir = tempfile.mkdtemp()  # Directorio temporal para guardar imágenes

    def chat_interface(
        self, message: str, history: List[Dict[str, str]]
    ) -> Tuple[List[Dict[str, str]], Optional[str]]:
        """
        Función principal para la interfaz de chat

        Args:
            message: El mensaje/elección del usuario
            history: El historial de chat de Gradio

        Returns:
            Historial actualizado y componente de audio
        """
        # Si la historia no ha comenzado todavía, iniciarla sin importar el mensaje
        if (
            not self.story_started
            or message.lower() == "start"
            or message.lower() == "restart"
            or message.lower() == "comenzar"
            or message.lower() == "iniciar"
            or message.lower() == "reiniciar"
        ):
            return self._start_story(history)

        # Manejar la elección del usuario
        try:
            # Analizar la elección del mensaje - esperando un número o el texto de una opción
            choice_index = self._parse_choice(message)
            if choice_index is not None:
                return self._process_choice(choice_index, history)
            else:
                # Si no pudimos analizar una opción válida, pedir una
                history.append(
                    {
                        "role": "assistant",
                        "content": "Por favor selecciona una de las opciones numeradas.",
                    }
                )
                return history, None
        except Exception as e:
            print(f"Error en la interfaz de chat: {e}")
            history.append(
                {
                    "role": "assistant",
                    "content": "Algo salió mal. Por favor intenta de nuevo o inicia una nueva historia.",
                }
            )
            return history, None

    def _start_story(
        self, history: List[Dict[str, str]]
    ) -> Tuple[List[Dict[str, str]], Optional[str]]:
        """Iniciar una nueva historia y devolver la escena inicial"""
        try:
            print("Iniciando nueva historia...")
            # Generar la historia inicial y opciones
            scene, options = self.story_generator.start_story()
            self.current_scene = scene
            self.current_options = options
            self.story_started = True

            # Generar una imagen para la escena
            optimized_prompt = self.prompt_optimizer.optimize_prompt(scene)
            print(f"Prompt de imagen: {optimized_prompt[:50]}...")
            self.current_image_b64 = self.image_generator.generate_image(
                optimized_prompt
            )

            # Seleccionar música inicial
            self.current_music = self.music_evaluator.evaluate_scene_for_music(scene)

            # Formatear el mensaje de respuesta con la escena y las opciones
            response_text = FORMAT_STORY_RESPONSE(scene, options)

            # Si tenemos una imagen, incluirla en el historial antes del texto
            if self.current_image_b64:
                image_component = self._b64_to_image_component(self.current_image_b64)
                if image_component:
                    history.append({"role": "assistant", "content": image_component})

            # Añadir el texto de la respuesta al historial
            history.append({"role": "assistant", "content": response_text})

            print(f"Historia iniciada con éxito con {len(options)} opciones.")

            return history, self.current_music
        except Exception as e:
            print(f"Error al iniciar la historia: {e}")
            history.append(
                {
                    "role": "assistant",
                    "content": "Error al iniciar la historia. Por favor intenta de nuevo.",
                }
            )
            return history, None

    def _process_choice(
        self, choice_index: int, history: List[Dict[str, str]]
    ) -> Tuple[List[Dict[str, str]], Optional[str]]:
        """Procesar la elección del usuario y continuar la historia"""
        if not 0 <= choice_index < len(self.current_options):
            history.append(
                {
                    "role": "assistant",
                    "content": "Elección inválida. Por favor selecciona una opción válida.",
                }
            )
            return history, None

        try:
            # Obtener la siguiente parte de la historia basada en la elección
            scene, options = self.story_generator.continue_story(choice_index)
            self.current_scene = scene
            self.current_options = options

            # Generar una imagen para la nueva escena
            optimized_prompt = self.prompt_optimizer.optimize_prompt(
                scene, self.current_options[choice_index]
            )
            self.current_image_b64 = self.image_generator.generate_image(
                optimized_prompt
            )

            # Evaluar si la música necesita cambiar
            self.current_music = self.music_evaluator.evaluate_scene_for_music(
                scene, self.current_music
            )

            # Formatear la respuesta
            response_text = FORMAT_STORY_RESPONSE(scene, options)

            # Si tenemos una imagen, incluirla en el historial antes del texto
            if self.current_image_b64:
                image_component = self._b64_to_image_component(self.current_image_b64)
                if image_component:
                    history.append({"role": "assistant", "content": image_component})

            # Añadir el texto de la respuesta al historial
            history.append({"role": "assistant", "content": response_text})

            return history, self.current_music
        except Exception as e:
            print(f"Error procesando elección: {e}")
            history.append(
                {
                    "role": "assistant",
                    "content": "Error continuando la historia. Por favor intenta de nuevo.",
                }
            )
            return history, None

    def _parse_choice(self, message: str) -> Optional[int]:
        """Analizar la elección del usuario desde su mensaje"""
        # Primero intentar analizar como un número (1, 2, 3)
        try:
            choice = int(message.strip())
            if 1 <= choice <= len(self.current_options):
                return choice - 1  # Convertir a índice base 0
        except ValueError:
            pass

        # Si no es un número, verificar si el mensaje coincide con una de las opciones
        for i, option in enumerate(self.current_options):
            if message.lower().strip() == option.lower().strip():
                return i

        # Si llegamos aquí, no pudimos analizar una elección válida
        return None

    def _b64_to_image_component(self, b64_string: Optional[str]) -> Optional[gr.Image]:
        """Convertir una cadena base64 a un componente de imagen para el chatbot"""
        if not b64_string:
            return None

        try:
            # Convertir base64 a imagen PIL
            image_data = base64.b64decode(b64_string)
            pil_image = Image.open(BytesIO(image_data))

            # Guardar la imagen en un archivo temporal
            img_path = os.path.join(self.temp_dir, f"scene_{hash(b64_string)}.png")
            pil_image.save(img_path)

            # Crear un componente gr.Image con la ruta del archivo
            return gr.Image(value=img_path)
        except Exception as e:
            print(f"Error al convertir base64 a componente de imagen: {e}")
            return None

    def create_interface(self) -> gr.Blocks:
        """Crear y lanzar la interfaz de chat de Gradio"""
        # CSS personalizado para mejor estilo
        css = CUSTOM_CSS

        # Crear la interfaz de chat
        with gr.Blocks(css=css, title=UI_TITLE) as interface:
            # Añadir encabezado y descripción
            gr.Markdown(UI_HEADER)
            gr.Markdown(UI_DESCRIPTION)

            # Mensaje inicial para el chatbot
            welcome_message = WELCOME_MESSAGE

            # Inicializar componentes que necesitan ser accedidos en los callbacks
            chatbot = gr.Chatbot(
                **CHATBOT_CONFIG,
                avatar_images=(None, Path(AVATAR_IMAGE)),
                value=welcome_message,  # Añadir mensaje de bienvenida
            )

            # Reproductor de audio oculto - estará completamente oculto pero funcional
            audio_output = gr.Audio(**AUDIO_CONFIG)

            chat_input = gr.Textbox(
                placeholder=UI_INPUT_PLACEHOLDER,
                label="Tu Elección",
                lines=1,
            )

            # Acciones
            def on_submit(
                message: str, history: List[Dict[str, str]]
            ) -> Tuple[str, List[Dict[str, str]], Optional[str], str]:
                # Procesar el mensaje del usuario
                user_message = message
                history.append({"role": "user", "content": user_message})

                # Obtener la respuesta del chatbot
                updated_history, audio = self.chat_interface(user_message, history)

                # Actualizar el texto del botón según el estado de la historia
                button_text = (
                    CONTINUE_BUTTON_TEXT if self.story_started else START_BUTTON_TEXT
                )

                return "", updated_history, audio, button_text

            # Definir un botón de limpieza para reiniciar la historia
            def clear_and_restart() -> Tuple[List[Dict[str, str]], None, str]:
                self.story_started = False
                # Volvemos al mensaje de bienvenida original
                return welcome_message, None, START_BUTTON_TEXT

            # Estado inicial del botón
            initial_button_text = START_BUTTON_TEXT
            submit_btn = gr.Button(
                initial_button_text,
                elem_classes=CSSClass.PRIMARY_BUTTON.value,
                variant="primary",
            )
            clear_btn = gr.Button(
                CLEAR_BUTTON_TEXT, elem_classes=CSSClass.SECONDARY_BUTTON.value
            )

            # Conectar todo
            submit_btn.click(
                on_submit,
                [chat_input, chatbot],
                [chat_input, chatbot, audio_output, submit_btn],
            )

            chat_input.submit(
                on_submit,
                [chat_input, chatbot],
                [chat_input, chatbot, audio_output, submit_btn],
            )

            clear_btn.click(
                clear_and_restart,
                None,
                [chatbot, audio_output, submit_btn],
                queue=False,
            )

            # Añadir JavaScript personalizado para gestionar autoplay y ocultar el audio
            interface.load(
                None,
                js=AUDIO_HANDLER_JS,
            )

        return interface


def create_interface() -> gr.Blocks:
    """Crear y devolver la interfaz de StoryCraft"""
    ui = StoryCraftUI()
    return ui.create_interface()
