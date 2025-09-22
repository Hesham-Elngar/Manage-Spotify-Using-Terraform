# catch_redirect.py
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os
import webbrowser

# Load environment variables from .env file
load_dotenv()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the incoming request
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Check if the authorization code is in the query parameters
        if 'code' in query_params:
            code = query_params['code'][0]
            print(f"\n🎉 SUCCESS! Authorization Code: {code}")
            
            # Send response to browser
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response_html = """
            <html><body>
            <h1>Authentication Successful!</h1>
            <p>You can close this tab and return to your terminal.</p>
            </body></html>
            """
            self.wfile.write(response_html.encode())
            
            # Now get the access token using the code
            self.get_access_token(code)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Missing authorization code')

    def get_access_token(self, code):
        """Exchange the authorization code for an access token"""
        import requests
        import base64
        
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

        
        # Prepare the request
        token_url = "https://accounts.spotify.com/api/token"
        redirect_uri = os.getenv("SPOTIFY_Redirect_URI")
        
        auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri
        }
        
        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Make the request
        response = requests.post(token_url, data=data, headers=headers)
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['access_token']
            print(f"\n✅ ACCESS TOKEN: {access_token}")
            print("\nCopy this token into your terraform.tfvars file:")
            print(f"spotify_access_token = \"{access_token}\"")
        else:
            print(f"❌ Error getting access token: {response.text}")

def run_server(port=27228):
    server = HTTPServer(('localhost', port), RequestHandler)
    print(f"🚀 Local server running on http://localhost:{port}")
    print("Waiting for Spotify redirect...")
    server.handle_request()

if __name__ == '__main__':
    run_server()  # This line was missing - it needs to be indented and added