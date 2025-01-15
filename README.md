  Папка service1 описывает grpc-сервис, который описывает взаимодействие между gateway-сервисом и grpc-сервером.
  В папке service1 лежит Dockerfile, по которому создается в дальнейшем контейнер grpc_server внутри docker-compose.yml.
  В папке service1 лежит requirements.txt, описывающий используемые библиотеки, необходимые для работы данного сервиса. Эти библиотеки автоматически устанавливаются в docker'e благодаря Dockerfile.
  В файле service1/DBConnection.py описывается:
    1. класс, используемый для взаимодействия с базой данных PostgreSQL; 
    2. функция work_with_db используется для возвращения результата select-запроса, отправленного в PostgreSQL; 
    3. функция make_update используется для отправки в базу данных запросов типа delete, update, create и т.д., то есть запросов без значимого возращаемого результата.   
  В файле service1/sql_provider.py описывается класс, который принимает на вход папку со всеми sql-запросами (в данном случае blueprint/sql) и имеет возможность брать из оной нужный файл с sql-запросом (например, blueprint/sql/add_user.sql).
  В файле service1/docker-compose.yml описывается поднятие сервисов grpc_server, gateway по их Dockerfile, базы данных PostgreSQL, redis, их очередность, а также сети network, необходимой для общения всего перечисленного между друг другом внутри docker.
  
  В папке service1/config_for_redis находится файл redis.conf, необходимый для инициалиазации redis внутри docker'a.
  В папке service1/init_db_postgresql находится файл init.sql, необходимый для инициалиазации PostgreSQL внутри docker'a. Он поднимает таблицы roles и users.

  В папке service1 лежит requirements.txt, описывающий используемые библиотеки, необходимые для работы данного сервиса. Эти библиотеки автоматически устанавливаются в docker'e благодаря Dockerfile.

  Директория service1/sql содержит все запросы, которые используются для взаимодействия с базой данных PostgreSQL.
  
  Директория blueprint/generated содержит в себе файлы, генерируемые при запуске:
    python3 -m grpc_tools.protoc --proto_path=blueprint/proto \
            --python_out=blueprint/generated \
            --grpc_python_out=blueprint/generated \
            blueprint/proto/*.proto
    по входящему Protobuffer файлу proto/users.proto, описывающий grpc-сервис.
    
  Файл blueprint/__main__.py необходим для запуска grpc-сервиса. В него импортируется класс Server, описывающий grpc-сервер (внутри класса также происходит запуск этого сервера с таким-то host и с таким-то port).
  Файл blueprint/__init__.py используется для инициализации redis и provider, описанного выше.
  Файл blueprint/app.py описывает grpc-сервер, упомянутый выше.

  Файл blueprint/functions.py описывает "дополнительные" функции, используемые в grpc.py, а именно:
  1. get_users, которая в зависимости от флага берет данные из кэша redis или напрямую из базы данных;
  2. make_response для генерации окончательного ответа grpc-сервиса fastapi.

  Файл blueprint/grpc.py описывает класс UsersSer, наследованный от UsersServices, ручки которого были описаны в файле blueprint/proto/users.proto да и сам сервис описан там же.

  Для работы docker-compose.yml папки service1 и service2 должны находиться в одной директории.
