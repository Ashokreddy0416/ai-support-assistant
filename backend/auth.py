import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

def sign_up(email: str, password: str):
    res = supabase.auth.sign_up({"email": email, "password": password})
    return res.user

def log_in(email: str, password: str):
    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
    return res.session.access_token