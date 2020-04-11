DROP DATABASE IF EXISTS bot_telegram;
CREATE DATABASE IF NOT EXISTS bot_telegram;
USE bot_telegram;
CREATE TABLE user(
    telegram_id INT(20) PRIMARY KEY ,
    telegram_username VARCHAR(150) NOT NULL ,
    kabupaten VARCHAR(150) NOT NULL ,
    kecamatan VARCHAR(150) NOT NULL ,
    nama_outlet VARCHAR(150) NOT NULL ,
    nomor_mkios BIGINT(30) NOT NULL ,
    tgl_registrasi TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orderan(
    id INT NOT NULL AUTO_INCREMENT ,
    pack_id INT(20) NULL ,
    telegram_id INT(20) NOT NULL ,
    bot_message_id INT(20) NULL ,
    status BOOLEAN NOT NULL DEFAULT FALSE ,
    kode_barang VARCHAR(150) NOT NULL ,
    qty INT NOT NULL ,
    tgl_beli TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

# CREATE TABLE product(
#     id INT NOT NULL AUTO_INCREMENT ,
#     nama INT(20) NOT NULL ,
#     status BOOLEAN NOT NULL DEFAULT FALSE ,
#     kode_barang VARCHAR(150) NOT NULL ,
#     qty INT NOT NULL ,
#     tgl_beli TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY (id)
# );