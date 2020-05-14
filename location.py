import pandas as pd

import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt
import plotly_express as px
import tqdm
from tqdm.notebook import tqdm_notebook
from datetime import datetime
from datetime import date
import mysql.connector


import unicodedata

def database(ora,date1,locatie1):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      database="mydatabase"
    )

    
    mycursor = mydb.cursor()

    #mycursor = mydb.cursor()
    #sql = "DROP TABLE customers"
    #mycursor.execute("ALTER DATABASE mydatabase CHARACTER SET utf8 COLLATE utf8_general_ci")
    #mycursor.execute("ALTER TABLE Adrese DEFAULT CHARACTER SET utf8, COLLATE utf8_general_ci")
    #mycursor.execute("CREATE TABLE Adrese (id INT AUTO_INCREMENT PRIMARY KEY, ora VARCHAR(255), date1 VARCHAR(255),country VARCHAR(255), city VARCHAR(255), house_number VARCHAR(255), street VARCHAR(255), street_number VARCHAR(255), village VARCHAR(255))") 
   
    #mycursor.execute("DROP TABLE locatie")
    #mycursor.execute("CREATE TABLE locatie (id INT AUTO_INCREMENT PRIMARY KEY, ora VARCHAR(255),date1 VARCHAR(255),locatie VARCHAR(255))")

    sql = "INSERT INTO locatie (ora,date1,locatie) VALUES (%s,%s,%s)"
    val = (ora,date1,locatie1)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")





def Adresa(coordinates):
    geolocator = Nominatim(timeout=6,user_agent="Android 7.0")
    #coordinates = "47.171052, 27.562426"
    #coordinates = "47.165314, 27.412312"

    location = geolocator.reverse(coordinates)
    adresa=location.raw

    #aici aflam ora
    now = datetime.now()
    ora = now.strftime("%H:%M:%S")
    print("Ora: "  , ora)

    #aici aflam data
    today = date.today()
    date1 = today.strftime("%d/%m/%Y")
    print("Date: ", date1)


    village="None"

    #tara
    country=""
    lista=['country']
    if lista[0] not in adresa['address']:
        country="None"
    else:
        country=adresa['address']['country']
    print("Tara: ",country)

    #orasul
    city=""
    lista=['city']
    if lista[0] not in adresa['address']:
        city=adresa['address']['county']
        village=adresa['address']['village']
    else:
        city=adresa['address']['city']
    print("Orasul: ",city)
    if village!="None":
        print("Comuna: ",village)

    #house number
    house_number=""
    lista=['house_number']
    if lista[0] not in adresa['address']:
        house_number="None"
    else:
        house_number=adresa['address']['house_number']
    print("Numarul casei: ",house_number)

    #strada(road)
    street=""
    lista=['road']
    if lista[0] not in adresa['address']:
        street="None"
    else:
        street=adresa['address']['road']
    print("Numele strazii: ",street)

    #strada(street_number)
    street_number=""
    lista=['address29']
    if lista[0] not in adresa['address']:
        street_number="None"
    else:
        street_number=adresa['address']['address29']
    print("Numarul strazii: ",street_number)





    #eliminare diacritice
    def remove_accents(input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        return only_ascii

    def eliminare_diacritice(string1):
        string3=""
        string2=str(remove_accents(string1))
        for i in range(0,len(string2)):
            if string2[i]=="'":
                i=i+1
                while string2[i]!="'":
                    string3=string3+string2[i]
                    i=i+1
                break
        return string3
    country=eliminare_diacritice(country)
    city=eliminare_diacritice(city)
    house_number=eliminare_diacritice(house_number)
    street=eliminare_diacritice(street)
    street_number=eliminare_diacritice(street_number)
    village=eliminare_diacritice(village)




    Locatie1=country+"~"+city+"~"+house_number+"~"+street+"~"+street_number+"~"+village



    database(ora,date1,Locatie1)

#coordinates = "47.173171, 27.559389" #strada garii
#coordinates = "47.165314, 27.412312" #Letcani
coordinates = "47.171052, 27.562426" #pacurari
Adresa(coordinates)







#conectare la baza de date
#mysql -u root -p -h localhost


#mysql -u root -p -h localhost -ppass --default-character-set=utf8

#mysql -h localhost -u root -ppass --default-character-set=utf8







'''

print(adresa['address']['address29'])
print(adresa['address']['house_number'])
print(adresa['address']['road'])
print(adresa['address']['residential'])
print(adresa['address']['suburb'])
print(adresa['address']['city'])
print(adresa['address']['county'])
print(adresa['address']['country'])
print(adresa['address']['country_code'])
'''
