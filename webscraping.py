import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

# Queremos coletar adequadamente todos os dados de todos os produtos de certa subcategoria
# Isso pode ser feito iternado sobre cada pagina do site, ate nao haver mais conteúdo
# a cada iteracao acessamso a pagina individual de cada produto e lemos suas caracteristicas
# Caracteristicas: Nome, preço, avaliação, numero de avaliacoes, conteúdo escrito da avaliacoes
# depois de coletar todas a caracteristicas podemos armazenar estas informacoes num dicionario onde a chave e o nome do produto

def fetch_individual_product_info(product_url):
    product_page = requests.get(product_url)
    product_page_soup = BeautifulSoup(product_page.text, "lxml")
    name = product_page_soup.find("h1", class_="title").text

    # preço é exibido como "$x.xxx,cc" onde c sao centavos - para adequadamente transformar o preço num float removemos o préfixo e a vírgula
    price = float((product_page_soup.find("span", class_="price theme-money").text).removeprefix("$").replace(",",""))

    reviews = product_page_soup.find_all("div",class_="stamped-review")
    if len(reviews) == 0: # Se não existir avaliação, associamos valores default para as características do produto
        rating = "none"
        num_reviews = "none"
        review_content = "none"
    else:
        review_content = []
        rating = float(product_page_soup.find("span",class_="stamped-summary-text-1").text)

        # número de avaliações eh aramazenada como o texto padrão "Based on X reviews" - assim para poder adequadamente 
        # transformar essa variável num inteiro selecionamos apenas o X dessa string
        num_reviews = int((product_page_soup.find("span",class_="stamped-summary-caption stamped-summary-caption-2").find("span").text).split(" ")[2])

        # para executar uma análise qualitativa dos dados precisamos isolar o conteúdo escrito de cada avaliação
        for each_review in reviews:
            header = (each_review.find("div", class_="stamped-review-body").find(class_="stamped-review-header-title").text).strip() # achamos o titulo da avaliação - Muito importante porque muitas vezes resume proposito da avaliação
            body = (each_review.find("div", class_="stamped-review-body").find(class_="stamped-review-content-body").text).strip() # achamaos tambem o conteúdo escrito da avaliação
            content = f"{header}: {body}"
            review_content.append(content) # aramzenamos o todas as avaliacoes em uma lista
    return {'name':name,'price':price,'rating':rating,'# reviews': num_reviews,'review content':review_content}

def collect_all_product_info(default_url): # temos como parametro a url basica do site
    page_num = 1
    all_product_info = []
    while True:
        page_url = default_url+str(page_num) # esepecificamos qual pagina queremos acessar
        main_page = requests.get(page_url)
        main_page_soup = BeautifulSoup(main_page.text, "lxml")
        if main_page_soup.find_all("div", class_="main-content") == []: # Se a a pagina n tiver mais conteúdo saimos do loop, pois revistamos todo o site
            break
        else:
            products_on_page = main_page_soup.find_all("a",class_="product-link") # todo produto possui um segmento individual sobre a class product-link
            product_urls = []
            for each_product in products_on_page:
                product_url = "https://sipwhiskey.com"+each_product['href'] # adcionamos a url basica do site o complemento do site do produto especifico
                product_urls.append(product_url)  
            with Pool() as pool:
                all_product_info.append(pool.map(fetch_individual_product_info,product_urls)) # para agilizar a coleta da pagina processamos em paralelo a coleta de cada produto
        page_num+=1 # seguimos para a proxima pagina
    return all_product_info
