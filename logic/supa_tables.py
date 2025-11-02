from supabase import create_client, Client

url: str = "https://nmnyrrbwjbblwkjlylqc.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5tbnlycmJ3amJibHdramx5bHFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyOTIzMTcsImV4cCI6MjA3NTg2ODMxN30.D9KAYBZJ1FqRmhGPsglxXXKNXiVAvZzJz0ggwCDfA18"
supabase: Client = create_client(url, key)

def sign_in():
    email = "wilsonpkyle@gmail.com"
    password = "nq741963"
    if not email:
        email = input("Email:")
        password = input("Password:")
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.user and response.session:
            print("User logged in successfully:", response.user.email)
            print("Session created:")
            return response.session
        else:
            print("Login failed. Check your email and password.")
    except Exception as e:
        print(f"Error during sign in: {e}")
    return None

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

def atomic_pos_swap(from_talent_id, to_talent_id):
    response = supabase.rpc(
        'swap_talent_pos_ids', {
            'id1': from_talent_id,
            'id2': to_talent_id
        }
    ).execute()


sign_in()
