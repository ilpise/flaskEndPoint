# Copyright 2021 Simone Corti. All rights reserved

from flask import Blueprint, request, jsonify, current_app

# Use of pyserial with conversion of HEX values to binary
# This fits better the command codes of COGES
import serial
import serial.tools.list_ports as port_list

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
apicoges_blueprint = Blueprint('apicoges', __name__, template_folder='templates')

@apicoges_blueprint.route('/api/coges_engine/request', methods=['POST'])
def coges_engine_request():

    json_data = request.get_json()
    command_code = json_data["command_code"]

    port = current_app.config["COGES_PORT"]
    baudrate = current_app.config["COGES_BAUDRATE"]

    serialPort = serial.Serial(port=port, baudrate=baudrate,
                                    bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)

    # COGES PARTS
    start = '{'
    stop = '}'

    slave_address = '1'

    # Calculate the checksum
    a = format(ord(slave_address), "x") # 31

    if command_code == "81":
        # Transform  the json_data["deductVal"] 001000 in $31 $30 $30 $30
        val = list(json_data["deductVal"])
        # for i in range( 0, len( val ) ):
        #     if val[i] != '0':
        #         val = val[i:]
        #         break

        print(val)
        # Set the additional hex string ASCII numeric characters
        # additional = ''
        # checkAdd = 0
        # for char in val :
        #     additional += format( ord( char ), "x" )
        #     checkAdd += int( char, 16 )
        #
        # checksum = hex( int( a, 16 ) + int( command_code, 16 ) + checkAdd)
        # # checksum = hex( int( a, 16 ) + int( command_code, 16 ) )

    elif command_code == "80":

        # costruiamo un array per calcolare la checksum e comporre il payload
        fcArray = [format(ord(slave_address), "x"), command_code]

        # elemento addizionale inserito hard da portare nel javascript
        priceline = [format(ord("0"), "x"), format(ord("0"), "x"),format(ord("6"), "x")]
        fcArray.extend(priceline)

        # Transform the json_data["deductVal"] e.g. 001000 in $31 $30 $30 $30
        val = list(json_data["deductVal"])
        # Remove 0's from the head
        for i in range( 0, len( val ) ):
            if val[i] != '0':
                val = val[i:]
                break
        # Append the transformed values to the array
        for char in val :
            fcArray.append( format( ord( char ), "x" ))

        print("VERIFICA ", fcArray)

        # The payload is composed by the device id the command and eventually other chars
        payload = ''.join( fcArray )
        print("PAYLOAD", payload)

        # Calculate the checksum
        checksumInt = 0
        print("Priceline ", priceline)
        for char in fcArray :
            print(char)
            checksumInt += int(char, 16)

        print("checksum int ",  checksumInt)
        checksum = hex (checksumInt)
    else :
        checksum = hex(int(a, 16) + int(command_code, 16))

    # remove the 0x before the number and fill an array
    checkarr = list(checksum[2:])
    print(checkarr)
    # Compose the command

    if (command_code == "81" or command_code == "80"):
        fullcommand = format( ord( start ), "x" )  + payload + format( ord( stop ), "x" ) + format(
            ord( checkarr[1].upper() ), "x" ) + format( ord( checkarr[2].upper() ), "x" )
        print("Fullcommand 80", fullcommand)
    else :
        fullcommand = format( ord( start ), "x" ) + a + str( command_code ) + format( ord( stop ), "x" ) + format(
            ord( checkarr[0].upper() ), "x" ) + format( ord( checkarr[1].upper() ), "x" )
        print ("Fullcommand simple", fullcommand)

    serialPort.write(bytes.fromhex(fullcommand))

    # read the response
    line = serialPort.readline()
    serialPort.close()

    ret = {"req": command_code,
           # "resp": line,
           "response": line.decode('utf-8')
           }
    return(jsonify(ret), 200)


@apicoges_blueprint.route('/api/coges_engine/checksum', methods=['GET'])
def coges_test_checksum():

    # chesumt1 = hex( 31+20 )
    print(int( "31", 16 ))
    print( hex (int( "31", 16 )) )
    checksumt2 = hex ( int( "31", 16 ) + int( "70", 16) )
    checkarr = list( checksumt2[2:] )
    commandCHeck = format( ord( checkarr[0].upper() ), "x" ) + format( ord( checkarr[1] ), "x" )

    # checksum1  = hex( 31+80+30+30+36+35+30+30 )
    checksumInt = int( "31", 16 ) + int( "80", 16 ) + int( "30", 16) + int( "30", 16) + int( "36", 16) + int( "35", 16) + int( "30", 16) + int( "30", 16)
    print(checksumInt)
    print(hex (checksumInt))
    checksum2 = hex( int( "31", 16 ) + int( "80", 16 ) + int( "30", 16) + int( "30", 16) + int( "36", 16) + int( "35", 16) + int( "30", 16) + int( "30", 16))
    # checksum2 = hex( int( "31", 16 ) + int( "80", 16 ) + int( "30", 16) + int( "30", 16) + int( "36", 16))
    # checksum2 = hex( int( "31", 16 ) + int( "80", 16 ) )
    # checksum2 = hex( int( "31", 16 ) + int( command_code, 16 ) + checkAdd )

    checkarr2 = list( checksum2[2:] )
    commandCHeck2 = format( ord( checkarr2[0].upper() ), "x" ) + format( ord( checkarr2[1] ), "x" )


    ret = {"A 70": checksumt2, "A 70 req": commandCHeck, "B 80": checksum2, "B 80 req": commandCHeck2}
    # ret = {"A": chesumt1, "B":checksumt2, "C": checksum1, "D" : checksum2}
    return (jsonify( ret ), 200)