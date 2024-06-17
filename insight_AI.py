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