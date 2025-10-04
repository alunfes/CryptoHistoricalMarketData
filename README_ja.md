# CryptoHistoricalMarketData

暗号通貨の過去の市場データを取得、処理、保存するためのPythonアプリケーションです。

## 概要

CryptoHistoricalMarketDataは、複数の暗号通貨取引所から過去の市場データを自動的に取得し、構造化されたCSV形式で保存するためのツールです。OHLCV（始値、高値、安値、終値、出来高）データと銘柄情報の取得に対応しています。

### 主な特徴

- **複数取引所対応**: Bybit、OKX、dYdX、ApexProの4つの主要取引所に対応
- **増分ダウンロード**: 既存データを確認し、差分のみを効率的にダウンロード
- **全銘柄対応**: 各取引所の全ての銘柄のデータを自動取得
- **1分足データ**: 詳細な1分足のOHLCVデータを取得
- **自動重複排除**: データの重複を自動的に検出・削除
- **Docker対応**: コンテナ化されており、簡単にデプロイ可能
- **非同期処理**: 効率的な非同期ダウンロードで高速処理

## ディレクトリ構成

```
CryptoHistoricalMarketData/
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── README.md                    # 英語版README
├── README_ja.md                 # 日本語版README（このファイル）
├── INCREMENTAL_DOWNLOAD.md      # 増分ダウンロード機能の詳細
├── IMPLEMENTATION_SUMMARY.md    # 実装概要
├── app/
│   ├── DataDownLoader.py        # データダウンロード処理
│   ├── DataWriter.py            # データ書き込み処理
│   ├── OHLCData.py             # OHLCデータ管理
│   ├── OhlcConverter.py        # OHLCデータ変換
│   ├── TickerConverter.py      # 銘柄情報変換
│   ├── TickerData.py           # 銘柄情報管理
│   ├── main.py                 # メインエントリーポイント
│   ├── test.py                 # テストスイート
│   ├── test_incremental_download.py  # 増分ダウンロードのユニットテスト
│   ├── test_full_workflow.py   # 統合テスト
│   ├── Dockerfile              # Dockerイメージ定義
│   └── requirements.txt        # Python依存パッケージ
└── ignore/
    ├── apiendpoints.yaml       # API エンドポイント設定
    └── params.yaml             # アプリケーション設定
```

## 必要要件

- Python 3.8 以上
- Docker と Docker Compose（コンテナ利用時）
- 各取引所のAPIへのアクセス権限

## インストール方法

### ローカル環境での実行

1. **リポジトリをクローン**
   ```bash
   git clone https://github.com/alunfes/CryptoHistoricalMarketData.git
   cd CryptoHistoricalMarketData
   ```

2. **依存パッケージをインストール**
   ```bash
   pip install -r requirements.txt
   ```

3. **設定ファイルを編集**（詳細は後述）
   ```bash
   # ignore/params.yaml と ignore/apiendpoints.yaml を編集
   ```

4. **アプリケーションを実行**
   ```bash
   python app/main.py
   ```

### Docker環境での実行

1. **リポジトリをクローン**
   ```bash
   git clone https://github.com/alunfes/CryptoHistoricalMarketData.git
   cd CryptoHistoricalMarketData
   ```

2. **Docker Composeでビルド・実行**
   ```bash
   docker-compose up --build
   ```

## 設定方法

### パラメータ設定（ignore/params.yaml）

アプリケーションの動作を制御する主要な設定ファイルです。

```yaml
# データを取得する取引所のリスト
exchanges: ['bybit', 'okx', 'dydx', 'apexpro']

# 初回ダウンロード時に何日前からデータを取得するか
since_num_days_before: 90

# 各取引所のデータ取得間隔（1分足）
ohlcv_data_interval:
  okx: '1m'       # OKXの1分足
  bybit: 1        # Bybitの1分足
  dydx: '1MIN'    # dYdXの1分足
  apexpro: 1      # ApexProの1分足

# 1回のAPI呼び出しで取得する最大データ数
max_download_per_trial:
  okx: 100
  bybit: 200
  dydx: 100
  apexpro: 1500
```

**設定項目の説明:**

