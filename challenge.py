import pyRofex
import sys

############################ Funciones #######################
def logout():
    print("Cerrando sesion de Remarkets")
    try:   
        pyRofex.close_websocket_connection()
    except:
        print("Error al cerrar sesion")
    sys.exit()

def check_order_send(arg):
    if arg["status"] == "ERROR":
        print("Error al ingresar la orden")

#############################################################



#Check de los argumentos
if len(sys.argv)!=8 or sys.argv[2]!="-u" or sys.argv[4]!="-p" or sys.argv[6]!="-a":
    print("Argumentos invalidos!")
    sys.exit()

instrumento=sys.argv[1]

#inicializo el environment
print("Iniciando sesion en Remarkets")
try:
    pyRofex.initialize(
        user=sys.argv[3],
        password=sys.argv[5],
        account=sys.argv[7],
        environment = pyRofex.Environment.REMARKET)
except:
    print("Usuario y/o contraseña incorrectos")
    sys.exit()



# Inicializo la conexion Websocket
try:
    pyRofex.init_websocket_connection()
except:
    print("Error al establecer una conexion websocket")
    sys.exit()



#Obtengo la MARKET_DATA
print("Consultando simbolo")
md = pyRofex.get_market_data(instrumento, [pyRofex.MarketDataEntry.BIDS,
                                           pyRofex.MarketDataEntry.LAST])


#Check del simbolo
if md["status"] == "ERROR" and md["description"] == "Security {0}:ROFX doesn't exist".format(instrumento):
    print("Simbilo invalido")
    logout()

try:
    print("Ultimo precio operado: ${0}".format(md["marketData"]["LA"]["price"]))
except:
    print("Ultimo precio operado: None")

#CONSULTO EL PRECIO DEL BID
print("Consultando BID")

try:
#Si exitsen entradas, creo una a $0,01 menos que el precio del BID
    bi = md["marketData"]["BI"][0]["price"]
    print("Precio del BID: ${0}".format(bi))
    print("Ingresando orden a ${0}".format(bi-0.01))
    chk = pyRofex.send_order(instrumento, side=pyRofex.Side.BUY, size=1, price=bi-0.01, order_type=pyRofex.OrderType.LIMIT)
#Chequeo que la orden se haya realizado con exito
    check_order_send(chk)
except:
#Si no existen entradas, creo una a $75,25
    print("No hay BIDs activos")
    print("Ingresando orden a $75,25")
    chk = pyRofex.send_order(instrumento, side=pyRofex.Side.BUY, size=1, price=75.25, order_type=pyRofex.OrderType.LIMIT)
#Chequeo que la orden se haya realizado con exito
    check_order_send(chk)

logout()