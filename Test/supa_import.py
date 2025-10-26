import json
from supabase import create_client, Client
from pathlib import Path


# Initialize the Supabase client with your URL and anon key
# You must use the ANON key, not the SERVICE_ROLE_KEY for client-side authentication
url: str = "https://nmnyrrbwjbblwkjlylqc.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5tbnlycmJ3amJibHdramx5bHFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyOTIzMTcsImV4cCI6MjA3NTg2ODMxN30.D9KAYBZJ1FqRmhGPsglxXXKNXiVAvZzJz0ggwCDfA18"
supabase: Client = create_client(url, key)

def sign_in(email, password):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.user and response.session:
            print("User logged in successfully:", response.user.email)
            print("Session created:", response.session.access_token)
            return response.session
        else:
            print("Login failed. Check your email and password.")
    except Exception as e:
        print(f"Error during sign in: {e}")
    return None

email = "wilsonpkyle@gmail.com"
password = "nq741963"

sign_in(email, password)

def loadData(filename: str | None = None):
    here = Path(__file__).resolve().parent
    path = here / (filename or "data.json")   # default: data.json next to Builder.py
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
    
json_data = loadData()

def normalize(json_data):
    for tree in json_data["trees"]:
        tree_name = tree["name"]
        for talent in tree["talents"]:
            x, y = talent["position"]
            
            response = (
                supabase.table("talents")
                .insert({
                    "tree": tree_name,
                    "name": talent['name'],
                    "description": talent['description'],
                    "x_pos": x,
                    "y_pos": y,
                    "connections": talent['connections'],
                    "old_id": talent['id']
                })
                .execute())

normalize(json_data)