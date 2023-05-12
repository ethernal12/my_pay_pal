import os

from dotenv import load_dotenv

load_dotenv()

STRIPE_API_KEY = os.environ['STRIPE_API_KEY']
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']