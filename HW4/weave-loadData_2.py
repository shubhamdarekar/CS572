from weaviate import *
import json

client = Client(
    url = "http://localhost:8080/",  
)




# specify schema for the data we'll be using 
# x = client.schema.get()

# client.schema.delete_class("CarSearch") 

class_obj = {
    "class": "CarSearch",
    "vectorizer": "text2vec-transformers"
}
client.schema.create_class(class_obj)


# download data
import requests
url = 'http://localhost:8000/data2.json'
resp = requests.get(url)
data = json.loads(resp.text)

# send data to weaviate, to vectorize
with client.batch as batch:
    batch.batch_size=100
    # Batch import all data
    for i, d in enumerate(data):
        print(f"\nimporting datum: {i}")

        properties = {
            "Brand": d["Brand"],
            "Model": d["Model"],
            "Year": d["Year"],
        }
        print(f"properties: {properties}")

        client.batch.add_data_object(properties, "SimSearch")
        
        

