import numpy as np
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os
import pinecone
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class QuestionController:
    def __init__(self):
        # Initialize Pinecone using the new API
        self.api_key = os.getenv('PINECONE_API_KEY')
        self.index_name = os.getenv('PINECONE_INDEX_NAME')
        self.environment = os.getenv('PINECONE_ENVIRONMENT')
        self.host = os.getenv('PINECONE_HOST')
        self.region = os.getenv('PINECONE_REGION')

        # Correct Pinecone initialization (no PineconeGRPC)
        pinecone = Pinecone(api_key=self.api_key,
                            environment=self.region)

        # Connect to the index
        self.index = pinecone.Index(self.index_name, host="https://vn-news-l3hau0c.svc.aped-4627-b74a.pinecone.io")

    def query_by_vector(self, input_vector, top_k=100, filter=None):
        result = self.index.query(
            vector=input_vector,
            top_k=top_k,
            include_metadata=True,
            filter=filter
        )
        return result['matches']

