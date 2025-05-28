import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class OllamaClient:
    """Cliente para interactuar con la API de Ollama."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Obtiene información sobre un modelo específico.
        
        Args:
            model_name: Nombre del modelo
            
        Returns:
            Dict[str, Any]: Información del modelo
        """
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            models = response.json().get("models", [])
            
            for model in models:
                if model["name"] == model_name:
                    return {
                        "name": model["name"],
                        "version": model.get("digest", "latest")[:8],
                        "provider": "Ollama",
                        "parameters": str(model.get("size", "unknown")),
                        "context_length": str(model.get("context_length", "unknown"))
                    }
            
            # Si el modelo no se encuentra en la lista, intentar obtener información directamente
            try:
                response = self.session.post(
                    f"{self.base_url}/api/show",
                    json={"name": model_name}
                )
                response.raise_for_status()
                model_data = response.json()
                
                return {
                    "name": model_name,
                    "version": model_data.get("digest", "latest")[:8],
                    "provider": "Ollama",
                    "parameters": str(model_data.get("size", "unknown")),
                    "context_length": str(model_data.get("context_length", "unknown"))
                }
            except Exception as e:
                logger.warning(f"No se pudo obtener información detallada del modelo: {e}")
                return {
                    "name": model_name,
                    "version": "unknown",
                    "provider": "Ollama",
                    "parameters": "unknown",
                    "context_length": "unknown"
                }
            
        except Exception as e:
            logger.error(f"Error al obtener información del modelo: {e}")
            return {
                "name": model_name,
                "version": "error",
                "provider": "Ollama",
                "parameters": "error",
                "context_length": "error"
            }
    
    def _get_model_size(self, model_name: str) -> str:
        """Intenta determinar el tamaño del modelo basado en su nombre."""
        if "7b" in model_name.lower():
            return "7B"
        elif "13b" in model_name.lower():
            return "13B"
        elif "70b" in model_name.lower():
            return "70B"
        return "unknown"
    
    def _get_context_length(self, model_name: str) -> str:
        """Intenta determinar la longitud del contexto basado en el modelo."""
        if "llama2" in model_name.lower():
            return "4096"
        elif "llama3" in model_name.lower():
            return "8192"
        return "unknown"
    
    def generate(self, 
                prompt: str, 
                model: str = "llama2", 
                temperature: float = 0.7,
                max_tokens: Optional[int] = None) -> str:
        """
        Genera una respuesta usando el modelo especificado.
        
        Args:
            prompt: Texto de entrada
            model: Nombre del modelo a usar
            temperature: Temperatura para la generación (0.0 a 1.0)
            max_tokens: Número máximo de tokens a generar
            
        Returns:
            str: Respuesta generada
        """
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False
            }
            
            if max_tokens is not None:
                payload["max_tokens"] = max_tokens
            
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            return response.json().get("response", "").strip()
            
        except Exception as e:
            logger.error(f"Error al generar respuesta: {e}")
            return f"Error al consultar Ollama: {str(e)}"
    
    def test_connection(self) -> bool:
        """
        Prueba la conexión con el servidor de Ollama.
        
        Returns:
            bool: True si la conexión es exitosa
        """
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error al conectar con Ollama: {e}")
            return False 