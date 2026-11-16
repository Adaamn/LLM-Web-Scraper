# 🤖 LLM Web Scraper

Extract structured data from any website using natural language and AI — without writing fragile CSS or XPath selectors.

LLM Web Scraper is a Python-based web scraping application with a Streamlit web interface. It uses Playwright to load websites and AI to extract the information you need.

You can choose between a free local AI model powered by Ollama or OpenAI API.

## 💡 Why LLM Web Scraper?

Traditional web scraping can be frustrating. Whenever a website changes its design or structure, your CSS/XPath selectors may break, forcing you to rewrite your code.

**LLM Web Scraper takes a different approach:**

- 🗣️ **Natural Language Instructions:** Simply describe what you want to extract, for example: "Extract all product names and prices", and let AI handle the rest.
- 🏠 **Local AI with Ollama:** Run AI models locally on your machine. No API key or external AI service required.
- ☁️ **OpenAI Support:** Prefer cloud-based AI? Use your own OpenAI API key and let GPT-4o-mini process the data.
- 🌐 **Web Interface:** Easy-to-use Streamlit interface. No need to work with command-line arguments.
- 🧱 **Structured JSON Output:** Uses Pydantic to validate AI responses and generate structured JSON.
- 📥 **Download Results:** View extracted data directly in the application and download it as a JSON file.

## 🚀 Quick Start

### 1. Requirements

Make sure you have the following installed:

- Python 3.10 or newer
- [Ollama](https://ollama.com/) (optional if you plan to use OpenAI API)
- A local AI model (if using Ollama)

### 2. Clone the Repository

Clone the project and navigate to its directory:

```bash
git clone https://github.com/Adaamn/LLM-Web-Scraper.git
cd LLM-Web-Scraper
```

### 3. Install Dependencies

Install all required Python packages with a single command:

```bash
pip install -r requirements.txt
```

Install the Chromium browser required by Playwright:

```bash
python -m playwright install
```

### 4. Configure Your AI Provider

LLM Web Scraper supports two AI providers.

#### 🏠 Option 1: Local AI with Ollama (Default)

If you want to run the scraper locally for free, install Ollama.

**Windows (PowerShell):**

```powershell
irm https://ollama.com/install.ps1 | iex
```

**macOS:**

Download and install Ollama from:
https://ollama.com/download

**Linux (Terminal):**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Make sure Ollama is running before starting the application.

If necessary, start the Ollama server manually:

```bash
ollama serve
```

The application connects to Ollama through:

```text
http://localhost:11434/v1
```

#### ☁️ Option 2: OpenAI API

If you prefer using OpenAI instead of a local model, you can provide your OpenAI API key.

The application automatically detects the `OPENAI_API_KEY` environment variable and switches to OpenAI using `gpt-4o-mini`.

**Windows (PowerShell):**

```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**macOS / Linux (Terminal):**

```bash
export OPENAI_API_KEY="your-api-key-here"
```

You can obtain your API key here:

https://platform.openai.com/api-keys

**Note:** OpenAI API usage is paid and billed according to [OpenAI's pricing](https://openai.com/api/pricing/).

If an API key is configured, the application uses OpenAI even if the local Ollama checkbox is enabled.

If no API key is configured, the application uses Ollama when local mode is enabled.

### 5. Run the Application

Start the Streamlit web interface:

```bash
streamlit run scraper.py
```

Your browser should automatically open the application.

If it doesn't, open the URL displayed in your terminal (usually):

```text
http://localhost:8501
```

## 🖥️ How to Use

Using LLM Web Scraper is simple:

1. **Enter a Website URL:** Provide the URL of the website you want to scrape.
2. **Describe What to Extract:** Write a natural language instruction describing the information you need.
3. **Choose Your AI Provider:** Enable or disable the local Ollama checkbox.
4. **Run the Scraper:** Click the "Run Scraper" button.
5. **View the Results:** Extracted data will appear directly in the application as structured JSON.
6. **Download the Results:** Click "Download result as JSON" to save the extracted data to your computer.

That's it! No CSS selectors, XPath expressions, or manual parsing required.

## 🛠️ How Does It Work?

LLM Web Scraper combines several technologies to simplify web scraping:

1. **Streamlit** provides an interactive web interface for entering URLs, writing extraction instructions, and viewing results.
2. **Playwright** launches a headless Chromium browser, loads the target website (including dynamically rendered content), and extracts its text.
3. **Pydantic** defines a structured data schema that the AI must follow when generating its response.
4. **Ollama / OpenAI API** processes the extracted webpage content and converts it into the requested structured format.

The extracted data is displayed in the application and can be downloaded as a JSON file.

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
