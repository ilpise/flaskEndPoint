
import json
from app import db, mqtt
from app.models.user_models import User, Vendor, Role

# Set default subscriptions
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe( 'vendors/create_update' )
    mqtt.subscribe( 'users/1' )


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    # print(client)
    # print(data)
    # print( data['topic'] )
    if data['topic'] == 'vendors/create_update':
        resp = json.loads(data['payload'])
        # print(resp)
        vendor = Vendor.query.filter_by(id=resp['gid']).first()
        vendor.title = resp['title']
        db.session.commit()

    # Update/Create the user with new data - credit
    if data['topic'] == 'users/1':
        print('MQTT users/1')
        resp = json.loads(data['payload'])
        print(resp)
        # see https://github.com/ilpise/flaskEndPoint/issues/3#issuecomment-943432104
        user = User.query.filter_by(username=resp['username']).first()

        if user is None:
            print('USER CREATE')
            # Get the customer role
            role = Role.query.filter( Role.name == str( 'customer' ) ).first()
            # Create the user
            user = User( username=resp['username'],
                         uid=resp['uid'],
                         password='plaintextpassword',
                         email=resp['email'],
                         active=True,
                         credit=resp['credit'])
            if role:
                user.roles.append( role )
            db.session.add( user )
        else:
            # Update the user
            print('USER UPDATE')
            if user.uid == resp['uid']:
                user.email=resp['email']
                user.credit=resp['credit']
            else:
                # this is the case of the registering EndPoint that will result with an empty uid
                user.uid = resp['uid']
                user.email=resp['email']
                user.credit=resp['credit']

        print()
        db.session.commit()
