from bs4 import BeautifulSoup
import requests 
import pandas as pd


url = "https://www.programmableweb.com"
url_category = "/category/all/apis"

api_no = 0
api_pb = {}
url_tag = 0


while True:

    response = requests.get(url+url_category)
    data = response.text
    soup = BeautifulSoup(data,"html.parser")
    
    apis = soup.find_all("tr")

    for api in apis:
        title_td = api.find("td",{"class":"views-field-pw-version-title"})
        if(title_td):
            #print(title_td)
            api_name = title_td.find("a").text
            #print(api_name)
            api_url = url+title_td.find("a").get("href")
            #print(api_url)

            category_td = api.find("td",{"class":"views-field-field-article-primary-category"})
            category_a = category_td.find("a")
            #print(category_a)
            if category_a is not None:
                category = category_a.text
            else:
                category = ""
            #print(category)

            description = api.find("td",{"class":"views-field-field-api-description"}).text
            #print(description)

            api_no += 1
            api_pb[api_no] = [api_name,api_url,category,description]
            #print("________________________\n")
            
            
    url_tag = soup.find('a',{'title':'Go to next page'})

    if url_tag is not None:
        url_category = url_tag.get('href')
        print(url_category)
    else:
        break
        
print("Total apis:", api_no)
print("________________________\n")


np_apis_df = pd.DataFrame.from_dict(api_pb, orient = 'index', columns = ["Name","URL","Category","Description"])
np_apis_df.head()
np_apis_df.to_csv('np_apis.csv')