- `exchanges`: データを取得したい取引所を指定します。不要な取引所はリストから削除できます。
- `since_num_days_before`: 初回実行時に何日前からデータを取得するかを指定します（デフォルト90日）。
- `ohlcv_data_interval`: 各取引所でのローソク足の時間間隔を指定します。
- `max_download_per_trial`: 各取引所からの1回のAPI呼び出しで取得する最大データポイント数です。

### APIエンドポイント設定（ignore/apiendpoints.yaml）

各取引所のAPIエンドポイントを定義します。通常、この設定を変更する必要はありません。

```yaml
bybit:
  ticker: https://api.bybit.com//v5/market/instruments-info?category=linear
  ohlc: https://api.bybit.com/v5/market/kline?category=linear
okx:
  ticker: https://aws.okx.com/api/v5/public/instruments?instType=SWAP
  ohlc: https://aws.okx.com/api/v5/market/history-candles
dydx:
  ticker: https://api.dydx.exchange/v3/markets
  ohlc: https://api.dydx.exchange/v3/candles/
apexpro:
  ticker: https://pro.apex.exchange/api/v1/symbols
  ohlc: https://pro.apex.exchange/api/v1/klines
```

## 使い方

### 基本的な使い方

1. **設定ファイルを編集**
   - `ignore/params.yaml`で取得したい取引所と期間を設定
   - 必要に応じて`ignore/apiendpoints.yaml`を確認

2. **アプリケーションを実行**
   ```bash
   python app/main.py
   ```

3. **データの確認**
   - ダウンロードされたデータは`app/Data/`ディレクトリに保存されます
   - ファイル名形式: `{取引所}-{ベース通貨}-{クォート通貨}.csv`
   - 例: `bybit-BTC-USDT.csv`, `dydx-ETH-USD.csv`

### 実行例

#### 初回実行（データがない場合）

```bash
$ python app/main.py
/home/user/CryptoHistoricalMarketData

Downloading target tickers...
Download Ticker Done for dydx, num tickers=37

Started ohlc download process...
Downloaded dydx-BTC-USD (BTC-USD): 129600 records
Downloaded dydx-ETH-USD (ETH-USD): 129600 records
Downloaded dydx-LINK-USD (LINK-USD): 129600 records
... (全37銘柄について続く)

Completed download all symbol data.
```

初回実行時は、`since_num_days_before`で指定した日数分（デフォルト90日）のデータを全銘柄について取得します。

#### 2回目以降の実行（増分ダウンロード）

```bash
$ python app/main.py
/home/user/CryptoHistoricalMarketData

Downloading target tickers...
Download Ticker Done for dydx, num tickers=37

Started ohlc download process...
Updated dydx-BTC-USD (BTC-USD): 60 records
Updated dydx-ETH-USD (ETH-USD): 60 records
Updated dydx-LINK-USD (LINK-USD): 60 records
... (全37銘柄について続く)

Completed download all symbol data.
```

2回目以降は、既存データの最終タイムスタンプ以降のデータのみを効率的に取得します。

#### データが最新の場合

```bash
$ python app/main.py
/home/user/CryptoHistoricalMarketData

Downloading target tickers...
Download Ticker Done for dydx, num tickers=37

Started ohlc download process...
Skipping dydx-BTC-USD: data is up to date
Skipping dydx-ETH-USD: data is up to date
Skipping dydx-LINK-USD: data is up to date
... (全37銘柄について続く)

Completed download all symbol data.
```

データが既に最新の場合、不要なAPIコールを避けてスキップします。

### データ形式

ダウンロードされたデータはCSV形式で保存され、以下のカラムを含みます：

| カラム名 | 説明 | 単位 |
|---------|------|------|
| timestamp | タイムスタンプ | ミリ秒単位のUnix時刻 |
| open | 始値 | 通貨単位 |
| high | 高値 | 通貨単位 |
| low | 安値 | 通貨単位 |
| close | 終値 | 通貨単位 |

**CSVファイルの例:**
```csv
timestamp,open,high,low,close
1686632400000,26056.4,26123.0,26029.1,26077.6
1686632460000,26077.6,26089.5,26065.2,26078.3
1686632520000,26078.3,26095.1,26072.8,26089.4
```

### 特定の取引所のみを対象にする

`ignore/params.yaml`の`exchanges`リストを編集して、特定の取引所のみを指定できます：

```yaml
# dYdXのみを取得する場合
exchanges: ['dydx']

# BybitとOKXのみを取得する場合
exchanges: ['bybit', 'okx']
```

