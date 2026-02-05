import os
import sys

# Add Graphviz to PATH explicitly
graphviz_path = r"C:\Program Files\Graphviz\bin"
if graphviz_path not in os.environ["PATH"]:
    os.environ["PATH"] += ";" + graphviz_path

from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.programming.framework import Fastapi
from diagrams.programming.language import Python
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Redis # Memory representation

print("Generating diagram...")

with Diagram("Flash-Serve Architecture", show=False, filename="architecture_diagram_v4", direction="TB"):
    
    user = User("User Request")
    
    with Cluster("Flash-Serve Ecosystem"):
        api = Fastapi("API Server\n(FastAPI)")
        
        with Cluster("Inference Engine"):
            scheduler = Python("Scheduler")
            
            with Cluster("Worker"):
                model = Server("Model Executor\n(GPU)")
                memory = Redis("Block Manager\n(PagedAttention)")
            
            # Application Logic
            scheduler >> Edge(label="Batch") >> model
            scheduler >> Edge(label="Alloc/Free") >> memory
            model >> Edge(label="KV Cache") >> memory
        
        # Request Flow
        api >> Edge(label="Prompt") >> scheduler

    user >> Edge(label="HTTP") >> api

print("Success!")
