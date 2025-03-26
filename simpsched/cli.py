import click
from rich.console import Console


LOGO = """
     _                          _              _ 
 ___(_)_ __ ___  _ __  ___  ___| |__   ___  __| |
/ __| | '_ ` _ \\| '_ \\/ __|/ __| '_ \\ / _ \\/ _` |
\\__ \\ | | | | | | |_) \\__ \\ (__| | | |  __/ (_| |
|___/_|_| |_| |_| .__/|___/\\___|_| |_|\\___|\\__,_|
                |_|
"""

console = Console()


@click.command()
def cli():
    console.print(LOGO, style="#9bcffa", highlight=False)


if __name__ == "__main__":
    cli()
