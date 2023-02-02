import requests

# Converts money from one currency to another
class cur_conversion():
    def get_czk_rom_usd(value: str):
        money_response = requests.get(f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/usd/czk.json")
        data = money_response.json()
        
        czk = data["czk"]
        czk_return = float(czk) * float(value)
        return czk_return

    
    def get_usd_rom_czk(value: str):
        money_response = requests.get(f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/czk/usd.json")
        data = money_response.json()
        
        usd = data["usd"]
        usd_return = float(usd) * float(value)
        return usd_return
