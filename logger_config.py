import logging
import sys
from pathlib import Path

def setup_logger(name: str = "fii_dashboard", log_file: str = "app.log"):
    """
    Configura logger com handlers para arquivo e console.

    Args:
        name: Nome do logger
        log_file: Caminho do arquivo de log

    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Evitar duplicação de handlers
    if logger.handlers:
        return logger

    # Formato de log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler para arquivo
    log_path = Path(log_file)
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
