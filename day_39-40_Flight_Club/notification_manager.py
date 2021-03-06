from my_conf import account_sid, auth_token, twilio_phone, my_phone, EMAIL, EMAIL_TO, PWD
from twilio.rest import Client
import smtplib
from flight_data import FlightData


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def send_msg(self, flight: FlightData, email, name):
        msg = f'Hello {name}! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport}' \
              f' to {flight.dest_city}-{flight.dest_airport}, from {flight.out_date} to {flight.return_date}'
        if flight.stop_overs:
            msg += f'\nFlight has 1 stop over, via {flight.via_city}'

        # client = Client(account_sid, auth_token)
        # message = client.messages.create(body=msg, from_=twilio_phone, to=my_phone)
        # print(message.sid)

        with smtplib.SMTP('smtp.mail.yahoo.com') as conn:
            conn.starttls()
            conn.login(user=EMAIL, password=PWD)
            conn.sendmail(from_addr=EMAIL,
                          to_addrs=email,
                          msg=f'Subject:Low price alert!\n\n{msg}')