### データ取得期間の変更

初回ダウンロード時の取得期間を変更するには、`ignore/params.yaml`の`since_num_days_before`を編集します：

```yaml
# 過去30日分のデータを取得
since_num_days_before: 30

# 過去180日分（約6ヶ月）のデータを取得
since_num_days_before: 180
```

## 対応取引所

### Bybit
- **銘柄情報API**: https://api.bybit.com/v5/market/instruments-info?category=linear
- **OHLC API**: https://api.bybit.com/v5/market/kline?category=linear
- **対応商品**: Linear契約（無期限先物）

### OKX
- **銘柄情報API**: https://aws.okx.com/api/v5/public/instruments?instType=SWAP
- **OHLC API**: https://aws.okx.com/api/v5/market/history-candles
- **対応商品**: スワップ契約

### dYdX
- **銘柄情報API**: https://api.dydx.exchange/v3/markets
- **OHLC API**: https://api.dydx.exchange/v3/candles/
- **対応商品**: パーペチュアル契約

### ApexPro
- **銘柄情報API**: https://pro.apex.exchange/api/v1/symbols
- **OHLC API**: https://pro.apex.exchange/api/v1/klines
- **対応商品**: 先物契約

## テスト

プロジェクトには包括的なテストスイートが含まれています。

### 全テストの実行

```bash
python app/test.py
```

### 増分ダウンロード機能のテスト

```bash
cd app
python test_incremental_download.py
```

このテストでは以下を検証します：
- 最終タイムスタンプの取得
- ファイル存在確認
- データの追記処理
- 重複データの処理

### 統合テスト

```bash
cd app
python test_full_workflow.py
```

このテストでは以下のシナリオを検証します：
- 初回ダウンロード（データがない状態）
- 増分ダウンロード（既存データがある状態）
- スキップ処理（データが最新の状態）
- データにギャップがある場合の処理

## 高度な機能

### 増分ダウンロード機能

このアプリケーションの主要機能の一つが増分ダウンロード機能です。この機能により：

1. **既存データの自動検出**: 各銘柄の既存データファイルを確認し、最終タイムスタンプを取得
2. **効率的なデータ取得**: 最終タイムスタンプ以降のデータのみをダウンロード
3. **自動マージ**: 新規データを既存データに自動的に追加
4. **重複排除**: タイムスタンプベースで重複データを自動削除
5. **ソート**: タイムスタンプ順にデータを自動ソート

詳細は`INCREMENTAL_DOWNLOAD.md`を参照してください。

### カスタマイズ

各モジュールをカスタマイズすることで、独自の処理を追加できます：

- **DataDownLoader.py**: データダウンロードロジックのカスタマイズ
- **DataWriter.py**: データ保存形式のカスタマイズ
- **OhlcConverter.py**: データ変換ロジックのカスタマイズ
- **TickerConverter.py**: 銘柄情報変換ロジックのカスタマイズ

## トラブルシューティング

### データがダウンロードされない

1. **ネットワーク接続を確認**
   - 各取引所のAPIエンドポイントにアクセス可能か確認
   ```bash
   curl https://api.dydx.exchange/v3/markets
   ```

2. **設定ファイルを確認**
   - `ignore/params.yaml`が正しく設定されているか確認
   - `ignore/apiendpoints.yaml`のURLが正しいか確認

3. **ログを確認**
   - エラーメッセージが表示されていないか確認
   - APIレート制限に引っかかっていないか確認

### "Data is not found in data writer!" エラー

このエラーは、データのダウンロードまたは変換プロセスで問題が発生した場合に表示されます：

1. **APIレスポンスを確認**
   - 取引所のAPIが正常に応答しているか確認
   - 指定した銘柄が取引所に存在するか確認

2. **タイムアウトを確認**
   - ネットワークが遅い場合、タイムアウトが発生する可能性があります

### ファイルの読み書きエラー

1. **権限を確認**
   ```bash
   # Dataディレクトリの作成権限を確認
   ls -la app/
   ```

2. **ディスク容量を確認**
   ```bash
   df -h
   ```

3. **既存ファイルの形式を確認**
   - CSVファイルが破損していないか確認
   - 必要に応じて破損したファイルを削除して再ダウンロード

### Docker環境での問題

1. **Dockerログを確認**
   ```bash
   docker-compose logs
   ```

