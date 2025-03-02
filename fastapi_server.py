from fastapi import FastAPI, Request, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
async def proxy_endpoint(request: Request):
    target_url = request.query_params.get("url")
    if not target_url:
        raise HTTPException(status_code=400, detail="URL parameter is missing")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(target_url)
            return JSONResponse(content=response.json(), headers={"Access-Control-Allow-Origin": "*"})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Run the server
if __name__ == "_main_":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)