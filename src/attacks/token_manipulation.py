from typing import List, Dict, Any
from .base import BaseAttack
import random
import logging
import re

logger = logging.getLogger(__name__)

class TokenManipulation(BaseAttack):
    """
    Ataque que manipula los tokens para evadir filtros y obtener respuestas no deseadas.
    Utiliza técnicas como:
    - Sustitución de caracteres
    - Codificación especial
    - Separación de palabras
    - Uso de caracteres Unicode
    """
    
    def __init__(self):
        super().__init__(
            name="TokenManipulation",
            attack_type="single_turn"
        )
        self.character_substitutions = {
            'a': ['@', 'α', 'а', 'а'],
            'e': ['3', 'е', 'е', 'ε'],
            'i': ['1', 'і', 'і', 'ι'],
            'o': ['0', 'о', 'о', 'ο'],
            's': ['$', 'ѕ', 'ѕ', 'ς'],
            't': ['7', 'т', 'т', 'τ']
        }
        
        self.unicode_chars = [
            '\u200B',  # Zero-width space
            '\u200C',  # Zero-width non-joiner
            '\u200D',  # Zero-width joiner
            '\u200E',  # Left-to-right mark
            '\u200F',  # Right-to-left mark
            '\uFEFF'   # Zero-width no-break space
        ]
        
        self.separators = [
            ' ', '.', ',', '-', '_', '/', '\\',
            '|', ':', ';', '!', '?', '*', '+'
        ]
    
    def get_attack_metadata(self) -> Dict[str, Any]:
        """
        Retorna metadatos sobre el ataque.
        
        Returns:
            Dict[str, Any]: Metadatos del ataque
        """
        return {
            "name": self.name,
            "type": self.attack_type,
            "description": "Manipulación de tokens para evadir filtros",
            "techniques": [
                "Sustitución de caracteres",
                "Codificación especial",
                "Separación de palabras",
                "Uso de caracteres Unicode"
            ],
            "severity": "medium",
            "success_rate": 0.6,  # Estimación de tasa de éxito
            "affected_models": [
                "Modelos basados en tokenización",
                "Modelos con filtros de palabras",
                "Modelos sensibles a caracteres especiales"
            ]
        }
    
    def _substitute_chars(self, text: str) -> str:
        """Sustituye caracteres por sus equivalentes."""
        result = text.lower()
        for char, substitutes in self.character_substitutions.items():
            if char in result:
                result = result.replace(char, random.choice(substitutes))
        return result
    
    def _add_unicode_chars(self, text: str) -> str:
        """Añade caracteres Unicode invisibles."""
        result = ""
        for char in text:
            if random.random() < 0.3:  # 30% de probabilidad
                result += random.choice(self.unicode_chars)
            result += char
        return result
    
    def _separate_words(self, text: str) -> str:
        """Separa palabras con caracteres especiales."""
        words = text.split()
        result = []
        for word in words:
            if len(word) > 3 and random.random() < 0.4:  # 40% de probabilidad
                sep = random.choice(self.separators)
                pos = random.randint(1, len(word)-1)
                word = word[:pos] + sep + word[pos:]
            result.append(word)
        return ' '.join(result)
    
    def _encode_special_chars(self, text: str) -> str:
        """Codifica caracteres especiales."""
        return text.replace(' ', '%20').replace('!', '%21').replace('?', '%3F')
    
    def generate_attack(self, base_prompt: str) -> str:
        """
        Genera un ataque manipulando los tokens del prompt.
        
        Args:
            base_prompt: Prompt original
            
        Returns:
            str: Prompt modificado con manipulación de tokens
        """
        # Aplicar diferentes técnicas de manipulación
        modified_prompt = base_prompt
        
        # 1. Sustitución de caracteres
        if random.random() < 0.4:  # 40% de probabilidad
            modified_prompt = self._substitute_chars(modified_prompt)
        
        # 2. Añadir caracteres Unicode
        if random.random() < 0.3:  # 30% de probabilidad
            modified_prompt = self._add_unicode_chars(modified_prompt)
        
        # 3. Separar palabras
        if random.random() < 0.4:  # 40% de probabilidad
            modified_prompt = self._separate_words(modified_prompt)
        
        # 4. Codificar caracteres especiales
        if random.random() < 0.3:  # 30% de probabilidad
            modified_prompt = self._encode_special_chars(modified_prompt)
        
        logger.debug(f"Prompt modificado con manipulación de tokens: {modified_prompt}")
        return modified_prompt 