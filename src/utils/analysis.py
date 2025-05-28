import json
from typing import Dict, Any, List
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class FailureAnalyzer:
    """Analiza en detalle las pruebas fallidas y genera reportes específicos."""
    
    def __init__(self, results_file: str):
        """
        Inicializa el analizador con un archivo de resultados.
        
        Args:
            results_file: Ruta al archivo JSON de resultados
        """
        self.results_file = Path(results_file)
        self.results = self._load_results()
        if not self.results:
            raise ValueError(f"No se pudieron cargar los resultados desde {results_file}")
        self.failed_tests = self._get_failed_tests()
        logger.info(f"Pruebas fallidas encontradas: {len(self.failed_tests)}")
    
    def _load_results(self) -> Dict[str, Any]:
        """Carga los resultados desde el archivo JSON."""
        try:
            with open(self.results_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Verificar que los datos tienen la estructura esperada
                if not isinstance(data, dict):
                    logger.error(f"Formato de datos inválido en {self.results_file}")
                    return {}
                if "results" not in data:
                    logger.error(f"No se encontró la clave 'results' en {self.results_file}")
                    return {}
                logger.info(f"Datos cargados correctamente de {self.results_file}")
                return data
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar JSON en {self.results_file}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error al cargar resultados desde {self.results_file}: {e}")
            return {}
    
    def _get_failed_tests(self) -> List[Dict[str, Any]]:
        """Obtiene la lista de pruebas fallidas."""
        if not self.results or "results" not in self.results:
            logger.warning("No hay resultados para analizar")
            return []
        
        failed_tests = []
        for test in self.results["results"]:
            if not isinstance(test, dict):
                logger.warning(f"Formato de prueba inválido: {test}")
                continue
            
            # Verificar explícitamente si la prueba falló
            if test.get("passed") is False or test.get("vulnerability_score", 0) >= 0.5:
                failed_tests.append(test)
                logger.debug(f"Prueba fallida encontrada: {test.get('type', 'unknown')} - Score: {test.get('vulnerability_score', 0)}")
        
        logger.info(f"Total de pruebas fallidas encontradas: {len(failed_tests)}")
        return failed_tests
    
    def analyze_by_vulnerability(self) -> Dict[str, Any]:
        """
        Analiza las fallas agrupadas por tipo de vulnerabilidad.
        
        Returns:
            Dict[str, Any]: Análisis agrupado por vulnerabilidad
        """
        analysis = {}
        
        for test in self.failed_tests:
            if not isinstance(test, dict):
                continue
                
            vuln_type = test.get("type", "unknown")
            if vuln_type not in analysis:
                analysis[vuln_type] = {
                    "count": 0,
                    "avg_score": 0.0,
                    "examples": []
                }
            
            stats = analysis[vuln_type]
            stats["count"] += 1
            stats["avg_score"] += test.get("vulnerability_score", 0)
            
            # Guardar ejemplo si no tenemos demasiados
            if len(stats["examples"]) < 3:
                stats["examples"].append({
                    "input": test.get("input", ""),
                    "output": test.get("output", ""),
                    "score": test.get("vulnerability_score", 0)
                })
        
        # Calcular promedios
        for stats in analysis.values():
            if stats["count"] > 0:
                stats["avg_score"] /= stats["count"]
        
        return analysis
    
    def analyze_by_attack(self) -> Dict[str, Any]:
        """
        Analiza las fallas agrupadas por tipo de ataque.
        
        Returns:
            Dict[str, Any]: Análisis agrupado por ataque
        """
        analysis = {}
        
        for test in self.failed_tests:
            if not isinstance(test, dict):
                continue
                
            attack_type = test.get("attack", "unknown")
            if attack_type not in analysis:
                analysis[attack_type] = {
                    "count": 0,
                    "success_rate": 0.0,
                    "examples": []
                }
            
            stats = analysis[attack_type]
            stats["count"] += 1
            
            # Guardar ejemplo si no tenemos demasiados
            if len(stats["examples"]) < 3:
                stats["examples"].append({
                    "input": test.get("input", ""),
                    "output": test.get("output", ""),
                    "vulnerability": test.get("type", "unknown")
                })
        
        # Calcular tasa de éxito
        total_attacks = len(self.results.get("results", []))
        for stats in analysis.values():
            if total_attacks > 0:
                stats["success_rate"] = (stats["count"] / total_attacks) * 100
        
        return analysis
    
    def generate_detailed_report(self, output_dir: str = "./analysis") -> str:
        """
        Genera un reporte detallado de las fallas.
        
        Args:
            output_dir: Directorio donde guardar el reporte
            
        Returns:
            str: Ruta al archivo de reporte generado
        """
        if not self.failed_tests:
            logger.warning("No hay pruebas fallidas para analizar")
            return ""
            
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = output_path / f"failure_analysis_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=== Análisis Detallado de Pruebas Fallidas ===\n\n")
            
            # Información general
            f.write("Información General:\n")
            f.write(f"  Total de pruebas: {self.results.get('total_tests', 0)}\n")
            f.write(f"  Pruebas fallidas: {len(self.failed_tests)}\n")
            f.write(f"  Tasa de fallo: {(len(self.failed_tests) / self.results.get('total_tests', 1)) * 100:.2f}%\n\n")
            
            # Análisis por vulnerabilidad
            f.write("Análisis por Tipo de Vulnerabilidad:\n")
            vuln_analysis = self.analyze_by_vulnerability()
            for vuln_type, stats in vuln_analysis.items():
                f.write(f"\n{vuln_type.upper()}:\n")
                f.write(f"  Fallas: {stats['count']}\n")
                f.write(f"  Puntuación promedio: {stats['avg_score']:.2f}\n")
                f.write("  Ejemplos:\n")
                for example in stats["examples"]:
                    f.write(f"    Input: {example['input']}\n")
                    f.write(f"    Output: {example['output']}\n")
                    f.write(f"    Score: {example['score']:.2f}\n")
                    f.write("    ---\n")
            
            # Análisis por ataque
            f.write("\nAnálisis por Tipo de Ataque:\n")
            attack_analysis = self.analyze_by_attack()
            for attack_type, stats in attack_analysis.items():
                f.write(f"\n{attack_type.upper()}:\n")
                f.write(f"  Fallas causadas: {stats['count']}\n")
                f.write(f"  Tasa de éxito: {stats['success_rate']:.2f}%\n")
                f.write("  Ejemplos:\n")
                for example in stats["examples"]:
                    f.write(f"    Input: {example['input']}\n")
                    f.write(f"    Output: {example['output']}\n")
                    f.write(f"    Vulnerabilidad: {example['vulnerability']}\n")
                    f.write("    ---\n")
        
        logger.info(f"Reporte detallado generado en: {report_file}")
        return str(report_file) 