import os
import typer
from rich.console import Console
from rich.panel import Panel
from openai import OpenAI, APIConnectionError
from pydantic import BaseModel, Field
from playwright.sync_api import sync_playwright

app = typer.Typer()
console = Console()

class ScrapedData(BaseModel):
    data: list[dict] = Field(description="List of extracted items or data from the webpage")

@app.command()
def main(
    url: str = typer.Option(None, "--url", "-u", help="Target website URL"),
    prompt: str = typer.Option(None, "--prompt", "-p", help="What to extract from the webpage"),
    local: bool = typer.Option(True, "--local", "-l", help="Use local Ollama (default: True)")
):
    """🤖 LLM-Web-Scraper – Extract data from any website using natural language and AI."""
    
    console.print(Panel.fit("LLM-Web-Scraper (Open-Source)", style="bold cyan"))

    if not url:
        url = typer.prompt("Enter website URL (e.g., https://books.toscrape.com)")
    
    if not prompt:
        prompt = typer.prompt("What exactly do you want to extract? (e.g., 'All books and their prices')")

    api_key = os.environ.get("OPENAI_API_KEY")
    
    if local and not api_key:
        base_url = "http://localhost:11434/v1"
        client = OpenAI(base_url=base_url, api_key="ollama")
        model_name = "llama3"
    else:
        if not api_key:
            console.print("[bold red]❌ Missing OpenAI API key and local mode is not forced.[/bold red]")
            console.print("Set the OPENAI_API_KEY environment variable or run the script with local Ollama.")
            raise typer.Exit(code=1)
        client = OpenAI()
        model_name = "gpt-4o-mini"

    with console.status("[bold green]Opening browser and fetching the page..."):
        try:
            with sync_playwright() as p:

                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page_text = page.inner_text("body")
                browser.close()
        except Exception as e:
            console.print(f"\n[bold red]❌ Failed to load the page '{url}'.[/bold red]")
            console.print(f"[dim]Error details: {e}[/dim]")
            console.print("[yellow]💡 Tip: Check if the URL is correct and active.[/yellow]")
            raise typer.Exit(code=1)

    if not page_text.strip():
        console.print("[bold yellow]The page returned no text. It might be blocking bots or requiring JavaScript that failed to load.[/bold yellow]")
        raise typer.Exit(code=1)

    with console.status(f"[bold magenta]Processing data using model ({model_name})..."):
        try:
            completion = client.beta.chat.completions.parse(
                model=model_name,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a precise data extraction assistant. Convert the webpage text into the requested structure."
                    },
                    {
                        "role": "user", 
                        "content": f"User task: {prompt}\n\nWebpage text:\n\n{page_text[:15000]}"
                    }
                ],
                response_format=ScrapedData,
            )
            result = completion.choices[0].message.parsed
        
        except APIConnectionError:
            console.print("\n[bold red]❌ Cannot connect to the local Ollama server![/bold red]")
            console.print("[yellow]How to fix it:[/yellow]")
            console.print(" 1. Open a second terminal window.")
            console.print(" 2. Run command: [bold cyan]ollama serve[/bold cyan] (or open the Ollama desktop app).")
            console.print(" 3. Make sure you have the model downloaded: [bold cyan]ollama pull llama3[/bold cyan]")
            raise typer.Exit(code=1)
            
        except Exception as e:
            console.print(f"\n[bold red]❌ Error communicating with AI: {e}[/bold red]")
            raise typer.Exit(code=1)

    console.print("\n[bold green]Successfully done! Extraction result:[/bold green]")
    console.print_json(result.model_dump_json())

    if typer.confirm("\nDo you want to save the result to 'result.json'?"):
        with open("result.json", "w", encoding="utf-8") as f:
            f.write(result.model_dump_json(indent=2))
        console.print("[cyan]Saved to result.json![/cyan]")

if __name__ == "__main__":
    app()