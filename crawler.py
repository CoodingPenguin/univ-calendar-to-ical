from selenium import webdriver

def is_official_holiday(content):
    if '공휴일' in content:
        return True
    else:
        return False

f = open('cau_calendar.csv', 'w')
f.write('Content, StartTime, EndTime, Duration\n')

driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.cau.ac.kr/cms/FR_CON/index.do?MENU_ID=590')

schedules = driver.find_elements_by_css_selector('div.calendar_list ul.calView_tb li')

for s in schedules:
    cont_time = s.text.split('\n')
    content = cont_time[0].replace(',', '/')
    datetime = cont_time[1]

    try:
        start_end = datetime.split('~')
        start_time = start_end[0]
        end_time = start_end[1]
        duration = True
    except:
        start_time = datetime
        end_time = datetime
        duration = False

    if not is_official_holiday(content):
        f.write(content + ',' + start_time + ',' + end_time + ',' + str(duration) + '\n')

f.close()