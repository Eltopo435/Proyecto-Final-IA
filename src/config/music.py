"""
    Sergio Gabriel Pérez
    23-EISN-2-028

    Configuración y gestión de música para la aplicación StoryCraft.
    Define categorías de música, rutas y mapeo de archivos musicales.
"""

import os
import pathlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Union

# Definir el directorio raíz del proyecto
ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
MUSIC_DIR = ASSETS_DIR / "music"

# Asegurar que el directorio de música exista
os.makedirs(MUSIC_DIR, exist_ok=True)


class MusicCategory(Enum):
    """Enumeración de categorías musicales para diferentes contextos de historia"""

    CALM = "calm"  # Calmado
    TENSE = "tense"  # Tenso
    ADVENTURE = "adventure"  # Aventura
    MYSTERY = "mystery"  # Misterio
    BATTLE = "battle"  # Batalla
    ROMANTIC = "romantic"  # Romántico
    SAD = "sad"  # Triste
    HAPPY = "happy"  # Feliz
    EPIC = "epic"  # Épico
    FOREST = "forest"  # Bosque
    CITY = "city"  # Ciudad
    DUNGEON = "dungeon"  # Mazmorra
    SPACE = "space"  # Espacio
    URBAN = "urban"  # Urbano

    @classmethod
    def get_all_categories(cls) -> List[str]:
        """Obtener una lista de todos los valores de categoría"""
        return [category.value for category in cls]


class MusicFileType(Enum):
    """Enumeración de tipos de archivos de música soportados"""

    MP3 = ".mp3"
    WAV = ".wav"
    OGG = ".ogg"

    @classmethod
    def is_supported(cls, filename: str) -> bool:
        """Verificar si un archivo tiene una extensión de música soportada"""
        return any(filename.lower().endswith(ext.value) for ext in cls)


@dataclass
class MusicFile:
    """Clase que representa un archivo de música con sus metadatos asociados"""

    path: pathlib.Path  # Ruta del archivo
    categories: List[MusicCategory] = field(default_factory=list)  # Categorías asociadas

    @property
    def filename(self) -> str:
        """Obtener solo el nombre del archivo"""
        return self.path.name

    @property
    def relative_path(self) -> str:
        """Obtener la ruta relativa al directorio de música"""
        return str(self.path.relative_to(MUSIC_DIR))

    @property
    def absolute_path(self) -> str:
        """Obtener la ruta absoluta como string"""
        return str(self.path.absolute())

    @property
    def category_values(self) -> List[str]:
        """Obtener los valores de categoría como strings"""
        return [category.value for category in self.categories]

    def matches_category(self, category: Union[MusicCategory, str]) -> bool:
        """Verificar si el archivo de música coincide con una categoría específica"""
        if isinstance(category, str):
            return any(cat.value == category for cat in self.categories)
        return category in self.categories


@dataclass
class MusicLibrary:
    """Clase para gestionar la colección de archivos de música"""

    music_files: Dict[str, MusicFile] = field(default_factory=dict)  # Diccionario de archivos

    def __post_init__(self) -> None:
        """Inicializar la biblioteca de música escaneando el directorio de música"""
        self.refresh()

    def refresh(self) -> None:
        """Actualizar la biblioteca de música escaneando el directorio"""
        self.music_files.clear()

        if not MUSIC_DIR.exists():
            return

        for file_path in MUSIC_DIR.glob("**/*"):
            if file_path.is_file() and MusicFileType.is_supported(file_path.name):
                music_file = MusicFile(path=file_path)
                self.music_files[music_file.absolute_path] = music_file

    def add_file(self, file_path: Union[str, pathlib.Path]) -> Optional[MusicFile]:
        """Añadir un archivo a la biblioteca"""
        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path)

        if not file_path.exists() or not MusicFileType.is_supported(file_path.name):
            return None

        music_file = MusicFile(path=file_path)
        self.music_files[music_file.absolute_path] = music_file
        return music_file

    def assign_categories(
        self,
        file_path: Union[str, pathlib.Path],
        categories: List[Union[MusicCategory, str]],
    ) -> bool:
        """Asignar categorías a un archivo de música"""
        if isinstance(file_path, str):
            abs_path = str(pathlib.Path(file_path).absolute())
        else:
            abs_path = str(file_path.absolute())

        if abs_path not in self.music_files:
            return False

        music_file = self.music_files[abs_path]
        music_file.categories = []

        for category in categories:
            if isinstance(category, str):
                try:
                    music_file.categories.append(MusicCategory(category))
                except ValueError:
                    # Omitir strings de categoría inválidos
                    pass
            else:
                music_file.categories.append(category)

        return True

    def get_by_category(self, category: Union[MusicCategory, str]) -> List[MusicFile]:
        """Obtener todos los archivos de música que coinciden con una categoría específica"""
        result = []

        for music_file in self.music_files.values():
            if music_file.matches_category(category):
                result.append(music_file)

        return result

    def get_all_files(self) -> List[MusicFile]:
        """Obtener todos los archivos de música en la biblioteca"""
        return list(self.music_files.values())

    def get_all_paths(self) -> List[str]:
        """Obtener todas las rutas de archivos de música como strings"""
        return [file.absolute_path for file in self.music_files.values()]

    @property
    def is_empty(self) -> bool:
        """Verificar si la biblioteca está vacía"""
        return len(self.music_files) == 0


