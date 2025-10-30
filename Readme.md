# 🎃 Halloween Doorbell Jumpscare Thing (For Home Assistant and Tapo Doorbells)
So I made this weird little contraption for Halloween that plays spooky sounds when someone rings my doorbell. It listens to my Home Assistant doorbell via MQTT and then BOOM - random creepy noises. Made the whole thing quick, so expect jank.
## What Does It Do?
When someone rings the doorbell:
1. Home Assistant sends an MQTT message to topic `h_doorbell_on`
2. This script catches it
3. Picks a random spooky sound from the folder `sounds`
4. Plays it for up to 8 seconds
5. Sends another MQTT message back to Home Assistant (h_doorbell_off) when it's done and an automation resets the trigger. For more info as to why I did this travesty look at https://github.com/JurajNyiri/HomeAssistant-Tapo-Control/issues/1015 and the known workarounds for battery powered tapo doorbells and not exposing their bell press sensor.
6. Hook up a guitar amp or something to the output and you're done!

That's it! Simple but effective for freaking out trick-or-treaters 😈

## Setup
You'll need:
- Python 3.x
- Home Assistant with MQTT broker set up
- Some spooky sound files (I've got witches, creaky windows, evil laughs, the whole nine yards)

Install the required packages:
``` bash
pip install paho-mqtt python-dotenv pygame
```

Configuration
Create a .env file in the project root with your MQTT credentials:
``` 
username=your_mqtt_username
password=your_mqtt_password
```

Update the MQTT broker IP and topics in main.py if needed (look for host and the topic names).
Throw your spooky sound files (mp3, wav, ogg, etc.) into the sounds folder.
Running It
Just run:
``` bash
python main.py
```
Press Ctrl+C when you're done scaring children.
## Notes
- Yeah, the code's a bit janky - it was a quick Halloween hack
- Sounds are limited to 8 seconds max so people don't have to stand there forever
- Works with pretty much any audio format pygame supports
- The doorbell automation sends a message to topic `h_doorbell_on`

Happy haunting! 👻
