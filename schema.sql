CREATE DATABASE IF NOT EXISTS bot_telegram;
USE bot_telegram;
CREATE TABLE IF NOT EXISTS user(
    telegram_id INT(20) PRIMARY KEY ,
    telegram_username VARCHAR(150) NOT NULL ,
    kabupaten VARCHAR(150) NOT NULL ,
    kecamatan VARCHAR(150) NOT NULL ,
    nama_outlet VARCHAR(150) NOT NULL ,
    nomor_mkios INT(20) NOT NULL ,
    tgl_registrasi DATE NOT NULL
)