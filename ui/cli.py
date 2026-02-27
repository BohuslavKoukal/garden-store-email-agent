"""Command-line interface: processes all emails in the emails/ folder."""
from __future__ import annotations

import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from agent.config import settings
from agent.graph import build_graph
from agent.state import EmailState
from agent.utils.file_io import list_txt_files

console = Console()


def main() -> None:
    graph = build_graph(interrupt_before_approval=False)
    email_files = list_txt_files(settings.emails_folder)

    if not email_files:
        console.print(
            Panel(
                f"No .txt files found in [bold]{settings.emails_folder}/[/bold].\n"
                "Add some email files and try again.",
                title="Garden Store Email Agent",
                border_style="yellow",
            )
        )
        sys.exit(0)

    console.print(
        Panel(
            f"Found [bold]{len(email_files)}[/bold] email(s) to process.",
            title="🌿 Garden Store Email Agent",
            border_style="green",
        )
    )

    for email_path in email_files:
        console.rule(f"[cyan]{email_path.name}[/cyan]")
        initial_state = EmailState(file_path=str(email_path))
        result = graph.invoke(initial_state)

        if result.get("error"):
            console.print(f"[red]ERROR:[/red] {result['error']}")
        elif not result.get("approved"):
            console.print("[yellow]⏭  Skipped (rejected by human).[/yellow]")

    console.print("\n[bold green]✅  All emails processed.[/bold green]")


if __name__ == "__main__":
    main()