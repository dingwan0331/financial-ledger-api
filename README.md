# financial-ledger-api

가계부 api 시스템입니다.

# 주요 기술 및 버젼

python = 3.9
Django = 4.1.4
mysql = 5.7
redis = alpine (도커 이미지)
docker-compose = 1.29.2

# 프로젝트 실행방법

해당 프로젝트는 docker-compose를 활용하여 실행합니다.

### 1. sample.env의 안내에 따라 .env파일을 하여 줍니다.

.env폴더는 sample.env폴더와 같은 위치에 위치하여야 합니다.

### 2. 아래의 명령어를 통해 컨테이너를 실행합니다.

```
docker-compose up --build
```

### 3. 아래의 명령어를 통하여 python 컨테이너로 들어가 migrate를 수동으로 하여줍니다.

```
docker exec -it api /bin/bash

python manage.py migrate
```

### 주의 사항

- 13306, ,16379, 8000 포트가 이미 사용중일 시 실행이 안됩니다.
- .env에 한개의 key라도 부족할 시 KeyError가 납니다.

# 프로젝트 폴더 구조

### root

```
.
├── apps
├── ├── auth (django app dir)
├── ├── transaction (django app dir)
├── ├── url (django app dir)
├── └── util
├── config (django project dir)
├── manage.py
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .gitignore
```

- apps: 프로젝트에 사용되는 app들이 모여있습니다.
  - auth: 유저 + jwt토큰 관련 로직을 처리합니다.
  - transaction: 가계부와 관련된 로직을 처리합니다.
  - url: 단축 url과 관련한 로직을 처리합니다.
  - util: 프로젝트전반에 사용되는 모듈들이 모여있습니다.
- config: Django로 생성한 프로젝트 폴더입니다.

- auth, transactions앱에는 기본앱에 추가로 아래의 두가지 .py가 존재합니다.
  - manage.py: custom models.manage 클래스를 관리합니다.
  - dtos.py: 인스턴스를 생성하여 validate처리후 인스턴스를 반환하는 dto를 관리합니다.

### config

```
config
├── __init__.py
├── asgi.py
├── settings.py
├── urls.py
├── wsgi.py
├── env.py    #(1)
└── ddl.sql   #(2)
```

- env.py: .env에서 환경변수를 불러와 변수에 할당하여 관리합니다.
- ddl.sql: 프로젝트 모델링의 ddl 쿼리문입니다.

### apps

```
apps
├── auth
├── ├── auth (django app dir)
├── ├── transaction (django app dir)
├── ├── url (django app dir)
├── └── util
├── config (django project dir)
├── manage.py
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .gitignore
```

# 프로젝트 모델링

<img width="887" alt="image" src="https://user-images.githubusercontent.com/100751719/210061733-8fef65cf-255b-414a-aed2-c683e96343b7.png">

### 기본

- users 와 transactions 는 1:N관계를 형성합니다.
- created_at과 updated_at은 차후 인덱스 설정을위하여 FloatField를 사용하였으며 어플리케이션 단에서 unix_time으로 저장합니다.

### users 테이블

- password: 암호화 되어 byte로 저장되기에 longblob을 사용하였습니다.
- email: unique속성을 부여하였습니다.

### transactions 테이블

- deposit: 해당 날짜의 지출, 소득 금액을 의미합니다.(음수와 양수로 지출,소득을 구분합니다.)
- title: 가게부 목록에 노출될 간단한 메모 입니다.
- description: 상세 내용에 노출될 상세한 메모 입니다.

# JWT 로직

- 회원가입, 로그인을 제외한 모든 기능은 access_token을 요구합니다.
- 유저 로그인시 access_token 과 refresh_token을 발급 후
  - access_token 헤더의 Authrization에 담아 응답
  - refresh_token은 레디스에 refresh_token의 만료시간과 똑같은 expire설정으로 저장합니다.
- 유저 로그아웃시 해당토큰의 value를 logout으로 저장합니다.(만료시간은 access_token의 만료시간과 동일합니다.)
- 토큰 검증시 레디스를 조회하여 value가 logout으로 확인되면 유효하지않은 토큰으로 판단합니다.

# 프로젝트 기능

- body값 중 optional이 아닌 값이 없을시 400 key error를 반환합니다.
- 바디값이 json형식이 아닐시 400 Request body must be json를 반환합니다.

