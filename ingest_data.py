"""
ingest_data.py

A simple script to embed the sample dataset and upload it to Pinecone.
Before running this, ensure your .env file is fully populated with:
  OPENAI_API_KEY
  PINECONE_API_KEY
  PINECONE_ENV
  PINECONE_INDEX
"""

import sys
import os

# Ensure the project root directory is on sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.pinecone_client import MOCK_DATABASE, embed_and_upsert


def main():
    print("Starting data ingestion to Pinecone...")

    for doc in MOCK_DATABASE:
        doc_id = doc["id"]
        text = doc["text"]

        print(f"Embedding and upserting document: {doc_id}...")
        try:
            embed_and_upsert(text, doc_id, metadata={"source": "starter_kit_demo"})
            print(f"✅ Successfully upserted {doc_id}")
        except Exception as e:
            print(f"❌ Failed to upsert {doc_id}: {e}")

    print("\nIngestion complete!")


if __name__ == "__main__":
    main()
