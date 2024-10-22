# temp/color_test.py

from rich.console import Console

console = Console(force_terminal=True)
console.print("[bold green]Успешно! Это цветной текст.[/bold green]")
console.print("[red]Ошибка! Это красный текст.[/red]")
console.print("[blue]Информация. Это синий текст.[/blue]")
