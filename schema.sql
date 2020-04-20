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


CREATE TABLE complain_digipos(
    id INT NOT NULL AUTO_INCREMENT ,
    complain_id VARCHAR(100) NULL ,
    status VARCHAR(100) NULL DEFAULT 'unprogress' ,
    kabupaten VARCHAR(100) NULL ,
    telegram_id INT(20) NULL ,
    kecamatan VARCHAR(100) NULL ,
    id_outlet VARCHAR(100) NULL ,
    nama_outlet VARCHAR(100) NULL ,
    no_mkios VARCHAR(100) NULL ,
    no_pelanggan VARCHAR(100) NULL ,
    tgl_transaksi VARCHAR(100) NULL ,
    detail TEXT NULL ,
    pay_method VARCHAR(100) NULL ,
    versi_apk_dipos VARCHAR(100) NULL ,
    channel_lain VARCHAR(100) NULL ,
    photo VARCHAR(100) NULL ,
    chat_id VARCHAR(100) NULL ,
    message_id VARCHAR(100) NULL ,
    handler_user_id VARCHAR(100) NULL ,
    created TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);