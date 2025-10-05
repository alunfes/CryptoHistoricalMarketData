# Dev Container 設定

このディレクトリには、CryptoHistoricalMarketDataプロジェクト用のVS Code Dev Container設定が含まれています。

## ファイル

- `devcontainer.json` - VS Code Dev Containersのメイン設定ファイル
- `README.md` - 英語版のREADME
- `README_ja.md` - このファイル（日本語版README）

## 使用方法

1. このリポジトリをVS Codeで開きます
2. "Dev Containers" 拡張機能 (ms-vscode-remote.remote-containers) をインストールします
3. プロンプトが表示されたら「コンテナで再度開く」をクリックするか、コマンドパレットから「Dev Containers: Reopen in Container」を実行します

コンテナはルートの`docker-compose.yml`を使用してビルドされ、`crypto-data-fetcher`サービスに接続します。

## 作業ディレクトリ

コンテナの作業ディレクトリは`/app`に設定されており、ここにアプリケーションコードがあります。

## ポストクリエイトコマンド

コンテナ作成後、`python3 --version`を実行してPythonのインストールを確認します。

## インストールされる拡張機能

以下のVS Code拡張機能がコンテナ内に自動的にインストールされます：

- `ms-python.python` - Python言語サポート
- `ms-python.vscode-pylance` - Python型チェックと自動補完

## トラブルシューティング

### エラー: "service 'app' has neither an image nor a build context specified"

このエラーは、以前の設定で存在しないdocker-compose.ymlファイルを参照していた場合に発生していました。
現在の設定では、ルートの`docker-compose.yml`のみを参照するため、このエラーは発生しません。

### コンテナが起動しない場合

1. Docker Desktopが起動していることを確認してください
2. `docker compose -f docker-compose.yml config`を実行して設定を確認してください
3. VS Codeを再起動してみてください
