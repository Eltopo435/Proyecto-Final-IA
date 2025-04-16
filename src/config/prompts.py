"""

    Sergio Gabriel Pérez
    23-EISN-2-028

    Plantillas de prompts para los diversos modelos de IA en StoryCraft.
    Utilizando clases con anotaciones de tipo y enumeraciones para una mejor estructura.
"""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, List


class SystemRoleType(Enum):
    """Enumeración para tipos de roles del sistema"""

    STORYTELLER = "STORYTELLER"  # Narrador de historias
    PROMPT_OPTIMIZER = "PROMPT_OPTIMIZER"  # Optimizador de prompts
    MUSIC_EXPERT = "MUSIC_EXPERT"  # Experto en música


class PromptType(Enum):
    """Enumeración para tipos de prompts"""

    STORY_START = "STORY_START"  # Inicio de historia
    STORY_CONTINUE = "STORY_CONTINUE"  # Continuación de historia
    PROMPT_OPTIMIZATION = "PROMPT_OPTIMIZATION"  # Optimización de prompts
    MUSIC_EVALUATION = "MUSIC_EVALUATION"  # Evaluación musical


@dataclass
class PromptTemplate:
    """Clase base para plantillas de prompts"""

    prompt_type: PromptType  # Tipo de prompt
    template: str  # Plantilla de texto


@dataclass
class SystemPrompt:
    """Prompt del sistema para modelos de IA"""

    role_type: SystemRoleType  # Tipo de rol del sistema
    content: str  # Contenido del prompt


