
from app import mqtt


# Set default subscriptions
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe( 'vendors/create_update' )


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print( data )
