# Chapter1. REST API の設計

## 1. アプリの概要

ここでは、シンプルな todo サービスの開発を行います。ざっくり表現すると以下のようになります。

1. ユーザーの作成、読み取り、更新、削除
2. タスクの作成、読み取り、更新、削除

こう考えてみると「ユーザー」と「タスク」に関するデータがこのアプリケーションの構築の上で必要になることになります。ここではそれぞれの取り扱うデータは以下であるとします。

- ユーザー

  - `user_id` : ユーザーを識別する一意の ID
  - `name` : ユーザーの指定した名前
  - `created_at`: ユーザーが作成された日時
  - `updated_at`: ユーザー情報が更新された日時

- タスク
  - `task_id`: タスクを識別する一意の ID
  - `title`: タスクの名称
  - `description`: タスクの詳細な説明
  - `status`: タスクの現在の状態
    - 未着手 : `not_started`
    - 進行中 : `progress`
    - 完了 : `done`
  - `user_id`: ユーザーを識別する一意の ID
  - `created_at`: タスクが作成された日時
  - `updated_at`: タスクが更新された日時

これらの情報に基づいて、REST API を構築してみましょう。

## 2. REST API のあるべき姿

### 2.1. REST とは

REST はスケーラブルな疎結合 API を構築するためのアーキテクチャスタイルのことであり、リソースの概念は REST アプリケーションの基本となります。ここでいうリソースとは、URL を使って参照できるエンティティ(ここではユーザーやタスク)のことです。

リソースには、**シングルトン**と**コレクション**の 2 種類があります。シングルトンとは単一のリソースのことで、例えばユーザーであれば「一人のユーザーの情報」を指します。一方でコレクションは複数のリソースのことです。この違いを意識してエンドポイントを設計する必要があります。例えば、

- `/users` : ユーザーの情報のコレクションを扱うエンドポイント
- `/users/{user_id}` : あるユーザーの情報（シングルトン）を扱うエンドポイント

といった形になります。次に、構築した API がどの程度 REST に準拠したものであるかを判断する基準である、リチャードソン成熟度モデルについて触れたいと思います。

### 2.2. リチャードソン成熟度モデル

リチャードソン成熟度モデルは、構築した API がどの程度 REST に準拠したものであるかを判断するのに役立つ思考モデルです。このモデルは、レベル 0 からレベル 3 の段階で定義されており、レベルが高くなるにつれて準拠度合が高まることを意味します。それでは、各レベルがどのようなものを示すか簡単に説明します。

#### 2.2.1. レベル 0

レベル 0 の段階では、すべての処理が同じエンドポイントで、かつ同じ HTTP メソッドで表現される状況です。例えば、`/api` というエンドポイントに、POST メソッドで、「タスクの削除」「ユーザーの追加」「タスクの取得」などが指示されている状況を指します。

#### 2.2.2. レベル 1

各リソース（ユーザーやタスク）を示すエンドポイントが導入された状態を示します。`/api` という単一のエンドポイントを用意する代わりに、`/users` や `/users/{user_id}`, `/tasks`, `/tasks/{tasks_id}` が準備されている状態です。ただし、HTTP メソッドは相変わらず１つだけ使われている状態です。

#### 2.2.3. レベル 2

レベル 1 の各リソースを示すエンドポイントの導入に加え、HTTP メソッド(GET, POST, PUT, DELETE 等)の区別によるアクションの指示やステータスコード(200, 404, 500 など)が導入された状態です。

#### 2.2.4. レベル 3

レベル 2 の状態に加えて、「発見可能性」の概念が加えられている状態。詳細が気になる方は HATEOAS (Hypermedia As The Engine Of Application State) について調べるとよいかもしれません。

## 3. 今回のアプリの API 設計の概要

それではこれらの視点を踏まえて、今回の Todo サービスに対して API を設計しましょう。

基本的にパラメータはリクエストボディに含みますが、一部クエリパラメータ（例えば、`/orders?limit=10` のようにエンドポイントに付加するパラメータのこと）として定義します。一般的にクエリパラメータは GET リクエストについてデータの取得をフィルタリングする場合に用いられることが多いため、この慣例にならうこととします。

- `users`

  - `get`
    - 機能: ユーザー情報をまとめて取得
    - クエリパラメータ
      - `limit`
    - ステータスコード
      - `200 OK`
      - `422 Unprocessable Entity`
  - `post`
    - 機能 : ユーザー情報を作成
    - パラメータ
      - `name`
    - ステータスコード
      - `201 Created`
      - `422 Unprocessable Entity`

- `users/{user_id}`

  - `get`
    - 機能 : 指定されたユーザーの情報を取得
    - ステータスコード
      - `200 OK`
      - `404 Not Found`
      - `422 Unprocessable Entity`
  - `put`
    - 機能 : 指定されたユーザーの情報を更新
    - パラメータ
      - `name`
    - ステータスコード
      - `200 OK`
      - `404 Not Found`
      - `422 Unprocessable Entity`
  - `delete`
    - 機能 : 指定されたユーザーの情報を削除
    - ステータスコード
      - `204 No Content`
      - `404 Not Found`
      - `422 Unprocessable Entity`

- `users/{user_id}/tasks`

  - `get`
    - 機能 : 指定されたユーザーのタスクをまとめて取得
    - クエリパラメータ
      - `limit`
      - `status`
    - ステータスコード
      - `200 OK`
      - `404 Not Found`
      - `422 Unprocessable Entity`

- `tasks`

  - `get`
    - 機能 : タスクをまとめて取得
    - クエリパラメータ
      - `limit`
      - `status`
    - ステータスコード
      - `200 OK`
      - `422 Unprocessable Entity`
  - `post`
    - 機能 : タスクを作成
    - パラメータ
      - `title`
      - `description`
      - `status`
      - `user_id`
    - ステータスコード
      - `201 Created`
      - `422 Unprocessable Entity`

- `tasks/{task_id}`
  - `get`
    - 機能 : 指定されたタスクの詳細を取得
    - ステータスコード
      - `200 OK`
      - `404 Not Found`
      - `422 Unprocessable Entity`
  - `put`
    - 機能 : 指定されたタスクを更新
    - パラメータ
      - `title`
      - `description`
      - `status`
      - `user_id`
    - ステータスコード
      - `200 OK`
      - `404 Not Found`
      - `422 Unprocessable Entity`
  - `delete`
    - 機能 : 指定されたタスクを削除
    - ステータスコード
      - `204 No Content`
      - `404 Not Found`
      - `422 Unprocessable Entity`

`422 Unprocessable Entity` とは、必要なパラメータが不足していたり、不適切なパラメータが付与されていた時にそれを明示するものです。

それでは FastAPI を用いて、このアプリケーションを構築しましょう。
