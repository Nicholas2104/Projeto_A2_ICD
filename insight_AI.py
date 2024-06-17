# Coleta todas as avaliacoes de 6 produtos amostrais, 3 bem avaliados e 3 nao tao bem avalidos, no final devolve uma string como amostra
def coletar_amostra(all_product_info): # toma como parametro as informacoes dos produtos no site
    SAMPLE_LIMIT = 6
    well_rated_samples_taken = 0 # contagem de produtos bem avaliados tomados na amostra
    poorly_rated_samples_taken = 0 # contagem de produtos mal avaliados tomados na amostra
    review_sample = ""

    half_sample_limit = SAMPLE_LIMIT//2 # cada classificacao de amostra de ter numero de produtos amostrados iguais
    for each_page in all_product_info: # iteramos sobre cada produto de cada pagina do site
        for each_product in each_page:
            review_content = each_product['review content'] 
            rating = each_product['rating']
            if review_content != "none": # Se nao houver avaliacoes pulamos o produto
                # caso contrario armazenamos todas as avalaicoes do produto
                # e dependo da classificacao itermaos a contagem respectiva
                if rating > 4 and well_rated_samples_taken < half_sample_limit: 
                    for each_review in review_content:
                        review_sample += f"{each_review}\n"
                    well_rated_samples_taken +=1
                elif rating <=4 and poorly_rated_samples_taken < half_sample_limit:
                    for each_review in review_content:
                        review_sample += f"{each_review}\n"
                    poorly_rated_samples_taken +=1
    return review_sample # finalmente devolvemos o string amostral

"""Utiliza Chat-GPT para devolver uma sintese de possiveis problemas e melhorias para"""
from openai import OpenAI

# constructing client object
#BUENO, insira a chave aqui em baixo
OPEN_AI_KEY = ""
client = OpenAI(api_key=OPEN_AI_KEY)

prompt = []
#Produz um insight sobre os produtos
def generate_feedback(review_sample, max_reponse_tokens=1000, model="gpt-3.5-turbo-0125"):
    user_query = f'''You are a whiskey connoisseur tasked with providing comprehensive feedback of a series of product reviews for different brands of rye whiskeys. Your goal is to summarize the main characteristics, strengths, and weaknesses of the
products in general, offer an overall assessment of the quality of the products reviewed, provide suggestions for improvement based on customer reviews, and identify
general areas for improvement across the product category. Don't make a feedback for every review, instead give a general feedback. Separete your asnwer in two categories: pros and cons. Provided information: {review_sample}'''
    # save user prompts so model remembers out ocnversation while session is running (*)
    prompt.append({"role":"user","content":user_query})
    # query the model by creating assistant reponse
    assistant_response = client.chat.completions.create(
        model=model,
        messages=prompt,
        max_tokens=max_reponse_tokens,
        temperature=0)
    assistant_response_content = assistant_response.choices[0].message.content
    return assistant_response_content