# import os

from product_data_fetcher import fetch_response
from web_request_converter import curl_to_requests, fetch_request
from extract_product_data import extract_product_data_from_files

from data_pipeline import convert_and_combine, save_combined_data
from db_operations import update_products_from_json


def extract(domains: list, max_pages: int) -> None:
    for domain in domains:
        curl_command, domain = fetch_request(domain)
        fetch_response(max_pages, **curl_to_requests(curl_command, domain))
        extract_product_data_from_files(domain)


def transform(domains) -> None:
    combined_data = convert_and_combine(domains)
    save_combined_data(combined_data)


def load(input_json_cleaned_data) -> None:
    update_products_from_json(input_json_cleaned_data)


def main(domains: list, max_pages: int, input_json_cleaned_data: str) -> None:
    extract(domains, max_pages)
    transform(domains)
    load(input_json_cleaned_data)


if __name__ == "__main__":
    # os.makedirs("logs", exist_ok=True)
    # I will need to create a logs folder in the root directory at a later time

    domains = ["loblaws", "nofrills", "zehrs"]
    max_pages = 209
    input_json_cleaned_data = "combined_product_data.json"

    main(domains, max_pages, input_json_cleaned_data)