@dataclass
class PromptTemplates:
    """Colección de todas las plantillas de prompts utilizadas en la aplicación"""

    # Prompts del Generador de Historias
    STORY_START_PROMPT: ClassVar[PromptTemplate] = PromptTemplate(
        prompt_type=PromptType.STORY_START,
        template="""
Create the beginning of an interactive adventure story in Spanish. 
The story should be engaging, descriptive and immersive with rich sensory details.
Use a varied, colorful vocabulary and evocative language to create a vivid narrative.
Develop an interesting initial scenario that draws the reader in.

Provide 3 distinct options for the user to choose from to continue the story. These options should be meaningful choices that would lead the story in different directions.

Format your response as a JSON with the following structure:
{
    "scene": "The descriptive scene text in Spanish",
    "options": ["Option 1 in Spanish", "Option 2 in Spanish", "Option 3 in Spanish"]
}
""",
    )

    STORY_CONTINUE_PROMPT: ClassVar[PromptTemplate] = PromptTemplate(
        prompt_type=PromptType.STORY_CONTINUE,
        template="""
{context}

The user chose: "{choice}"

Continue the interactive adventure story in Spanish based on this choice.
The continuation should be engaging, descriptive and maintain narrative consistency with what has happened before.
Expand the world and characters with each continuation, adding depth and nuance to the story.
Maintain a consistent tone and writing style, while building tension and development.

Provide 3 distinct and meaningful options for what the user can do next. These options should:
- Offer real agency to the user
- Present interesting dilemmas or choices
- Lead the story in different potential directions

Format your response as a JSON with the following structure:
{{
    "scene": "The descriptive scene text that follows from the choice in Spanish",
    "options": ["Option 1 in Spanish", "Option 2 in Spanish", "Option 3 in Spanish"]
}}
""",
    )

    # Prompts del Optimizador de Prompts
    PROMPT_OPTIMIZATION_TEMPLATE: ClassVar[PromptTemplate] = PromptTemplate(
        prompt_type=PromptType.PROMPT_OPTIMIZATION,
        template="""
Based on the following story scene in Spanish, create a detailed prompt in English for an image generation model.
The prompt should describe a vivid, detailed visual scene that captures the essence of the story moment.
Focus on key visual elements, setting, atmosphere, characters, lighting, angle, style, mood, and emotions.

Use specific artistic references when appropriate (photorealistic, cinematic, anime style, etc.)
Include technical details that would enhance the quality (depth of field, high resolution, detailed, etc.)
The prompt should be 2-3 sentences long and highly descriptive for optimal image generation.

Story scene: "{context}"
""",
    )

    # Prompts del Evaluador de Contexto Musical
    MUSIC_EVALUATION_PROMPT: ClassVar[PromptTemplate] = PromptTemplate(
        prompt_type=PromptType.MUSIC_EVALUATION,
        template="""
I'm going to provide you with a story scene in Spanish and the current background music categories.
Please analyze the emotional tone, atmosphere, and narrative context of the scene carefully.
Evaluate if the current music is still appropriate for the scene.
If it's not appropriate, recommend a new music category that would fit better.

Consider:
- The emotional tone and intensity of the scene
- The narrative context (action, dialogue, reflection, etc.)
- The setting and atmosphere described
- Character emotions and tensions
- Pacing and dramatic progression

Story scene: "{scene}"

Current music categories: {categories}

Format your response as JSON in Spanish:
{{
    "is_appropriate": true or false,
    "explanation": "Brief explanation of your decision in Spanish",
    "recommended_categories": ["category1", "category2", ...],  // Include even if 'is_appropriate' is true as fallback options
    "emotional_tone": "Brief description of the scene's emotional tone in Spanish"
}}
""",
    )

    # Prompts de rol del sistema
    STORY_SYSTEM_PROMPT: ClassVar[SystemPrompt] = SystemPrompt(
        role_type=SystemRoleType.STORYTELLER,
        content="""You are a creative storyteller creating interactive adventures in Spanish.
You excel at crafting engaging, atmospheric narratives with rich descriptions and meaningful choices.
Always respond in Spanish only. Format all outputs using the specified JSON structure.
Your writing should be immersive, varied, and appropriate for general audiences.""",
    )

    PROMPT_OPTIMIZER_SYSTEM_PROMPT: ClassVar[SystemPrompt] = SystemPrompt(
        role_type=SystemRoleType.PROMPT_OPTIMIZER,
        content="""You are an expert at creating detailed, evocative prompts for image generation.
You can analyze a scene written in Spanish and extract the key visual elements to create the perfect image generation prompt in English.
Focus on visual details, atmosphere, composition, artistic style, and emotional resonance.""",
    )

    MUSIC_SYSTEM_PROMPT: ClassVar[SystemPrompt] = SystemPrompt(
        role_type=SystemRoleType.MUSIC_EXPERT,
        content="""You are an expert at matching music to narrative contexts.
You specialize in analyzing scenes written in Spanish and determining the perfect musical accompaniment.
You understand how music can enhance storytelling through emotional tone, pacing, and atmosphere.
Always respond in Spanish only.""",
    )

    @classmethod
    def format_story_continue(cls, context: str, choice: str) -> str:
        """Formatea el prompt de continuación de historia con contexto y elección"""
        return cls.STORY_CONTINUE_PROMPT.template.format(context=context, choice=choice)

    @classmethod
    def format_prompt_optimization(cls, context: str) -> str:
        """Formatea la plantilla de optimización de prompts con contexto"""
        return cls.PROMPT_OPTIMIZATION_TEMPLATE.template.format(context=context)

    @classmethod
    def format_music_evaluation(cls, scene: str, categories: List[str]) -> str:
        """Formatea el prompt de evaluación musical con escena y categorías"""
        return cls.MUSIC_EVALUATION_PROMPT.template.format(
            scene=scene, categories=categories
        )


# Para compatibilidad con versiones anteriores
STORY_START_PROMPT = PromptTemplates.STORY_START_PROMPT.template
STORY_CONTINUE_PROMPT = PromptTemplates.STORY_CONTINUE_PROMPT.template
PROMPT_OPTIMIZATION_TEMPLATE = PromptTemplates.PROMPT_OPTIMIZATION_TEMPLATE.template
MUSIC_EVALUATION_PROMPT = PromptTemplates.MUSIC_EVALUATION_PROMPT.template

STORY_SYSTEM_PROMPT = PromptTemplates.STORY_SYSTEM_PROMPT.content
PROMPT_OPTIMIZER_SYSTEM_PROMPT = PromptTemplates.PROMPT_OPTIMIZER_SYSTEM_PROMPT.content
MUSIC_SYSTEM_PROMPT = PromptTemplates.MUSIC_SYSTEM_PROMPT.content
