import csv
from io import StringIO
import subprocess
import sys

from fastapi import FastAPI
from fastapi.responses import HTMLResponse




app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_test():
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
        No query selected.
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/region", response_class=HTMLResponse)
async def read_test():
    html_content = enclose_xsv_in_html(convert_xsv_into_html(*run_batched_query(app.state.base_user, app.state.base_password, "use ev_charger; select region.region_name, round(avg(session.total_duration), 3) as `Average Duration`, round(avg(session.energy_kwh), 3) as `Average Energy Pull` from region right join (charger right join session on charger.charger_id = session.charger_id) on charger.region_id = region.region_id group by region.region_id order by `Average Duration`;")), 3)
    return HTMLResponse(content=html_content)

@app.get("/types", response_class=HTMLResponse)
async def read_test():
    html_content = enclose_xsv_in_html(convert_xsv_into_html(*run_batched_query(app.state.base_user, app.state.base_password, "use ev_charger; select charger.charger_type, round(avg(session.charge_duration), 3) as `Average Charge Duration`, round(avg(session.total_duration), 3) as `Average Session Duration` from region right join (charger right join session on charger.charger_id = session.charger_id) on charger.region_id = region.region_id group by charger.charger_type order by `Average Charge Duration`;")), 3)
    return HTMLResponse(content=html_content)

def enclose_xsv_in_html(html_to_enclose, columns=1):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    #col_grid {{
        display: grid;
        column-gap: 10px;
        grid-template-columns: repeat({columns}, 1fr);
    }}
  </style>
    </head>
    <body>
        {html_to_enclose}
    </body>
    </html>
    """

def run_batched_query(user, password, query):
    cmd = [
    r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",  # full path
    "-u", user,
    f"-p{password}",
    "--batch", "",
    "-e", query,
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr

def convert_xsv_into_html(xsv, error, delimiter="\t"):
    f = StringIO(xsv)
    
    reader = csv.DictReader(f, delimiter=delimiter)
    
    output_html = ""

    output_html += f"<div id=col_grid>{"".join(map(lambda i: f"<div class=col_name>{i}</div>", reader.fieldnames))}"

    for row in reader:
        output_html += f"{"".join(map(lambda i: f"<div class=returned_item>{row[i]}</div>", row))}"
    
    output_html += "</div>"
    
    output_html += f"<div class=error_container>{error}</div>"
    
    
    return output_html