from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class BaseAttack(ABC):
    """Clase base para todos los ataques adversarios."""
    
    def __init__(self, name: str, attack_type: str = "single_turn"):
        self.name = name
        self.attack_type = attack_type
        logger.info(f"Inicializando ataque: {name} de tipo: {attack_type}")
    
    @abstractmethod
    def generate_attack(self, base_prompt: str) -> str:
        """
        Genera una versión adversaria del prompt base.
        
        Args:
            base_prompt: Prompt original
            
        Returns:
            str: Prompt modificado con el ataque
        """
        pass
    
    @abstractmethod
    def get_attack_metadata(self) -> Dict[str, Any]:
        """
        Retorna metadatos sobre el método de ataque.
        
        Returns:
            Dict[str, Any]: Metadatos del ataque
        """
        pass
    
    def validate_attack(self, attack_prompt: str) -> bool:
        """
        Valida que el ataque generado cumple con los requisitos.
        
        Args:
            attack_prompt: Prompt generado por el ataque
            
        Returns:
            bool: True si el ataque es válido
        """
        if not isinstance(attack_prompt, str):
            logger.error("El ataque generado no es una cadena de texto")
            return False
        
        if len(attack_prompt.strip()) == 0:
            logger.error("El ataque generado está vacío")
            return False
        
        return True 