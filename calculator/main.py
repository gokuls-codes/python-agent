# main.py

import sys
from fractions import Fraction
from pkg.calculator import Calculator
from pkg.history import save_to_history, load_history

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.text import Text
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

def format_result(result):
    if isinstance(result, Fraction):
        if result.denominator == 1:
            return str(result.numerator)
        return str(result)
    elif isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)

def print_separator():
    print("-" * 40)

def print_simple_panel(title, content):
    print_separator()
    print(f"| {title.upper()} |")
    print_separator()
    print(f"  {content}")
    print_separator()

def main():
    calculator = Calculator()
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ("--interactive", "-i"):
            if RICH_AVAILABLE:
                interactive_mode_rich(calculator, Console())
            else:
                interactive_mode_simple(calculator)
        elif arg in ("--help", "-h"):
            print_help()
        else:
            expression = " ".join(sys.argv[1:])
            if RICH_AVAILABLE:
                process_expression(calculator, expression, console=Console())
            else:
                process_expression(calculator, expression, use_rich=False)
    else:
        # Default to interactive mode if no arguments are provided
        if RICH_AVAILABLE:
            interactive_mode_rich(calculator, Console())
        else:
            interactive_mode_simple(calculator)

def print_help():
    if RICH_AVAILABLE:
        console = Console()
        table = Table(title="Calculator App Usage", border_style="cyan")
        table.add_column("Command", style="bold yellow")
        table.add_column("Description")
        table.add_row("python main.py [expression]", "Evaluate an expression directly")
        table.add_row("python main.py --interactive / -i", "Enter interactive mode")
        table.add_row("python main.py --help / -h", "Show this help message")
        console.print(table)
    else:
        print("Calculator App Usage:")
        print("  python main.py [expression]        - Evaluate an expression")
        print("  python main.py --interactive / -i  - Enter interactive mode")
        print("  python main.py --help / -h         - Show this help message")

def process_expression(calculator, expression, console=None, use_rich=True):
    try:
        result = calculator.evaluate(expression)
        if result is not None:
            formatted_result = format_result(result)
            
            if use_rich and console:
                panel = Panel(
                    Text(f"{expression} = {formatted_result}", style="bold green"),
                    title="Result",
                    border_style="blue",
                    expand=False
                )
                console.print(panel)
            else:
                print_simple_panel("Result", f"{expression} = {formatted_result}")
        else:
            if use_rich and console:
                console.print("[red]Error: Expression is empty or contains only whitespace.[/red]")
            else:
                print("Error: Expression is empty or contains only whitespace.")
    except Exception as e:
        if use_rich and console:
            console.print(f"[bold red]Error:[/bold red] {e}")
        else:
            print(f"Error: {e}")

def interactive_mode_simple(calculator):
    print("================================")
    print("   SIMPLE CLI CALCULATOR")
    print("      (Interactive mode)")
    print("================================")
    print("Type 'exit' or 'quit' to leave.\n")
    
    history = load_history()
    if history:
        print("Previous history:")
        for h in history[-5:]:
            print(f"  {h}")
        print()
    
    while True:
        try:
            expression = input("> ")
            
            if expression.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            
            if not expression.strip():
                continue
            
            save_to_history(expression)
            process_expression(calculator, expression, use_rich=False)
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

def interactive_mode_rich(calculator, console):
    console.print(Panel("[bold blue]Simple CLI Calculator[/bold blue]\nType 'exit' or 'quit' to leave.", border_style="cyan"))
    
    history = load_history()
    if history:
        console.print("[dim]Last 5 entries from history:[/dim]")
        for h in history[-5:]:
            console.print(f"[dim]  {h}[/dim]")
    
    while True:
        try:
            expression = Prompt.ask("[bold yellow]Enter expression[/bold yellow]")
            
            if expression.lower() in ("exit", "quit"):
                console.print("[dim]Goodbye![/dim]")
                break
            
            if not expression.strip():
                continue
            
            save_to_history(expression)
            process_expression(calculator, expression, console=console)
        except EOFError:
            break
        except KeyboardInterrupt:
            console.print("\n[dim]Goodbye![/dim]")
            break

if __name__ == "__main__":
    main()
