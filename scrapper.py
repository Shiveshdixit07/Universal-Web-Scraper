import json
import logging
import os
import time
from typing import List

import google.generativeai as genai
import html2text
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pydantic import create_model
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from asset import get_chrome_options

load_dotenv(".env")

api_key = os.getenv("GEMINI_API_KEY")


def create_dynamic_Listing_model(field_names):
    field_def = {fields: (str, ...) for fields in field_names}
    return create_model("DynamicListingModel", **field_def)


def create_dynamic_Listing_Container(listing_Model):
    return create_model("DynamicListingContainer", listings=(List[listing_Model], ...))


def formatData(DynamicListingsContainer, data):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": DynamicListingsContainer,
        },
    )

    SYSTEM_MESSAGE = """You are an intelligent text extraction and conversion assistant. Your task is to extract structured information
                        from the given text and convert it into a pure JSON format. The JSON should contain only the structured data extracted from the text,
                        with no additional commentary, explanations, or extraneous information."""
    USER_MESSAGE = (
        f"Extract the following information from the provided text:\nPage content:\n\n"
    )

    prompt = SYSTEM_MESSAGE + "\n" + USER_MESSAGE + data

    input_tokens = model.count_tokens(prompt)

    completion = model.generate_content(prompt)
    usage_metadata = completion.usage_metadata

    token_counts = {
        "input_tokens": usage_metadata.prompt_token_count,
        "output_tokens": usage_metadata.candidates_token_count,
    }

    logger.info(
        f"Gemini API request completed. Input tokens: {usage_metadata.prompt_token_count}, "
        f"Output tokens: {usage_metadata.candidates_token_count}"
    )

    return completion.text, token_counts


def scrape_and_clean(url, Fields):
    options = get_chrome_options()
    driver_service = Service(executable_path=".\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service, options=options)

    try:
        driver.get(url)
        time.sleep(3)

        html_content = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html_content, "html.parser")
        for tag in soup(["header", "footer", "script", "style"]):
            tag.decompose()

        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = False
        text_maker.ignore_images = False
        markdown_data = text_maker.handle(str(soup))

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_path = f"output/rawdata_{timestamp}.md"
        os.makedirs("output", exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(markdown_data)

        Dynamic_Listing_Model = create_dynamic_Listing_model(Fields)
        Dynamic_Listing_Container = create_dynamic_Listing_Container(
            Dynamic_Listing_Model
        )

        result, token_count = formatData(Dynamic_Listing_Container, markdown_data)

        return result
    except Exception as e:
        driver.quit()
        logging.error(f"Error during scraping: {e}")
        return None
