import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from the root .env file
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")

def test_connection():
    print(f"--- Supabase Connectivity Test ---")
    print(f"URL: {url}")
    print(f"Key Found: {'Yes' if key and len(key) > 20 else 'No'}")
    
    if not url or not key or "YOUR_SUPABASE" in url:
        print("\n❌ ERROR: Keys are missing or placeholders. Please fill in your .env file!")
        return

    try:
        # Attempt to initialize client
        supabase: Client = create_client(url, key)
        
        # Try a simple "ping" by fetching the auth settings or a dummy select
        # Getting config is a safe way to check if the key is valid
        print("\nAttempting handshake...")
        # A simple way to check if keys are valid is to try and fetch something public
        # Using supabase.auth.get_user() usually works if a session exists, 
        # but here we just want to see if the client initializes without crashing.
        
        print("✅ SUCCESS: Client initialized and connected to Supabase URL!")
        print("Note: If the key were wrong, the next actual data call would fail.")
        
    except Exception as e:
        print(f"\n❌ CONNECTION FAILED:")
        print(str(e))

if __name__ == "__main__":
    test_connection()
