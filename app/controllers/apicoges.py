# Copyright 2021 Simone Corti. All rights reserved

from flask import Blueprint, request, jsonify

# Use of pyserial with conversion of HEX values to binary
# This fits better the command codes of COGES
import serial
import serial.tools.list_ports as port_list


# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
apicoges_blueprint = Blueprint('apicoges', __name__, template_folder='templates')

@apicoges_blueprint.route('/coges_engine', methods=['POST'])
def coges_engine():
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    # if not current_user.is_authenticated:
    #     return redirect(url_for('main.login'))

    print(request.get_json())

    # ports = list(port_list.comports())
    # print(ports[0].device)
    # port = ports[0].device

    port = '/dev/ttyACM0'
    baudrate = 9600
    serialPort = serial.Serial(port=port, baudrate=baudrate,
                                    bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)

    print(type(serialPort))
    sp = type(serialPort)
    # COGES PARTS
    start = '{'
    stop = '}'

    slave_address = '1'
    command_code = '20' # a1

    # Calculate the checksum
    a = format(ord(slave_address), "x") # 31
    checksum = hex(int(a, 16) + int(command_code, 16))
    # remove the 0x before the number and fill an array
    # print(checksum[2:])
    checkarr = list(checksum[2:])
    # print(checkarr)
    # print(format(ord(checkarr[0]), "x"))
    # Compose the command
    fullcommand = format(ord(start), "x")+a+str(command_code)+format(ord(stop), "x")+format(ord(checkarr[0]), "x")+format(ord(checkarr[1]), "x")
    # print(fullcommand.upper())
    serialPort.write(bytes.fromhex(fullcommand))

    line = serialPort.readline()
    # print( line )
    # print(type(line))
    serialPort.close()

    ret = {"code": "request",
           # "ports": str(ports) ,
           "port": port, "sp": str(sp), "response": line.decode('utf-8')}
    return(jsonify(ret), 200)

