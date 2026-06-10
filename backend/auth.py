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

def get_user_from_token(token: str):
    res = supabase.auth.get_user(token)
    return res.user

def save_chat(token: str, question: str, answer: str, route: str):
    user = get_user_from_token(token)
    supabase.postgrest.auth(token)
    supabase.table("chats").insert({
        "user_id": user.id,
        "question": question,
        "answer": answer,
        "route": route,
    }).execute()
    return user.id