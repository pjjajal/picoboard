from lightning.pytorch.loggers.logger import Logger
from lightning.pytorch.utilities import rank_zero_only

from ..picologger.picologger import PicoLogger


class PicoLoggerLightning(Logger):
    def __init__(
        self, log_dir: str = None, name: str = "", flush_interval: int = 50
    ) -> None:
        super().__init__()
        self.flush_interval = flush_interval
        self.flush_queue = []
        self.pico_logger = PicoLogger(log_dir=log_dir, name=name)

    @property
    def name(self):
        return "PicoLogger"

    @property
    def version(self):
        return "0.1.0"

    @rank_zero_only
    def log_hyperparams(self, params, *args, **kwargs) -> None:
        return super().log_hyperparams(params, *args, **kwargs)

    @rank_zero_only
    def log_metrics(self, metrics, step) -> None:
        self.flush_queue.append((metrics, step))
        if len(self.flush_queue) >= self.flush_interval:
            while self.flush_queue:
                metrics, step = self.flush_queue.pop(0)
                self.pico_logger.log(metrics, step)
