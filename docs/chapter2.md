# Chapter2. FastAPI を用いた Rest API の実装

## 1. 本章のスコープ

本章では主に FastAPI を用いた API 構築に焦点を当てて、Chapter1 で設計した API を構築します。ただし本章ではまだデータベースについては実装せず、python のリストを使ってデータを保存します。本章で取り扱う主な内容は以下です。

1. プロジェクトの構成について（モジュラーモノリス型の採用）
2. 型バリデーションに用いるスキーマの定義の方法
3. APIRouter の実装方法
   - パスパラメータ、クエリパラメータ、リクエストボディの設定
   - ステータスコードの設定方法

## 2. 実装

### 2.1. 前準備

この時点では、ディレクトリは以下のような構造になっているはずです。

```
/src/todo_application
├── __init__.py
└── app.py
```

ここで、 `chapter2` ディレクトリを追加します。

```
/src/todo_application
├── __init__.py
├── app.py
└── chapter2
```

本章の以降の作業は全てこの `chapter2` ディレクトリで行います。

### 2.2. 設計

####　 2.2.1. モジュラーモノリス型の採用

chapter1 で設定したエンドポイントでは、`/tasks`, `/users` の 2 つのエンドポイントがありました。つまりユーザー、タスクという２つのリソースが本 API における大きな焦点となっています。そこで今回は users と tasks という 2 つのモジュールに切り分けて開発を行いたいと思います。つまり、この時点で以下のプロジェクト構成になります。

```
/src/todo_application/chapter2
├── tasks
└── users
```

