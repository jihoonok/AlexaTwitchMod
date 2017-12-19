# AlexaTwitchModerator


The AlexaTwitchModerator is a tool which streamers can use their voice to invoke chat commands, rather than the streamer having to alt tab to input the commands they wish to invoke on their chat. <br />

Alexa -> lambda (process command and send the command in sqs message) <br />
Python code runs locally and then parse the command from the sqs message and then do the command in twitch. <br />
<br />
AWS Services: alexa skill kit, sqs message, lambda, s3 <br />

AWS keys/some urls are deleted for the sake of security <br /> 

Youtube Link: https://youtu.be/Qc-SxqBI9AQ <br />

Architecture Image: https://imgur.com/4LgjAY3
