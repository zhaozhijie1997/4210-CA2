# Name: Zhao Zhijie
# Matric No: A0150102H
# EE4210 CA2 ASSIGNMENT

import socket,re,os,sys,time
from socket import SHUT_RDWR

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def rec_web():
    rec = 'HTTP/1.1 200 OK\r\n' +\
      time.strftime('Date: %a, %d %b %Y %H:%M:%S SGT\r\n') +\
      'Content-Type: text/html\r\n' + '\r\n' +\
      '<HTML><HEAD>\r\n' +\
      '<TITLE>200 OK</TITLE>' +\
      '</HEAD><BODY>\r\n' +\
      '<form action="" method="get"><input type="text" name="input" value=""><br><br><input type="submit" value="Submit"></form>\r\n' +\
      '</BODY></HTML>\r\n'
    return rec

def send_web(data):
    send = 'HTTP/1.1 200 OK\r\n' +\
          time.strftime('Date: %a, %d %b %Y %H:%M:%S SGT\r\n') +\
          'Content-Type: text/html\r\n' + '\r\n' +\
          '<HTML><HEAD>\r\n' +\
          '<TITLE>200 OK</TITLE>' +\
          '</HEAD><BODY>\r\n' +\
          data +\
          '</BODY></HTML>\r\n'
    return send

def respond(client,addr):
    # print("Connected With address: {}".format(addr))
    recbuff = client.recv(1024)
    recbuff = recbuff.decode()
    if "GET /?input=" in recbuff:
        inputData = re.search('/?input=(.*) HTTP/1.1',recbuff).group(1)
        print('Received : {}'.format(inputData))
        client.send(send_web(inputData).encode())
    elif "GET / HTTP/1.1" in recbuff:
        client.send(rec_web().encode())
        print('Response Sent !! ')
    client.shutdown(SHUT_RDWR)
    client.close()
    os.exit(0)


def main(port):
    try:
        serversock.bind(('0.0.0.0',port))
    except Exception as e:
        print("Error with binding")
        sys.exit(1)

    try:
        serversock.listen(1)
    except Exception as e:
        print('Error Occured during Listening. Exiting!!')
        sys.exit(1)

    while True:
        try:
            client, addr = serversock.accept()
            child_pid = os.fork()
            if child_pid==0:
                respond(client,addr)
            else:
                os.waitpid(-1, os.WNOHANG)
        except Exception as e:
            print('{} Error Occured!!'.format(e))
if __name__ == "__main__":
    if len(sys.argv) == 2:
        Portnum = int(sys.argv[1])
    else:
        print("Wrong number of arguments. Shut down now.")
        print("Command should be : python {} <port>".format(__file__))
        sys.exit(1)
    main(Portnum)
