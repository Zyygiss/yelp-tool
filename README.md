# Yelp Fusion v3 API with Python

This Python script is used to grab information from Yelp Fusion API v3 and generate a CSV file with the results.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This code is written in Python 2.7 and you will need Python 2.7 installed along with PIP install

First, check which version of Python (if any) you are running.  Open cmd, terminal or Git Bash and run:

```
python --version
```
Install cURL and PIP
install cURL: https://stackoverflow.com/questions/9507353/how-do-i-install-set-up-and-use-curl-on-windows
install PIP: https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip

Make sure you are runing Pythgon 2.7 and then install dependencies:

```
dependencies

pip install requests
```

## Running the script

Enter into the Yelp file and execute the Python script.
yelp_upload.csv is a CSV file with keyword search term column and location column. 
yelp_results.csv is a CSV file with results from the search

Keyword search term is defined by Yelp as: Search term (e.g. "food", "restaurants"). If term isn’t included we search everything. The term keyword also accepts business names such as "Starbucks".
Location is defined by Yelp as: Specifies the combination of "address, neighborhood, city, state or zip, optional country" to be used when searching for businesses.

Please make sure this information is not blank for the script to work
```
python yelp.py
```

## Limitations
Yelp imposes a limit of 50 results per request and 1,000 results hard limit. Radius is also limited to 40,000 meters (25 miles) from the location requested

see details at:
https://www.yelp.com/developers/documentation/v3/business_search# yelp-tool
