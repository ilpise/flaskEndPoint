import os
import requests

# Smartcard
from smartcard.Exceptions import NoCardException
from smartcard.System import readers
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from flask_login import encode_cookie
from flaskwebgui import FlaskUI

from app import create_app, socketio

app = create_app()

# https://stackoverflow.com/questions/8470431/what-is-the-best-way-to-implement-a-forced-page-refresh-using-flask
#defines the job
# def job():
#     # new_price = get_new_price();
#     #job emits on websocket
#     socketio.emit('price update',new_price, broadcast=True)
#
# #schedule job
# scheduler = BackgroundScheduler()
# running_job = scheduler.add_job(job, 'interval', seconds=4, max_instances=1)
# scheduler.start()

# a simple card observer that prints inserted/removed cards
class PrintObserver(CardObserver):
    """A simple card observer that is notified
    when cards are inserted/removed from the system and
    prints the list of cards
    """

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            print("+Inserted: ", toHexString(card.atr))
            # user = User.query.filter_by( username='admin' ).first()
            # print(user)
            # test = requests.get('http://localhost:5000/sample_api_request')
            # test = requests.get( 'http://localhost:5000/sc_login' )
            # test = requests.get( 'http://localhost:5000/api/login' )
            # test = requests.get( 'http://localhost:5000/login' )
            # test = requests.post('http://localhost:5000/login', params={'q': 'raspberry pi request'})
            response = requests.post( 'http://localhost:5000/register', json={"name": "top", "charge": "+2/3"} )
            print(response)
            print(response.json())
            # socketio.emit( 'my event', 'My data', broadcast=True )
            # with self.client.session_transaction():
            #     self.client.set_cookie(
            #         self.app.config['SERVER_NAME'],
            #         'remember_token',
            #         encode_cookie( user_id )
            #     )
        for card in removedcards:
            print("-Removed: ", toHexString(card.atr))

# ATT Uncomment per avere il thread attivo
cardmonitor = CardMonitor()
# # cardobserver = PrintObserver()
cardmonitor.addObserver( PrintObserver() )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    # socket.run( app, host='127.0.0.1', port=8001, debug=True,
    #             use_reloader=False )
    # socketio.run( app )
    FlaskUI( app, socketio=socketio, start_server="flask-socketio" ).run()