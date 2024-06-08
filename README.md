# Задание второго спринта

## Полезные ссылки 

- https://labs.play-with-docker.com/ - рекомендую, можно попробовать развернуть кластер.
- https://docs.portainer.io/v/ce-2.9/start/install/server/swarm/linux
- https://docs.docker.com/engine/install/ubuntu/

# Терминология Swarm
- **Node** - это наши виртуальные машины, на которых установлен docker. Есть manager и workers ноды. Manager нода управляет workers нодами. Она отвечает за создание/обновление/удаление сервисов на workers, а также за их масштабирование и поддержку в требуемом состоянии. Workers ноды используются только для выполнения поставленных задач и не могут управлять кластером.
- **Stack** - это набор сервисов, которые логически связаны между собой. По сути это набор сервисов, которые мы описываем в обычном compose файле. Части stack (services) могут располагаться как на одной ноде, так и на разных.
- **Service** - это как раз то, из чего состоит stack. Service является описанием того, какие контейнеры будут создаваться. Если вы пользовались docker-compose.yaml, то уже знакомы с этой сущностью. Кроме стандартных полей docker в режиме swarm поддерживает ряд дополнительных, большинство из которых находятся внутри секции deploy.
- **Task** - это непосредственно созданный контейнер, который docker создал на основе той информации, которую мы указали при описании service. Swarm будет следить за состоянием контейнера и при необходимости его перезапускать или перемещать на другую ноду.


```shell
docker swarm init
```

Если используется https://labs.play-with-docker.com/ там локальные ip и нужно указывать в явном виде:

```shell
docker swarm init --advertise-addr 192.168.0.13
```

На остальных нодах запускаем, команду, которая будет после выполнения init, например:

```shell
docker swarm join --token SWMTKN-1-211klil7va9ext75b5ga4kcruewo387a7d0yy1wc336yund2in-4d2k0vuihl8vv305mc5y080oe 188.120.246.20:2377
```


Установка Portainer для управления кластером. 
- `curl -L https://downloads.portainer.io/portainer-agent-stack.yml -o portainer-agent-stack.yml`
- `docker stack deploy -c portainer-agent-stack.yml portainer`


Полезные команды:

`docker stack services portainer` или `docker stack services django` - покажет все сервисы стека portainer или django

docker stack rm portainer - удалит стек

**docker swarm init --advertise-addr 192.168.0.13**

**docker node ls**

**docker node rm node3**

**docker swarm join-token worker**

**docker stack deploy -c stack.yaml django**

**docker stack ls**

**docker stack services django**

**docker service ls**

**docker service ps django_api**

**docker stack rm django**

**curl -L https://downloads.portainer.io/portainer-agent-stack.yml -o portainer-agent-stack.yml**

**docker stack deploy -c portainer-agent-stack.yml portainer**

**docker stack services portainer**

**docker stack rm portainer**


# Задание первого спринта

В консоли можно просмотреть список допустимых команд:

```bash
> make help

admin                          create admin user
compile-trans                  compile translations
django-makemigrations          apply migrations
django-migrate                 apply migrations
help                           Help
make-trans                     make translations
start-app                      start dev server
start-db                       start postgres
stop-db-clear                  stop postgres and clear all
transfer-data                  transfer data from sqlite

```

Запутить весь пайплайн можно командой:

```bash
make start-all
```

Выполнятся следующие команды `install-pip start-db wait_to_db transfer-data django-migrate admin start-app`

- Будут установлены зависимости
- Запустится контейнер с базой данных
- Скрипт ожидание запуска БД, иначе данные не перенесутся и миграции не применятся
- Будет осуществлен перенос данных из sqlite
- Применятся миграции Django
- Будет создан суперпользователь `admin/123123`
- Будет запущено приложение

http://127.0.0.1:8000/admin

![admin-panel.png](images/admin-panel.png)
