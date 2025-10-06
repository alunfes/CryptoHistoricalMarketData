> **日本語版のREADMEは[こちら](README_ja.md)をご覧ください。**
> **For Japanese documentation, please see [README_ja.md](README_ja.md).**

Overview

CryptoHistoricalMarketData is a Python-based application designed to fetch, process, and store historical cryptocurrency market data. The project supports handling OHLC (Open, High, Low, Close) and ticker data, offering modular functionality for data downloading, transformation, and storage.

Features

Data Downloading: Fetch historical cryptocurrency market data using API endpoints.

Data Transformation: Convert raw data into structured formats such as OHLC and Ticker data.

Data Storage: Save processed data to specified formats or databases.

Docker Support: Easy deployment with Docker and Docker Compose.

Directory Structure

CryptoHistoricalMarketData-main/
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── app/
│   ├── DataDownLoader.py
│   ├── DataWriter.py
│   ├── OHLCData.py
│   ├── OhlcConverter.py
│   ├── TickerConverter.py
│   ├── TickerData.py
│   ├── main.py
│   ├── test.py
│   └── requirements.txt
├── ignore/
│   ├── apiendpoints.yaml
│   └── params.yaml
├── Dockerfile
├── docker-compose.yml
└── .dockerignore

Prerequisites

**For Local Setup:**
- Python 3.8 or later
- pip (Python package manager)

**For Docker Setup:**
- Docker Engine 20.10 or later
- Docker Compose V2 (or docker-compose 1.29+)

Installation

Local Setup

Clone the repository:

git clone https://github.com/your-repo/CryptoHistoricalMarketData.git
cd CryptoHistoricalMarketData

Install dependencies:

pip install -r requirements.txt

Run the application:

python app/main.py

Docker Setup

#### Prerequisites

- Docker Engine 20.10 or later
- Docker Compose V2 (or docker-compose 1.29+)

#### Quick Start with Docker

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alunfes/CryptoHistoricalMarketData.git
   cd CryptoHistoricalMarketData
   ```

2. **Configure your settings:**
   
   Edit the configuration files in the `ignore/` directory:
   - `ignore/params.yaml` - Set exchanges, intervals, and download parameters
   - `ignore/apiendpoints.yaml` - API endpoints (usually no changes needed)

3. **Build and start the container:**
   ```bash
   docker-compose up --build -d
   ```

4. **Run the data fetcher:**
   ```bash
   docker-compose exec crypto-data-fetcher python3 app/main.py
   ```

5. **View logs:**
   ```bash
   docker-compose logs -f crypto-data-fetcher
   ```

6. **Access downloaded data:**
   
   Data is persisted in `./app/Data/` directory on your host machine

#### Docker Commands Reference

- **Stop the container:**
  ```bash
  docker-compose down
  ```

- **Rebuild after code changes:**
  ```bash
  docker-compose up --build
  ```

- **Run in interactive mode:**
  ```bash
  docker-compose exec crypto-data-fetcher /bin/bash
  ```

- **View container status:**
  ```bash
  docker-compose ps
  ```

- **Remove containers and volumes:**
  ```bash
  docker-compose down -v
  ```

#### Using Plain Docker (without docker-compose)

1. **Build the image:**
   ```bash
   docker build -t crypto-data-fetcher .
   ```

2. **Run the container:**
   ```bash
   docker run -it --rm \
     -v $(pwd)/ignore:/app/ignore \
     -v $(pwd)/app/Data:/app/app/Data \
     crypto-data-fetcher
   ```

#### Docker Volume Management

The Docker setup uses volumes to persist data:

- **Configuration files:** `./ignore` → `/app/ignore` (read-only recommended)
- **Downloaded data:** `./app/Data` → `/app/app/Data` (persistent storage)

This ensures:
- Configuration changes are reflected without rebuilding
- Downloaded data persists across container restarts
- Easy backup and data management

Configuration

API Endpoints: Define API endpoints in ignore/apiendpoints.yaml.

Parameters: Configure application parameters in ignore/params.yaml.

Usage

Modify the API endpoints and parameters as needed.

Use app/main.py to initiate data processing.

Customize data handling logic in:

DataDownLoader.py for downloading data.

DataWriter.py for saving data.

OhlcConverter.py and TickerConverter.py for data transformation.

Supported Exchanges

The application supports the following cryptocurrency exchanges:

Bybit

Ticker: https://api.bybit.com//v5/market/instruments-info?category=linear

OHLC: https://api.bybit.com/v5/market/kline?category=linear

OKX

OHLC: https://aws.okx.com/api/v5/market/history-candles

dYdX

Ticker: https://indexer.dydx.trade/v4/perpetualMarkets

OHLC: https://indexer.dydx.trade/v4/candles/perpetualMarkets/

ApexPro

Ticker: https://pro.apex.exchange/api/v1/symbols

OHLC: https://pro.apex.exchange/api/v1/klines

Testing

Run the test suite to validate functionality:

python app/test.py

Deployment

**Docker Deployment (Recommended for Production)**

The application is optimized for Docker deployment with the following benefits:
- Consistent environment across different systems
- Easy dependency management
- Isolated execution environment
- Simple data persistence through volumes

Follow the Docker Setup section above for deployment instructions.

**Scheduling Automated Runs**

For production use, you can schedule regular data fetches:

1. **Using cron with Docker:**
   ```bash
   # Add to crontab (crontab -e)
   0 * * * * cd /path/to/CryptoHistoricalMarketData && docker-compose exec -T crypto-data-fetcher python3 app/main.py >> /var/log/crypto-data.log 2>&1
   ```

2. **Using systemd timer:**
   Create a systemd service and timer for scheduled execution

3. **Using Kubernetes CronJob:**
   Deploy as a Kubernetes CronJob for cloud environments

Contribution

Contributions are welcome! Please follow these steps:

Fork the repository.

Create a feature branch.

Commit your changes.

Submit a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for det
