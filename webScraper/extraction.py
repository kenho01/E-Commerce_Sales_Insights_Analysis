from scraper import Scraper
import json
import glob
import os

scraper = Scraper()

def combine_json_files(input_dir, output_file):
        combined_data = []

        # Find all JSON files in the input directory
        for file_name in glob.glob(os.path.join(input_dir, '*.json')):
            with open(file_name, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):  
                    combined_data.extend(data)
                else:
                    combined_data.append(data)
    
        # Write combined data to the output file
        with open(output_file, 'w') as f:
            json.dump(combined_data, f, indent=4)

# Possible parameters
# gender = ('men', 'women')
# product = ('clothing', 'shoes', 'accessories', 'bags', 'sports', 'modest-wear', 'men-s-care', 'beauty') <- #beauty for women's collections
# brand = 
# occasion = ('Activewear', 'Casual', 'Special+Occasion', 'Workwear')

# For this project, we'll narrow down the things to scrape to be men's sportswear and gear

# Initialize a list to store things to scrape
# List of brands = nike, adidas, new-balance, puma, underarmour, 2xu, 
# Product = clothing, shoes, bags
items_attributes = [
    ("men", "clothing", "nike", "Activewear"), 
    ("men", "clothing", "adidas", "Activewear"),
    ("men", "clothing", "nike", "Casual"),
    ("men", "clothing", "puma", "Activewear"),
    ("men", "clothing", "new-balance", "Casual"),
    ("men", "clothing", "new-balance", "Activewear"),
    ("men", "shoes", "new-balance", "Casual"),
    ("men", "shoes", "adidas", "Activewear"),
]

# Begin the scrape 
for i in items_attributes:
    scraper.scrape(
        gender=i[0],
        product=i[1],
        brand=i[2],
        occassion=i[3]
    )

input_directory = './results'
output_directory = './final_results'
combine_json_files(input_directory,output_directory)

