import requests
import socket

# Twitch credentials
client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
channel = 'CHANNEL_NAME'
oauth_token = ''  # Place your OAuth token here if you have one

# Function to obtain the OAuth token using client information
def get_oauth_token(client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    return data['access_token']

# Retrieve OAuth token if not provided
if not oauth_token:
    oauth_token = get_oauth_token(client_id, client_secret)

# Twitch chat retrieval function
def retrieve_twitch_chat(channel_name):
    # Twitch IRC server and port
    server = 'irc.chat.twitch.tv'
    port = 6667

    # Twitch IRC authentication credentials
    nickname = 'justinfan123'
    token = get_oauth_token(client_id, client_secret)

    # Connect to the Twitch IRC server
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, port))

    # Send authentication credentials
    irc.send(f'PASS {token}\n'.encode())
    irc.send(f'NICK {nickname}\n'.encode())
    irc.send(f'JOIN #{channel_name}\n'.encode())

    # Start receiving Twitch chat messages
    while True:
        data = irc.recv(2048).decode().strip()
        if data.startswith('PING'):
            irc.send('PONG :tmi.twitch.tv\n'.encode())
        elif len(data) > 0:
            print(data)

    # Close the connection
    irc.close()

# Example usage
retrieve_twitch_chat(channel)
