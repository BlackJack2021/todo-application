# 本プロジェクトの概要

- todo アプリの開発を通じて実践的な FastAPI アプリケーションの構築の練習をします。

# 環境構築

依存関係の管理は rye を利用します。作成者の rye のバージョン情報は以下です。

```
rye 0.15.2
commit: 0.15.2 (e2beb3a90 2023-10-04)
platform: linux (x86_64)
self-python: cpython@3.11
symlink support: true
```

`rye init` コマンドを打ち込み初期環境を構築した後、`rye pin 3.11.6` コマンドにより python のバージョンを指定します。その後、fastapi 及び uvicorn を利用することを指定します。

```
rye add fastapi==0.109.0 uvicorn[standard]==0.
27.0
```

`rye sync` コマンドにより、これらの要件を満たす仮想環境の構築を行います。

# ローカルサーバーの立ち上げ

ローカルサーバーの立ち上げを行うためには、最低限 `/src/todo_application/app.py` を以下のように記述する必要があります。

```py
from fastapi import FastAPI

app = FastAPI()

@app.get('/hello')
def say_hello():
    return {
        'hello': 'world!'
    }
```

この記述ができたら、プロジェクトのルートディレクトリで以下のコマンドを打ちます。

```
rye run uvicorn src.todo_application.app:app --reload --port 8000
```

http://localhost:8000/docs にアクセスすると、この API の詳細が記述された Swagger UI を確認することができます。
