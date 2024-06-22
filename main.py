from webscraping import collect_all_product_info
from insight_AI import collect_sample, generate_feedback
from insight_quantitativo import criar_tabela
DEFAULT_WHISKEY_PAGE_URL = "https://sipwhiskey.com/collections/rye-whiskey?page="

if __name__ == "__main__":
    all_product_info = collect_all_product_info(DEFAULT_WHISKEY_PAGE_URL) #raspagem de dados
    review_sample = collect_sample(all_product_info) #amostra para o módulo da OpenAI
    ai_feedback = generate_feedback(review_sample) #gerando o feedback da API da OpenAI
    tabela = criar_tabela(all_product_info,ai_feedback) #criando a tabela com as características novas
    tabela.to_csv("Raw_Whiskey_Data.csv",index=False) #exportando nosso dataframe para um documento .csv