# Author: Devi Mahajan
# Date: 22.7.25
# Port to use: 8012

#You have already deployed the headline sentiment analysis model as a batch job. 
#Your task now is to deploy it as a web service so clients can make real-time requests.

# imports here
import logging
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import joblib
import uvicorn

