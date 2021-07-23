from rich.console import Console
from rich.theme import Theme


class Logger:
    def __init__(self) -> None:
        self.theme = Theme(
            {
                "success": "#7DEB34",
                "info": "dim #edffbd",
                "warning": "#d1ca3b",
                "error": "#8F003C",
            }
        )
        self.console = Console(theme=self.theme)

    def log(self, *args, **kwargs):
        self.console.log(*args, _stack_offset=2, **kwargs)

    def succes(self, *args, **kwargs):
        self.log(*args, style="success", **kwargs)

    def info(self, *args, **kwargs):
        self.log(*args, style="info", **kwargs)

    def warning(self, *args, **kwargs):
        self.log(*args, style="warning", **kwargs)

    def error(self, *args, **kwargs):
        self.log(*args, style="error", **kwargs)


logger = Logger()
