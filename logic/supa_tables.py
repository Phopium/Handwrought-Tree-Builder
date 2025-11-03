from supabase import create_client, Client
from tkinter import messagebox
import configparser
import os
import getpass

url: str = "https://nmnyrrbwjbblwkjlylqc.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5tbnlycmJ3amJibHdramx5bHFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyOTIzMTcsImV4cCI6MjA3NTg2ODMxN30.D9KAYBZJ1FqRmhGPsglxXXKNXiVAvZzJz0ggwCDfA18"
supabase: Client = create_client(url, key)

def sign_in():
    user_email, password = check_credentials()
    try:
        response = supabase.auth.sign_in_with_password({"email": user_email, "password": password})
        if response.user and response.session:
            print("User logged in successfully:", response.user.email)
            print("Supabase session created")
            return response.session
        else:
            print("Login failed. Check your email and password.")
    except Exception as e:
        print(f"Error during sign in: {e}")
    return None

# Supabase credentials
def check_credentials():
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(dir_path, "login_config.ini")
    
    # --- Check if config file exists ---
    if os.path.exists(config_file_path):
        config.read(config_file_path)
        try:
            db_user = config['credentials']['username']
            db_pass = config['credentials']['password']
            print("Credentials loaded from config file.")
        except KeyError:
            print("Config file found, but 'credentials' section missing or incomplete.")
            db_user = None
            db_pass = None
    else:
        # --- Prompt user if file doesn't exist ---
        print("Config file not found. Prompting for credentials...")
        db_user = input("Enter username: ")
        db_pass = getpass.getpass("Enter password: ")
        
        save = input("Save credentials? (y/n): ")
        if save.lower() == "y":
            config["credentials"] = {
                'username': db_user,
                'password': db_pass
            }
            try:
                with open(config_file_path, 'w') as configfile:
                    config.write(configfile)
                print(f"Credentials saved to {config_file_path}")
            except IOError as e:
                print(f"Error creating file: {e}")
                
    return db_user, db_pass


def loadData():
    response = (
        supabase.table("talents")
        .select("*, talent_positions!inner(*)")
        .execute()
    )
    return response.data

def getTrees():
    response = (supabase.table("trees")
        .select("id, name")
        .execute()
    )
    return response.data

def update_db_timestamp():
    updated_timestamp = (
        supabase.table("time_modified")
        .update({"update_target": "1"})
        .eq("table_name", "talents")
        .execute()
    )

def get_timestamp():
    response = (
        supabase.table("time_modified")
        .select("table_name, updated_at")
        .eq("table_name", "talents")
        .execute()
    )
    data = response.data[0]
    timestamp = data["updated_at"]
    return timestamp


def update_database(table, id, column, value):
    response = (
        supabase.table(table)
        .update({column: value})
        .eq("id", id)
        .execute()
    )
    update_db_timestamp()

def atomic_pos_swap(from_talent_id, to_talent_id):
    response = supabase.rpc(
        'swap_talent_pos_ids', {
            'id1': from_talent_id,
            'id2': to_talent_id
        }
    ).execute()
    update_db_timestamp()

def check_if_updated(local_timestamp):
    db_timestamp = get_timestamp()
    if db_timestamp == local_timestamp:
        return False, db_timestamp
    else:
        messagebox.showerror("Warning", "Another concurrent user has updated the database. No changes were made.")
        return True, db_timestamp


sign_in()
