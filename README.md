# Pixochi

Пиксельный вариант игры 
Тамагочи

### Тестирование

Запустить тесты:

```
cd pixochi-main
./manage.py test
```

### MySQL

Первичная настройка MySQL:

```
cd pixochi-main

# install python packages
pip3 install -r requirements.txt

# install dependencies
sudo apt-get install mysql-server mysql-client
sudo apt-get install python3-dev libmysqlclient-dev build-essential

# run mysql cli
mysql -u root -p

# inside mysql cli
CREATE DATABASE api DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE USER django@localhost IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON api.* TO django@localhost;
GRANT ALL PRIVILEGES ON *.* TO django@localhost;
FLUSH PRIVILEGES;
```