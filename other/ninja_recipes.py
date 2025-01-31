import requests
import json
import pandas as pd 


## read in ingredient df

# df = pd.read_csv('pcos_ingredients.csv')

# ingredients = df.Ingredient.values


ingredients = ["Brown Rice"]

for item in ingredients:
	print(f"Getting {item} recipes")

	url = "https://recipe-by-api-ninjas.p.rapidapi.com/v1/recipe"

	querystring = {"query":f"{item}"}

	headers = {
		"X-RapidAPI-Key": "b31ac1fa64msh8188c92e51230ebp17bdedjsn4d7cd65715d8",
		"X-RapidAPI-Host": "recipe-by-api-ninjas.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)
	data = response.json()
	print(response.json())
	with open(f'./recipes/{item}_recipe.json', 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=4)