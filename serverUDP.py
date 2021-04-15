# Name: Zhao Zhijie
# Matric No: A0150102H
# EE4210 CA2 ASSIGNMENT

import socket,os,time,sys

serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_back():
    res = 'HTTP/1.1 200 OK\r\n' +\
      time.strftime('Date: %a, %d %b %Y %H:%M:%S SGT\r\n') +\
      'Content-Type: text/html\r\n' + '\r\n' +\
      '<HTML><HEAD>\r\n' +\
      '<TITLE>200 OK</TITLE>' +\
      '</HEAD><BODY>\r\n' +\
      'EE-4210: Continuous assessment\r\n' +\
      '</BODY></HTML>\r\n'
    return res


def respond(recbuff,serversock):
    recbuff = recbuff
    data = recbuff[0].decode()
    addr = recbuff[1]
    if "GET / HTTP/1.1" in data:
        serversock.sendto(send_back().encode(),addr)
        print("Response Sent!!!")
    else:
        print('This is not a HTTP request!!')
    os._exit(0)


def main(port):
    try:
        serversock.bind(('0.0.0.0',port))
    except Exception as e:
        print('{} Error Occurred'.format(e))
        sys.exit(1)

    while True:
        try:
            recbuff = serversock.recvfrom(1024)
            data = recbuff[0].decode()

            if not data:
                print('No data is received')
                break
            child_pid = os.fork()
            if child_pid==0:
                print("Connection with client successful")
                respond(recbuff,serversock)
            else:
                os.waitpid(-1, os.WNOHANG)
        except Exception as e:
            print('{} Error Occurred'.format(e))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        portnum = int(sys.argv[1])
    else:
        print("Wrong number of arguments. Shut down now.")
        print("Command should be : python {} <port>".format(__file__))
        sys.exit(1)
    main(portnum)
