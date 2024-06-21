from webscraping import collect_all_product_info
from insight_AI import coletar_amostra, generate_feedback
from insight_quantitativo import criar_tabela
DEFAULT_TEQUILA_PAGE_URL = "https://sipwhiskey.com/collections/rye-whiskey?page="

if __name__ == "__main__":
    all_product_info = collect_all_product_info(DEFAULT_TEQUILA_PAGE_URL)
    # mais do loop principal aqui ... \/\/
    review_sample = coletar_amostra(all_product_info)
    ai_feedback = generate_feedback(review_sample)
    tabela = criar_tabela(all_product_info,ai_feedback)
    print(tabela.head)