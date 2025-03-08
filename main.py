import discord
from discord.ext import commands
import random
import os
import requests
import nltk
from bs4 import BeautifulSoup
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
import io



nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('popular')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

user_data = {}

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

questions = [
    "¿Cuánta electricidad usas al mes (en kWh)?",
    "¿Cuántos kilómetros conduces al mes?",
    "¿Cuántos vuelos tomas al año?",
    "¿Cuántos residuos generas al mes (en kg)?",
    "¿Cuántos productos locales compras al mes?"
]
def calculate_carbon_footprint(electricity, kilometers, flights, waste, local_products):
    # Example conversion factors (these are just placeholders, you should use real data)
    electricity_factor = 0.233  # kg CO2 per kWh
    kilometers_factor = 0.21  # kg CO2 per km
    flights_factor = 250  # kg CO2 per flight
    waste_factor = 0.5  # kg CO2 per kg of waste
    local_products_factor = -0.1  # kg CO2 per local product (negative for reduction)

    total_footprint = (
        electricity * electricity_factor +
        kilometers * kilometers_factor +
        flights * flights_factor +
        waste * waste_factor +
        local_products * local_products_factor
    )
    return total_footprint

# Define a function to provide recommendations based on the carbon footprint
def get_recommendations(total_footprint):
    high_threshold = 1000  # Example threshold for high carbon footprint
    low_threshold = 500  # Example threshold for low carbon footprint

    if total_footprint > high_threshold:
        return [
            "Tu huella de carbono es muy alta. Aquí hay algunas recomendaciones para reducirla:",
            "Reduce tu consumo de energía apagando luces y aparatos electrónicos cuando no los uses.",
            "Usa transporte público, comparte coche, anda en bicicleta o camina en lugar de conducir solo.",
            "Reduce, reutiliza y recicla para minimizar los residuos.",
            "Adopta una dieta basada en plantas o reduce tu consumo de carne.",
            "Usa electrodomésticos y bombillas de bajo consumo energético.",
            "Apoya fuentes de energía renovable como la solar y la eólica.",
            "Planta árboles y apoya proyectos de reforestación.",
            "Conserva agua arreglando fugas y usando dispositivos ahorradores de agua.",
            "Compra productos locales y sostenibles.",
            "Reduce los viajes en avión y opta por reuniones virtuales cuando sea posible."
        ]
    elif total_footprint > low_threshold:
        return [
            "Tu huella de carbono es promedio. Aquí hay algunas recomendaciones para reducirla:",
            "Apaga las luces y los aparatos electrónicos cuando no los uses.",
            "Usa transporte público o comparte coche en lugar de conducir solo.",
            "Recicla y reutiliza para reducir los residuos.",
            "Considera reducir tu consumo de carne.",
            "Usa bombillas de bajo consumo energético.",
            "Apoya fuentes de energía renovable.",
            "Planta árboles en tu comunidad.",
            "Conserva agua arreglando fugas.",
            "Compra productos locales.",
            "Opta por reuniones virtuales en lugar de viajes en avión."
        ]
    else:
        return ["Tu huella de carbono es baja. ¡Sigue así!"]
    
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola, soy un bot {bot.user}!')

@bot.command()
async def helpme(ctx):
    await ctx.send("¡Hola! Soy un bot que te ayudará a reducir tu huella de carbono. Puedes usar los siguientes comandos para interactuar conmigo:\n"
                   "/noticia: Resumir una noticia de un artículo en línea.\n"
                   "/recomendacion: Recibir una recomendación aleatoria para reducir tu huella de carbono.\n"
                    "/reducir:  Calcular tu huella de carbono y recibir recomendaciones para reducirla.\n"
                    "/huella: Calcular tu huella de carbono y recibir recomendaciones para reducirla.\n")
    



@bot.command()
async def noticia(ctx, url: str = "a"):
    if url == "a":
        await ctx.send("Por favor, proporciona la URL de un artículo en línea.")
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        paragraphs = soup.find_all('p')

        # Define keywords to filter out unwanted paragraphs
        unwanted_keywords = ["cookies", "privacidad", "terminos", "politicas", "anuncios", "publicidad", "relacionadas", "preferencias"]

        # Filter out paragraphs containing unwanted keywords
        filtered_paragraphs = [
            para for para in paragraphs
            if not any(keyword in para.get_text().lower() for keyword in unwanted_keywords)
        ]

        text = ' '.join([para.get_text() for para in filtered_paragraphs])
        sentences = nltk.tokenize.sent_tokenize(text, language='spanish')

        words = word_tokenize(text, language='spanish')
        fdist = FreqDist(words)

        common_words = [word for word, freq in fdist.most_common(50)]

        summary_sentences = [sentence for sentence in sentences if any(word in sentence for word in common_words)]
        summary = ' '.join(summary_sentences[:5])

        print(20 * "-")
        print(sentences)
        print(20 * "-")
        await ctx.send(f"Resumen: {summary}")


