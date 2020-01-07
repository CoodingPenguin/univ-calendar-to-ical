from selenium import webdriver

month31 = [1, 3, 5, 7, 8, 10, 12]
month30 = [2, 4, 6, 9, 11]

def is_official_holiday(content):
    if '공휴일' in content:
        return True
    else:
        return False

def convert_with_0(num):
    if num < 10:
        return '0'+str(num)
    else:
        return str(num)

def txt_to_date(txt, year='2020', end=False):
    date = txt.split('.')
    month = int(date[0])
    day = int(date[1])

    if end:
        if month in month30 and day == 30:
            month += 1
            day = 1
        elif month in month31 and day == 31:
            month = (month + 1) % 12
            day = 1
        else:
            day += 1

    return convert_with_0(month) + '/' + convert_with_0(day) + '/' + year

f = open('cau_calendar.csv', 'w')
f.write('Subject, Start Date, Start Time, End Date, End Time, All Day, Description, Location, UID\n')

driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.cau.ac.kr/cms/FR_CON/index.do?MENU_ID=590')

schedules = driver.find_elements_by_css_selector('div.calendar_list ul.calView_tb li')

for s in schedules:
    cont_time = s.text.split('\n')
    content = cont_time[0].replace(',', '/')
    datetime = cont_time[1]
    all_day = 'true'
    start_time = ''
    end_time = ''

    try:
        start_end = datetime.split('~')
        start_date = txt_to_date(start_end[0])
        if start_date[:2] == '12' and (float(start_end[1]) < 3 or float(start_end[1]) > 12.3):
            end_date = txt_to_date(start_end[1], year='2021', end=True)
        else:
            end_date = txt_to_date(start_end[1], end=True)

    except:
        start_date = txt_to_date(datetime)
        end_date = start_date


    if not is_official_holiday(content):
        f.write(content + ',' + start_date + ',' + start_time + ',' + end_date + ',' + end_time + ',' + all_day + ',' + ',' + ',' + '\n')

f.close()
