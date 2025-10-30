#Diren V1 Halloween Doorbell MQTT Doorbell Jumpscare
#Made in an hour, dont judge code.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# from paho import mqtt
import paho.mqtt.client as mqtt
import random
import sys
from dotenv import load_dotenv
import os
from pathlib import Path
import pygame
import time


def play_random_sound_limited(sounds_folder, max_duration=8):

    try:
        # Get all sound files from the folder
        sound_files = []
        sounds_path = Path(sounds_folder)

        if not sounds_path.exists():
            print(f"Sounds folder '{sounds_folder}' not found!")
            return
        audio_extensions = {'.mp3', '.wav', '.ogg', '.flac', '.m4a', '.wma', '.aac'}

        for file in sounds_path.iterdir():
            if file.is_file() and file.suffix.lower() in audio_extensions:
                sound_files.append(file)

        if not sound_files:
            print(f"No sound files found in '{sounds_folder}'")
            return

        # Select a random sound file anbd play
        selected_sound = random.choice(sound_files)
        print(f"Playing: {selected_sound.name}")
        pygame.mixer.init()
        pygame.mixer.music.load(str(selected_sound))
        pygame.mixer.music.play()

        # Wait for the sound to finish or max_duration.
        start_time = time.time()
        while pygame.mixer.music.get_busy():
            if time.time() - start_time >= max_duration:
                pygame.mixer.music.stop()
                print(f"Sound stopped after {max_duration} seconds (time limit)")
                break
            time.sleep(0.1)
        else:
            print("Sound finished playing")

        pygame.mixer.quit()

    except ImportError:
        print("pygame not installed")
    except Exception as e:
        print(f"Error playing sound: {e}")


def create_mqtt_client(host, port, username=None, password=None):

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    CONNACK_ACCEPTED = 0 # https://commandmasters.com/commands/mosquitto_sub-common/ <- No idea lol
    
    # Set username and password if provided
    if username and password:
        client.username_pw_set(username, password)
    
    if client.connect(host, port, 60) != CONNACK_ACCEPTED:
        print("Connection failed")
        sys.exit(1)
        #return None
    else:
        print("Connected")
        return client


def publish_message(host, port, topic, message, username=None, password=None):

    client = create_mqtt_client(host, port, username, password)
    
    if client is None:
        return False
    
    try:
        # Start the network loop to process callbacks and maintain connection
        client.loop_start()
        
        # Give it a moment to fully establish the connection
        time.sleep(0.5)
        
        # Publish with QoS 1 to ensure delivery once
        result = client.publish(topic, message, qos=1)
        
        # Wait for publish to complete
        result.wait_for_publish()
        
        print(f"Message published to {topic}: {message}")
        
        return True
    finally:
        client.loop_stop()
        client.disconnect()


def on_message(client, userdata, msg):

    print(f"Received message on {msg.topic}: {msg.payload.decode()}")
    # TODO: Add your message handling logic here
    print("Doorbell Press received")
    print("Playing Sound")


    # Doorbell Sounds. Spooky :>
    play_random_sound_limited("sounds", max_duration=8)


    # Publish to h_doorbell_off
    time.sleep(8)
    publish_message(host, port, topic_off, message, username, password)


def listen_to_topic(host, port, topic, username=None, password=None):

    client = create_mqtt_client(host, port, username, password)
    
    if client is None:
        return
    
    # run on message recieve
    client.on_message = on_message
    
    # Start the network loop
    client.loop_start()
    
    # Subscribe to the topic
    client.subscribe(topic, qos=1)
    print(f"Subscribed to {topic}, listening for messages...")
    
    try:
        # Keep listening (press Ctrl+C to stop)
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping listener...")
    finally:
        client.loop_stop()
        client.disconnect()


# Loops Press Ctrl+C to stop
if __name__ == '__main__':
    topic_on = "h_doorbell_on"
    topic_off = "h_doorbell_off"
    message = "(Null)"
    host = "192.168.8.165"
    port = 1883

    # Load environment variables from .env file
    load_dotenv()

    # Get credentials from .env file
    username = os.getenv('username')
    password = os.getenv('password')


    
    # Uncomment the line below to listen to h_doorbell_on instead
    listen_to_topic(host, port, topic_on, username, password)