@bot.command()
async def recomendacion(ctx):

    recomendations = [
        "Reduce tu consumo de energía apagando luces y aparatos electrónicos cuando no los uses.",
        "Usa transporte público, comparte coche, anda en bicicleta o camina en lugar de conducir solo.",
        "Reduce, reutiliza y recicla para minimizar los residuos.",
        "Adopta una dieta basada en plantas o reduce tu consumo de carne.",
        "Usa electrodomésticos y bombillas de bajo consumo energético.",
        "Apoya fuentes de energía renovable como la solar y la eólica.",
        "Planta árboles y apoya proyectos de reforestación.",
        "Conserva agua arreglando fugas y usando dispositivos ahorradores de agua.",
        "Compra productos locales y sostenibles.",
        "Reduce los viajes en avión y opta por reuniones virtuales cuando sea posible."]
    image = "./img/recycle.png"
    random_recomendation = random.choice(recomendations)
    await ctx.send(f"Recomendación: {random_recomendation}", file=discord.File(image))

@bot.command()
async def reducir(ctx, electricity: int = None, kilometers: int = None, flights: int = None, waste: int = None, local_products: int = None):
    if None in (electricity, kilometers, flights, waste, local_products):
        await ctx.send("No enviaste la información correcta, Este es el orden de la información que tienes que enviar: electricidad (kWh), kilómetros (km), vuelos (por año), cantidad de desechos (kg), productos locales (por mes).")
    else:
        user_data[ctx.author.id] = {
            'electricity': electricity,
            'kilometers': kilometers,
            'flights': flights,
            'waste': waste,
            'local_products': local_products
        }
        total_footprint = calculate_carbon_footprint(electricity, kilometers, flights, waste, local_products)
        await ctx.send(f"Gracias por facilitarnos los datos. Aquí están tus resultados:")
        for key, value in user_data[ctx.author.id].items():
            await ctx.send(f"{key.capitalize()}: {value}")
        await ctx.send(f"Tu huella de carbono total es de: {total_footprint:.2f} kg de CO2 por mes.")
        recommendations = get_recommendations(total_footprint)
        for recommendation in recommendations:
            await ctx.send(recommendation)
        del user_data[ctx.author.id]



@bot.command()
async def huella(ctx, electricity: int = None, kilometers: int = None, flights: int = None, waste: int = None, local_products: int = None):
    if None in (electricity, kilometers, flights, waste, local_products):
        await ctx.send("No enviaste la información correcta, Este es el orden de la información que tienes que enviar: electricidad (kWh), kilómetros (km), vuelos (por año), cantidad de desechos (kg), productos locales (por mes).")
    else:
        user_data[ctx.author.id] = {
            'electricity': electricity,
            'kilometers': kilometers,
            'flights': flights,
            'waste': waste,
            'local_products': local_products
        }
        total_footprint = calculate_carbon_footprint(electricity, kilometers, flights, waste, local_products)
        await ctx.send(f"Gracias por facilitarnos los datos. Aquí están tus resultados:")
        for key, value in user_data[ctx.author.id].items():
            await ctx.send(f"{key.capitalize()}: {value}")
        await ctx.send(f"Tu huella de carbono total es de: {total_footprint:.2f} kg de CO2 por mes.")
        
        high_threshold = 1000  # Example threshold for high carbon footprint
        low_threshold = 500  # Example threshold for low carbon footprint

        if total_footprint > high_threshold:
            await ctx.send("Tu huella de carbono es muy alta.")
        elif total_footprint > low_threshold:
            await ctx.send("Tu huella de carbono es promedio.")
        else:
            await ctx.send("Tu huella de carbono es baja.")
        
        del user_data[ctx.author.id]
        
@bot.command()
async def photo(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)
   

    
    
    
    
    

    
    


bot.run("Token goes here")