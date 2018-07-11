import requests
import csv, json

'''
Do not publish public API key, use env variables.
'''
# Yelp API Key
YELP_API_KEY = "YELP_API_KEY_HERE"

# settings
csv_upload_path = "yelp_upload.csv" # upload file path for csv containing keywords and locations
csv_download_path = "yelp_results.csv" # download file path for csv output results
limit = 50  # result limit, maximum is 50 per request
hard_limit = 1000 # hard limit imposed by yelp
radius_in_meters = 40000 # yelp limits to 40,000 meter (25 mile) radius
data = []   # data list for CSV file generation
locations = [] # upload csv containing keywords and locations

# Yelp request
def make_api_call(keyword, location, offset):
    global offset_count # import global variable to add to counter 
    
    url = "https://api.yelp.com/v3/businesses/search" 
    querystring = { "term":keyword, "location":location, "radius":radius_in_meters, "offset": offset, "limit":limit }
    headers = {
        'Authorization': "Bearer %s" % (YELP_API_KEY),
        'Cache-Control': "no-cache",
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    results = json.loads(response.text)
    # if the response has businesses key 
    try: 
        businesses = results['businesses']
        # if business key is NOT an empty list
        if businesses:
            for business in businesses:
                if business not in data:
                    data.append(business)
                else:
                    print("")
                    print("%s already exists" % (business['name']))
                    print("")
            print("%s businesses found (%s, %s)" % (offset_count, keyword, location))
            offset_count = offset_count + limit  # change global variable
            
            if offset_count < hard_limit:
                make_api_call(keyword, location, offset_count) 
            
            elif offset_count == hard_limit:
                print("request exceeds yelp's hard limit of 1,000 results")
        # if business key is an empty list (no businesses returned with the given criteria)
        elif not businesses:
            print("total businesses found: %s for (%s, %s)" % (len(data), keyword, location))
            print("")
        # error catch
        else:
            print("ERROR 1 with request data")
    # if response does not have businesses key, most likely an error    
    except:
        print("ERROR 2 with request data")

def generate_csv(data):

    try:
        with open(csv_download_path, 'wb') as csvfile:
            filewriter = csv.writer(csvfile)
            filewriter.writerow(['business name', 'distance in miles','phone number', 'category', 'address', 'address 2', 'address 3', 'city', 'state', 'zip'])
            for business in data:
                # category list
                categories = business['categories']
                cat_list =[]
                for category in categories:
                    cat_list.append(category['title'])
                # convert distance from meters to miles
                distance = round((int(business['distance'])/1609.344),2)
                # write rows to csv
                filewriter.writerow([
                    business['name'], 
                    distance,
                    business['phone'], 
                    ",".join(cat_list),
                    business['location']['address1'], 
                    business['location']['address2'], 
                    business['location']['address3'], 
                    business['location']['city'],
                    business['location']['state'],
                    business['location']['zip_code']
                ])
        print("Results added to CSV")
        print("")
    
    except:
        print("")
        print("ERROR with CSV data")
        print("ERROR %s items" % (len(data)))
        print("")

# takes list of dictionaries and uses key/value pair as keyword and location variables. 
def get_all_businesses(locations):
    global offset_count
    for location in locations:
        offset_count = 0
        make_api_call(location['keyword'], location['location'], offset_count)
    print("")
    print("please wait, generating csv....")
    generate_csv(data) 
    
# reads csv to create list of keywords and locations
def read_csv(file_name):
    with open(file_name, 'rb') as file:
        reader = csv.reader(file)
        
        row_number = 0
        for row in reader:
            if row_number >= 1:
                locations.append({"keyword":row[0], "location":row[1]})
            row_number = row_number + 1    
    
    print("%s complete" % (csv_upload_path))
    print("")
    get_all_businesses(locations)
    print("")
    print("DONE SON! Check %s for results" % (csv_download_path))

read_csv(csv_upload_path)