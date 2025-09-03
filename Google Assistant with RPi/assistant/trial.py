from google_auth_oauthlib.flow import InstalledAppFlow

# Define the OAuth scope and client secrets path
scope = ['https://www.googleapis.com/auth/assistant-sdk-prototype']
flow = InstalledAppFlow.from_client_secrets_file(
    '/home/khushwant/Desktop/rpi/client_secret_270922874153-jo07dgak4rcrko7vdfc90q8is4lpim0e.apps.googleusercontent.com.json', scopes=scope
)

# Use the headless authorization flow (no local server)
# Start the authorization flow without needing a local web server
auth_url, _ = flow.authorization_url(prompt='consent')

# Print the URL for manual authorization
print("Please go to this URL to authorize this application:")
print(auth_url)

# Ask for the authorization code manually
code = input("Enter the authorization code here: ")

# Complete the flow using the authorization code
flow.fetch_token(code=code)

# Save the credentials
creds = flow.credentials
with open('/home/khushwant/Desktop/rpi/credentials.json', 'w') as token:
    token.write(creds.to_json())

print("Authentication successful and credentials saved.")
