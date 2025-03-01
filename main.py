import discord
from discord.ext import commands
import random
import os
import requests
import nltk
from bs4 import BeautifulSoup
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize




nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('popular')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

user_data = {}

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
async def news(ctx, url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    paragraphs = soup.find_all('p')

    text = ' '.join([para.get_text() for para in paragraphs])
    sentences = nltk.tokenize.sent_tokenize(text, language='spanish')

    words = word_tokenize(text, language = 'spanish')
    fdist = FreqDist(words)

    common_words = [word for word, freq in fdist.most_common(50)]

    summary_sentences = [sentence for sentence in sentences if any(word in sentence for word in common_words)]
    summary = ' '.join(summary_sentences[:5])

    print(20 * "-")
    print(sentences)
    print(20 * "-")
    await ctx.send(f"Summary: {summary}")


@bot.command()
async def recomendation(ctx):

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
async def footprint(ctx, electricity: int = None, kilometers: int = None, flights: int = None, waste: int = None, local_products: int = None):
    if None in (electricity, kilometers, flights, waste, local_products):
        await ctx.send("You didn't send the proper data, This is the order of the information you need to provide: electricity (kWh), kilometers (km), flights (per year), waste (kg), local products (per month).")
    else:
        user_data[ctx.author.id] = {
            'electricity': electricity,
            'kilometers': kilometers,
            'flights': flights,
            'waste': waste,
            'local_products': local_products
        }
        total_footprint = calculate_carbon_footprint(electricity, kilometers, flights, waste, local_products)
        await ctx.send(f"Thank you for providing all the information. Here is your data:")
        for key, value in user_data[ctx.author.id].items():
            await ctx.send(f"{key.capitalize()}: {value}")
        await ctx.send(f"Your total carbon footprint is: {total_footprint:.2f} kg CO2 per month.")
        recommendations = get_recommendations(total_footprint)
        for recommendation in recommendations:
            await ctx.send(recommendation)
        del user_data[ctx.author.id]


            
        
    
    
    
    

    
    


bot.run("Token goes here")