"""
Using this script to test the call executed towards Land.id
used the following data : 
authentication token >> w1mBcRc5ouxfm5fFF7-r
request with data >>  https://parcels.id.land/parcels/v2/by_location.json?lng=-83.93399323458202&lat=39.18766110300089&X-Auth-Token=w1mBcRc5ouxfm5fFF7-r&X-Auth-Email=atomic.jacopo@gmail.com
"""

import asyncio
import re
from wsgiref.headers import Headers 
from playwright.sync_api import Page, expect
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import json
import logging
import requests




async def get_parcel_data(lng, lat, auth_token, auth_email):
 
  async with  async_playwright() as p:
    try:

      
      # Launch Playwright (headless mode optional)
      browser = await p.chromium.launch()
      context = await browser.new_context(
            extra_http_headers={'X-Auth-Token':auth_token, 'X-Auth-Email':auth_email}
        )
      page = await context.new_page()



   

      async def handle_request(route, request):
          print("executing")
          is_successful = False
          try:
              # Your request handling logic here
              #request.headers["X-Auth-Token"] = auth_token
              #request.headers["X-Auth-Email"] = auth_email
              print(request.headers)
              await route.continue_()
              is_successful = True 
          except Exception as e:
              is_successful = False
              logging.error("Error handling request: %s", str(e))

          logging.info("Request handled successfully: %s", is_successful)
          print(is_successful)

      # Intercept requests and set headers
      await page.route("https://parcels.id.land/**", handle_request)
      print("execute handle request")
      
    

      # Build the API URL with parameters
      url = f"https://parcels.id.land/parcels/v2/by_location.json?lng={lng}&lat={lat}"

      print(url)
      #print(requests.get(url))
        
      
      # Send GET request to the API and wait for response
      # timeout = 0 serve per eliminare il timeout della pagina
      response = await page.goto(url, timeout= 0)

      # Check for successful response (200 status code)
      if response.status == 200:
        # Parse the JSON response
        data = await response.json()
        return data
      else:
        # Handle error: Log or raise exception
        print(f"Error retrieving data: {response.status}")
        return None

    except Exception as e:
      # Handle other exceptions
      print(f"An error occurred: {e}")
      return None
    finally:
      # Close browser context
      await browser.close()





"""
Methods to extract data from the dictionary returned by the 
call to land.id
"""
def data_Extraction_parcels (data):
   #extractuion of specific data from the dictionary, parcels ID 
  parcels = []
  for parcel in data['parcels']:
    parcels.append(parcel['parcel_id'])

  return parcels
 

def data_Extraction_polygon (data):
   #extractuion of specific data from the dictionary, geometry made with WKT and ID 
  parcels = []
  for parcel in data['parcels']:
    polywkt = {'geom': parcel['geom_as_wkt'], 'parcelid':parcel['parcel_id']}
    parcels.append(polywkt)

  return parcels



def data_extraction_owner (data): 
  # Creation of secondary data structure of data related to owners
 #sequence of information: parcel_id,ownername,state, coordinates,address ,value  
 # owners is a dictionary made of tuples 
  owners=[]
  for land in data['parcels']:
    owner_info = (land['parcel_id'],land['owner_name'], land['state'],land['coordinates'],land['parcel_address'],land['value'])
    owners.append(owner_info)

  return owners


#Function to print data on file json give data dictionary as argument
def file_print(data): 
  print(" printing of refined data on file")
  data_json = json.dumps(data)
  with open ("test_json.json","w") as outfile:
    outfile.write(data_json) 
  print("Failed to retrieve data.")

# Example usage 
lng = -83.93399323458202
lat = 39.18766110300089
auth_token = "-"
auth_email = "-"

## data =  get_parcel_data(lng, lat, auth_token, auth_email)
data = asyncio.run(get_parcel_data(lng, lat , auth_token, auth_email))

if data:
  # Process the retrieved data
  print("data for the coordinates ==>  long : " + str(lng)+" --lat : "+str(lat))
  #print(data)
  print("[+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+][+]")
                    

  print(" printing of refined data on file")
  data_json = json.dumps(data)
  with open ("test_json.json","w") as outfile:
    outfile.write(data_json) 
else:
  print("Failed to retrieve data.")

# Convert the dictionary to a formatted JSON string
formatted_json_data = json.dumps(data, indent=4)

# Print the formatted JSON string to the terminal
print(formatted_json_data)
