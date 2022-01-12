# tfs

一時ファイル置き場 (Temporary File Storage)

アップロードから一定期間でファイルが自動削除されるオンラインストレージ。

認証機能なし。社内ネットワークなどアクセスできる人が限定された環境での利用を想定。

## 起動

    git clone git@github.com:saasan/tfs.git
    cd tfs
    docker-compose up -d

開発時は
[Visual Studio Code Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
で起動可能。

## DB の初期化

初回起動後、以下のコマンドでDBを初期化する。

    docker-compose exec app python -m migrate_db

## ブラウザで開く

- `docker-compose up` で起動した場合:

  <http://localhost/>

- Remote - Containers で起動した場合:

  <http://localhost:8080/>

## 設定

起動する前に環境変数を設定するか
.env ファイルを作成することで設定を変更可能。

### TFS_PAGE_TITLE

ページのタイトル

### TFS_FILE_EXPIRE_DAYS

ファイルの保存日数

### .env ファイルの例

    TFS_PAGE_TITLE=タイトル
    TFS_FILE_EXPIRE_DAYS=30

## Docker のボリューム

### tfs-data

アップロードされたファイル本体が保存される。

### mysql-data

アップロードされたファイルのサイズなどの情報が保存される。