2. **コンテナを再起動**
   ```bash
   docker-compose down
   docker-compose up --build
   ```

## パフォーマンスの最適化

### API呼び出しの最適化

1. **max_download_per_trialの調整**
   - より大きな値を設定すると、API呼び出し回数が減少
   - ただし、取引所のレート制限に注意

2. **取得期間の最適化**
   - `since_num_days_before`を必要最小限に設定
   - 定期的に実行することで、増分ダウンロードの効率を最大化

### ストレージの最適化

1. **古いデータの削除**
   - 不要になった古いデータファイルを定期的に削除

2. **データの圧縮**
   - 必要に応じて、CSVファイルを圧縮して保存

## 定期実行の設定

データを定期的に自動更新したい場合、cronジョブを設定できます。

### Linux/Mac での例

```bash
# crontabを編集
crontab -e

# 毎時0分に実行する場合
0 * * * * cd /path/to/CryptoHistoricalMarketData && /usr/bin/python3 app/main.py >> /var/log/crypto_data.log 2>&1

# 毎日午前3時に実行する場合
0 3 * * * cd /path/to/CryptoHistoricalMarketData && /usr/bin/python3 app/main.py >> /var/log/crypto_data.log 2>&1
```

### Dockerでの定期実行

Docker環境で定期実行する場合は、ホストシステムでcronを設定するか、専用のスケジューラーコンテナを使用します。

## データの活用例

### Pandasでのデータ分析

```python
import pandas as pd

# データを読み込む
df = pd.read_csv('app/Data/dydx-BTC-USD.csv')

# タイムスタンプを日時型に変換
df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

# 基本統計量を表示
print(df.describe())

# 日次の平均価格を計算
df['date'] = df['datetime'].dt.date
daily_avg = df.groupby('date')['close'].mean()
print(daily_avg)
```

### データの可視化

```python
import pandas as pd
import matplotlib.pyplot as plt

# データを読み込む
df = pd.read_csv('app/Data/dydx-BTC-USD.csv')
df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

# ローソク足チャートを作成（簡易版）
plt.figure(figsize=(12, 6))
plt.plot(df['datetime'], df['close'], label='Close Price')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.title('BTC-USD Price History')
plt.legend()
plt.grid(True)
plt.show()
```

## よくある質問（FAQ）

### Q1: 取得できるデータの最大期間は？

A: 各取引所のAPI制限によりますが、通常は数ヶ月〜数年分のデータを取得できます。`since_num_days_before`パラメータで調整できます。

### Q2: 複数の時間足に対応していますか？

A: 現在は1分足のみに対応していますが、`ignore/params.yaml`の`ohlcv_data_interval`を変更することで、各取引所がサポートする他の時間足も取得可能です。

### Q3: データはどのくらいの頻度で更新すべきですか？

A: 用途によりますが、1時間ごとまたは1日ごとの更新が一般的です。増分ダウンロード機能により、頻繁に実行しても効率的です。

### Q4: APIキーは必要ですか？

A: 現在サポートしている取引所の公開データAPIにはAPIキーは不要です。ただし、レート制限には注意が必要です。

### Q5: 他の取引所を追加できますか？

A: はい、可能です。新しい取引所を追加するには：
1. `ignore/apiendpoints.yaml`に取引所のエンドポイントを追加
2. `ignore/params.yaml`に取引所の設定を追加
3. `DataDownLoader.py`に対応するダウンロードメソッドを実装
4. `*Converter.py`に対応する変換ロジックを実装

## コントリビューション

プロジェクトへの貢献を歓迎します！以下の手順でコントリビュートしてください：

1. リポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成

### コーディング規約

- PEP 8に準拠したPythonコードを記述
- 適切なコメントとドキュメンテーションを追加
- 新機能には必ずテストを追加

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。詳細は`LICENSE`ファイルを参照してください。

## 関連ドキュメント

- [English README](README.md) - 英語版README
- [Incremental Download Feature](INCREMENTAL_DOWNLOAD.md) - 増分ダウンロード機能の詳細
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - 実装の概要と技術詳細

## サポート

問題が発生した場合や質問がある場合は、GitHubのIssueを作成してください。

---

**注意**: このツールは教育目的および個人利用を想定しています。商用利用の場合は、各取引所の利用規約とAPI利用ガイドラインを確認してください。
