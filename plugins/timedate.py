from datetime import date

def control():

    return "!date"

def main(array):

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = date.today()

    array[0].send(("PRIVMSG %s :%s, %s\r\n" % (array[1], days[today.weekday()], today)).encode())

    return