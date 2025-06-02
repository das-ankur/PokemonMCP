# Pokémon MCP Server

The **Pokémon MCP Server** is a modular backend service that provides Pokémon-related metadata, comparisons, and counter recommendations via RESTful APIs. It is designed to be used as standalone microservices or integrated as part of a larger system, and works seamlessly with the `fastmcp` Python client.

---

## 🧩 Core Features

- **counter_pokemon**: Offers recommendations for effective counters against any given Pokémon, based on type matchups and stats analysis.  
- **pokemon_compare**: Compares two Pokémon by analyzing their stats, abilities, and types to provide detailed matchup insights.  
- **pokemon_info**: Provides comprehensive metadata for Pokémon, including stats, moves, types, abilities, evolution chains, and habitats.  
- **pokemon_mcp_server**: The main FastAPI service that integrates all modules and exposes unified API endpoints.

Additional features include:  
- Microservice architecture enabling independent deployment and scalability of each module  
- Utilizes `fastmcp` as the client library for efficient communication and querying  
- Supports querying Pokémon data from PokéAPI with caching for improved performance  
- Easily deployable using Docker and Kubernetes, optimized for local development with Minikube  

---

## 🧰 Tech Stack

| Component        | Technology        |
|------------------|-------------------|
| Language         | Python            |
| Framework        | FastAPI, fastmcp  |
| Data Source      | PokéAPI           |
| Deployment       | Docker, Kubernetes (Minikube) |

---

## ⚙️ Deployment

### Prerequisites

- [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed and running  
- `kubectl` command-line tool  

### Quick Local Deployment

To automatically build and deploy all microservices locally using Kubernetes and Minikube, run:

```bash
bash local_deployment_setup.sh
```
This script will:

- Build Docker images for all core modules
- Deploy each module as a microservice on the Kubernetes cluster managed by Minikube
- Configure networking and services for seamless communication

---

## ⚙️ How It Works

1. **API Requests:** Client applications send REST API requests to the Pokémon MCP Server endpoints. These requests can query Pokémon metadata, request comparisons, or ask for counter recommendations.

2. **Module Handling:** The main server routes requests to the appropriate microservice module (`pokemon_info`, `pokemon_compare`, or `counter_pokemon`).

3. **Data Fetching and Processing:** Each module interacts with cached data from PokéAPI or performs computations such as comparison logic or counter analysis based on Pokémon types, stats, and moves.

4. **Response Generation:** The modules generate structured JSON responses with relevant Pokémon information, matchup analysis, or counter suggestions.

5. **Client Consumption:** The API responses are consumed by client apps or other services, enabling rich Pokémon data interactions.
