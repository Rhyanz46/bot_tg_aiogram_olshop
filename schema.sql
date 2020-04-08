DROP DATABASE IF EXISTS bot_telegram;
CREATE DATABASE IF NOT EXISTS bot_telegram;
USE bot_telegram;
CREATE TABLE user(
    telegram_id INT(20) PRIMARY KEY ,
    telegram_username VARCHAR(150) NOT NULL ,
    kabupaten VARCHAR(150) NOT NULL ,
    kecamatan VARCHAR(150) NOT NULL ,
    nama_outlet VARCHAR(150) NOT NULL ,
    nomor_mkios VARCHAR(30) NOT NULL ,
    tgl_registrasi DATE NOT NULL
);

CREATE TABLE orderan(
    id INT NOT NULL AUTO_INCREMENT ,
    telegram_id INT(20) NOT NULL ,
    product_name VARCHAR(150) NOT NULL ,
    qty INT NOT NULL ,
    tgl_beli DATE NOT NULL ,
    PRIMARY KEY (id)
);
