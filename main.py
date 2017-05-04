import socket

# Constants
BUFFER_SIZE = 2048


def main():
    # connect to twitch irc
    IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IRC.connect(('irc.chat.twitch.tv', 6667))

    IRC.send(bytes('PASS oauth:cuyfgmtcbi4b4wnswjb9jjjfye8edy\r\n', 'UTF-8'))
    IRC.send(bytes('NICK mroseman_bot\r\n', 'UTF-8'))

    # get messages and print out
    IRC.send(bytes('JOIN #timthetatman\r\n', 'UTF-8'))

    readbuffer = ''
    while True:
        readbuffer = readbuffer + str(IRC.recv(2048).decode('UTF-8'))
        temp = str.split(readbuffer, '\n')
        readbuffer = temp.pop()

        for line in temp:
            line = line.rstrip()
            line = line.split()

            if line[0] == 'PING':
                IRC.send(bytes('PONG' + line[1] + '\r\n', 'UTF-8'))
            if line[1] == 'PRIVMSG':
                # username goes from second character to the first !
                username = line[0][1:line[0].find('!')]
                msg = ' '.join(line[3:])
                # strip off the colon from the first word
                msg = msg[1:]
                print('{} said: {}'.format(username, msg))


if __name__ == '__main__':
    main()
