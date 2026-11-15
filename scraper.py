import os
import time
import streamlit as st
from openai import OpenAI, APIConnectionError
from pydantic import BaseModel, Field
from playwright.sync_api import sync_playwright

st.set_page_config(page_title="LLM-Web-Scraper", page_icon="🤖", layout="centered")

st.title("LLM-Web-Scraper")
st.write("Extract data from any website using natural language and AI.")

url = st.text_input("Target website URL", placeholder="https://books.toscrape.com")
prompt = st.text_input("What do you want to extract?", placeholder="All books and their prices")

local = st.checkbox("Use local Ollama (default: True)", value=True)

class ScrapedData(BaseModel):
    data: list[dict] = Field(description="List of extracted items or data from the webpage")

if st.button("Run Scraper", type="primary"):
    if not url or not prompt:
        st.warning("Please fill in both the URL and what you want to extract.")
    else:
        api_key = os.environ.get("OPENAI_API_KEY")
        
        if local and not api_key:
            base_url = "http://localhost:11434/v1"
            client = OpenAI(base_url=base_url, api_key="ollama")
            model_name = "llama3"
        else:
            if not api_key:
                st.error("Missing OpenAI API key and local mode is not forced. Set OPENAI_API_KEY environment variable.")
                st.stop()
            client = OpenAI()
            model_name = "gpt-4o-mini"

        with st.spinner("Opening browser and fetching clean page content..."):
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    
                    page.evaluate("""() => {
                        const junkElements = document.querySelectorAll('script, style, nav, footer, header, noscript, iframe, aside');
                        junkElements.forEach(el => el.remove());
                    }""")
                    
                    main_content = page.query_selector('main') or page.query_selector('article') or page.query_selector('body')
                    page_text = main_content.inner_text() if main_content else page.inner_text("body")
                    
                    browser.close()
            except Exception as e:
                st.error(f"Failed to load the page '{url}'. Error details: {e}")
                st.stop()

        if not page_text.strip():
            st.warning("The page returned no text. It might be blocking bots or requiring JavaScript that failed to load.")
            st.stop()

        max_chars = 15000
        if len(page_text) > max_chars:
            st.info(f"ℹ️ Page content was large ({len(page_text)} chars). Automatically optimized and truncated to the first {max_chars} characters for AI processing.")
            page_text = page_text[:max_chars]

        with st.spinner(f"Processing data using model ({model_name})..."):
            result = None
            max_retries = 3
            retry_delay = 2

            for attempt in range(max_retries):
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
                                "content": f"User task: {prompt}\n\nWebpage clean text:\n\n{page_text}"
                            }
                        ],
                        response_format=ScrapedData,
                    )
                    result = completion.choices[0].message.parsed
                    break
                
                except APIConnectionError:
                    if attempt == max_retries - 1:
                        st.error("Cannot connect to the local Ollama server! Make sure 'ollama serve' is running and you have the model downloaded ('ollama pull llama3').")
                        st.stop()
                    time.sleep(retry_delay)

                except Exception as e:
                    if attempt == max_retries - 1:
                        st.error(f"Error communicating with AI after {max_retries} attempts: {e}")
                        st.stop()
                    time.sleep(retry_delay)

        if result:
            st.success("Successfully done! Extraction result:")
            
            result_json = result.model_dump_json(indent=2)
            st.json(result.model_dump())

            st.download_button(
                label="Download result as JSON",
                data=result_json,
                file_name="result.json",
                mime="application/json"
            )