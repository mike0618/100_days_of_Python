from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager
from pprint import pprint

ORIGIN_CITY_IATA = "LON"

datamanager = DataManager()
flightsearch = FlightSearch()

datamanager.write_iata(flightsearch)

pprint(datamanager.sheet_data)

from_date = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
to_date = (datetime.now() + timedelta(days=180)).strftime("%d/%m/%Y")

notification_manager = NotificationManager()

for entry in datamanager.sheet_data:
    flight = flightsearch.check_flight(ORIGIN_CITY_IATA,
                                       entry['iataCode'],
                                       from_date,
                                       to_date)
    if flight.price < entry['lowestPrice']:
        notification_manager.send_msg(flight)
