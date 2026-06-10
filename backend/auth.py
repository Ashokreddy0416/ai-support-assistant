import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

_supabase = None

def _get_supabase():
    global _supabase
    if _supabase is None:
        _supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    return _supabase

def sign_up(email: str, password: str):
    res = _get_supabase().auth.sign_up({"email": email, "password": password})
    return res.user

def log_in(email: str, password: str):
    res = _get_supabase().auth.sign_in_with_password({"email": email, "password": password})
    return res.session.access_token

def get_user_from_token(token: str):
    res = _get_supabase().auth.get_user(token)
    return res.user

def save_chat(token: str, question: str, answer: str, route: str):
    sb = _get_supabase()
    user = sb.auth.get_user(token).user
    sb.postgrest.auth(token)
    sb.table("chats").insert({
        "user_id": user.id,
        "question": question,
        "answer": answer,
        "route": route,
    }).execute()
    return user.id

def get_history(token: str):
    sb = _get_supabase()
    sb.auth.get_user(token)
    sb.postgrest.auth(token)
    res = sb.table("chats").select("*").order("created_at", desc=True).limit(20).execute()
    return res.data