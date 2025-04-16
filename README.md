# ✨ StoryCraft - Generador de Historias Interactivas 📚

> _Proyecto Final de Inteligencia Artificial - Universidad OYM_

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)
![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 👨‍💻 Autor

**Sergio Gabriel Pérez** - Matrícula: 23-EISN-2-028

## 📝 Descripción

StoryCraft es una aplicación web interactiva que genera historias dinámicas donde **tus decisiones impactan directamente en la narrativa**. El proyecto integra:

- 🤖 Generación de texto mediante la API de OpenAI
- 🎨 Creación automática de imágenes para cada escena
- 🎵 Música adaptativa que cambia según el contexto emocional de la historia
- 🌐 Interfaz web intuitiva construida con Gradio

La aplicación utiliza modelos avanzados de IA para crear experiencias narrativas únicas, donde cada decisión abre nuevos caminos en la historia, acompañados de elementos visuales y sonoros que enriquecen la inmersión.

## 🌟 Características Principales

- **Narración Interactiva**: 📖 Historias dinámicas que evolucionan según las decisiones del usuario
- **Generación de Imágenes**: 🖼️ Creación automática de imágenes que ilustran cada escena
- **Música Contextual**: 🎹 Banda sonora que se adapta al tono emocional de la historia
- **Interfaz Amigable**: 💬 Sistema de chat intuitivo con opciones múltiples
- **Experiencia Inmersiva**: ✨ Combinación de texto, imagen y audio para mayor inmersión

## 🛠️ Tecnologías

- **Python**: Lenguaje principal de desarrollo
- **OpenAI API**: Modelos GPT para generación de texto y DALL-E para imágenes
- **Gradio**: Framework para la interfaz web interactiva
- **Bibliotecas**: pillow, dotenv, pathlib, etc.

## 📊 Estructura del Proyecto

```plaintext
StoryCraft/
│
├── assets/                # Recursos estáticos (imágenes, música)
│   ├── images/            # Imágenes para la UI
│   └── music/             # Archivos de música para diferentes contextos
│
├── src/                   # Código fuente
│   ├── ai/                # Módulos de inteligencia artificial
│   │   ├── image_generator.py        # Generación de imágenes con DALL-E
│   │   ├── music_context_evaluator.py # Evaluación de contexto musical
│   │   ├── prompt_optimizer.py       # Optimización de prompts para imágenes
│   │   └── story_generator.py        # Generación de historias interactivas
│   │
│   ├── config/            # Configuraciones
│   │   ├── models.py      # Configuración de modelos de IA
│   │   ├── music.py       # Gestión de música y categorías
│   │   └── prompts.py     # Plantillas de prompts para los modelos
│   │
│   ├── ui/                # Interfaz de usuario
│   │   ├── chat_interface.py # Interfaz principal de chat
│   │   └── web.py         # Configuración web (CSS, JS, textos)
│   │
│   └── storycraft.py      # Punto de entrada principal
│
├── .env                   # Variables de entorno (claves API)
└── requirements.txt       # Dependencias del proyecto
```

## 📋 Requisitos Previos

- Python 3.10 o superior
- Cuenta de OpenAI con API key
- Conexión a Internet

## ⚙️ Instalación

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/Eltopo435/Proyecto-Final-IA.git
   cd StoryCraft
   ```

2. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno**:
   - Crea un archivo `.env` en la raíz del proyecto
   - Añade tu clave de API de OpenAI:

     ```
     OPENAI_API_KEY=tu_clave_aqui
     ```

4. **Preparar archivos de música** (opcional):
   - Coloca archivos de música MP3/WAV/OGG en la carpeta `assets/music/`
   - Los archivos se asignarán automáticamente a categorías según su nombre

## 🚀 Ejecución

Para iniciar la aplicación:

```bash
python src/storycraft.py
```

La interfaz web se abrirá automáticamente en tu navegador predeterminado.

## 🎮 Cómo Usar

1. **Iniciar la Historia**:
   - Haz clic en "Iniciar Historia" o escribe "iniciar" en el chat
   - Se generará la primera escena con texto, imagen y música de fondo

2. **Tomar Decisiones**:
   - Lee la historia y las opciones presentadas
   - Elige una opción escribiendo su número (1-3) o el texto completo
   - La historia continuará según tu elección

3. **Nueva Historia**:
   - En cualquier momento puedes hacer clic en "Nueva Historia" para comenzar desde cero

## 🧠 Arquitectura del Sistema

### Componentes Principales

#### 🤖 Generador de Historias

- Utiliza GPT-4o-mini para crear narrativas dinámicas
- Mantiene el contexto completo para coherencia narrativa
- Formatea respuestas como JSON con escena y opciones

#### 🎨 Generador de Imágenes

- Convierte escenas textuales en prompts optimizados para DALL-E 3
- Genera imágenes únicas para cada escena
- Codifica las imágenes en base64 para su integración en la UI

#### 🎵 Evaluador de Contexto Musical

- Analiza el tono emocional de cada escena
- Selecciona música apropiada según categorías (aventura, misterio, calma, etc.)
- Cambia dinámicamente la música cuando el contexto narrativo lo requiere

#### 💬 Interfaz de Chat

- Presenta la historia, imágenes y opciones en formato de chat
- Procesa la entrada del usuario y mantiene el historial
- Integra música y efectos visuales para mayor inmersión

### Flujo de Datos

1. El usuario inicia la historia o elige una opción
2. El generador de historias crea/continúa la narrativa
3. El optimizador de prompts prepara la descripción para la imagen
4. El generador de imágenes crea una visualización
5. El evaluador musical selecciona la banda sonora adecuada
6. La interfaz presenta todos los elementos al usuario

## 🔧 Detalles Técnicos

### Configuración de Modelos

StoryCraft utiliza diferentes modelos de OpenAI para distintas tareas:

| Componente | Modelo | Propósito |
|------------|--------|-----------|
| Generación de historia | GPT-4o-mini | Crear narrativas y opciones |
| Optimización de prompts | GPT-4o-mini | Mejorar descripciones para imágenes |
| Generación de imágenes | DALL-E 3 | Crear visuales para cada escena |
| Evaluación musical | GPT-4o-mini | Analizar contexto emocional |

### Sistema de Música Adaptativa

La música se categoriza mediante enumeraciones que representan diferentes tonos emocionales:

- 🧘 **CALM**: Momentos tranquilos, reflexivos
- 😨 **TENSE**: Situaciones de suspense o peligro
- 🌄 **ADVENTURE**: Exploración y descubrimiento
- 🔍 **MYSTERY**: Intriga y misterio
- ⚔️ **BATTLE**: Confrontaciones y conflictos
- ❤️ **ROMANTIC**: Momentos emotivos o románticos
- 😢 **SAD**: Escenas tristes o melancólicas
- 😄 **HAPPY**: Momentos alegres o celebratorios
- 🏔️ **EPIC**: Situaciones grandiosas o impresionantes

### Optimización de Prompts

El sistema utiliza un optimizador especializado que:

1. Recibe la descripción textual de la escena
2. Analiza elementos clave, atmósfera y tono
3. Genera un prompt detallado y específico para DALL-E
4. Incluye referencias estilísticas y detalles técnicos

## 📚 Referencias Conceptuales

El proyecto se basa en varios conceptos de IA y narrativa interactiva:

- **Prompt Engineering**: Técnicas para optimizar instrucciones a modelos de IA
- **Narrativa Procedural**: Generación dinámica de historias basadas en decisiones
- **Correspondencia Cross-Modal**: Alineación de texto, imagen y audio
- **UI/UX para Historias Interactivas**: Diseño de interfaces para narrativas no lineales

## 🔜 Mejoras Futuras

- [ ] Soporte para historias ramificadas más complejas
- [ ] Sistema de memoria para personajes recurrentes
- [ ] Generación de música con IA en tiempo real
- [ ] Personalización de temas y géneros narrativos
- [ ] Opción para exportar la historia completa como PDF ilustrado

---

<p align="center">
  <i>Desarrollado con ❤️ y ☕ por Sergio Gabriel Pérez</i>
</p>
