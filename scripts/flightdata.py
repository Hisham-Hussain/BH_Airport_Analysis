import numpy as np
import datetime 
import pandas as pd
import requests 
from bs4 import BeautifulSoup
def collect_flight_data(day, flight_direction):
    '''
    Collects data from the  BH Intl Airport website. Returns it as a table. 

    Args:
    day(string) : either today(TD) or tomorrow (TM)
    flight_direction(string): either arrivals or departures

    Returns:
    Pandas DF that has 7 columns
    '''
    url = f"https://www.bahrainairport.bh/flight-{flight_direction}?date={day}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text)


    time_lst = []
    country_lst = []
    airways_lst = []
    gate_lst = []
    status_lst = []
    flight_lst = []
    
    #flights = soup.find_all("div", {"class": "flight-table-list row dvArrivalList"})
    #flights = soup.find_all("div", {"class": "flight-table-list row dvDepartureList"})
    #flights = soup.find_all("div", {"class": f"flight-table-list row dv(flight_direction[:-1].title()"}List') #checks if departure or arrival
    flights = soup.find_all("div", {"class": f"flight-table-list row dv{flight_direction[:-1].title()}List"})
    for flight in flights:
        try:
            airways_lst.append(flight.find('img')['alt'])
        except:
            airways_lst.append(pd.NA)
        status_lst.append(flight.find('div', class_="col col-flight-status").text.strip())
        flight_lst.append(flight.find('div', class_="col col-flight-no").text.strip())
        gate_lst.append(flight.find('div', class_="col col-gate").text.strip())
        time_lst.append(flight.find('div', class_="col col-flight-time").text.strip())
        country_lst.append(flight.find('div', class_="col col-flight-origin").text.strip())
    
    flights_data = {'country':country_lst, 
                        'flight_number':flight_lst,
                        'airline':airways_lst, 
                        'gate':gate_lst, 
                        'status':status_lst,
                        'time':time_lst}
        
    df = pd.DataFrame(flights_data)
    if day=='TD':
            date=datetime.date.today()
    elif day=='TM':
        date=datetime.date.today()+datetime.timedelta(days=1)
    df['arrival_date']=date
    df['direction']=flight_direction
    
        
        
        
    
    return df


import time
def collect_arr_dep():
    flight_table=[]
    directions=['arrivals','departures']
    days=['TD','TM']
    for direction in directions:
        for day in days:
            flight_table.append(collect_flight_data(day,direction))
            time.sleep(10) #slow down the requests
    df=pd.concat(flight_table)
    return df
def save_data(df):
    today=datetime.date.today()
    path = f'all_flights_data_{today}.csv'
    df.to_csv(path)

df=collect_arr_dep()
save_data(df)