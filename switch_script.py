import csv

connectors = dict()
chargers = dict()

rows = []

def convert_evse():
    regions = dict()
    fields = []
    with open('evwatts.public.evse.csv', mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        i = 1
        for row in csv_reader:
            
            # Each row is a dictionary
            if(row["region"] not in regions):
                regions[row["region"]] = i
                i += 1
    with open('evwatts.public.evse.csv', mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        fields = csv_reader.fieldnames
        for row in csv_reader:
            row["region"] = regions[row["region"]]
            if(row["pricing"] == "Paid"):
                row["pricing"] = 1
            elif(row["pricing"] == "Free"):
                row["pricing"] = 0
            elif(row["pricing"] == "Undesignated"):
                row["pricing"] = "null"
            rows.append(row)
    with open('evwatts.public.evse.csv', mode='w', newline='', encoding='utf-8') as file:
       csv_writer = csv.DictWriter(file, fieldnames=fields)
       csv_writer.writeheader()
       csv_writer.writerows(rows)
        
def create_insert_evse():
    with open('evwatts.public.evse.csv', mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            rows.append(row)
    with open('insert.sql', mode='w', newline='', encoding='utf-8') as file:
        file.write("SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';\n")
        for row in rows:
            file.write(f"INSERT INTO charger (charger_id, area_type, charger_type, venue, paid, metro_area, region_id) VALUES ({row["\ufeffevse_id"]}, \"{row["land_use"]}\", \"{row["charge_level"]}\", \"{row["venue"]}\", {row["pricing"]}, \"{row["metro_area"]}\", {row["region"]});\n")

def create_insert_connector():
    with open('evwatts.public.connector.csv', mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            rows.append(row)
            
    with open('insert.sql', mode='w', newline='', encoding='utf-8') as file:
        file.write("SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';\n")
        for row in rows:
            file.write(f"INSERT INTO connector (connector_id, charger_id, connector_type, power_kw) VALUES ({row["\ufeffconnector_id"]}, {row["evse_id"]}, \"{row["connector_type"]}\", \"{row["power_kw"]}\");\n")
   
def create_insert_session():
    with open('evwatts.public.session.csv', mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            rows.append(row)
    with open('insert.sql', mode='w', newline='', encoding='utf-8') as file:
        file.write("SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';\n")
        for row in rows:
            file.write(f"INSERT INTO session (session_id, charger_id, error_flag_id, connector_id, energy_kwh, start_datetime, end_datetime, charge_duration, total_duration) VALUES ({row["session_id"]}, {row["evse_id"]}, {row["flag_id"]}, {row["connector_id"]}, {row["energy_kwh"]}, \"{row["start_datetime"]}\", \"{row["end_datetime"]}\", {row["charge_duration"]}, {row["total_duration"]});\n")
    
def read_file(file_to_read, list_to_fill, id):
    with open(file_to_read, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            list_to_fill[row[id]] = 1   

def find_index(index_to_find, list_to_search):
    return list_to_search[index_to_find]

def verify_connector():
    i = 1
    errored_count = 0
    with open('evwatts.public.connector.csv', mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            try:
                chargers[row["evse_id"]]
            except:
                errored_count += 1
                continue
            rows.append(row)
            i += 1
    print(errored_count)
    
def verify_session():
    i = 1
    errored_count = 0
    with open('evwatts.public.session.csv', mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            try:
                chargers[row["evse_id"]]
                connectors[row["connector_id"]]
            except KeyError:
                errored_count += 1
                continue
            except:
                print("Non IndexError occured.")
                continue
            rows.append(row)
            i += 1
    print(errored_count)
    with open('insert.sql', mode='w', newline='', encoding='utf-8') as file:
        file.write("SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';")
        for row in rows:
            file.write(f"INSERT INTO session (session_id, charger_id, error_flag, connector_id, energy_kwh, start_datetime, end_datetime, charge_duration, total_duration) VALUES ({row["session_id"]}, {row["evse_id"]}, {row["flag_id"]}, {row["connector_id"]}, {row["energy_kwh"]}, \"{row["start_datetime"]}\", \"{row["end_datetime"]}\", {row["charge_duration"]}, {row["total_duration"]});\n")
                

read_file('evwatts.public.evse.csv', chargers, "\ufeffevse_id")
read_file('evwatts.public.connector.csv', connectors, "\ufeffconnector_id")

verify_session()