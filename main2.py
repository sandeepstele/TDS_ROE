# main2.py
from fastapi import FastAPI, Response, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
import json
import uvicorn

YOUR_EMAIL = "22f2001447@ds.study.iitm.ac.in"

# Load dataset
with open("q-fastapi-llm-query.json") as f:
    data = json.load(f)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/query")
def query(q: str = Query(...), response: Response):
    # 1) Inject X-Email header
    response.headers["X-Email"] = YOUR_EMAIL

    answer: Union[str, int] = "Not Found"
    q_clean = q.strip().rstrip("?")
    q_lower = q_clean.lower()

    try:
        # ————— Total sales of PRODUCT in CITY/STATE —————
        if q_lower.startswith("what is the total sales of") and " in " in q_lower:
            # Extract product and location
            _, rest = q_clean.split("sales of", 1)
            product, loc = rest.split(" in ", 1)
            product = product.strip().lower()
            loc = loc.strip().lower()

            total = sum(
                entry["sales"]
                for entry in data
                if entry["product"].strip().lower() == product
                and (
                    entry.get("city","").strip().lower() == loc
                    or entry.get("state","").strip().lower() == loc
                )
            )
            answer = total

        # ————— How many sales reps are there in STATE —————
        elif q_lower.startswith("how many sales reps are there in") and " in " in q_lower:
            _, region = q_clean.split(" in ", 1)
            region = region.strip().lower()
            reps = {
                entry["rep"].strip().lower()
                for entry in data
                if entry.get("state","").strip().lower() == region
            }
            answer = len(reps)

        # ————— Average sales for PRODUCT in CITY/STATE —————
        elif q_lower.startswith("what is the average sales for") and " in " in q_lower:
            _, rest = q_clean.split("sales for", 1)
            product, loc = rest.split(" in ", 1)
            product = product.strip().lower()
            loc = loc.strip().lower()

            vals = [
                entry["sales"]
                for entry in data
                if entry["product"].strip().lower() == product
                and (
                    entry.get("city","").strip().lower() == loc
                    or entry.get("state","").strip().lower() == loc
                )
            ]
            answer = round(sum(vals) / len(vals), 2) if vals else 0

        # ————— On what date did REP make the highest sale in CITY —————
        elif q_lower.startswith("on what date did") and " make the highest sale in " in q_lower:
            # “On what date did Jean Greenfelder make the highest sale in Cupertino”
            # split out rep and city
            after_did = q_clean.split("did", 1)[1]
            rep_full, after_rep = after_did.split(" make the highest sale in ", 1)
            rep = rep_full.strip().lower()
            city = after_rep.strip().lower()

            filtered = [
                entry
                for entry in data
                if entry["rep"].strip().lower() == rep
                and entry.get("city","").strip().lower() == city
            ]
            if not filtered:
                raise HTTPException(404, "No matching records")
            best = max(filtered, key=lambda e: e["sales"])
            answer = best["date"]

        else:
            # unrecognized pattern
            raise HTTPException(400, f"Question not recognized: '{q}'")

    except HTTPException:
        # re-raise FastAPI HTTP errors
        raise
    except Exception as e:
        # fallback
        answer = f"Error: {e}"

    return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run("main2:app", host="0.0.0.0", port=8003, reload=True)
