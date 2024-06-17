"""Utiliza Chat-GPT para devolver uma sintese de possiveis problemas e melhorias para"""
from openai import OpenAI

# constructing client object
#BUENO, insira a chave aqui em baixo
OPEN_AI_KEY = ""
client = OpenAI(api_key=OPEN_AI_KEY)

prompt = []
#Produz um insight sobre os produtos
def generate_feedback(review_sample, max_reponse_tokens=1000, model="gpt-3.5-turbo-0125"):
    user_query = f'''You are a whiskey connoisseur tasked with providing comprehensive feedback on a series of product reviews for different brands of whiskeys
 within the same category (e.g., Single Malt, Bourbon, Rye, etc.). Your goal is to summarize the main characteristics, strengths, and weaknesses of the
   products, offer an overall assessment of the quality of the products reviewed, provide suggestions for improvement based on customer reviews, and identify
     general areas for improvement across the product category. Provided information: {review_sample}'''
    # save user prompts so model remembers out ocnversation while session is running (*)
    prompt.append({"role":"user","content":user_query})
    # query the model by creating assistant reponse
    assistant_response = client.chat.completions.create(
        model=model,
        messages=prompt,
        max_tokens=max_reponse_tokens,
        temperature=0)
    assistant_response_content = assistant_response.choices[0].message.content
    # save responses also to avoid repetition
    prompt.append({"role":"assistant","content":assistant_response_content})
    return assistant_response_content