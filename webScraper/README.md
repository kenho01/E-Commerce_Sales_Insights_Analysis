
cd webScraper

docker build -t scraper .

docker run -v $(pwd)/results:/results scraper:latest
