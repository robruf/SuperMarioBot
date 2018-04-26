def control():
    return "!hello"

def main(array):

    array[0].sendall(("PRIVMSG %s :Hello world!\r\n" % (array[1])).encode())

    return
