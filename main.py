from database import get_connection
from ai_model import add_prediction_with_ai_model

from fastapi import FastAPI, Query, HTTPException
import psycopg2
import psycopg2.extras
import logging
import re

app = FastAPI(
    title="Freedom Travel API",
    description="API для поиска авиарейсов с предсказаниями",
    version="1.0"
)

def validate_query_format(query: str) -> bool:
    pattern = r"^[A-Z]{3}-[A-Z]{3}\d{8}\d{4}[A-Z]$"
    return bool(re.match(pattern, query))

@app.get("/search")
def search_flights(
    query: str = Query(
        ...,  # Обязательный параметр
        regex=r"^[A-Z]{3}-[A-Z]{3}\d{8}\d{4}[A-Z]$",
        description="Формат: AKX-ALA202401211000E"
    )
):
    try:
        if not validate_query_format(query):
            raise HTTPException(
                status_code=400, 
                detail="Invalid query format. Query must be in format AKX-ALA202401211000E"
            )

        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM freedom_travel.air_offers WHERE search_query = %s;", (query,))
        trips = cur.fetchall()
        cur.close()
        conn.close()
        trips = add_prediction_with_ai_model(trips, query)
        
        if not trips:
            return {"results": [], "length": 0, "message": "No flights found for the given query"}
            
        return {"results": trips, "length": len(trips)}
    except psycopg2.Error as db_err:
        logging.error(f"Database error: {str(db_err)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
