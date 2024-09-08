import datetime
import time
import requests
import re
import json
import glob
import os
from google.cloud import storage

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


class Scraper():
    def __init__(
        self,
        user_agent=None,
        root_url=None,
        api_url=None,
    ):
        self.user_agent = \
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36' if user_agent is None \
            else user_agent

        self.root_url = 'https://www.zalora.com.sg' if root_url is None else root_url
        self.root_url = self.root_url.strip("/")

        self.api_url = 'https://www.zalora.com.sg/_c/v1/desktop/list_catalog_full' if api_url is None else api_url
        self.api_url = self.api_url.strip("/")

        self.headers = {
            'User-Agent': self.user_agent
        }

    def _extract_metadata(self, gender, product, brand, occassion):
        url = f"{self.root_url}/{gender}/{product}/{brand}/?occasion={occassion}"
        text = requests.get(url, headers=self.headers).text

        brand_idx = text.index("brandIds")
        brand_code = int(
            re.match("^([0-9]+)", text[brand_idx+15:]).groups()[0])

        category_idx = text.index("categoryId=")
        category_code = int(
            re.match("^([0-9]+)", text[category_idx+11:]).groups()[0])

        return brand_code, category_code

    def _extract_from_api(self, gender, brand_code, category_code, occassion, start, end):
        parameters = [
            f"gender={gender}",
            f"segment={gender}",
            f"category_id={category_code}",
            "sort=popularity",
            "dir=desc",
            f"offset={start}",
            f"limit={end}",
            f"occasion={occassion}",
            f"brand={brand_code}",
            "special_price=false",
            "all_products=false",
            "new_products=false",
            "top_sellers=false",
            "catalogtype=Main",
            "lang=en",
            "is_brunei=false",
            "sort_formula=sum(product(0.01%2Cscore_simple_availability)%2Cproduct(0.0%2Cscore_novelty)%2Cproduct(0.99%2Cscore_product_boost)%2Cproduct(0.0%2Cscore_random)%2Cproduct(1.0%2Cscore_personalization))",
            "search_suggest=false",
            "enable_visual_sort=true",
            "enable_filter_ads=true",
            "compact_catalog_desktop=false",
            "name_search=false",
            "solr7_support=true",
            "pick_for_you=false",
            "learn_to_sort_catalog=false",
            "is_multiple_source=true",
        ]

        try:
            parameters_joined = "&".join(parameters)
            response = requests.get(
                self.api_url + "?" + parameters_joined, headers=self.headers)
            results = json.loads(response.text)["response"]["docs"]
            results = [{
                "brand": x["meta"]["brand"],
                "sku": x["meta"]["sku"],
                "name": x["meta"]["name"],
                "actual_price": x["meta"]["price"],
                "discounted_price": x["meta"]["special_price"]
            } for x in results]
            return results
        except Exception as e:
            print(e)
            return []
    
    def scrape(self, gender, product, brand, occassion, batch_size=100, identifier="sku"):
        print("\n\t[SCRAPER TOOL]\n")
        ts_start = time.time()
        now = str(datetime.datetime.now()).split(".")[
            0].replace(" ", "-").replace(":", "")
        print(f"\tScraping started at: {now}\n")

        # print("\tScraping parameters:")
        # print(f"\t\tGender: {gender}")
        # print(f"\t\tProduct: {product}")
        # print(f"\t\tBrand: {brand}")
        # print(f"\t\tOccassion: {occassion}\n")

        brand_code, category_code = self._extract_metadata(
            gender, product, brand, occassion)
        results = []
        batch_num = 0
        skus = set()
        while True:
            start = batch_num * batch_size
            end = (batch_num + 1) * batch_size
            batch = self._extract_from_api(
                gender, brand_code, category_code, occassion, start, end)
            batch = [x for x in batch if x[identifier] not in skus]
            results += batch
            skus |= {x[identifier] for x in batch}
            batch_num += 1
            if len(batch) == 0:
                break
        # print("\tFound", len(results), "products!\n")
        filename = f"zalora-{gender}-{product}-{brand}-{occassion}-{now}.json"
        with open(filename, "w") as f:
            json.dump(results, f, indent=4)
        # print(f"\tSaved to file: {filename}\n")
        print(f"\tTook {round(time.time() - ts_start, 2)} seconds\n")

def data_extraction():
    scraper = Scraper()

    genders = ['men', 'women']
    categories = ["clothing", "shoes", "sports"]
    men_brands_clothes = ["cos", "superdry", "calvin-klein", "hm", "oxgn"]
    men_brands_shoes  = ['vans', 'aldo', 'birkenstock', 'converse', 'dr-martens']
    brands_sports = ['adidas', 'under-armour', 'nike', 'puma', 'new-balance']
    women_brands_clothes = ['cos', 'calvin-klein', 'hm', 'oxgn', 'seasalt-cornwall']
    women_brands_shoes = ['aldo', 'betsy', 'birkenstock', 'converse', 'call-it-spring']
    occasions = ["Casual", "Activewear", "Workwear"]

    items = []

    for j in men_brands_clothes:
        for k in occasions:
            t = ("men", "clothing", j , k)
            items.append(t)
            
    for j in men_brands_shoes:
        for k in occasions:
            t = ("men", "shoes", j , k)
            items.append(t)

    for j in women_brands_clothes:
        for k in occasions:
            t = ("women", "clothing", j , k)
            items.append(t)
    for j in women_brands_shoes:
        for k in occasions:
            t = ("women", "shoes", j , k)
            items.append(t)

    for i in genders:
        for j in brands_sports:
            for k in occasions:
                t = (i, "sports", j, k)
                items.append(t)
            
    # Begin the scrape 
    for i in items:
        print(i[1], i[2])
        scraper.scrape(
            gender=i[0],
            product=i[1],
            brand=i[2],
            occassion=i[3]
        )

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {bucket_name}/{destination_blob_name}")
    
def combined_json_files(bucket_name):
    current_date = datetime.datetime.now().strftime("%d_%m_%Y")
    json_files = glob.glob("zalora-*.json")
    combined_data = []
    
    for json_file in json_files:
        with open(json_file, "r") as f:
            data = json.load(f)
            combined_data.extend(data) 

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    destination = f"{output_dir}/zalora_combined_{current_date}.json"

    with open(destination, "w") as f:
        json.dump(combined_data, f, indent=4)

    print(f"Combined JSON saved to: {destination}")

    for json_file in json_files:
        os.remove(json_file)
        print(f"Deleted file: {json_file}")
    
    destination_blob_name = f"zalora_combined_{current_date}.json"
    upload_to_gcs(bucket_name, destination, destination_blob_name)

    os.remove(destination)
    print(f"Deleted file: {destination}")

@custom
def main(*args, **kwargs):
    # Specify your custom logic here

    data_extraction()
    bucket_name = "ecommerce-insights-435001-raw-json-bucket"
    combined_json_files(bucket_name)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
