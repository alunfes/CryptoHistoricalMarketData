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
│   ├── Dockerfile
│   └── requirements.txt
└── ignore/
    ├── apiendpoints.yaml
    └── params.yaml

Prerequisites

Python 3.8 or later

Docker and Docker Compose (optional, for containerized deployment)

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

Build and run the application using Docker Compose:

docker-compose up --build

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

Ticker: https://api.dydx.exchange/v3/markets

OHLC: https://api.dydx.exchange/v3/candles/

ApexPro

Ticker: https://pro.apex.exchange/api/v1/symbols

OHLC: https://pro.apex.exchange/api/v1/klines

Testing

Run the test suite to validate functionality:

python app/test.py

Deployment

Use the provided Dockerfile to create a standalone Docker container.

Deploy the application using docker-compose.yml for multi-container setups.

Contribution

Contributions are welcome! Please follow these steps:

Fork the repository.

Create a feature branch.

Commit your changes.

Submit a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for det
