from fastapi import FastAPI,HTTPException,Request,WebSocket
import asyncio
import json 
import requests
import connection
from fastapi.responses import StreamingResponse
from typing import Iterator

app = connection.app
async def fetch_and_save_data(url, filename):
    while True:
        app.state.data_list = {}
        try:
            response = requests.get(url)
            response.raise_for_status()  
            with open(filename, "wb") as f:
                f.write(response.content)
                print(f"Data downloaded and saved as '{filename}'")
            try:
                with open(filename, "r") as file:
                    data = file.read()
                    if data.strip():
                        app.state.data_list = json.loads(data)
                    else:
                        continue
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {str(e)}")
                app.state.data_list = {}  
            
        except requests.RequestException as e:
            print(f"Error during data fetch: {str(e)}")
        await asyncio.sleep(2)

async def fetch_and_save_data_next(url, filename):
    while True:
        app.state.data_list_next = {}
        try:
            response = requests.get(url)
            response.raise_for_status()  
            with open(filename, "wb") as f:
                f.write(response.content)
                print(f"Data downloaded and saved as '{filename}'")
            try:
                with open(filename, "r") as file:
                    data = file.read()
                    if data.strip():
                        app.state.data_list_next = json.loads(data)
                    else:
                        #app.state.data_list = {}  # Empty data
                        continue
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {str(e)}")
                app.state.data_list_next = {}  
            
        except requests.RequestException as e:
            print(f"Error during data fetch: {str(e)}")
        await asyncio.sleep(2)

async def fetch_and_save_data_far(url, filename):
    while True:
        app.state.data_list_far = {}
        try:
            response = requests.get(url)
            response.raise_for_status()  
            with open(filename, "wb") as f:
                f.write(response.content)
                print(f"Data downloaded and saved as '{filename}'")
            try:
                with open(filename, "r") as file:
                    data = file.read()
                    if data.strip():
                        app.state.data_list_far = json.loads(data)
                    else:
                        #app.state.data_list = {}  # Empty data
                        continue
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {str(e)}")
                app.state.data_list_far = {}  
            
        except requests.RequestException as e:
            print(f"Error during data fetch: {str(e)}")
        await asyncio.sleep(2)

app.state.oi_pcr_avg = {}
app.state.x_data = []
app.state.y_data = []

async def generate_chart_data() -> Iterator[str]:

    with open("oi_pcr_avg_data.json", "r") as file:
        data = json.load(file)

    app.state.oi_pcr_avg = data
    for item in app.state.oi_pcr_avg:
        json_data = json.dumps(item)
        #print(json_data)
        yield f"data:{json_data}\n\n"

@app.get("/chart-data")
async def chart_data(request: Request) -> StreamingResponse:
    app.state.oi_pcr_avg = {}
    response = StreamingResponse(generate_chart_data(), media_type="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response