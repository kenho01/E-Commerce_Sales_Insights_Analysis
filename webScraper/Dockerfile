FROM python:3.12-bookworm

COPY requirements.txt /scraper/
COPY *.py /scraper/
COPY scraper.sh /scraper/
ADD results /scraper/results
ADD output /scraper/output/
RUN chmod +x /scraper/scraper.sh

WORKDIR /scraper

RUN pip install --upgrade pip \
    &&  pip install --trusted-host pypi.python.org --requirement requirements.txt

CMD ["sh", "scraper.sh"]