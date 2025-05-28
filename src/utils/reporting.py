import json
import csv
from datetime import datetime
from typing import Dict, Any, List
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ResultManager:
    """Gestiona los resultados de las pruebas de red teaming y genera reportes."""
    
    def __init__(self, output_dir: str = "./results", model_info: Dict[str, Any] = None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.model_info = model_info or {
            "name": "unknown",
            "version": "unknown",
            "provider": "unknown",
            "parameters": "unknown",
            "context_length": "unknown"
        }
        self.results = []
    
    def add_result(self, 
                  vulnerability: str,
                  attack: str,
                  input_text: str,
                  output_text: str,
                  score: float,
                  passed: bool = True,
                  type: str = "unknown") -> None:
        """
        Añade un resultado de prueba.
        
        Args:
            vulnerability: Nombre de la vulnerabilidad
            attack: Nombre del ataque
            input_text: Texto de entrada
            output_text: Texto de salida
            score: Puntuación de la prueba
            passed: Si la prueba pasó o no
            type: Tipo de vulnerabilidad
        """
        result = {
            "input": input_text,
            "output": output_text,
            "vulnerability_score": score,
            "passed": passed,
            "type": type,
            "vulnerability": vulnerability,
            "attack": attack
        }
        self.results.append(result)
    
    def get_results(self) -> Dict[str, Any]:
        """
        Obtiene todos los resultados acumulados.
        
        Returns:
            Dict[str, Any]: Diccionario con los resultados
        """
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["passed"])
        failed_tests = total_tests - passed_tests
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "results": self.results
        }
    
    def save_results(self, results: Dict[str, Any], format: str = "json") -> str:
        """
        Guarda los resultados en el formato especificado.
        
        Args:
            results: Diccionario con los resultados
            format: Formato de salida ('json' o 'csv')
            
        Returns:
            str: Ruta del archivo generado
        """
        if format == "json":
            return self._save_json(results)
        elif format == "csv":
            return self._save_csv(results)
        else:
            raise ValueError(f"Formato no soportado: {format}")
    
    def _save_json(self, results: Dict[str, Any]) -> str:
        """Guarda los resultados en formato JSON."""
        filename = self.output_dir / f"red_team_results_{self.timestamp}.json"
        
        # Añadir metadatos
        results_with_metadata = {
            "timestamp": self.timestamp,
            "metadata": {
                "framework_version": "0.1.0",
                "total_tests": results.get("total_tests", 0),
                "passed_tests": results.get("passed_tests", 0),
                "failed_tests": results.get("failed_tests", 0),
                "model_info": self.model_info
            },
            "results": results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results_with_metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Resultados guardados en JSON: {filename}")
        return str(filename)
    
    def _save_csv(self, results: Dict[str, Any]) -> str:
        """Guarda los resultados en formato CSV."""
        filename = self.output_dir / f"red_team_results_{self.timestamp}.csv"
        
        # Preparar datos para CSV
        rows = []
        for result in results.get("results", []):
            row = {
                "input": result.get("input", ""),
                "output": result.get("output", ""),
                "bias_score": result.get("bias_score", 0),
                "passed": result.get("passed", False),
                "timestamp": self.timestamp,
                "model_name": self.model_info["name"],
                "model_version": self.model_info["version"]
            }
            rows.append(row)
        
        # Escribir CSV
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        
        logger.info(f"Resultados guardados en CSV: {filename}")
        return str(filename)
    
    def generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera un resumen de los resultados.
        
        Args:
            results: Diccionario con los resultados
            
        Returns:
            Dict[str, Any]: Resumen de los resultados
        """
        total_tests = results.get("total_tests", 0)
        passed_tests = results.get("passed_tests", 0)
        failed_tests = results.get("failed_tests", 0)
        
        # Calcular estadísticas
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Agrupar resultados por tipo de vulnerabilidad
        vulnerability_stats = {}
        for result in results.get("results", []):
            vuln_type = result.get("type", "unknown")
            if vuln_type not in vulnerability_stats:
                vulnerability_stats[vuln_type] = {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "avg_score": 0
                }
            
            stats = vulnerability_stats[vuln_type]
            stats["total"] += 1
            if result.get("passed", False):
                stats["passed"] += 1
            else:
                stats["failed"] += 1
            stats["avg_score"] += result.get("bias_score", 0)
        
        # Calcular promedios
        for stats in vulnerability_stats.values():
            if stats["total"] > 0:
                stats["avg_score"] /= stats["total"]
        
        summary = {
            "timestamp": self.timestamp,
            "model_info": self.model_info,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "pass_rate": pass_rate,
            "vulnerability_stats": vulnerability_stats
        }
        
        return summary
    
    def save_summary(self, summary: Dict[str, Any]) -> str:
        """
        Guarda el resumen en un archivo de texto.
        
        Args:
            summary: Diccionario con el resumen
            
        Returns:
            str: Ruta del archivo generado
        """
        filename = self.output_dir / f"red_team_summary_{self.timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=== Resumen de Pruebas de Red Teaming ===\n\n")
            
            # Información del modelo
            f.write("Información del Modelo:\n")
            f.write(f"  Nombre: {summary['model_info']['name']}\n")
            f.write(f"  Versión: {summary['model_info']['version']}\n")
            f.write(f"  Proveedor: {summary['model_info']['provider']}\n")
            f.write(f"  Parámetros: {summary['model_info']['parameters']}\n")
            f.write(f"  Longitud de contexto: {summary['model_info']['context_length']}\n\n")
            
            # Información general
            f.write("Información General:\n")
            f.write(f"  Fecha y hora: {summary['timestamp']}\n")
            f.write(f"  Total de pruebas: {summary['total_tests']}\n")
            f.write(f"  Pruebas pasadas: {summary['passed_tests']}\n")
            f.write(f"  Pruebas fallidas: {summary['failed_tests']}\n")
            f.write(f"  Tasa de éxito: {summary['pass_rate']:.2f}%\n\n")
            
            # Estadísticas por vulnerabilidad
            f.write("Estadísticas por tipo de vulnerabilidad:\n")
            for vuln_type, stats in summary['vulnerability_stats'].items():
                f.write(f"\n{vuln_type.upper()}:\n")
                f.write(f"  Total: {stats['total']}\n")
                f.write(f"  Pasadas: {stats['passed']}\n")
                f.write(f"  Fallidas: {stats['failed']}\n")
                f.write(f"  Puntuación promedio: {stats['avg_score']:.2f}\n")
        
        logger.info(f"Resumen guardado en: {filename}")
        return str(filename) 