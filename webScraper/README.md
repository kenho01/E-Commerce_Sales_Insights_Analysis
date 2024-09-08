
cd webScraper

docker build -t scraper .

docker run -v $(pwd)/output:/output scraper:latest
