import numpy as np
import voyageai
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
vo = voyageai.Client()
client = Anthropic()

def urun_fiyati(urun: str) -> int:
    return {"Airpods": 5000, "iPhone": 60000}.get(urun, 0)

def kdv_hesapla(fiyat: int) -> int:
    return int(fiyat * 1.20)   # %20 KDV
