# Telegram Bot Olshop
sell your product with this bot

### DEPEDENCIES
- create table schema `mysql -u root -p < schema.sql`
- install pipenv with `python3 -m pip install pipenv` 
- run `pipenv shell`
- run `pipenv install`
- run `python main` 

### env conf

create `.env` file on folder and write your config with this format 
```.env
DATABASE_USER=""
DATABASE_PW=""
DATABASE_HOST=""
DATABASE_DB=""
BOT_API = ''
```