# scrapy
Scrapy spider to scrap data of newly launched and used cars from pakwheels.com

## Setup
Clone the repo in a virtual environment, create virtual env as follows if don't already have it:  
`python3 -m venv environment-name`  
Switch terminal to the respective environment:  
`source environment-name/bin/activate`  
Install all the dependencies:  
`pip install -r requirements.txt`  

## Usage
Use following command to run the spider:  
`scrapy crawl pakwheels`  

### Export Data
Use the following commands to export data in:  
CSV file:  
`scrapy crawl pakwheels -O filename.csv`  
JSON file:  
`scrapy crawl pakwheels -O filename.json`  
