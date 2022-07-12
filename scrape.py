import requests
from bs4 import BeautifulSoup
import xlwt


base_url = "https://clutch.co"

developer_type_url = ['/web-developers/india?page=', '/directory/mobile-application-developers-india?page=']
sheet_name = ['web-developer', 'mobile-developer']
sheet_heading = ['Company', 'Website', 'Tagline', 'Location', 'Rating', 'Review Count', 'Hourly Rate', 'Min Project Size', 'Employee Size', 'Percentage Related To Work']

heading_style = xlwt.easyxf('font: bold 1')
wb = xlwt.Workbook()
for developerTypeIdx in range(len(developer_type_url)):
    developer_type = developer_type_url[developerTypeIdx]
    # current url
    current_base_url = base_url + developer_type
    # current working sheet
    ws = wb.add_sheet(sheet_name[developerTypeIdx])
    # adding all heading to sheets 
    for headingIdx in range(len(sheet_heading)):
        ws.write(0, headingIdx, sheet_heading[headingIdx], heading_style)
        ws.col(headingIdx).width = len(sheet_heading[headingIdx]) * 500
    
    # current scraped page
    page = 0
    # current row for excel
    sheetRow = 1
    while True:
        # current url with page no to be scraped 
        current_url = current_base_url + str(page)
        r = requests.get(current_url)
        if r.status_code==404:
            # no more pages available
            break
        data = BeautifulSoup(r.content, 'html.parser')
        companies = data.find_all("li", class_='provider-row')
        i = 0
        for company in companies:
            try:
                # scrapping
                company_title = company.find(class_="company_title").text.strip()
                website_link = company.find(class_="website-link__item")['href']
                tagline = company.find(class_="tagline").text.strip()
                try:
                    rating = company.find(class_="rating").text.strip()
                    review_count = company.find(class_="sg-rating__reviews").text.strip()
                except:
                    rating = 'Null'
                    review_count = 'Null'
                extra_details = company.find_all(class_="list-item")
                percentage_related_to_work = company.find(class_="hidden-xs").find('span').find('span').text.strip()
                extra_details_array = []
                for detials in extra_details:
                    extra_details_array.append(detials.find('span').text.strip())
                
                min_project_size, hourly_rate, employee_size, location = extra_details_array
                
                # final details of company
                final_company_details = [company_title, website_link, tagline, location, rating, review_count, hourly_rate, min_project_size, employee_size, percentage_related_to_work]
                
                # writing to excel
                for col in range(len(sheet_heading)):
                    ws.write(sheetRow, col, final_company_details[col])
                sheetRow+=1
                wb.save('example.xls')  # saving after every page 
            
            except Exception as e:
                print(e)
                pass
        print(page) # just to get current progress
        page+=1
    wb.save('example.xls')
    print('-----------')