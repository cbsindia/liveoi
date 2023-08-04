import connection
import fetch 
import asyncio
import os

app = connection.app 

@app.on_event("startup")
async def startup_event():
    #timezone set
    os.environ['TZ'] = 'Asia/Calcutta'

    url = "https://groww.in/v1/api/option_chain_service/v1/option_chain/nifty?expiry=2023-08-10"  
    url_next = "https://groww.in/v1/api/option_chain_service/v1/option_chain/nifty?expiry=2023-08-17"
    url_far = "https://groww.in/v1/api/option_chain_service/v1/option_chain/nifty?expiry=2023-08-24"
    filename = "dw_data.json"  
    filename_next = "dw_data_next.json"
    filename_far = "dw_data_far.json"
    asyncio.create_task(fetch.fetch_and_save_data(url, filename))
    asyncio.create_task(fetch.fetch_and_save_data_next(url_next, filename_next))
    asyncio.create_task(fetch.fetch_and_save_data_far(url_far, filename_far))

