from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

class Pipeline(BaseModel):
    nodes: List[int]  # Assuming node IDs are integers
    edges: List[tuple]  # Assuming edges are represented as tuples of (start_node, end_node)

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
async def parse_pipeline(pipeline: Pipeline):
    nodes = pipeline.nodes
    edges = pipeline.edges

    num_nodes = len(nodes)
    num_edges = len(edges)
    
    # Check if the pipeline forms a Directed Acyclic Graph (DAG)
    is_dag = check_if_dag(nodes, edges)
    
    return {'num_nodes': num_nodes, 'num_edges': num_edges, 'is_dag': is_dag}

def check_if_dag(nodes, edges):
    from collections import defaultdict, deque

    graph = defaultdict(list)
    in_degree = {node: 0 for node in nodes}

    for start, end in edges:
        graph[start].append(end)
        in_degree[end] += 1

    # Topological sort (Kahn's Algorithm)
    queue = deque([node for node in nodes if in_degree[node] == 0])
    visited_count = 0

    while queue:
        node = queue.popleft()
        visited_count += 1
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return visited_count == len(nodes)
