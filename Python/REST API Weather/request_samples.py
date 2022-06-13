import requests

print("\t[/cities GET]")

url = 'http://localhost:10000/cities'
print(url)
request = requests.get(url)
print("Міста в базі даних: ")
cities = request.json()["cities"]
for i in range(len(cities)):
    print(" - ", cities[i])
    
print("\n\t[/mean GET]")
values = ['temp', 'pcp', 'clouds', 'pressure', 'humidity', 'wind_speed']
for i in [2,4]:
    city = cities[i]
    value_type = values[i]
    url = f'http://localhost:10000/mean?city={city}&value_type={value_type}'
    print(url)
    request = requests.get(url)
    value = request.json()["mean"]
    print(f"Середнє значення параметру {value_type} для міста {city}: \n - {value}\n")

print("\t[/records GET]")
start_dt = ['15.12.2021', '17.12.2021']
end_dt = ['17.12.2021', '20.12.2021']
for i in range(2):
    city = cities[i]
    start_date = start_dt[i]
    end_date = end_dt[i]
    url = f'http://localhost:10000/records?city="{city}"&start_dt={start_date}&end_dt={end_date}'
    print(url)
    request = requests.get(url)
    records = request.json()["records"]
    print(f"Параметри для міста {city} у вказаному діапазоні {start_date} - {end_date}:\n")
    for j in range(len(records)):
        record = records[j]
        print(f' + date: {record["date"]}\n')
        keys = list(record.keys())
        for k in range(7):
            if k!=1:
                print(f'\t - {keys[k]}: {record[keys[k]]}\n')
                
print("\n\t[/moving_mean GET]")
for i in [2,3]:
    city = cities[i+1]
    value_type = values[i]
    url = f'http://localhost:10000/moving_mean?city={city}&value_type={value_type}'
    print(url)
    request = requests.get(url)
    moving_mean = request.json()["moving_mean"]
    print(f"Значення параметру {value_type} за алгоритмом ковзаного середнього для міста {city} для всіх дат: \n")
    for j in range(7):  
        mov_mean = moving_mean[j]
        print(f' - {mov_mean["date"]}: {mov_mean[value_type]}\n')
            
        
