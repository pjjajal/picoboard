import loguru

from .picologger import PicoLogger

__all__ = ["PicoLogger"]

try:
    from .extensions.lightning import PicoLoggerLightning

    __all__.append("PicoLoggerLightning")
except ModuleNotFoundError:
    loguru.logger.warning("Lightning extension not available. Skipping import.")
