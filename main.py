from webscraping import collect_all_product_info
from insight_AI import coletar_amostra, generate_feedback
DEFAULT_TEQUILA_PAGE_URL = "https://sipwhiskey.com/collections/rye-whiskey?page="

if __name__ == "__main__":
    all_product_info = collect_all_product_info(DEFAULT_TEQUILA_PAGE_URL)
    # mais do loop principal aqui ... \/\/
    sample_review_info = coletar_amostra(all_product_info)
    generate_feedback(sample_review_info)