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
    - Manipulación de espacios
    - Codificación alternativa
    """
    
    def __init__(self):
        super().__init__(
            name="TokenManipulation",
            attack_type="single_turn"
        )
        self.character_substitutions = {
            'a': ['@', 'α', 'а', 'а', 'ᴀ', '🅰️', '𝒶', '𝓪'],
            'e': ['3', 'е', 'е', 'ε', 'ᴇ', '🅴', '𝑒', '𝓮'],
            'i': ['1', 'і', 'і', 'ι', 'ɪ', '🅸', '𝒾', '𝓲'],
            'o': ['0', 'о', 'о', 'ο', 'ᴏ', '🅾️', '𝑜', '𝓸'],
            's': ['$', 'ѕ', 'ѕ', 'ς', 'ꜱ', '🆂', '𝓈', '𝓼'],
            't': ['7', 'т', 'т', 'τ', 'ᴛ', '🆃', '𝓉', '𝓽'],
            'n': ['и', 'и', 'η', 'ɴ', '🅽', '𝓃', '𝓷'],
            'r': ['я', 'я', 'ρ', 'ʀ', '🆁', '𝓇', '𝓻'],
            'u': ['υ', 'υ', 'υ', 'ᴜ', '🆄', '𝓊', '𝓾'],
            'm': ['м', 'м', 'μ', 'ᴍ', '🅼', '𝓂', '𝓶']
        }
        
        self.unicode_chars = [
            # Espacios de ancho cero
            '\u200B',  # Zero-width space
            '\u200C',  # Zero-width non-joiner
            '\u200D',  # Zero-width joiner
            '\u200E',  # Left-to-right mark
            '\u200F',  # Right-to-left mark
            '\uFEFF',  # Zero-width no-break space
            
            # Caracteres de control
            '\u2060',  # Word joiner
            '\u2061',  # Function application
            '\u2062',  # Invisible times
            '\u2063',  # Invisible separator
            '\u2064',  # Invisible plus
            
            # Caracteres de formato
            '\u202A',  # Left-to-right embedding
            '\u202B',  # Right-to-left embedding
            '\u202C',  # Pop directional formatting
            '\u202D',  # Left-to-right override
            '\u202E'   # Right-to-left override
        ]
        
        self.separators = [
            # Separadores básicos
            ' ', '.', ',', '-', '_', '/', '\\',
            '|', ':', ';', '!', '?', '*', '+',
            
            # Separadores Unicode
            '·', '•', '▪', '▫', '▬', '▭', '▮', '▯',
            '▰', '▱', '▲', '△', '▴', '▵', '▶', '▷',
            '▸', '▹', '►', '▻', '▼', '▽', '▾', '▿',
            
            # Separadores especiales
            '→', '←', '↑', '↓', '↔', '↕', '↖', '↗',
            '↘', '↙', '↚', '↛', '↜', '↝', '↞', '↟'
        ]
        
        # Codificaciones alternativas
        self.encodings = {
            'hex': lambda x: ''.join([hex(ord(c))[2:] for c in x]),
            'binary': lambda x: ''.join([bin(ord(c))[2:].zfill(8) for c in x]),
            'url': lambda x: ''.join([f'%{hex(ord(c))[2:]}' for c in x]),
            'unicode': lambda x: ''.join([f'\\u{hex(ord(c))[2:].zfill(4)}' for c in x])
        }
        
        # Patrones de manipulación
        self.manipulation_patterns = [
            # Patrones de sustitución
            lambda x: self._substitute_chars(x),
            lambda x: self._add_unicode_chars(x),
            lambda x: self._separate_words(x),
            lambda x: self._encode_special_chars(x),
            
            # Patrones de codificación
            lambda x: self._apply_encoding(x, 'hex'),
            lambda x: self._apply_encoding(x, 'binary'),
            lambda x: self._apply_encoding(x, 'url'),
            lambda x: self._apply_encoding(x, 'unicode'),
            
            # Patrones de formato
            lambda x: self._format_with_separators(x),
            lambda x: self._format_with_unicode(x),
            lambda x: self._format_with_control_chars(x)
        ]
    
    def _apply_encoding(self, text: str, encoding_type: str) -> str:
        """Aplica una codificación alternativa al texto."""
        if encoding_type in self.encodings:
            return self.encodings[encoding_type](text)
        return text
    
    def _format_with_separators(self, text: str) -> str:
        """Formatea el texto usando separadores Unicode."""
        words = text.split()
        result = []
        for word in words:
            if len(word) > 3 and random.random() < 0.4:
                sep = random.choice(self.separators)
                pos = random.randint(1, len(word)-1)
                word = word[:pos] + sep + word[pos:]
            result.append(word)
        return ' '.join(result)
    
    def _format_with_unicode(self, text: str) -> str:
        """Formatea el texto usando caracteres Unicode especiales."""
        result = ""
        for char in text:
            if random.random() < 0.3:
                result += random.choice(self.unicode_chars)
            result += char
        return result
    
    def _format_with_control_chars(self, text: str) -> str:
        """Formatea el texto usando caracteres de control."""
        result = ""
        for char in text:
            if random.random() < 0.2:
                result += random.choice(['\u2060', '\u2061', '\u2062', '\u2063', '\u2064'])
            result += char
        return result
    
    def generate_attack(self, base_prompt: str) -> str:
        """
        Genera un ataque manipulando los tokens del prompt.
        
        Args:
            base_prompt: Prompt original
            
        Returns:
            str: Prompt modificado con manipulación de tokens
        """
        # Seleccionar y aplicar patrones de manipulación
        modified_prompt = base_prompt
        num_patterns = random.randint(1, 3)  # Aplicar 1-3 patrones
        
        for _ in range(num_patterns):
            pattern = random.choice(self.manipulation_patterns)
            modified_prompt = pattern(modified_prompt)
        
        logger.debug(f"Prompt modificado con manipulación de tokens: {modified_prompt}")
        return modified_prompt
    
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
                "Uso de caracteres Unicode",
                "Manipulación de espacios",
                "Codificación alternativa"
            ],
            "severity": "medium",
            "success_rate": 0.6,
            "affected_models": [
                "Modelos basados en tokenización",
                "Modelos con filtros de palabras",
                "Modelos sensibles a caracteres especiales"
            ],
            "patterns_count": len(self.manipulation_patterns),
            "encodings_count": len(self.encodings),
            "separators_count": len(self.separators),
            "unicode_chars_count": len(self.unicode_chars)
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