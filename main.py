from webscraping import collect_all_product_info

DEFAULT_TEQUILA_PAGE_URL = "https://sipwhiskey.com/collections/rye-whiskey?page="

if __name__ == "__main__":
    all_product_info = collect_all_product_info(DEFAULT_TEQUILA_PAGE_URL)
    print("pass")
