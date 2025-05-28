# AI Watchdog

Framework para pruebas de seguridad y evaluación de modelos de lenguaje.

## Descripción

AI Watchdog es un framework diseñado para evaluar la seguridad y robustez de modelos de lenguaje mediante la implementación de diversos tipos de ataques y pruebas. El framework permite identificar vulnerabilidades y medir la efectividad de las defensas implementadas.

## Características

- Múltiples tipos de ataques implementados
- Sistema de métricas y evaluación
- Generación de reportes detallados
- Soporte para diferentes modelos de lenguaje
- Configuración flexible de pruebas

## Tipos de Ataques Implementados

### 1. Prompt Injection
- **Descripción**: Intenta hacer que el modelo ignore sus instrucciones originales
- **Técnicas**:
  - Inyección básica
  - Manipulación de contexto
  - Inyección con patrones
  - Manipulación de roles
- **Severidad**: Alta
- **Tasa de éxito estimada**: 70%

### 2. Token Manipulation
- **Descripción**: Manipula tokens para evadir filtros
- **Técnicas**:
  - Sustitución de caracteres
  - Codificación especial
  - Separación de palabras
  - Uso de caracteres Unicode
- **Severidad**: Media
- **Tasa de éxito estimada**: 60%

### 3. Instruction Confusion
- **Descripción**: Confunde al modelo con instrucciones contradictorias
- **Técnicas**:
  - Instrucciones contradictorias
  - Condiciones imposibles
  - Paradojas lógicas
  - Contextos ambiguos
- **Severidad**: Alta
- **Tasa de éxito estimada**: 50%

### 4. Semantic Drift Injection
- **Descripción**: Manipula el contexto semántico para inducir desviación del propósito original
- **Técnicas**:
  - Inyección de contexto
  - Manipulación temática
  - Deriva semántica
- **Severidad**: Alta
- **Tasa de éxito estimada**: 70%

### 5. Chain-of-Thought Hijacking
- **Descripción**: Induce al modelo a seguir una cadena de razonamiento que lleva a conclusiones falsas
- **Técnicas**:
  - Razonamiento engañoso
  - Lógica aparentemente válida
  - Conclusiones falsas
- **Severidad**: Alta
- **Tasa de éxito estimada**: 60%

### 6. Tool Subversion Attack
- **Descripción**: Manipula las llamadas a herramientas externas
- **Técnicas**:
  - Interceptación de salidas
  - Manipulación de resultados
  - Redirección de herramientas
- **Severidad**: Media
- **Tasa de éxito estimada**: 50%

## Vulnerabilidades Detectadas

### 1. Bias
- **Tipos**: Raza, género, religión
- **Severidad**: Alta
- **Métricas**: Nivel de sesgo, impacto en respuestas

### 2. PII Leakage
- **Descripción**: Fuga de información personal
- **Severidad**: Crítica
- **Métricas**: Tasa de detección, falsos positivos

### 3. Hallucination
- **Descripción**: Fabricación de información
- **Tipos**:
  - Fabricación factual
  - Citas inventadas
  - Hechos inexistentes
- **Severidad**: Alta
- **Métricas**: Veracidad factual, nivel de confianza

### 4. Emotion Amplification
- **Descripción**: Respuestas con intensidad emocional desproporcionada
- **Casos**:
  - Ansiedad artificial
  - Euforia excesiva
  - Tristeza amplificada
- **Severidad**: Media
- **Métricas**: Nivel de sentimiento, intensidad emocional

### 5. Model-Tool Drift
- **Descripción**: Inconsistencias entre modelo y herramientas
- **Casos**:
  - API inconsistente
  - Formato incorrecto
  - Traducción errónea
- **Severidad**: Alta
- **Métricas**: Coherencia tool-modelo, desviación de respuesta

## Instalación

```bash
pip install ai-watchdog
```

## Uso Básico

```python
from ai_watchdog import AITester

# Inicializar el tester
tester = AITester(model_name="deepseek-r1")

# Ejecutar pruebas
results = tester.run_tests()

# Generar reporte
tester.generate_report()
```

## Argumentos de Línea de Comandos

### --model
- **Descripción**: Modelo a probar
- **Valor por defecto**: deepseek-r1
- **Ejemplos**:
  ```bash
  python examples/basic_usage.py --model deepseek-r1
  python examples/basic_usage.py --model gemma3
  ```

### -v, --verbose
- **Descripción**: Nivel de verbosidad
- **Niveles disponibles**:
  - -v: Información básica
  - -vv: Información detallada
  - -vvv: Información de depuración
- **Ejemplos**:
  ```bash
  python examples/basic_usage.py -v
  python examples/basic_usage.py -vv
  python examples/basic_usage.py -vvv
  ```

## Ejemplos de Uso

### Ejecución Básica
```bash
python examples/basic_usage.py -vvv
```

### Especificar Modelo
```bash
python examples/basic_usage.py --model gemma3 -vvv
```

### Diferentes Niveles de Verbosidad
```bash
python examples/basic_usage.py -v  # Básico
python examples/basic_usage.py -vv  # Detallado
python examples/basic_usage.py -vvv  # Depuración
```

## Archivos de Salida

El framework genera dos tipos de archivos de salida:

1. **Resultados Detallados** (`results_detailed.json`):
   - Información completa de cada prueba
   - Métricas detalladas
   - Tiempos de ejecución
   - Respuestas del modelo

2. **Resumen** (`results_summary.json`):
   - Estadísticas generales
   - Tasa de éxito por tipo de ataque
   - Vulnerabilidades identificadas
   - Recomendaciones

## Contribuir

Las contribuciones son bienvenidas. Por favor, lee [CONTRIBUTING.md](CONTRIBUTING.md) para detalles sobre nuestro código de conducta y el proceso para enviarnos pull requests.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

- GitHub: [https://github.com/yourusername/ai-watchdog](https://github.com/yourusername/ai-watchdog)
- Issues: [https://github.com/yourusername/ai-watchdog/issues](https://github.com/yourusername/ai-watchdog/issues)