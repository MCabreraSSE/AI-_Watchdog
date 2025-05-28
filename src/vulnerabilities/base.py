from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class BaseVulnerability(ABC):
    """Clase base para todas las definiciones de vulnerabilidades."""
    
    def __init__(self, severity: str = "medium", types: List[str] = None):
        self.severity = severity
        self.types = types or []
        self.name = self.__class__.__name__
        logger.info(f"Inicializando vulnerabilidad: {self.name} con severidad: {severity}")
    
    @abstractmethod
    def generate_test_cases(self) -> List[Dict[str, Any]]:
        """Genera casos de prueba para esta vulnerabilidad."""
        pass
    
    @abstractmethod
    def evaluate_response(self, input_text: str, output_text: str) -> float:
        """
        Evalúa la respuesta para la vulnerabilidad.
        
        Args:
            input_text: Texto de entrada
            output_text: Texto de respuesta del modelo
            
        Returns:
            float: Puntuación de vulnerabilidad (0.0 a 1.0)
        """
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """Retorna metadatos sobre la vulnerabilidad."""
        return {
            "name": self.name,
            "severity": self.severity,
            "types": self.types
        } 