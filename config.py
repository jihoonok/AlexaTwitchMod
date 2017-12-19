import boto3
import requests

def additional_commands(self, e, cmds, bucket_name):
	c = self.connection
	cmd = cmds.split(' ')
	#print cmd[0]

	if cmd[0] == "feelsbadman":
		c.privmsg(self.channel, "FeelsBadMan")
	elif cmd[0] == "post":
		s3command = cmd[2]
		if s3command == "image":
			s4 = boto3.client('s3')
			url = s4.generate_presigned_url(
								ClientMethod = 'get_object',
                                Params={
                                    'Bucket': bucket_name,
                                    'Key': 'meme.jpg',
                                })
			splitUrl = url.split("?");
			print(splitUrl[0])
			c.privmsg(self.channel, splitUrl[0])
		elif s3command == "music":
			s4 = boto3.client('s3')
			url = s4.generate_presigned_url(
								ClientMethod = 'get_object',
                                Params={
                                    'Bucket': bucket_name,
                                    'Key': 'music.mp3',
                                })
			splitUrl = url.split("?");
			print(splitUrl[0])
			c.privmsg(self.channel, splitUrl[0])



