"""Módulo para criar insights quantitativos e criar uma tabela com os dados coletados"""
import pandas as pd

#Vamos criar a tabela com as informações coletadas no módulo de webscrapping, adicionar mais duas características de análise e a OpenAI
def create_table(all_product_info, ai_feedback):
    headers= ['name','price','rating','total reviews', 'total positive reviews', 'total negative reviews','Cost Efficiency','Consumer Satisfaction ratio',"AI Feedback"]
    tabela = pd.DataFrame(columns=headers)
    for each_page in all_product_info: #O módulo de webscrapping nos retorna uma lista de listas de dicionários, usando dois for loops, encontramos as informações para os produtos
        for each_product in each_page:
            
            WS_values = list(each_product.values())[0:-1]
            #utilizamos o slicing para tirar a coluna de reviews de usuários, já que eles já foram usados pelo módulo da OPENAI
            price, rating,total_reviews,positive_reviews = WS_values[1:5] 
            #criamos as colunas "cost efficiency" e "consumer satisfaction", que estão explicadas na definição das funções
            cost_efficiency = cost_efficency_calc(rating,price)
            consumer_satisfaction = consumer_satisfaction_calc(positive_reviews,total_reviews)

            tabela.loc[len(tabela)] = WS_values+[cost_efficiency,consumer_satisfaction,""]
    #adicionando o comentário da openai na primeira linha, para podermos exportar essa string para o excel
    tabela.loc[0,'AI Feedback'] = ai_feedback
    return tabela

#Como primeira característica extra, temos uma nova coluna "custo benefício" ou "cost efficiency"
#Decidimos criar essa coluna pois é um indicador bastante influente na compra de um produto
def cost_efficency_calc(rating,price):
    #Cuidando dos casos em que não existem reviews
    if rating == "none" or price == "Out of Stock":
        return "none"
    else:
        return (price//rating)

#A probabilidade de satisfação é um indicador que "suaviza" o peso das avaliações de produtos com poucos reviews
#Produtos que tem muitas avalliações serão pouco afetados por essa função, enquanto produtos com poucas terão seus pesos suavizados
def consumer_satisfaction_calc(positive_reviews,total_reviews):
    #cuidando dos casos em que não existem reviews, precisamos apenas checar pelos "positive reviews", pois se o resultado for "none"
    #não existem reviews no produto (se tivessem apenas reviews negativos, o resultado seria "0")
    if positive_reviews == "none":
        return "none"
    else:
        print(int((positive_reviews+1)/(total_reviews+2)*100))
        return int((positive_reviews+1)/(total_reviews+2)*100) #retorna a chance em porcentagem do consumidor estar satisfeito com o produto
        