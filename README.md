# scrapy
Scrapy spiders to scrap data of newly launched and used cars from pakwheels.com and scrap user data by logging into github.com

## Setup
Clone the repo in a virtual environment, create virtual env as follows if don't already have it:  
`python3 -m venv environment-name`  
Switch terminal to the respective environment:  
`source environment-name/bin/activate`  
Install all the dependencies:  
`pip install -r requirements.txt`  
Add `.env` file in spiders directory and following fields in it:  
LOGIN = your login  
PASSWORD = your password  

## Usage
Use following command to run the:  
Pakwheels spider:    
`scrapy crawl pakwheels`  
Github spider:  
`scrapy crawl github`  
These commands will not print anytihng on terminal. You'll have to export data as described below.

### Export Data
Use the following commands to export data in:  
CSV file:  
`scrapy crawl pakwheels -O filename.csv`  
JSON file:  
`scrapy crawl pakwheels -O filename.json`  
Similarly:  
`scrapy crawl github -O filename.csv`  
and  
`scrapy crawl github -O filename.json`  
