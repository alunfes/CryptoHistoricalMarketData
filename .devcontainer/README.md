# Dev Container Configuration

This directory contains the VS Code Dev Container configuration for the CryptoHistoricalMarketData project.

## Files

- `devcontainer.json` - Main configuration file for VS Code Dev Containers

## Usage

1. Open this repository in VS Code
2. Install the "Dev Containers" extension (ms-vscode-remote.remote-containers)
3. Click "Reopen in Container" when prompted, or use Command Palette: "Dev Containers: Reopen in Container"

The container will be built using the root `docker-compose.yml` and will connect to the `crypto-data-fetcher` service.

## Working Directory

The container's working directory is set to `/app`, where the application code is located.

## Post-Create Command

After the container is created, it will run `python3 --version` to verify the Python installation.
