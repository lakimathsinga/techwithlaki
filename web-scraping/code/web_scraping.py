import requests
from bs4 import BeautifulSoup
import csv 

# Define the URL of the website
url = "https://www.yelp.com/search?find_desc=Burgers&find_loc=Queenstown%2C+Singapore"

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200: 
  # open the file in the write mode
  file = open('burger_shops.csv', 'w')
  writer = csv.writer(file)
  # Request successful, access the content of the website
  content = response.text
  print(f"The website content starts with: {content[:100]}...")  # Print first 100 characters
  # Parse the HTML code
  soup = BeautifulSoup(response.content, 'html.parser')
  #find a ul tag with class list__09f24__ynIEd
  ul_tag = soup.find('ul', class_='list__09f24__ynIEd')
  if ul_tag:
    #Create an empty row to insert in the csv file
    row = []
    #Iterate through the li elements of the ul tag
    for li_element in ul_tag.find_all('li', class_='css-1qn0b6x'):
      #find a h3 tag in the list element which has a class starts with businessName
      business_name_tag = li_element.find('h3', class_=lambda class_: class_ and class_.startswith('businessName'))
      if business_name_tag:
        #find an a tag inside the h3 tag found previously
        link_to_title = business_name_tag.find('a')
        #get the title text and add to the row
        row.append(link_to_title.text.strip())
      #find a div tag which has a class css-1jq1ouh, inside the li tag
      rating_tag = li_element.find('div', class_='css-1jq1ouh')
      if rating_tag:
        #get the rating text and add to the row
        row.append(rating_tag.text.strip())
        #write the row to the csv
        print(row)
        writer.writerow(row)
        #make the row empty for the next burger shop
        row = []
  else:
    print("No ul element found.")
  file.close()

else:
  # Request failed, print the status code
  print(f"Request failed. Status code: {response.status_code}")