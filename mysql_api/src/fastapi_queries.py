import csv
from io import StringIO
import subprocess
import sys

from fastapi import FastAPI
from fastapi.responses import HTMLResponse




app = FastAPI()

@app.get("/test", response_class=HTMLResponse)
async def read_test():
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
        {convert_xsv_into_html(*run_batched_query(app.state.base_user, app.state.base_password, "use ev_charger; select region.region_name, avg(session.total_duration) as `Average Duration`, avg(session.energy_kwh) as `Average Energy Pull` from region right join (charger right join session on charger.charger_id = session.charger_id) on charger.region_id = region.region_id group by region.region_id order by `Average Duration`;"))}
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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

    output_html += f"<div class=col_grid>{"".join(map(lambda i: f"<div class=col_name>{i}</div>", reader.fieldnames))}"

    for row in reader:
        output_html += f"{"".join(map(lambda i: f"<div class=returned_item>{row[i]}</div>", row))}"
    
    output_html += "</div>"
    
    output_html += f"<div class=error_container>{error}</div>"
    
    
    return output_html