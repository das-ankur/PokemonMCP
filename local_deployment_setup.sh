#!/bin/bash

set -e

# === Config ===
NAMESPACE="pokemon"
SERVICE_NAME="pokemon-mcp-service"
DNS_NAME="pokemon-mcp-server"

# === Folders and Docker tags ===
declare -A SERVICES=(
  [counter_pokemon]="counter-pokemon-app:latest"
  [pokemon_compare]="pokemon-compare-app:latest"
  [pokemon_info]="pokemon-info-app:latest"
  [pokemon_mcp_server]="pokemon-mcp-app:latest"
)

echo "🔧 Building Docker images and applying deployments..."
for folder in "${!SERVICES[@]}"; do
  echo "📦 Processing $folder..."
  cd "$folder" || { echo "❌ Folder $folder not found"; exit 1; }

  echo "🛠️ Building image ${SERVICES[$folder]}..."
  docker build -t "${SERVICES[$folder]}" -f meta/Dockerfile .

  echo "🚀 Applying deployment from meta/deployments.yaml..."
  kubectl apply -f meta/deployments.yaml

  cd - > /dev/null
done

# === Start Minikube tunnel if not already running ===
if ! pgrep -f "minikube tunnel" > /dev/null; then
  echo "🌐 Starting minikube tunnel in background..."
  nohup minikube tunnel > /dev/null 2>&1 &
  sleep 5
else
  echo "✅ Minikube tunnel is already running."
fi

# === Wait for external IP assignment ===
echo "⏳ Waiting for external IP to be assigned to $SERVICE_NAME..."
for i in {1..20}; do
  EXTERNAL_IP=$(kubectl get svc "$SERVICE_NAME" -n "$NAMESPACE" -o jsonpath="{.status.loadBalancer.ingress[0].ip}" 2>/dev/null || true)
  if [[ -n "$EXTERNAL_IP" ]]; then
    echo "🌍 External IP: $EXTERNAL_IP"
    break
  fi
  sleep 2
done

if [[ -z "$EXTERNAL_IP" ]]; then
  echo "❌ Failed to retrieve external IP for $SERVICE_NAME."
  exit 1
fi

# === Update /etc/hosts ===
HOSTS_LINE="$EXTERNAL_IP $DNS_NAME"
if grep -q "$DNS_NAME" /etc/hosts; then
  echo "🔁 Updating existing /etc/hosts entry..."
  sudo sed -i.bak "/$DNS_NAME/d" /etc/hosts
else
  echo "➕ Adding new /etc/hosts entry..."
fi
echo "$HOSTS_LINE" | sudo tee -a /etc/hosts > /dev/null

echo "✅ Setup complete. You can access the service at: http://$DNS_NAME"
