from threading import Thread
import requests
import sys, socket, string, datetime
import json
import time

class DataBot(Thread):

    # DO NOT CHANGE
    SERVER = 'irc.twitch.tv'
    PORT = 6667
    NICKNAME = 'mroseman_bot'
    PASSWORD = 'oauth:1a6m7cnaoispip8l00zy0h9nv2hten'

    BUFFER_SIZE = 1024

    #  if the user count drops below this stop monitoring
    user_limit = 250

    
    # default constructor
    def __init__(self, channel_id, channel):
        # initialize threading
        Thread.__init__(self)
        self.daemon = True

        # create IRC socket object 
        self.IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # join the channel and authenticate
        self.channel_id = channel_id
        self.channel = channel
        self.irc_conn()
        self.login(self.NICKNAME, self.PASSWORD)
        self.join(channel)

        print ("succesfully joined channel " + channel)
        # execute thread
        self.start()
    
    #  open connection
    def irc_conn(self):
        self.IRC.connect((self.SERVER, self.PORT))
    
    #  send data through socket
    def send_data(self, command):
        self.IRC.send(command + '\r\n')
    
    #  get data through socket
    def get_data(self):
        return self.IRC.recv(self.BUFFER_SIZE)
    
    #  join a channel
    def join(self, channel):
        self.send_data("JOIN #%s" % channel)
    
    #  send login data
    def login(self, nickname, password=None):
        self.send_data("PASS %s" % password)
        self.send_data("NICK %s" % nickname)
    
    # insert to database
    def insert_message(self, username, msg):
        msg = msg.replace('\'', '\\\'')
        msg = msg.replace ('\"', '\\\"')

        #  insert the username if it doesnt already exist
        # query = """
        # INSERT IGNORE Users (UserName, Monitor) VALUES ('{0}', FALSE);
        # """.format(username)
	print msg

        #  insert this specific message to the Messages table

        # optionally print the messages
        # print timestamp, username, msg

    def keep_monitoring(self):
        """
        queries the database to see if this channel should still be monitored
        returns true if the thread should remain and false if the thread should
        stop
        """

        #  if the channel has fewer than 250 users
        num_users = r.json()['stream']['viewers']
        if num_users < self.user_limit:
            self.con.query(query, {'channel':self.channel})

    # override run function from interface
    def run(self):
        print ('thread started')

        readbuffer = ""

        oldtime = time.time()

        while 1:
            #  Check to see if this channel should still be monitored

            

            # self.con.close()
            readbuffer=readbuffer + self.get_data()
            temp = string.split(readbuffer, '\n')
            readbuffer = temp.pop()
    
            for line in temp:
                line = string.rstrip(line)
                line = string.split(line)

                if (line[0] == 'PING'):
                    self.send_data('PONG %s' % line[1])
                if (line[1] == 'PRIVMSG'):
                    username = line[0].replace(":", "",  1)
                    index = line[0].find('!')
                    username = username[:index - 1]
    
                    msg = ' '.join(line[3:])[1:]

                    self.insert_message(username, msg)
bot = DataBot(1, "yoda")
while 1:
	pass
