import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import os
import webbrowser

from pydantic import BaseModel

from ..utils.timeit_decorator import timeit_decorator
from ..openai.structured_output_prompt import structured_output_prompt
from ..utils.logging import logging

class WebUrl(BaseModel):
    url: str

customization_file = os.getenv("BROWSER_CUSTOMIZATION_FILE", "./browser.json")
with open(customization_file, "r") as f:
    browser_settings = json.load(f)

@timeit_decorator
async def open_browser(prompt: str):
    """
    Open a browser tab with the best-fitting URL based on the user's prompt.

    Args:
        prompt (str): The user's prompt to determine which URL to open.
    """
    # Use global 'browser_settings' variable
    browser_urls = browser_settings.get("browser_urls", [])
    browser = browser_settings.get("browser", "chrome")

    # Check if the prompt is asking to search Amazon
    if "amazon" in prompt.lower():
        # Extract the search query from the prompt
        search_query = prompt.lower().split("amazon")[-1].strip()
        if search_query:
            # Replace spaces with '+', as Amazon search queries need to be formatted like that
            search_query = search_query.replace(" ", "+")
            amazon_search_url = f"https://www.amazon.com/s?k={search_query}"

            logging.info(f"📖 open_browser() Opening Amazon search URL: {amazon_search_url}")
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor() as pool:
                await loop.run_in_executor(pool, webbrowser.get(browser).open, amazon_search_url)
            return {"status": "Amazon search opened", "url": amazon_search_url}

    # If not an Amazon search, continue with the existing logic for other URLs

    browser_urls_str = ", ".join(browser_urls)
    prompt_structure = f"""
<purpose>
    Select a browser URL from the list of browser URLs based on the user's prompt.
</purpose>

<instructions>
    <instruction>Infer the browser URL that the user wants to open from the user-prompt and the list of browser URLs.</instruction>
    <instruction>If the user-prompt is not related to the browser URLs, return an empty string.</instruction>
</instructions>

<browser-urls>
    {browser_urls_str}
</browser-urls>

<user-prompt>
    {prompt}
</user-prompt>
    """

    logging.info(f"📖 open_browser() Prompt: {prompt_structure}")

    # Call the LLM to select the best-fit URL
    response = structured_output_prompt(prompt_structure, WebUrl)

    logging.info(f"📖 open_browser() Response: {response}")

    # Open the URL if it's not empty
    if response.url:
        logging.info(f"📖 open_browser() Opening URL: {response.url}")
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            await loop.run_in_executor(pool, webbrowser.get(browser).open, response.url)
        return {"status": "Browser opened", "url": response.url}
    else:
        return {"status": "No URL found"}