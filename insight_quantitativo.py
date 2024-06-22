"""Módulo para criar insights quantitativos e criar uma tabela com os dados coletados"""
import pandas as pd
#Precisamos criar uma tabela que contenha os dados coletados no webscrapping e o review gerado pela inteligência artificial
#Além disso, vamos também características novas a partir dos dados que temos

#Como primeira característica extra, temos uma nova coluna "custo benefício"
#Decidimos criar essa coluna pois é um indicador bastante influente na compra de um produto
def cost_efficency_calc(rating,price):
    if rating == "none":
        return "none"
    else:
        return (price//rating)

#Utilizando as duas últimas colunas criadas, podemos criar nossa quarta e última característica (quantiativa) extra
#A probabilidade de satisfação é um indicador que "suaviza" o peso das avaliações de produtos com poucos reviews
#Produtos que tem muitas avalliações serão pouco afetados por essa função, enquanto produtos com poucas terão seus pesos suavizados
def consumer_satisfaction_calc(positive_reviews,total_reviews):
    if positive_reviews == "none":
        return "none"
    else:
        return (positive_reviews+1)//(total_reviews+2)*100

#Finalizamos criando uma tabela com os dados dos produtos
def criar_tabela(all_product_info, ai_feedback):
    headers= ['name','price','rating','total reviews', 'total positive reviews', 'total negative reviews','Cost Efficiency','Consumer Satisfaction ratio',"AI Feedback"]
    tabela = pd.DataFrame(columns=headers)
    for each_page in all_product_info:
        for each_product in each_page:

            WS_values = list(each_product.values())[0:-1]
            price, rating,total_reviews,positive_reviews = WS_values[1:5]

            cost_benfit = cost_efficency_calc(rating,price)
            consumer_satisfaction = consumer_satisfaction_calc(positive_reviews,total_reviews)

            tabela.loc[len(tabela)] = WS_values+[cost_benfit,consumer_satisfaction,""]
    tabela.loc[0,'AI Feedback'] = ai_feedback
    return tabela