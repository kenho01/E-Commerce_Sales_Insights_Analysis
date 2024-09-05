import glob
import json
from datetime import datetime
import os

# genders = ['men', 'women']
# categories = ["clothing", "shoes", "sports"]
# men_brands_clothes = ["cos", "superdry", "calvin-klein", "hm", "oxgn"]
# men_brands_shoes  = ['addias', 'aldo', 'birkenstock', 'converse', 'dr-martens']
# brands_sports = ['adidas', 'under-armour', 'nike', 'puma', 'new-balance']
# women_brands_clothes = ['cos', 'calvin-klein', 'hm', 'oxgn', 'seasalt-cornwall']
# women_brands_shoes = ['aldo', 'betsy', 'birkenstock', 'converse', 'call-it-spring']
# occasions = ["Casual", "Activewear", "Workwear"]

# items = []
# for x in genders:
#     for i in categories:
#         for j in men_brands_clothes:
#             for k in occasions:
#                 t = (x, i, j , k)
#                 items.append(t)

# print(items)
# print(len(items))

def combined_json_files():
    current_date = datetime.now().strftime("%d_%m_%Y")
    folder_path = "results"
    json_files = glob.glob(f"{folder_path}/*.json")
    objects = []
    for json_file in json_files:
        with open(json_file, "r") as f:
            objects.append(json.load(f))
    destination = f"output/{current_date}.json"
    with open(destination, "w") as f:
        json.dump(objects, f, indent=4)

def remove_subresults():
    directory = 'results'
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path): 
            os.remove(file_path)

combined_json_files()
remove_subresults()