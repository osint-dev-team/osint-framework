#!/usr/bin/env python3

from art import text2art
from rich.panel import Panel
from rich import box
from rich.console import Console


def show_opener() -> None:
    """
    Show logo art
    :return: None
    """
    text = text2art("osint-framework", font="cjk", chr_ignore=True)
    console = Console()
    console.print(Panel(text, expand=False, border_style="red", box=box.DOUBLE))
