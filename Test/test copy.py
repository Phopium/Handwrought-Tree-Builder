import pandas as pd
from supabase import create_client, Client
import json

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


response = (supabase.table("talents")
    .select("*")
    .execute()
)
talents = response.data

response = (supabase.table("trees")
    .select("*")
    .execute()
)
trees = response.data

for talent in talents:
    for tree in trees:
        if tree["name"] == talent["tree"]:
            response = (
                supabase.table("talents")
                .update({"tree_id": tree["id"]})
                .eq("id", talent["id"])
                .execute()
            )