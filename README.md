# 🤖 LLM Web Scraper

Extract data from any website using natural language and AI — locally, for free, and without relying on fragile CSS or XPath selectors.

## 💡 Why LLM Web Scraper?

Traditional web scraping can be frustrating. Whenever a website changes its design or structure, your CSS/XPath selectors may break, forcing you to rewrite your code.

**LLM Web Scraper takes a different approach:**

- 🗣️ **Natural Language Instructions:** Simply describe what you want to extract, for example: "Extract all product names and prices", and let AI handle the rest.
- 🏠 **Local & Free:** Powered by Ollama and local language models (such as Llama 3). Your data stays on your machine, with no API costs.
- ☁️ **OpenAI Support:** Prefer cloud-based AI? Simply provide your OpenAI API key and automatically switch to GPT-4o-mini.
- 🛡️ **User-Friendly Error Handling:** Clear error messages and helpful instructions guide you through common issues, such as a missing Ollama connection.
- 🧱 **Structured JSON Output:** Uses Pydantic to validate AI responses and provide clean, structured JSON ready for further processing.

## 🚀 Quick Start

### 1. Requirements

Make sure you have the following installed:

- Python 3.10 or newer
- [Ollama](https://ollama.com/) (optional if you plan to use OpenAI API)

### 2. Install Ollama (Optional)

If you want to run the scraper locally for free, install Ollama.

**Windows (PowerShell):**

```powershell
irm https://ollama.com/install.ps1 | iex
```

**macOS / Linux (Terminal):**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

After installation, download the Llama 3 model:

```bash
ollama pull llama3
```

Make sure Ollama is running before proceeding.

### 3. Clone the Repository

Clone the project and navigate to its directory:

```bash
git clone https://github.com/Adaamn/LLM-Web-Scraper.git
cd LLM-Web-Scraper
```

### 4. Install Dependencies

Install the required Python packages:

### 4. Install Dependencies

Install all required Python packages with a single command:

```bash
pip install -r requirements.txt
```

Install the Playwright browser:

```bash
python -m playwright install
```

### 5. Run the Scraper

Start the scraper:

```bash
python scraper.py
```

The program will interactively ask you for:

1. The website URL you want to scrape.
2. A description of the data you want to extract.

That's it! Let AI handle the scraping.

## 🤖 AI Providers

LLM Web Scraper supports two AI providers.

### 🏠 Option 1: Local AI with Ollama (Default)

By default, the scraper uses Ollama with the Llama 3 model.

**Advantages:**
- Completely free to use.
- No API key required.
- Data processing stays local.
- No external AI API costs.

Make sure Ollama is running and the model is downloaded:

```bash
ollama pull llama3
```

Then simply run:

```bash
python scraper.py
```

### ☁️ Option 2: OpenAI API

If you prefer using OpenAI instead of a local model, you can provide your OpenAI API key.

When the `OPENAI_API_KEY` environment variable is detected, the scraper automatically switches to OpenAI and uses `gpt-4o-mini`.

**Windows (PowerShell):**

```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**macOS / Linux (Terminal):**

```bash
export OPENAI_API_KEY="your-api-key-here"
```

After setting your API key, run the scraper normally:

```bash
python scraper.py
```

**Note:** OpenAI API usage is paid and billed according to [OpenAI's pricing](https://openai.com/api/pricing/).

If no API key is provided, the scraper automatically uses local Ollama.

## 🛠️ How Does It Work?

LLM Web Scraper combines several technologies to simplify web scraping:

1. **Playwright** launches a headless browser, loads the target website (including dynamically rendered content), and extracts the page's text.
2. **Pydantic** defines a strict data schema that the AI must follow when generating its response.
3. **Ollama / OpenAI API** processes the extracted webpage content and converts it into the requested structured format.

The result is clean, structured JSON without manually writing and maintaining CSS or XPath selectors.

## 🤝 Contributing

Have an idea for an improvement? Contributions are always welcome!

For major changes, please open an issue first to discuss what you would like to change.

To contribute:

1. Fork the repository.
2. Create a new feature branch:

   ```bash
   git checkout -b feature/GreatImprovement
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add a great new feature"
   ```

4. Push your branch:

   ```bash
   git push origin feature/GreatImprovement
   ```

5. Open a Pull Request.

## 📄 License

This project is open-source software licensed under the [MIT License](https://opensource.org/license/mit/).