プロジェクト構造には異なる切り分け方も考えられます。広く用いられているのは、`/schemas`, `/routers`... といった形で、アプリ自体の機能ではなくプログラムが果たす機能ごとに切り分けるアプローチです。しかし、[こちらのドキュメント](https://github.com/zhanymkanov/fastapi-best-practices) では以下のように記述されています。

> Although the project structure, where we separate files by their type (e.g. api, crud, models, schemas) presented by @tiangolo is good for microservices or projects with fewer scopes, we couldn't fit it into our monolith with a lot of domains and modules. Structure that I found more scalable and evolvable is inspired by Netflix's Dispatch with some little modifications.

> 以下日本語訳 :
> @tiangolo が提示したプロジェクト構造（例えば、api、crud、models、schemas などのタイプごとにファイルを分ける）は、マイクロサービスや範囲が狭いプロジェクトには適していますが、多くのドメインとモジュールを持つ私たちのモノリシックなプロジェクトには適合しませんでした。私が見つけたよりスケーラブルで進化可能な構造は、Netflix の Dispatch に触発され、少し修正を加えたものです。

そのため、どちらの構成を取るかはプロジェクトの性質に応じて判断するのが良いと思われます。今回は

1. モノリスでアプリケーションを構築すること
2. アプリケーションに今後機能が実装されること

を見越してアプリケーションの機能ごとに切り分けるアプローチ(**モジュラーモノリス**)で実装したいと思います。

#### 2.2.2. データベースモックの準備

以下の `db_mock` ディレクトリにデータベースのモックを用意します。

```
/src/todo_application/chapter2
├── tasks
├── users
└── db_mock
    ├── __init__.py
    └── db.py
```

`db.py` は以下のように記述しましょう。

```py
from datetime import datetime
from typing import List, Literal, Optional, TypedDict
from uuid import UUID
import uuid
from ..tasks.schemas import Status as TaskStatus

class User(TypedDict):
    user_id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

user1_id = uuid.uuid4()
user2_id = uuid.uuid4()

task1_id = uuid.uuid4()
task2_id = uuid.uuid4()

# サンプルのユーザーデータ
users: List[User] = [
    {
        "user_id": user1_id,
        "name": "ねっと",
        "created_at": datetime(year=2023, month=1, day=2),
        "updated_at": datetime(year=2023, month=1, day=4)
    },
    {
        "user_id": user2_id,
        "name": "さいと",
        "created_at": datetime(year=2023, month=2, day=2),
        "updated_at": datetime(year=2023, month=2, day=5)
    },
]

class Task(TypedDict):
    task_id: UUID
    title: str
    description: Optional[str]
    status: TaskStatus
    user_id: UUID
    created_at: datetime
    updated_at: datetime

# サンプルのタスクデータ
tasks: List[Task] = [
    {
        "task_id": task1_id,
        "title": "宿題",
        "description": "漢字のノートを書く",
        "status": TaskStatus.NOT_STARTED,
        "user_id": user1_id,
        "created_at": datetime(year=2023, month=1, day=2),
        "updated_at": datetime(year=2023, month=1, day=4)
    },
    {
        "task_id": task2_id,
        "title": "買い物",
        "description": "りんごを2つ買う",
        "status": TaskStatus.PROGRESS,
        "user_id": user2_id,
        "created_at": datetime(year=2023, month=2, day=4),
        "updated_at": datetime(year=2023, month=2, day=8)
    },
]
```

`tasks/schemas.py` はまだ記述していませんが、本モジュールの記述に必要な Status の定義だけ抜き出すと以下のようです。

```py
class Status(Enum):
    NOT_STARTED = 'not_started'
    PROGRESS = 'progress'
    DONE = 'done'
```

何点か要点を説明します。

- `TypedDict` について
  - これは辞書の型を指定するために必要なクラスです。上記 `User` や `Task` クラスのように、このクラスを継承させてクラスを定義することで、「ある辞書が持つべきプロパティやその型」を示す型を構築することができます。
  - ご存じの通り python は動的型付け言語であり、こうした型情報は必ずしも記述する必要はないですが、記述することで得られるメリットも多くあります。このメリットは複数人で開発する場合に顕著ですが、個人で開発する場合においてもエディタの補完機能を有効に活用できるようになり、開発がしやすくなりますのでお勧めです。
- `Enum` について
  - 列挙型と呼ばれる機能で、変数が特定の値しかとらないことが分かっている場合に利用します。この記述により、タスクのステータスが `not_started`, `progress`, `done` の３つのいずれかであることが明示されます。

#### 2.2.3. スキーマの準備

FastAPI では pydantic を利用して、エンドポイントへのリクエストとレスポンスの型バリデーションを行うことができます。その型バリデーションのために必要な型情報を含んだモジュールを、`tasks/schemas.py` として定義します。このファイルは以下のように記述します。

```py
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Status(Enum):
    NOT_STARTED = 'not_started'
    PROGRESS = 'progress'
    DONE = 'done'

class TaskCreate(BaseModel):
    '''POST /tasks のリクエストボディが満たすべきスキーマ'''
    title: str
    description: Optional[str]
    status: Status
    user_id: UUID

class TaskUpdate(BaseModel):
    '''PUT /tasks のリクエストボディが満たすべきスキーマ'''
    title: str
    description: Optional[str]
    status: Status
    user_id: UUID

class Task(BaseModel):
    '''レスポンスで返すタスク情報のスキーマ'''
    title: str
    description: Optional[str]
    status: Status
    user_id: UUID
    task_id: UUID
    created_at: datetime
    updated_at: datetime
```

バリデーションに用いる型を定義するためには、クラスに `BaseModel` を継承する形で実装します。

#### 2.2.4. ルーターの定義

最後に、`tasks/routers.py` にて、エンドポイントへのリクエストに対し、どのような処理を行うかについて記述しましょう。

```py
import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette import status

from ..db_mock.db import tasks
from .schemas import Status, Task, TaskCreate, TaskUpdate

router = APIRouter()

def task_not_found_message(task_id: UUID) -> str:
    '''タスクが見つからない場合の例外メッセージの生成'''
    return f'指定されたタスク task_id={task_id} が存在しません'

@router.get("/tasks")
async def get_tasks(
    limit: Optional[int] = None,
    status: Optional[Status] = None
) -> List[Task]:
    '''タスクのコレクションを取得する

    Args:
        limit (Optional[int]) : タスクを最大何個まで返すかを指定。Noneなら該当したタスクを全て返す
        status (Optional[Status]) : status を確認し、該当するもののみを抽出

    Returns:
        List[Task] : 条件に基づいて抽出されたタスクのリスト
    '''
    _tasks = tasks.copy()

    # status に条件があればフィルタリング
    if status is not None:
        _tasks = [_task for _task in _tasks if _task['status'] == status]

    # limit が指定されていればその数に限定
    if limit is not None:
        _tasks = _tasks[:limit]

    return _tasks

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(
    request_body: TaskCreate
) -> Task:
    '''タスクを追加する'''
    task_id = uuid.uuid4()
    created_at = datetime.now()
    updated_at = datetime.now()
    new_task: Task = {
        **request_body.model_dump(),
        "task_id": task_id,
        "created_at": created_at,
        "updated_at": updated_at
    }

    tasks.append(new_task)
    return new_task

@router.get('/tasks/{task_id}')
async def get_task(
    task_id: UUID,
) -> Task:
    '''指定されたタスクを取得する'''
    for task in tasks:
        if task['task_id'] == task_id:
            return task
    raise HTTPException(
        status_code=404,
        detail=task_not_found_message(task_id)
    )


@router.put('/tasks/{task_id}')
async def update_task(
    task_id: UUID,
    request_body: TaskUpdate
) -> Task:
    '''指定されたタスクを更新する'''
    request_body_dict = request_body.model_dump()
    for task in tasks:
        if task['task_id'] == task_id:
            task.update(request_body_dict)
            task['updated_at'] = datetime.now()
            return task
    raise HTTPException(
        status_code=404,
        detail=task_not_found_message(task_id)
    )

@router.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID
):
    '''指定されたタスクを削除する'''
    for index, task in enumerate(tasks):
        if task['task_id'] == task_id:
            tasks.pop(index)
            return
    raise HTTPException(
        status_code=404,
        detail=task_not_found_message(task_id)
    )
```

いくつか補足点をまとめておきます。

- パラメータ及びリクエストボディについて
  - これらは関数の引数で宣言します。FastAPI はこれらのパラメータの型情報などを利用して、それらのパラメータがクエリパラメータか、パスパラメータか、リクエストボディか自動で判断してくれます。例えば
    - `task_id`: エンドポイントで `/tasks/{task_id}` と指定されているため、パスパラメータと解釈
    - `request_body`: 型情報に `pydantic.BaseModel` が継承されたクラスが指定されているため、リクエストボディと解釈
    - それ以外(`limit`, `status`): クエリパラメータと解釈。
- ステータスコード
  - 正常に処理された場合のステータスコードはデコレータの status 引数で定義します。例えば `@router.post("/tasks", status=HTTP_201_CREATED)` のようにです。デフォルトで `HTTP_200_OK` が指定されているので、200 を返す場合は宣言する必要がありません。
  - 正常な処理が行えなかった場合のステータスコードについて
    - 422 Unprocessable Entity や 500 Internal Server Error など、エラーとなる場合は FastAPI が自動的に設定してくれるため気にする必要がありません。
    - 一方処理上エラーが出るわけではない場合、例えば上記のコードでいう 404 Not Found に関しては、明示的に指定しましょう。

#### 2.2.5. `app.py` の準備

最後に仕上げとして、`chapter2` ディレクトリ直下に `__init__.py` 及び `app.py` を作成し、`app.py` に以下のように記述しましょう。

```py
from fastapi import FastAPI

from .tasks.router import router as task_router
#from .users.router import router as user_router

app = FastAPI()

app.include_router(task_router)
# users の実装ができたらコメントアウトを外す
#app.include_router(user_router)
```

`app.include_router(task_router)` の記述により、先ほど定義した各 API が FastAPI に認識されます。

#### 2.2.5. 実装のまとめ

ここまでの実装が完了していれば、プロジェクトの構造は以下のようになっていることが期待されます。

```
/src/todo_application/chapter2
├── tasks
    ├── __init__.py (空のファイルです、作成だけしておいてください)
    ├── router.py
    └── schemas.py
├── users
└── db_mock
    ├── __init__.py
    └── db.py
├── __init__.py
└── app.py
```

なお、users の方も同様に `__init__.py`, `router.py`, `schemas.py` を定義する必要があります。しかしほとんど tasks のモジュールと同じように構築すれば問題なく、追加的に解説すべきことがありません。そのためこちらについてはソースコードを確認してください。

#### 2.2.6. ローカルサーバーの立ち上げと Swagger UI の確認

ここまで実装が完了している場合、プロジェクトのルートディレクトリ(`pyproject.toml` があるディレクトリ)をカレントディレクトリとして、以下のコマンドを実行することによりローカルサーバーを立ち上げることが可能です。

```
rye run uvicorn src.todo_application.app:app --reload --port 8000
```

ご存じのように、この状態で http://localhost:8000/docs にアクセスすると、定義されている API が文書化された Swagger UI を確認することができます。ここでは各 API の処理をテストすることもできますので、挙動に問題がないことを確かめてください。

## 3. 終わりに

本章ではモックのデータベースを用いて、REST API をどのように FastAPI で実装すればよいか確認しました。今回のモックのデータベースはインメモリであり、サーバーを落としてしまえばデータが消えてしまい、永続性がありません。そこで次章では RDB を用いて、より実践的なアプリケーションの構築を行います。
