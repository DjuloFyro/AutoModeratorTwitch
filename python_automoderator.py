import requests
import socket
import unicodedata
import sys

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
    nickname = 'justinfan123' # Anonymous Twitch username
    token = get_oauth_token(client_id, client_secret)

    # Connect to the Twitch IRC server
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, port))

    # Send authentication credentials
    irc.send(f'PASS {token}\n'.encode())
    irc.send(f'NICK {nickname}\n'.encode())
    irc.send(f'JOIN #{channel_name}\n'.encode())

    count = 0 
    # Start receiving Twitch chat messages
    while True:
        
        count += 1
        if count == 100: 
            break

        data = irc.recv(2048).decode().strip()
        if data.startswith('PING'):
            irc.send('PONG :tmi.twitch.tv\n'.encode())
        elif len(data) > 0:
            # Parse the IRC message and extract the chat message
            parsed_message = parse_chat_message(data)

            if parsed_message is not None:
                channel = parsed_message['channel']
                username = parsed_message['username']
                message = parsed_message['message']

                # Normalize the username and message to handle special characters and emojis
                normalized_username = unicodedata.normalize('NFKD', username)
                normalized_message = unicodedata.normalize('NFKD', message)

                # Print the channel name, username, and message with UTF-8 encoding
                output = f'[#{channel}] {normalized_username}: {normalized_message}\n'
                sys.stdout.buffer.write(output.encode('utf-8'))
                sys.stdout.buffer.write(b'\n')
                sys.stdout.flush()

    # Close the connection
    irc.close()

def parse_chat_message(raw_message):
    parts = raw_message.split(':', 2)
    if len(parts) >= 3:
        prefix = parts[1].strip()
        channel = ''
        username = ''
        message = ''

        # Extract channel name, username, and message based on different prefix formats
        if 'PRIVMSG' in prefix:
            channel = prefix.split('#', 1)[1].split(' ', 1)[0].strip()
            username = prefix.split('!', 1)[0].strip()
            message = parts[2].strip()
        elif 'WHISPER' in prefix:
            username = prefix.split('!', 1)[0].strip()
            message = parts[2].strip()
        elif 'USERNOTICE' in prefix:
            channel = prefix.split('#', 1)[1].split(' ', 1)[0].strip()
            message = parts[2].strip()

        return {
            'channel': channel,
            'username': username,
            'message': message
        }

    return None


# Example usage
retrieve_twitch_chat(channel)
