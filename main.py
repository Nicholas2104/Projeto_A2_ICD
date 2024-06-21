from webscraping import collect_all_product_info
from insight_AI import collect_sample, generate_feedback
from insight_quantitativo import criar_tabela
DEFAULT_WHISKEY_PAGE_URL = "https://sipwhiskey.com/collections/rye-whiskey?page="

if __name__ == "__main__":
    all_product_info = collect_all_product_info(DEFAULT_WHISKEY_PAGE_URL)
    # mais do loop principal aqui ... \/\/
    review_sample = collect_sample(all_product_info)
    ai_feedback = generate_feedback(review_sample)
    tabela = criar_tabela(all_product_info,ai_feedback)
    tabela.to_csv("Raw_Whiskey_Data.csv", index=False)