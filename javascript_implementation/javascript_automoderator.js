import tmi from "tmi.js"
import fetch from "node-fetch";

// Twitch client credentials
const CLIENT_ID = 'CLIENT_ID';
const CLIENT_SECRET = 'CLIENT_SECRET';
const CHANNEL_NAME = 'CHANNEL_NAME';

// Function to obtain the OAuth token using client information
async function getOAuthToken() {
  const response = await fetch('https://id.twitch.tv/oauth2/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      grant_type: 'client_credentials',
    }),
  });
  const data = await response.json();
  return data.access_token;
}

// Function to join Twitch chat and listen to messages
async function joinTwitchChat() {
  const oauthToken = await getOAuthToken();
  
  // Configure the Twitch client
  const client = new tmi.Client({
    connection: {
      secure: true,
      reconnect: true,
    },
    identity: {
      username: 'justinfan123',
      password: `oauth:${oauthToken}`,
    },
    channels: [CHANNEL_NAME],
  });

  // Connect to Twitch chat
  await client.connect().catch(console.error);

  // Listen for chat messages
  client.on('message', (channel, tags, message, self) => {
    if (self) return;

    // Extract relevant information from the tags and message
    const { 'display-name': displayName, 'user-type': userType, 'user-id': userId } = tags;

    // Process the received chat message or perform moderation tasks
    console.log(`[${channel}] ${displayName}: ${message}`);
    // Your message handling logic goes here
  });
}

// Call the function to join Twitch chat
joinTwitchChat();
