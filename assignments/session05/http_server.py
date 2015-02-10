import mimetypes
import os
import socket
import sys
import glob

#print >>sys.stderr, sys.path[0]
server_path = sys.path[0]

def response_ok(uri_content, mimetype):
    """returns a basic HTTP response"""
    #directory = os.getcwd()
    #print >>sys.stderr, directory
    #print >>sys.stderr, sys.path[0]
    resp = []
    resp.append("HTTP/1.1 200 OK")
    #resp.append("Content-Type: text/plain")
    resp.append("Content-Type: ".format(mimetype))
    resp.append("")
    resp.append(uri_content)
    #resp.append("this is a pretty minimal response")
    return "\r\n".join(resp)

def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp)


def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    print >>sys.stderr, 'This is the URI: ', uri
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    print >>sys.stderr, 'request is okay'
    return uri

def resolve_uri(uri):

    home_dir = 'webroot'

    print 'uri is: ', uri

    print 'current dir is: ', os.getcwd()
    
    #Make sure we're in the right directory
    if os.getcwd() == server_path:

        #print 'switching from', os.getcwd()
        os.chdir(home_dir)
        #print 'New directory: ', os.getcwd()

    #Remove leading slash and turn resource into an absolute path
    path_to_resource = os.path.join(str(os.getcwd()),str(uri.strip('/')))

    #If resource doesn't exist, RETURN 404 with extreme prejudice
    if not os.path.exists(path_to_resource):
        raise ValueError
        return response_not_found()


    print 'The Path to the resource is: ', path_to_resource

    #Guess the mimetype of the resource
    mimetype_guess = mimetypes.guess_type(uri)

    print 'It looks like the mimetype is: ', mimetypes.guess_type(uri)[0]
    
    #If this is a directory, set mimetype
    if os.path.isdir(path_to_resource):
        print '\nThis is a directory!\n' 
        mimetype_guess = 'text/plain'
    
    print 'Now The mimetype is: ', mimetype_guess

    #begin formulating the response
    resp = []
    resolve_response = ''

    #resp.append("HTTP/1.1 200 OK")
    #resp.append("Content-Type: text/plain")

    #Add the guessed Mimetype
    #resp.append("Content-Type: {}".format(mimetype_guess[0]))

    #Adding necessary blank line
    #resp.append("")

    #Print each Entry if the URI is a directory
    if os.path.isdir(path_to_resource):
        [resp.append(i) for i in os.listdir(path_to_resource)]
        #resp.append(os.listdir(path_to_resource))
        resolve_response = "\r\n".join(resp)

    #resp.append(file_object)

    if mimetype_guess[0] == 'image/jpeg' or mimetype_guess[0] == 'image/png':

        file_object = open(path_to_resource, 'rb')
        #return file_object.read()
        resolve_response = file_object.read()

    #return "\r\n".join(resp)

    #return ("\r\n".join(resp), mimetype_guess[0])
    return (resolve_response, mimetype_guess)


def response_not_found():
    """returns a 404 - Not Found response"""
    resp = []
    resp.append("HTTP/1.1 404 Not Found")
    resp.append("")
    resp.append("THAT'S A 404, PLEASE TRY AGAIN!")
    return "\r\n".join(resp)

def server():
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print >>sys.stderr, "making a server on %s:%s" % address
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print >>sys.stderr, 'waiting for a connection'
            conn, addr = sock.accept() # blocking
            try:
                print >>sys.stderr, 'connection - %s:%s' % addr
                request = ""
                while True:
                    data = conn.recv(1024)
                    request += data
                    if len(data) < 1024 or not data:
                        break

                try:
                    uri = parse_request(request)
                except NotImplementedError:
                    response = response_method_not_allowed()
                else:
                    # replace this line with the following once you have
                    # written resolve_uri

                    #response = resolve_uri(uri)
                    
                    content, type = resolve_uri(uri) # change this line

                    ## uncomment this try/except block once you have fixed
                    ## response_ok and added response_not_found
                    try:
                        response = response_ok(content, type)
                    except NameError:
                        response = response_not_found()

                print >>sys.stderr, 'sending response'
                conn.sendall(response)
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
