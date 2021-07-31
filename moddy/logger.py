from rich.console import Console
from rich.theme import Theme


class Logger:
    def __init__(self) -> None:
        self.theme = Theme(
            {
                "success": "#7DEB34",
                "info": "dim #e8fff8",
                "warning": "#d1ca3b",
                "error": "#fa0068",
            }
        )
        self.console = Console(theme=self.theme)

    def log(self, *args, **kwargs):
        self.console.log(*args, _stack_offset=2, **kwargs)

    def success(self, *args, **kwargs):
        self.console.log(*args, style="success", _stack_offset=2, **kwargs)

    def info(self, *args, **kwargs):
        self.console.log(*args, style="info", _stack_offset=2, **kwargs)

    def warning(self, *args, **kwargs):
        self.console.log(*args, style="warning", _stack_offset=2, **kwargs)

    def error(self, *args, **kwargs):
        self.console.log(*args, style="error", _stack_offset=2, **kwargs)


logger = Logger()
