# smart_proxy.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json
import re

def get_access_token_from_tfvars():
    """Read the access token from terraform.tfvars file"""
    try:
        with open('terraform.tfvars', 'r') as f:
            content = f.read()
        
        # Use regex to find the access token value
        match = re.search(r'spotify_access_token\s*=\s*"([^"]+)"', content)
        if match:
            return match.group(1)
        else:
            raise ValueError("Access token not found in terraform.tfvars")
            
    except FileNotFoundError:
        raise FileNotFoundError("terraform.tfvars file not found")
    except Exception as e:
        raise Exception(f"Error reading terraform.tfvars: {e}")

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request('GET')
    
    def do_POST(self):
        self.handle_request('POST')
    
    def do_PUT(self):
        self.handle_request('PUT')
    
    def do_DELETE(self):
        self.handle_request('DELETE')
    
    def handle_request(self, method):
        try:
            # Read the access token from terraform.tfvars for each request
            access_token = get_access_token_from_tfvars()
            
            # Forward to Spotify API
            response = requests.request(
                method,
                f"https://api.spotify.com/v1{self.path}",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }
            )
            
            self.send_response(response.status_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.content)
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

def run_server():
    # Test that we can read the token first
    try:
        token = get_access_token_from_tfvars()
        print(f"✅ Successfully read access token from terraform.tfvars")
        print(f"🚀 Proxy server running on http://localhost:27228")
        print("Press Ctrl+C to stop the server")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    server = HTTPServer(('localhost', 27228), ProxyHandler)
    server.serve_forever()

if __name__ == '__main__':
    run_server()