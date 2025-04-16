"""
Sergio Gabriel Pérez
23-EISN-2-028

Configuración para la interfaz web de la aplicación StoryCraft.
Este módulo centraliza los elementos de estilo, JavaScript y configuraciones de interfaz.
Se utilizan Enums, dataclasses y anotaciones de tipo para una mejor estructura de código.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class UIComponent(Enum):
    """Enumeración para los componentes principales de la UI"""

    CHATBOT = "story_chatbot"
    AUDIO = "background_music"
    SUBMIT_BUTTON = "submit_button"
    CLEAR_BUTTON = "clear_button"


class CSSClass(Enum):
    """Enumeración para clases CSS utilizadas en la UI"""

    HIDDEN_AUDIO = "hidden-audio"
    MESSAGE_BUBBLE = "message-bubble"
    PRIMARY_BUTTON = "primary-button"
    SECONDARY_BUTTON = "secondary-button"


@dataclass
class StyleConfig:
    """Configuración para estilos CSS de la aplicación"""

    # CSS personalizado para la aplicación
    CUSTOM_CSS: str = """
        .hidden-audio {
            display: none !important;
        }
        
        /* Mejoras visuales generales */
        #story_chatbot {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            animation: fadeIn 0.5s ease-in-out;
        }
        
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Estilo de botones */
        button.primary-button {
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            background-size: 200% 200%;
            animation: gradientBG 5s ease infinite;
            border: none !important;
            color: white !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            font-size: 0.9em !important;
        }
        
        button.primary-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(110, 142, 251, 0.4) !important;
        }
        
        button.secondary-button {
            background: linear-gradient(135deg, #FF9A8B, #FF6A88);
            background-size: 200% 200%;
            animation: gradientBG 5s ease infinite;
            border: none !important;
            color: white !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            font-size: 0.9em !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
        }
        
        button.secondary-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(255, 106, 136, 0.4) !important;
        }
        
        /* Añadir brillo a botones al hacer clic */
        button:active {
            transform: scale(0.98) !important;
        }
        
        /* Estilizar el input */
        #component-8 {
            border-radius: 12px !important;
            border: 2px solid #e0e0e0 !important;
            transition: all 0.3s ease !important;
            padding: 10px !important;
            background: rgba(255, 255, 255, 0.9) !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
        }
        
        #component-8:focus-within {
            border-color: #6e8efb !important;
            box-shadow: 0 0 0 3px rgba(110, 142, 251, 0.2) !important;
        }
        
        /* Estilo para el header */
        h1 {
            animation: gradientBG 10s ease infinite;
            text-align: center !important;
            font-weight: 800 !important;
            letter-spacing: 0.5px !important;
            margin-bottom: 10px !important;
            filter: drop-shadow(0 2px 5px rgba(0,0,0,0.1));
        }
                
        /* Mejorar párrafos de descripción */
        .prose p {
            font-size: 1.2em !important;
            line-height: 1.7 !important;
            text-align: center !important;
            max-width: 90% !important;
            color: #444 !important;
        }
                
        /* Burbujas de chat con esquinas más suaves */
        .user-message {
            background-color: #e9f0ff !important;
            border-top-right-radius: 5px !important;
            padding: 15px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
            border-left: 3px solid #6e8efb !important;
        }
        
        .assistant-message {
            background-color: #f9f7ff !important;
            border-top-left-radius: 5px !important;
            padding: 15px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
            border-left: 3px solid #a777e3 !important;
        }
        
        /* Estilizar imágenes en el chat para hacerlas más bonitas */
        #story_chatbot img {
            border-radius: 18px !important;
            box-shadow: 0 8px 20px rgba(0,0,0,0.12) !important;
            margin: 15px 0 !important;
            max-width: 100% !important;
            transition: all 0.3s ease !important;
            border: 3px solid rgba(255, 255, 255, 0.7) !important;
            transform: scale(0.98);
        }
        
        #story_chatbot img:hover {
            box-shadow: 0 12px 28px rgba(110, 142, 251, 0.25) !important;
            transform: scale(1);
        }

        /* Corregir alineación del avatar */
        #story_chatbot .avatar-container img {
            object-fit: cover !important;
            width: 100% !important;
            height: 100% !important;
            border-radius: 50% !important;
            border: 2px solid #fff !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
        }

        /* Asegurar que el círculo contenedor del avatar está bien posicionado */
        #story_chatbot .avatar-container {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            overflow: hidden !important;
        }
        
        /* Contenedor principal con un borde decorativo */
        .main-container {
            border-radius: 15px;
            border: none;
            box-shadow: 0 5px 30px rgba(0,0,0,0.08);
            overflow: hidden;
            background: linear-gradient(to bottom, #ffffff, #f9f9ff);
            padding: 10px;
        }
        
        /* Estilizar opciones numeradas en el chatbot */
        ol, ul {
            margin-left: 20px !important;
            margin-top: 10px !important;
        }
        
        li {
            margin-bottom: 8px !important;
            padding-left: 5px !important;
            line-height: 1.5 !important;
        }
        
        /* Destacar "¿Qué harás?" */
        strong {
            color: #6e8efb !important;
            font-size: 1.1em !important;
            display: block !important;
            margin: 10px 0 !important;
        }
        """


@dataclass
class JavaScriptConfig:
    """Configuración para scripts JavaScript de la aplicación"""

    # JavaScript para gestión del reproductor de audio
    AUDIO_HANDLER_JS: str = """
                function setupMusicHandler() {
                    // Obtener el elemento de audio 
                    const audioEl = document.querySelector('#background_music audio');
                    if (!audioEl) return;
                    
                    // Configurarlo para que se reproduzca en bucle y gestionar el volumen
                    audioEl.loop = true;
                    audioEl.volume = 0.3;
                    
                    // Ocultar completamente el contenedor de audio y los controles
                    const audioContainer = document.querySelector('#background_music');
                    if (audioContainer) {
                        audioContainer.style.display = 'none';
                    }
                }
                
                function enhanceUI() {
                    // Mejorar estilo de las burbujas de chat
                    const chatBubbles = document.querySelectorAll('.message-bubble');
                    chatBubbles.forEach(bubble => {
                        // Determinar si es un mensaje de usuario o asistente
                        const isUser = bubble.closest('.user');
                        if (isUser) {
                            bubble.classList.add('user-message');
                        } else {
                            bubble.classList.add('assistant-message');
                        }
                    });
                    
                    // Añadir una clase al contenedor principal para los estilos de borde
                    const mainContainer = document.querySelector('#story_chatbot').closest('.gradio-container');
                    if (mainContainer) {
                        mainContainer.classList.add('main-container');
                    }
                    
                    // Hacer que las imágenes sean más atractivas y redondeadas
                    const images = document.querySelectorAll('#story_chatbot img:not(.avatar-container img)');
                    images.forEach(img => {
                        img.style.borderRadius = '18px';
                        img.style.boxShadow = '0 8px 20px rgba(0,0,0,0.12)';
                        img.style.margin = '10px 0';
                        img.style.maxWidth = '100%';
                        img.style.border = '3px solid rgba(255, 255, 255, 0.7)';
                        img.style.transition = 'all 0.4s ease';
                        
                        // Aplicar un pequeño efecto de animación al cargar
                        img.style.opacity = '0';
                        img.style.transform = 'scale(0.96)';
                        
                        // Asegurar que la imagen esté cargada para la animación
                        if (img.complete) {
                            setTimeout(() => {
                                img.style.opacity = '1';
                                img.style.transform = 'scale(1)';
                            }, 100);
                        } else {
                            img.onload = () => {
                                img.style.opacity = '1';
                                img.style.transform = 'scale(1)';
                            };
                        }
                        
                        // Efecto hover
                        img.addEventListener('mouseenter', () => {
                            img.style.boxShadow = '0 12px 28px rgba(110, 142, 251, 0.3)';
                            img.style.transform = 'scale(1.01)';
                        });
                        
                        img.addEventListener('mouseleave', () => {
                            img.style.boxShadow = '0 8px 20px rgba(0,0,0,0.12)';
                            img.style.transform = 'scale(1)';
                        });
                    });
                    
                    // Corregir la alineación de los avatares
                    const avatars = document.querySelectorAll('#story_chatbot .avatar-container img');
                    avatars.forEach(avatar => {
                        // Asegurar que el avatar esté bien alineado en su contenedor
                        const container = avatar.closest('.avatar-container');
                        if (container) {
                            container.style.display = 'flex';
                            container.style.alignItems = 'center';
                            container.style.justifyContent = 'center';
                            container.style.overflow = 'hidden';
                            
                            // Configurar la imagen del avatar
                            avatar.style.objectFit = 'cover';
                            avatar.style.width = '100%';
                            avatar.style.height = '100%';
                            avatar.style.borderRadius = '50%';
                            avatar.style.position = 'relative';
                            avatar.style.border = '2px solid #fff';
                            avatar.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
                        }
                    });
                }
                
                // Ejecutar la configuración al cargar la página
                setupMusicHandler();
                setTimeout(enhanceUI, 100);
                
                // También ejecutar cuando el componente se actualiza
                document.addEventListener('DOMContentLoaded', function() {
                    setTimeout(setupMusicHandler, 1000);
                    setTimeout(enhanceUI, 1000);
                });
                
                // Observador para cambios dinámicos de contenido 
                const observer = new MutationObserver(function(mutations) {
                    setupMusicHandler();
                    enhanceUI();
                });
                
                // Comenzar a observar
                observer.observe(document.body, { childList: true, subtree: true });
                
                // Devolver una función vacía como Gradio espera
                () => {}
            """


@dataclass
class UITextConfig:
    """Configuración de textos para la interfaz de usuario"""

    TITLE: str = "📚 StoryCraft - Narrador de Historias Interactivo"
    HEADER: str = "# 📚✨ StoryCraft: Narrador de Historias Interactivo ✨📚"
    DESCRIPTION: str = "🌟 Embárcate en una aventura interactiva donde tus elecciones dan forma a la historia. 🔍 Escribe un número (1-3) o el texto completo de una opción para hacer tu elección. 🎭 ¿Qué camino tomarás?"
    WELCOME_MESSAGE: List[Dict[str, str]] = field(
        default_factory=lambda: [
            {
                "role": "assistant",
                "content": '👋 ¡Bienvenido a StoryCraft! ✨\n\nSoy tu narrador de historias interactivas. 📖 Cada decisión que tomes moldeará una aventura única y te llevará por caminos inexplorados. 🛤️\n\n🔮 Haz clic en "Iniciar Historia" para comenzar tu viaje o escribe "iniciar" en el chat. ¡Tu aventura te espera! 🚀',
            },
        ]
    )
    INPUT_PLACEHOLDER: str = (
        "Escribe 'iniciar' para comenzar o ingresa tu elección (1-3)..."
    )
    SUBMIT_BUTTON: str = "Enviar"
    CLEAR_BUTTON: str = "Nueva Historia"
    CONTINUE_BUTTON: str = "Continuar"
    START_BUTTON: str = "Iniciar Historia"


@dataclass
class StoryFormattingConfig:
    """Configuración para el formato de presentación de la historia"""

    OPTION_EMOJIS: List[str] = field(
        default_factory=lambda: ["🔍", "🧠", "⚔️", "🗣️", "🧩", "🔮", "🛤️", "🚪", "🧭"]
    )
    SCENE_DECORATION: str = "✨"
    QUESTION_TEXT: str = "**¿Qué harás? 🤔**"


@dataclass
class ChatbotConfig:
    """Configuración para el componente Chatbot de Gradio"""

    ELEM_ID: str = "story_chatbot"
    BUBBLE_FULL_WIDTH: bool = False
    HEIGHT: int = 500
    RENDER_MARKDOWN: bool = True
    LINE_BREAKS: bool = True
    SHOW_COPY_BUTTON: bool = True
    TYPE: str = "messages"


@dataclass
class AudioConfig:
    """Configuración para el componente Audio de Gradio"""

    ELEM_ID: str = "background_music"
    ELEM_CLASSES: str = "hidden-audio"
    AUTOPLAY: bool = True
    VISIBLE: bool = True
    LABEL: Optional[str] = None


@dataclass
class WebConfig:
    """Configuración principal para la interfaz web de la aplicación"""

    # Instancias de cada configuración individual
    STYLE: StyleConfig = field(default_factory=StyleConfig)
    JAVASCRIPT: JavaScriptConfig = field(default_factory=JavaScriptConfig)
    TEXT: UITextConfig = field(default_factory=UITextConfig)
    STORY_FORMAT: StoryFormattingConfig = field(default_factory=StoryFormattingConfig)
    CHATBOT: ChatbotConfig = field(default_factory=ChatbotConfig)
    AUDIO: AudioConfig = field(default_factory=AudioConfig)

    @property
    def custom_css(self) -> str:
        """Obtiene el CSS personalizado"""
        return self.STYLE.CUSTOM_CSS

    @property
    def audio_handler_js(self) -> str:
        """Obtiene el JavaScript para el manejador de audio"""
        return self.JAVASCRIPT.AUDIO_HANDLER_JS

    @property
    def ui_title(self) -> str:
        """Obtiene el título de la UI"""
        return self.TEXT.TITLE

    @property
    def ui_header(self) -> str:
        """Obtiene el encabezado de la UI"""
        return self.TEXT.HEADER

    @property
    def ui_description(self) -> str:
        """Obtiene la descripción de la UI"""
        return self.TEXT.DESCRIPTION

    @property
    def ui_input_placeholder(self) -> str:
        """Obtiene el placeholder del input"""
        return self.TEXT.INPUT_PLACEHOLDER

    @property
    def submit_button_text(self) -> str:
        """Obtiene el texto del botón de envío"""
        return self.TEXT.SUBMIT_BUTTON

    @property
    def clear_button_text(self) -> str:
        """Obtiene el texto del botón de limpiar"""
        return self.TEXT.CLEAR_BUTTON

    @property
    def continue_button_text(self) -> str:
        """Obtiene el texto del botón de continuar"""
        return self.TEXT.CONTINUE_BUTTON

    @property
    def start_button_text(self) -> str:
        """Obtiene el texto del botón de iniciar"""
        return self.TEXT.START_BUTTON

    @property
    def ui_welcome_message(self) -> List[Dict[str, str]]:
        """Obtiene el mensaje de bienvenida"""
        return self.TEXT.WELCOME_MESSAGE

    @property
    def chatbot_config(self) -> Dict:
        """Obtiene la configuración del chatbot"""
        return {
            "elem_id": self.CHATBOT.ELEM_ID,
            "bubble_full_width": self.CHATBOT.BUBBLE_FULL_WIDTH,
            "height": self.CHATBOT.HEIGHT,
            "render_markdown": self.CHATBOT.RENDER_MARKDOWN,
            "line_breaks": self.CHATBOT.LINE_BREAKS,
            "show_copy_button": self.CHATBOT.SHOW_COPY_BUTTON,
            "type": self.CHATBOT.TYPE,
        }

    @property
    def audio_config(self) -> Dict:
        """Obtiene la configuración del reproductor de audio"""
        return {
            "elem_id": self.AUDIO.ELEM_ID,
            "elem_classes": self.AUDIO.ELEM_CLASSES,
            "autoplay": self.AUDIO.AUTOPLAY,
            "visible": self.AUDIO.VISIBLE,
            "label": self.AUDIO.LABEL,
        }

    def format_story_response(self, scene: str, options: List[str]) -> str:
        """Formatear la respuesta de la historia con escena y opciones"""
        # Añadir decoración a la escena
        decorated_scene = f"{self.STORY_FORMAT.SCENE_DECORATION} {scene}"

        # Crear el mensaje de respuesta
        response = f"{decorated_scene}\n\n{self.STORY_FORMAT.QUESTION_TEXT}\n\n"

        # Añadir cada opción con un emoji único
        for i, option in enumerate(options):
            emoji = self.STORY_FORMAT.OPTION_EMOJIS[
                i % len(self.STORY_FORMAT.OPTION_EMOJIS)
            ]
            response += f"{i + 1}. {emoji} {option}\n"

        return response


# Crear una instancia de la configuración para usar en toda la aplicación
CONFIG = WebConfig()

# Para compatibilidad con versiones anteriores
CUSTOM_CSS = CONFIG.custom_css
AUDIO_HANDLER_JS = CONFIG.audio_handler_js
UI_TITLE = CONFIG.ui_title
UI_HEADER = CONFIG.ui_header
UI_DESCRIPTION = CONFIG.ui_description
WELCOME_MESSAGE = CONFIG.ui_welcome_message
UI_INPUT_PLACEHOLDER = CONFIG.ui_input_placeholder
SUBMIT_BUTTON_TEXT = CONFIG.submit_button_text
CLEAR_BUTTON_TEXT = CONFIG.clear_button_text
CONTINUE_BUTTON_TEXT = CONFIG.continue_button_text
START_BUTTON_TEXT = CONFIG.start_button_text
CHATBOT_CONFIG = CONFIG.chatbot_config
AUDIO_CONFIG = CONFIG.audio_config
FORMAT_STORY_RESPONSE = CONFIG.format_story_response
