import dotenv, os, random, csv
from pydantic import BaseModel
from typing import List
from openai import OpenAI
import openai


dotenv.load_dotenv(".env")
openai.api_key = os.getenv("OPEN_API_KEY")


class House(BaseModel):
    price: float
    area: float
    bedrooms: int
    bathrooms: int
    stories: int
    mainroad: str
    guestroom: str
    basement: str
    hotwaterheating: str
    airconditioning: str
    parking: int
    prefarea: str
    furnishingstatus: str
        

def load_houses() -> List[House]:
    houses = []
    with open("Housing.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            houses.append(House(**row))
    return houses
    

def generate_post(house: House) -> str:
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": f"""
                You an expert in house selling marketing. Your job is to make Instagram post content for the house provided below.
                Your content should attact clients using house information and convince them to buy a house.
                House information is provided below in JSON format:
                {house.model_dump_json(indent=2)}
            """
            }],
        temperature=0.2
    )
    return response.choices[0].message.content
    

if __name__ == "__main__":
    outfile = "EXAMPLE.md"
    
    houses = load_houses()
    
    with open(outfile, "w+") as f:
        for i in range(20):    
            house = random.choice(houses)
            post = generate_post(house)
            sample = f"{house.model_dump_json(indent=2)}\n\nContent:\n{post}\n------------------------\n\n"""
            f.write(sample)