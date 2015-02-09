import socket
import sys


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 8080)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print >>log_buffer, "making a server on {0}:{1}".format(*address)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print >>log_buffer, 'waiting for a connection'
            conn, addr = sock.accept() # blocking
            try:
                print >>log_buffer, 'connection - {0}:{1}'.format(*addr)

                request = ""

                while True:

                    data = conn.recv(1024)

                    request+=data

                    if len(data) < 1024:
                        break

                try:

                    uri = parse_request(request)

                except NotImplementedError:
                    response = response_method_not_allowed()

                else:

                    content, _type = resolve_uri(uri)

                try:
                    response = response_ok(content, type)

                except NameError:
                    response = response_not_found()

                print >>log_buffer, 'sending response'
                
                conn.sendall(response)

                    #print >>log_buffer, 'received "{0}"'.format(data) 

#                    if data:
#                        msg = 'sending data back to client'
#                        print >>log_buffer, msg
#                        conn.sendall(data)
#                    else:
#                        msg = 'no more data from {0}:{1}'.format(*addr)
#                        print >>log_buffer, msg
#                        break
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return

def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":

        raise NotImplementedError('This is not a GET request')
    
    print >>sys.stderr, 'request is okay'
    return uri



def response_method_not_allowed():
    """returns a method_not_allowed HTTP response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp)

def response_ok():
    """returns a basic HTTP response"""
    resp = []
    resp.append("HTTP/1.1 200 OK")
    resp.append("Content-Type: text/plain")
    resp.append("")
    resp.append("this is a pretty minimal response")
    return "\r\n".join(resp)


if __name__ == '__main__':
    server()
    sys.exit(0)
