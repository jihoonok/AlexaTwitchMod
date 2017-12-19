import sys
import irc.bot
import requests
import json
import random
import urllib
import boto3
import botocore

from config import additional_commands

sqs = boto3.resource('sqs')
s3 = boto3.resource('s3')

sqs_client = boto3.client('sqs')

name = ""
bucket_name = ""

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # Get the channel id
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print 'Connecting to ' + server + ' on port ' + str(port) + '...'
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)
        

    def on_welcome(self, c, e):
        print 'Joining ' + self.channel

        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

        queue = sqs.get_queue_by_name(QueueName="TwitchModerator")
    	sqs_client.set_queue_attributes(
    		QueueUrl= "url",
    		Attributes={'ReceiveMessageWaitTimeSeconds': '0'}
    	)

    	global name
    	global bucket_name
    	bucket_name = "twitch_bucket_" + name

    	
    	try:
    		s3.meta.client.head_bucket(Bucket=bucket_name)
    	except botocore.exceptions.ClientError as e:
    		s3.create_bucket(Bucket=bucket_name)

    	while True:
	    	messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20, MessageAttributeNames=['All'])
	    	for message in messages:
	    		cmd = message.body
	    		#print(message.body)
	    		self.do_command(e, cmd)
	    		message.delete()
    	return

    def do_command(self, e, cmds):
        c = self.connection

        cmd = cmds.split(' ')
        print cmd
        global name
        global bucket_name
        bucket = s3.Bucket(bucket_name)
        # Display current game streamer is playing
        if cmd[0] == "game":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])

        # Display the title of the streamer
        elif cmd[0] == "title":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' channel title is currently ' + r['status'])

        # common commands that streamers use.
        elif cmd[0] == "raffle":
        	url = "https://tmi.twitch.tv/group/user/" + name + "/chatters"
        	response = urllib.urlopen(url)
        	data = json.loads(response.read())
        	choice = random.choice(data['chatters']['viewers'])
        	message = choice + " has won " + cmd[1]
        	c.privmsg(self.channel, message)
        elif cmd[0] == "schedule":
			# obj = s3.Object(bucket, "schedule.txt")
			# print(obj.get()['Body'].read().decode('utf-8')) 
			link = "url" 
			f = urllib.urlopen(link)
			message = f.read()
			split = message.split('\n')
			for line in split:
				c.privmsg(self.channel, line)
        elif cmd[0] == "timeout":
        	time = cmd[3]
        	time = time[2:-1]
        	message = "/timeout " + cmd[1] + " " + time
        	c.privmsg(self.channel, message)
    	elif cmd[0] == "ban":
    		message = "/ban " + cmd[1]
    		c.privmsg(self.channel, message)
    	elif cmd[0] == "slow":
    		print cmd
    		message = "/slow " + cmd[1]
    		c.privmsg(self.channel, message)
    	elif cmd[0] == "slowOff":
    		c.privmsg(self.channel, "/slowoff")
    	elif cmd[0] == "subscribers":
    		c.privmsg(self.channel, "/subscribers")
    	elif cmd[0] == "subscribersOff":
    		c.privmsg(self.channel, "/subscribersoff")
    	elif cmd[0] == "host":
    		name = cmd[1]
    		message = "/host " + name 
    		c.privmsg(self.channel, name)
    	elif cmd[0] == "unhost":
    		message = "/unhost"
    		c.privmsg(self.channel, message)
        # The command was not recognized
        else:
        	additional_commands(self, e, cmds, bucket_name)
            #c.privmsg(self.channel, "Did not understand command: " + cmd)

def main():
    if len(sys.argv) != 5:
        print("Usage: twitchbot <username> <client id> <token> <channel>")
        sys.exit(1)

    username  = sys.argv[1]
    client_id = sys.argv[2]
    token     = sys.argv[3]
    channel   = sys.argv[4]
    global name
    name = username;
    bot = TwitchBot(username, client_id, token, channel)
    bot.start()

if __name__ == "__main__":
    main()
