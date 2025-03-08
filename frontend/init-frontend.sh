#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "Installing dependencies..."
npm install @chakra-ui/icons @chakra-ui/react @emotion/react @emotion/styled framer-motion react react-dom react-query react-router-dom recharts axios

echo "Configuring TypeScript..."
npm install -D typescript @types/react @types/react-dom @vitejs/plugin-react

echo "Setup complete!"