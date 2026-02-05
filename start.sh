#!/bin/bash

# Start the API server in the background
python serve/api_server.py &

# Wait for the API server to start (simple sleep or check)
echo "Waiting for API server to start..."
sleep 5

# Start the Streamlit UI (listening on the port HF expects: 7860)
echo "Starting Streamlit UI found at chat_ui.py..."
streamlit run chat_ui.py --server.port 7860 --server.address 0.0.0.0
