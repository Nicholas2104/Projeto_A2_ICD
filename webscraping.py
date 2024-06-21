"""Responsavel para ripar caracteristicas de cada produto e suas avaliacoes """
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

# Queremos coletar adequadamente todos os dados de todos os produtos de certa subcategoria
# Isso pode ser feito iterando sobre cada página do site, até não haver mais conteúdo
# a cada iteração acessamos a página individual de cada produto e lemos suas características
# Características: Nome, preço, avaliação, número de avaliações, conteúdo escrito da avaliações
# depois de coletar todas as características podemos armazenar estas informações num dicionário onde a chave é o nome do produto

def fetch_individual_product_info(product_url): # Devolve dicionário da características de cada produto
    product_page = requests.get(product_url)
    product_page_soup = BeautifulSoup(product_page.text, "lxml")
    name = product_page_soup.find("h1", class_="title").text

    # preço é exibido como "$x,xxx.cc" onde c sao centavos - para adequadamente transformar o preço num float removemos o préfixo e a vírgula
    price = float((product_page_soup.find("span", class_="price theme-money").text).removeprefix("$").replace(",",""))

    reviews = product_page_soup.find_all("div",class_="stamped-review") # contem conteudo da avaliacoes
    review_summary = product_page_soup.find_all("div",class_="summary-rating") # contem sumario estatistico da avaliacoes
    if len(reviews) == 0: # Se não existir avaliação, associamos valores default para as características do produto
        rating = "none"
        total_reviews = "none"
        positive_review_count = "none"
        negative_review_count = "none"
        review_content = "none"
    else:
        review_content = []
        rating = float(product_page_soup.find("span",class_="stamped-summary-text-1").text)
        # para coletar o numero de avaliacoes positivas, negativas e total, olhamos para o sumario quantitativo das avaliacoes
        total_reviews = 0
        positive_review_count = 0
        negative_review_count = 0
        for index , each_summary in enumerate(review_summary):
            # consideramos toda avaliacao maior o igual a 4 positivo
            if index <= 1: # pagina ordena contagem em ordem decresencte 5 estrelas , 4 estrelas ...
                positive_review_count += int(each_summary['data-count'])
            # menor que quatro sao negativos
            else:
                negative_review_count += int(each_summary['data-count'])
        total_reviews += (positive_review_count + negative_review_count)

        # para executar uma análise qualitativa dos dados precisamos isolar o conteúdo escrito de cada avaliação
        for each_review in reviews:
            header = (each_review.find("div", class_="stamped-review-body").find(class_="stamped-review-header-title").text).strip() # achamos o titulo da avaliação - Muito importante porque muitas vezes resume o propósito da avaliação
            body = (each_review.find("div", class_="stamped-review-body").find(class_="stamped-review-content-body").text).strip() # achamos também o conteúdo escrito da avaliação
            content = f"{header}: {body}"
            review_content.append(content) # armazenamos todas as avaliações em uma lista
    return {'name':name,
            'price':price,
            'rating':rating,
            'total reviews': total_reviews,
            'total positive reviews':positive_review_count,
            'total negative reviews':negative_review_count,
            'review content':review_content}

def collect_all_product_info(default_url): # Devolve Lista de Listas, cada uma contém todos os produto de cada página
    page_num = 1
    all_product_info = []
    while True:
        page_url = default_url+str(page_num) # especificamos qual página queremos acessar
        main_page = requests.get(page_url)
        main_page_soup = BeautifulSoup(main_page.text, "lxml")
        if main_page_soup.find_all("div", class_="main-content") == []: # Se a página não tiver mais conteúdo, saímos do loop, pois passamos por todas as páginas do site
            break
        else:
            products_on_page = main_page_soup.find_all("a",class_="product-link") # todo produto possui um segmento individual sobre a class product-link
            product_urls = []
            for each_product in products_on_page:
                product_url = "https://sipwhiskey.com"+each_product['href'] # adicionamos à url básica do site o endereço de um produto específico
                product_urls.append(product_url)  
            with Pool() as pool:
                all_product_info.append(pool.map(fetch_individual_product_info,product_urls)) # para agilizar a coleta da página processamos em paralelo a coleta de cada produto
        page_num+=80 # seguimos para a próxima página
    return all_product_info