### 회원가입

- 엔드포인트

```
POST /users

request.body = {
    "email"   : "",
    "password : ""
}

Response

201 : {"message":"Created"},
      headers.Location = "/users/<int:user_id>"
400 : {
    "message":
        "Invalid password" |
        "Invalid email" |
        "Duplicated email"
    }
```

- 중복된 email은 회원가입이 불가능합니다.
- password는 영문, 숫자, 특수문자($@$!%\*#?&) 만 허용되며 최소 1개의 영문 1개의 숫자 1개의 특수문자를 조합하여 사용하여야 합니다.
- email은 올바른 형식의 email구조여야 합니다.

### 로그인

- 엔드포인트

```
POST /users/sign-in

request.body = {
    "email"   : "",
    "password : ""
}

Response

204 : headers.Authorization = aceess_token(jwt)
400 : {
    "message":
        "Invalid password" |
        "Invalid email" |
        "Sign up first"
    }
```

- 성공시 헤더에 Authrization으로 jwt 토큰을 반환합니다.
- 성공시 redis에 access_token:refresh_token을 key:value로 저장합니다.
  - 이때 redis 만료시간은 refresh_token의 만료시간과 동일합니다.
- 회원가입한 유저가 아닐 시 Sign up first 로 400에러를 반환합니다.

### 로그아웃

- 엔드포인트

```
POST /users/log-out

request.headers.Authorization = aceess_token(jwt)

Response

204 : No content
401 : { "message": "Invalid token" | "Expired token" }
```

- 로그아웃 성공시 204 status를 반환합니다.
- 헤더의 토큰이 없거나 잘못된 토큰일 시 Invalid token을 반환합니다.
- 만료된 토큰일 시 Expired token을 반환합니다.

### 토큰 재발급

- 엔드포인트

```
GET /users/token

request.headers.Authorization = aceess_token(jwt)

Response

204 : headers.Authorization = aceess_token(jwt)
401 : { "message": "Invalid token" }
```

- 로그아웃 성공시 204 status와 헤더에 새 access_token을 담아 반환합니다.
- 해당 access_token이 로그아웃처리된 token이면 Invalid token을 반환합니다.
- 해당 토큰에 상응하는 refresh_token이 없을 시 Invalid token을 반환합니다.

### 가계부 작성

- 엔드포인트

```
POST /transactions

request.body = {
    "deposit" : str(int),
    "title" : str length(20) -optianal,
    "discription" : str length(100) -optianal
}

request.headers.Authorization = aceess_token(jwt)

Response

201 : {"message":"Created"},
      headers.Location = "/transactions/<int:transaction_id>"
400 : {
    "message":
        "Invalid deposit" | "Invalid title" | "Invalid description"
    }
401 : { "message": "Invalid token" | "Expired token" }
```

- 성공시 헤더에 location을 답아 201 status코드를 반환합니다.
- title, description은 None으로 들어올시 공백의 문자열로 적용됩니다.

### 가계부 수정

- 엔드포인트

```
PATCH /transactions/<int:transaction_id>

request.body = {
    "deposit" : str(int),
    "title" : str length(20) -optianal,
    "discription" : str length(100) -optianal
}

request.headers.Authorization = aceess_token(jwt)

Response

204 : No content
400 : {
    "message":
        "Invalid deposit" | "Invalid title" | "Invalid description"
    }
401 : { "message": "Invalid token" | "Expired token" }
403 : { "message": "Don't have permission" }
404 : { "message": "Not found url" }
```

- deposit, title, description이 가능합니다.
- title, description은 optianal이지만 None으로 들어올시 공백의 문자열로 적용됩니다.
- 본인의 가계부가 아닌 다른 가계부에 수정시 403 에러를 반환합니다.
- path의 기재된 transaction_id에 해당하는 data가 없을시 404에러를 반환합니다.

### 가계부 삭제

- 엔드포인트

```
DELETE /transactions/<int:transaction_id>

request.headers.Authorization = aceess_token(jwt)

Response

204 : No content
401 : { "message": "Invalid token" | "Expired token" }
403 : { "message": "Don't have permission" }
404 : { "message": "Not found url" }
```

- 단일데이터 삭제기능만을 지원합니다.
- 성공시 204 status를 반환합니다.
- 본인의 가계부가 아닌 다른 가계부에 삭제시 403 에러를 반환합니다.
- path의 기재된 transaction_id에 해당하는 data가 없을시 404에러를 반환합니다.

### 가계부 세부 조회

- 엔드포인트

```
GET /transactions/<int:transaction_id>

request.headers.Authorization = aceess_token(jwt)

Response

200 : {
    "transaction":
        {
            "id"          : int
            "deposit"     : int,
            "title"       : str,
            "description" : str,
            "created_at"  : datetime,
            "updated_at"  : datetime
        }
    }
401 : { "message": "Invalid token" | "Expired token" }
403 : { "message": "Don't have permission" }
404 : { "message": "Not found url" }
```

- 본인의 가계부가 아닌 다른 가계부에 요청시 403 에러를 반환합니다.
- path의 기재된 transaction_id에 해당하는 data가 없을시 404에러를 반환합니다.

### 가계부 리스트 조회

- 엔드포인트

```
GET /transactions

request.query = {
    "order"             : "-created-at" | "created-at",
    "transsaction-type" : "income" | "expenditure" | "all",
    "offset"            : str(int),
    "limit"             : str(int)
}

request.headers.Authorization = aceess_token(jwt)

Response

200 : {
    "transactions":[
            {
                "id"         : int
                "deposit"    : int,
                "title"      : str,
                "created_at" : datetime,
            }
        ]
    }
400 : {
    "message":
        "Invalid offset" |
        "Invalid limit" |
        "Invalid transaction-type" |
        "Invalid order"
    }
401 : { "message": "Invalid token" | "Expired token" }
```

- 유저의 가계부 리스트를 조회하며 페이지네이션 기능, 최신순,오래된순 정렬 기능, 지출,소득 별 조회를 지원합니다..
- 성공시 pk, 거래금액, title, 작성시간으로된 객체 리스트를 반환합니다.
- request.query에 기재된 값이 아닌 쿼리가 들어올시 400에러를 반환합니다.
- request.query의 default값은 아래와 같습니다.

```
request.query = {
    "order"             : "-created-at",
    "transsaction-type" : "all",
    "offset"            : "0",
    "limit"             : "30"
}
```

### 가계부 임시 url 생성 엔드포인트

```
POST /urls/transactions/<int:transaction_id>

request.headers.Authorization = aceess_token(jwt)

Response

201 : { "signed_url" : signed_url ( ex) "urls/transactions/<uuid> ) },
headers.Location = "urls/transactions/<uuid>"
401 : { "message": "Invalid token" | "Expired token" }
403 : { "message": "Don't have permission" }
404 : { "message": "Not found url" }
```

- 가계부작성자 이외의 서비스회원이 볼 수 있는 임시 url을 생성하는 엔드포인트 입니다.
- 해당 path로 db 조회 후 임시url: 기존 url을 1시간 만료시간으로 레디스에 저장합니다.
- 가계부 작성자 본인만 요청 가능합니다.
- 해당 pk의 가계부가 없을 시 404에러를 반환합니다.
- url으 만료시간은 1시간입니다.
- 반환된 임시 url로 요청시 서비스회원이라면 누구든 사용할 수 있습니다.

### 가계부 임시 url로 가계부 조회 엔드포인트

```
GET /urls/transactions/<uuid:transaction_uuid>

request.headers.Authorization = aceess_token(jwt)

Response

200 : {
    "transaction":
        {
            "id"          : int
            "deposit"     : int,
            "title"       : str,
            "description" : str,
            "created_at"  : datetime,
            "updated_at"  : datetime
        }
    }
401 : { "message": "Invalid token" | "Expired token" }
404 : { "message": "Not found url" }
```

- 임시 url로 가계부를 조회하는 엔드 포인트 입니다.
- 해당 임시 url만료시 404 에러를 반환합니다.
- 해당 url은 서비스회원이면 누구든 조회가 가능합니다.

해당사항은 redirect로 구현하려했지만 시간부족으로 해당 엔드포인트에서 데이터를 반환하는식으로 처리하였습니다.

### 가계부의 세부 내역을 복제

해당사항은 가계부 조회시에 반환된 json을 그대로 사용하면 된다고 생각하여 구현하지 않았습니다.
