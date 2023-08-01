from fastapi import Request, HTTPException
from datetime import datetime
import start_app
import connection
import check_json
from pydantic import BaseModel 
import json 

app = connection.app

app.state.data_list = {}
app.state.data_list_next = {}
app.state.data_list_far = {}

start_app.startup_event()

@app.get("/")
async def get_table(request: Request):
    return connection.templates.TemplateResponse("oi_table.html", {"request": request})

oi_Data = []
oi_Data_next = []
oi_Data_far = []
@app.get("/api/table-data")
async def get_table_data():
    curr_time = datetime.now().strftime("%d-%B-%Y %H:%M:%S")
    oi_Data.clear()
    oi_Data_next.clear()
    oi_Data_far.clear()
    try:
        option_chains = app.state.data_list.get("optionChains", [])
        option_chains_next = app.state.data_list_next.get("optionChains", [])
        option_chains_far = app.state.data_list_far.get("optionChains", [])
        for option_chain in option_chains:
            ce_open_interest = option_chain["callOption"]["openInterest"]
            pe_open_interest = option_chain["putOption"]["openInterest"]
            ce_volume = option_chain["callOption"]["volume"]
            pe_volume = option_chain["putOption"]["volume"]
            oi_Data.append({"strikePrice": option_chain["strikePrice"], "ce_openInterest": ce_open_interest, "pe_openInterest": pe_open_interest, "ce_volume": ce_volume,"pe_volume": pe_volume})

        for option_chain_next in option_chains_next:
            ce_open_interest_next = option_chain_next["callOption"]["openInterest"]
            pe_open_interest_next = option_chain_next["putOption"]["openInterest"]
            ce_volume_next = option_chain_next["callOption"]["volume"]
            pe_volume_next = option_chain_next["putOption"]["volume"]
            oi_Data_next.append({"strikePrice": option_chain_next["strikePrice"], "ce_openInterest": ce_open_interest_next, "pe_openInterest": pe_open_interest_next, "ce_volume": ce_volume_next,"pe_volume": pe_volume_next})

        for option_chain_far in option_chains_far:
            ce_open_interest_far = option_chain_far["callOption"]["openInterest"]
            pe_open_interest_far = option_chain_far["putOption"]["openInterest"]
            ce_volume_far = option_chain_far["callOption"]["volume"]
            pe_volume_far = option_chain_far["putOption"]["volume"]
            oi_Data_far.append({"strikePrice": option_chain_far["strikePrice"], "ce_openInterest": ce_open_interest_far, "pe_openInterest": pe_open_interest_far, "ce_volume": ce_volume_far,"pe_volume": pe_volume_far})
    except KeyError as e:
        print(f"Error accessing optionChains: {str(e)}")
    return {"oi_data": oi_Data,"oi_data_next":oi_Data_next,"oi_data_far":oi_Data_far, "curr_time": curr_time}

oi_pcr_avg_data = []

class OIPCRAvgData(BaseModel):
    curr_time: str
    oi_pcr_avg: float

@app.post("/api/save-oi-pcr-avg")
async def save_oi_pcr_avg(data: OIPCRAvgData):

    input_datetime_str = data.curr_time
    input_format = "%d-%B-%Y %H:%M:%S"
    dt_obj = datetime.strptime(input_datetime_str, input_format)
    hours = dt_obj.hour
    minutes = dt_obj.minute
    seconds = dt_obj.second
    output_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    data.curr_time = output_time_str

    try:
        oi_pcr_avg_data.append({"curr_time": data.curr_time, "oi_pcr_avg": data.oi_pcr_avg})
        with open("oi_pcr_avg_data.json", 'w') as file:
            json.dump(oi_pcr_avg_data, file)
            
        return {print("oi_PCR_avg and current time values saved successfully.")}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error saving oi_PCR_avg and current time values.")
