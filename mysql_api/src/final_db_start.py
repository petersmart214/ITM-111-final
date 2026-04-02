import sys

import uvicorn

def startup():
    print(sys.argv)
    if(len(sys.argv) < 3):
        print("Please input your MySql Database user and password.")
        sys.exit()
        
    if(len(sys.argv) > 3):
        print("Too many arguments to run!")
        sys.exit()
        
        
    from fastapi_queries import app

    app.state.base_user = sys.argv[1]
    app.state.base_password = sys.argv[2]


    uvicorn.run("fastapi_queries:app", host="127.0.0.1", port=8000)
    
if __name__ == "__main__":
     startup()