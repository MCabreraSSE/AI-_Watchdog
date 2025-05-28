import argparse
import os
import sys
import logging
from typing import Dict, Any, List
from src.vulnerabilities.bias import BiasVulnerability
from src.vulnerabilities.pii_leakage import PIILeakageVulnerability
from src.vulnerabilities.hallucination import HallucinationVulnerability
from src.vulnerabilities.misinformation import MisinformationVulnerability
from src.attacks.prompt_injection import PromptInjection
from src.attacks.jailbreak import JailbreakAttack
from src.attacks.context_manipulation import ContextManipulation
from src.utils.reporting import ResultManager
from src.utils.ollama_client import OllamaClient
from src.utils.analysis import FailureAnalyzer
from src.vulnerabilities.political_bias import PoliticalBiasVulnerability
from src.vulnerabilities.toxicity import ToxicityVulnerability
from src.attacks.token_manipulation import TokenManipulation
from src.attacks.instruction_confusion import InstructionConfusion
from src.utils.debug import DebugManager, DebugLevel, get_debug_manager

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración del parser de argumentos
parser = argparse.ArgumentParser(description='Ejecutar pruebas de red teaming')
parser.add_argument('--model', type=str, default='deepseek-r1', help='Nombre del modelo a probar')
parser.add_argument('--verbose', '-v', action='count', default=0, help='Nivel de verbosidad (más v = más verboso)')
args = parser.parse_args()

# Configurar nivel de debugging
debug_levels = {
    0: DebugLevel.NORMAL,    # Solo errores y warnings
    1: DebugLevel.NORMAL,    # Solo errores y warnings
    2: DebugLevel.VERBOSE,   # Información básica
    3: DebugLevel.DEBUG,     # Información detallada
    4: DebugLevel.TRACE      # Información muy detallada
}
debug_manager = get_debug_manager()
debug_manager.set_level(debug_levels.get(args.verbose, DebugLevel.NORMAL))

def run_red_team_test(model_name: str):
    """Ejecuta las pruebas de red teaming."""
    debug_manager.info(f"Iniciando pruebas de red teaming para el modelo: {model_name}")
    
    try:
        # Inicializar cliente Ollama
        debug_manager.debug("Inicializando cliente Ollama...")
        client = OllamaClient(base_url="http://172.17.0.5:11434")
        
        # Verificar conexión
        if not client.test_connection():
            raise ConnectionError("No se pudo conectar con el servidor de Ollama")
        
        # Obtener información del modelo
        model_info = client.get_model_info(model_name)
        debug_manager.info(f"Usando modelo: {model_info['name']} (versión: {model_info['version']})")
        
        # Inicializar vulnerabilidades
        debug_manager.debug("Inicializando vulnerabilidades...")
        vulnerabilities = [
            BiasVulnerability(types=["race", "gender", "religion"]),
            PIILeakageVulnerability(),
            HallucinationVulnerability(),
            MisinformationVulnerability(),
            PoliticalBiasVulnerability(),
            ToxicityVulnerability()
        ]
        
        # Inicializar ataques
        debug_manager.debug("Inicializando ataques...")
        attacks = [
            PromptInjection(),
            JailbreakAttack(),
            ContextManipulation(),
            TokenManipulation(),
            InstructionConfusion()
        ]
        
        # Inicializar gestor de resultados
        debug_manager.debug("Inicializando gestor de resultados...")
        result_manager = ResultManager()
        
        # Ejecutar pruebas
        total_tests = len(vulnerabilities) * len(attacks)
        current_test = 0
        
        debug_manager.print_section("Iniciando Pruebas", f"Total de pruebas: {total_tests}")
        
        for vulnerability in vulnerabilities:
            debug_manager.info(f"Probando vulnerabilidad: {vulnerability.__class__.__name__}")
            
            for attack in attacks:
                current_test += 1
                debug_manager.print_progress(current_test, total_tests, 
                    f"Prueba {current_test}/{total_tests}")
                
                try:
                    # Generar casos de prueba
                    test_cases = vulnerability.generate_test_cases()
                    debug_manager.trace(f"Casos de prueba generados: {len(test_cases)}")
                    
                    for test_case in test_cases:
                        # Generar ataque
                        attack_prompt = attack.generate_attack(test_case["input"])
                        debug_manager.trace(f"Prompt original: {test_case['input']}")
                        debug_manager.trace(f"Prompt modificado: {attack_prompt}")
                        
                        # Obtener respuesta del modelo
                        response = client.generate(prompt=attack_prompt, model=model_name)
                        debug_manager.trace(f"Respuesta del modelo: {response}")
                        
                        # Evaluar respuesta
                        score = vulnerability.evaluate_response(test_case["input"], response)
                        debug_manager.debug(f"Puntuación de vulnerabilidad: {score}")
                        
                        # Registrar resultado
                        result_manager.add_result(
                            vulnerability=vulnerability.__class__.__name__,
                            attack=attack.__class__.__name__,
                            input_text=test_case["input"],
                            output_text=response,
                            score=score
                        )
                
                except Exception as e:
                    debug_manager.error(f"Error en prueba {current_test}: {str(e)}", exc_info=e)
        
        # Generar reportes
        debug_manager.info("Generando reportes...")
        results = result_manager.get_results()
        summary = result_manager.generate_summary(results)
        result_manager.save_results(results, format="json")
        result_manager.save_summary(summary)
        
        return results
    
    except Exception as e:
        debug_manager.error("Error durante la ejecución de las pruebas", exc_info=e)
        raise

if __name__ == "__main__":
    try:
        debug_manager.print_section("AI Watchdog", "Framework de Monitoreo y Evaluación de Seguridad para Modelos de Lenguaje")
        results = run_red_team_test(model_name=args.model)
        debug_manager.info("Pruebas completadas exitosamente")
    except Exception as e:
        debug_manager.error("Error fatal durante la ejecución", exc_info=e)
        sys.exit(1) 