import logging
import sys
from typing import Optional
from enum import Enum
import colorama
from colorama import Fore, Style

# Inicializar colorama para colores en consola
colorama.init()

class DebugLevel(Enum):
    """Niveles de verbosidad para el debugging."""
    QUIET = 0      # Sin output
    NORMAL = 1     # Solo errores y warnings
    VERBOSE = 2    # Información adicional
    DEBUG = 3      # Información detallada
    TRACE = 4      # Información muy detallada

class DebugManager:
    """Gestor de debugging con diferentes niveles de verbosidad."""
    
    def __init__(self, level: DebugLevel = DebugLevel.NORMAL):
        self.level = level
        self.logger = logging.getLogger('ai_watchdog')
        self._setup_logger()
    
    def _setup_logger(self):
        """Configura el logger con el formato y nivel apropiados."""
        self.logger.setLevel(logging.DEBUG)
        
        # Crear handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        
        # Definir formato con colores
        formatter = logging.Formatter(
            f'{Fore.CYAN}%(asctime)s{Style.RESET_ALL} - '
            f'{Fore.GREEN}%(name)s{Style.RESET_ALL} - '
            f'{Fore.YELLOW}%(levelname)s{Style.RESET_ALL} - '
            f'%(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Añadir handler al logger
        self.logger.addHandler(console_handler)
    
    def set_level(self, level: DebugLevel):
        """Establece el nivel de verbosidad."""
        self.level = level
        self.logger.setLevel(self._get_logging_level())
    
    def _get_logging_level(self) -> int:
        """Convierte DebugLevel a nivel de logging."""
        levels = {
            DebugLevel.QUIET: logging.ERROR,
            DebugLevel.NORMAL: logging.WARNING,
            DebugLevel.VERBOSE: logging.INFO,
            DebugLevel.DEBUG: logging.DEBUG,
            DebugLevel.TRACE: logging.DEBUG
        }
        return levels[self.level]
    
    def error(self, message: str, exc_info: Optional[Exception] = None):
        """Registra un error."""
        if self.level.value >= DebugLevel.QUIET.value:
            self.logger.error(f"{Fore.RED}{message}{Style.RESET_ALL}", exc_info=exc_info)
    
    def warning(self, message: str):
        """Registra una advertencia."""
        if self.level.value >= DebugLevel.NORMAL.value:
            self.logger.warning(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
    
    def info(self, message: str):
        """Registra información general."""
        if self.level.value >= DebugLevel.VERBOSE.value:
            self.logger.info(f"{Fore.BLUE}{message}{Style.RESET_ALL}")
    
    def debug(self, message: str):
        """Registra información de debugging."""
        if self.level.value >= DebugLevel.DEBUG.value:
            self.logger.debug(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
    
    def trace(self, message: str):
        """Registra información muy detallada."""
        if self.level.value >= DebugLevel.TRACE.value:
            self.logger.debug(f"{Fore.MAGENTA}[TRACE] {message}{Style.RESET_ALL}")
    
    def print_section(self, title: str, content: str):
        """Imprime una sección formateada."""
        if self.level.value >= DebugLevel.VERBOSE.value:
            print(f"\n{Fore.CYAN}{'='*50}")
            print(f"{title}")
            print(f"{'='*50}{Style.RESET_ALL}")
            print(content)
            print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    def print_progress(self, current: int, total: int, prefix: str = ""):
        """Imprime una barra de progreso."""
        if self.level.value >= DebugLevel.NORMAL.value:
            bar_length = 50
            filled_length = int(bar_length * current / total)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            percent = 100 * current / total
            print(f"\r{prefix} |{bar}| {percent:.1f}%", end='')
            if current == total:
                print()

# Instancia global del DebugManager
debug_manager = DebugManager()

def get_debug_manager() -> DebugManager:
    """Retorna la instancia global del DebugManager."""
    return debug_manager 