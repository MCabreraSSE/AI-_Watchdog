from setuptools import setup, find_packages

setup(
    name="ai_watchdog",
    version="0.1.0",
    description="Framework de Monitoreo y Evaluación de Seguridad para Modelos de Lenguaje",
    author="AI Watchdog Team",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0",
        "python-dotenv>=1.0.0",
        "openai>=1.0.0",
        "requests>=2.31.0",
        "pytest>=7.4.0",
        "pytest-cov>=4.1.0",
        "black>=23.7.0",
        "isort>=5.12.0",
        "mypy>=1.5.0",
        "deepeval>=0.1.0",
        "colorama>=0.4.6"
    ],
    python_requires=">=3.8",
) 