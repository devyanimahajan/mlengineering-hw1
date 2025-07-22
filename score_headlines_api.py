# Author: Devi Mahajan
# Date: 22.7.25
# Port to use: 8012

#You have already deployed the headline sentiment analysis model as a batch job. 
#Your task now is to deploy it as a web service so clients can make real-time requests.

#Note: the environment needed for this differs from that of score_headlines.py
#Use apienv.yml 

# IMPORTS
import logging
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import joblib
import uvicorn

# SETUP
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
app = FastAPI()

# PATHS
CLASSIFIER_PATH = "./svm.joblib"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# LOAD
try:
    classifier = joblib.load(CLASSIFIER_PATH)
    encoder = SentenceTransformer(EMBEDDING_MODEL_NAME)
    log.info("Model and embedding loaded successfully.")
except Exception as e:
    log.error(f"Startup failure: could not load model or encoder. {e}")
    raise RuntimeError(f"Startup failed: {e}") from e

class HeadlinePayload(BaseModel):
    #Expected input format: list of headlines
    headlines: List[str]

# LOGS
@app.get("/healthcheck")
def healthcheck():
    #Basic GET endpoint to verify the API is up
    log.info("Healthcheck ping received.")
    return {"status": "ok"}

@app.post("/analyze")
def analyze_headlines(payload: HeadlinePayload):
    #Score list of headlines using encoder + SVM model
    log.info("Received headline scoring request.")

    if not payload.headlines:
        log.warning("Empty headline list received.")
        raise HTTPException(status_code=400, detail="Headline list is empty.")

    try:
        vectors = encoder.encode(payload.headlines)
        predictions = classifier.predict(vectors)
        log.info("Successfully scored headlines.")
        return {"predictions": predictions.tolist()}
    except Exception as e:
        log.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Model failed to make predictions. {e}") from e


# RUN
if __name__ == "__main__":
    uvicorn.run("score_headlines_api:app", host="0.0.0.0", port=8007, reload=True)