"""Módulo para criar insights quantitativos e criar uma tabela com os dados coletados"""
import pandas as pd

#Precisamos criar uma tabela que contenha os dados coletados no webscrapping e o review gerado pela inteligência artificial
#Além disso, vamos também características novas a partir dos dados que temos

#Primeiro, precisamos criar uma tabela com os dados dos produtos
def cria_tabela():
    tabela = pd.DataFrame(all_product_info)
    return tabela

#Como primeira característica extra, temos uma nova coluna "custo benefício"
#Decidimos criar essa coluna pois é um indicador bastante influente na compra de um produto
def custo_beneficio():
    tabela["custo-benefício"] = tabela["rating"]/tabela["price"]
    return tabela

#Como segunda e terceira características, decidimos contar a quantidade de Reviews positivos e negativos
#Definimos uma nota maior ou igual a 5 como positiva, enquanto o restante é negativo
def reviews_pos_neg():
    tabela["reviews positivos"] = tabela.apply(lambda linha: (linha["rating"]>=5)*linha["# reviews"],axis=1)
    tabela["reviews negativos"] = tabela["# reviews"]-tabela["reviews positivos"]
    return tabela

#Utilizando as duas últimas colunas criadas, podemos criar nossa quarta e última característica (quantiativa) extra
#A probabilidade de satisfação é um indicador que "suaviza" o peso das avaliações de produtos com poucos reviews
#Produtos que tem muitas avalliações serão pouco afetados por essa função, enquanto produtos com poucas terão seus pesos suavizados
def prob_satisfacao():
    tabela["chance de gostar"] = (tabela["reviews positivos"]+1)/(tabela["reviews negativos"]+1)
    return tabela

#Por fim, adicionamos uma coluna com uma análise qualitativa do produto, feita pela API da OpenAI
def adiciona_IA():
    tabela["Review feito por IA"] = assistant_response_content
    return tabela