# Crear una instancia global de la biblioteca de música
MUSIC_LIBRARY = MusicLibrary()

# Mapeo de tipos de estado de ánimo/escena a categorías de música recomendadas
MOOD_TO_CATEGORY_MAP: Dict[str, List[MusicCategory]] = {
    "action": [MusicCategory.BATTLE, MusicCategory.ADVENTURE, MusicCategory.EPIC],  # Acción
    "relaxed": [MusicCategory.CALM, MusicCategory.ROMANTIC],  # Relajado
    "tense": [MusicCategory.TENSE, MusicCategory.MYSTERY],  # Tenso
    "sad": [MusicCategory.SAD],  # Triste
    "happy": [MusicCategory.HAPPY, MusicCategory.ADVENTURE],  # Feliz
    "nature": [MusicCategory.FOREST],  # Naturaleza
    "urban": [MusicCategory.CITY],  # Urbano
    "otherworldly": [MusicCategory.SPACE, MusicCategory.MYSTERY],  # Sobrenatural
    "dungeon": [MusicCategory.DUNGEON, MusicCategory.MYSTERY],  # Mazmorra
}

# Lista predeterminada de asignaciones de categoría para los archivos de música reales en la carpeta assets/music
DEFAULT_MUSIC_ASSIGNMENTS: Dict[str, List[MusicCategory]] = {
    "Adventure.mp3": [MusicCategory.ADVENTURE, MusicCategory.EPIC],
    "Battle.mp3": [MusicCategory.BATTLE, MusicCategory.TENSE],
    "Calm.mp3": [MusicCategory.CALM, MusicCategory.ROMANTIC],
    "City.mp3": [MusicCategory.CITY, MusicCategory.URBAN],
    "Dungeon.mp3": [MusicCategory.DUNGEON, MusicCategory.MYSTERY],
    "Epic.mp3": [MusicCategory.EPIC, MusicCategory.ADVENTURE],
    "Forrest.mp3": [MusicCategory.FOREST, MusicCategory.CALM],
    "Happy.mp3": [MusicCategory.HAPPY, MusicCategory.CALM],
    "Memories.mp3": [MusicCategory.SAD, MusicCategory.ROMANTIC],
    "Mistery.mp3": [MusicCategory.MYSTERY, MusicCategory.TENSE],
    "Sad.mp3": [MusicCategory.SAD],
    "Space.mp3": [MusicCategory.SPACE, MusicCategory.MYSTERY],
    "Tense.mp3": [MusicCategory.TENSE, MusicCategory.BATTLE],
}


def assign_default_categories() -> None:
    """
    Asignar automáticamente categorías a los archivos de música en la biblioteca basándose en DEFAULT_MUSIC_ASSIGNMENTS.
    Esto asegura que todos los archivos de música tengan categorías apropiadas.
    """
    music_library = MUSIC_LIBRARY
    music_library.refresh()

    for music_file in music_library.get_all_files():
        filename = music_file.filename
        if filename in DEFAULT_MUSIC_ASSIGNMENTS:
            music_library.assign_categories(
                music_file.path, DEFAULT_MUSIC_ASSIGNMENTS[filename]
            )


if __name__ == "__main__":
    # Código de prueba que se ejecuta solo cuando se ejecuta este archivo directamente
    print(ROOT_DIR)  # Imprimir directorio raíz
    print(ASSETS_DIR)  # Imprimir directorio de assets
    print(MUSIC_DIR)  # Imprimir directorio de música

    # Crear una instancia nueva de la biblioteca de música
    music_library = MusicLibrary()

    # Asegurarse de tener los archivos más recientes
    music_library.refresh()

    # Imprimir archivos antes de la asignación de categorías (para depuración)
    print("\nAntes de la asignación de categorías:")
    for music_file in music_library.get_all_files():
        print(f"Archivo: {music_file.filename}, Categorías: {music_file.category_values}")

    # Limpiar y asignar categorías a cada archivo explícitamente
    print("\nAsignando categorías...")
    for music_file in music_library.get_all_files():
        filename = music_file.filename
        if filename in DEFAULT_MUSIC_ASSIGNMENTS:
            categories = DEFAULT_MUSIC_ASSIGNMENTS[filename]
            music_library.assign_categories(music_file.path, categories)
            print(f"Asignadas {[cat.value for cat in categories]} a {filename}")

    # Imprimir todos los archivos de música y sus categorías después de la asignación
    print("\nDespués de la asignación de categorías:")
    for music_file in music_library.get_all_files():
        print(f"Archivo: {music_file.filename}, Categorías: {music_file.category_values}")
