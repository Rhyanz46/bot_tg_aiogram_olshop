from aiogram import types


async def voucer_fisik_complain_format_model_handler(message: types.Message, state, reset_proxy, default_proxy):
    from core import regex_special_character, is_registered, User
    from complain import upload_bukti_ask
    registered: User = await is_registered(
        message.from_user.id
    )
    if not registered.ok:
        await message.reply(
            "Sorry, Kamu Belum Terdaftar 😝",
            reply_markup=types.ReplyKeyboardRemove()
        )
    async with state.proxy() as proxy:
        await default_proxy(proxy, addtions={
            'complain_vf_kabupaten': None,
            'complain_vf_kecamatan': None,
            'complain_vf_nama_outlet': None,
            'complain_vf_id_digipos_outlet': None,
            'complain_vf_nomor_pelanggan': None,
            'complain_vf_serial_number': None,
            'complain_vf_tgl_inject_voucher': None,
            'complain_vf_paket': None,
            'complain_vf_masalah': None,
            'complain_photo_require': False,
            'complain_photo': None,
            'complain_vf_valid': None
        })
        # print(message.text)
        data: list = message.text.split('\n')
        search_data: list = message.text.lower().split('\n')
        pertanyaan: list = [
            'kabupaten',
            'kecamatan',
            'nama outlet',
            'id digipos outlet',
            'nomor pelanggan',
            'serial number',
            'tanggal inject voucher',
            'paket',
            'masalah'
        ]
        valid: list = []
        if not proxy['complain_vf_valid']:
            for index, item in enumerate(data):
                if 'kabupaten :' in search_data[index]:
                    kabupaten = item.replace('Kabupaten : ', '')
                    if regex_special_character.search(kabupaten):
                        karakter = kabupaten[regex_special_character.search(kabupaten).span()[0]]
                        return await message.answer(f"Kabupaten tidak boleh memiliki special karakter {karakter}")
                    if len(kabupaten.strip()) > 149:
                        return await message.answer(f"Kabupaten tidak boleh lebih dari 149 karakter")
                    valid.append('kabupaten')
                    proxy["complain_vf_kabupaten"] = kabupaten.strip().lower()
                if 'kecamatan :' in search_data[index]:
                    kecamatan = item.replace('Kecamatan : ', '')
                    if len(kecamatan.strip()) > 149:
                        return await message.answer(f"Kecamatan tidak boleh lebih dari 149 karakter")
                    valid.append('kecamatan')
                    proxy["complain_vf_kecamatan"] = kecamatan.strip().lower()
                if 'nama outlet :' in search_data[index]:
                    nama_outlet = item.replace('Nama Outlet : ', '')
                    if len(nama_outlet.strip()) > 149:
                        return await message.answer(f"Nama Outlet : tidak boleh lebih dari 149 karakter")
                    valid.append('nama outlet')
                    proxy["complain_vf_nama_outlet"] = nama_outlet.strip()
                if 'id digipos outlet :' in search_data[index]:
                    id_digipos_outlet = item.replace('ID Digipos Outlet : ', '')
                    if len(id_digipos_outlet.strip()) > 29:
                        return await message.answer(f"ID Digipos Outlet tidak boleh lebih dari 29 karakter")
                    try:
                        id_digipos_outlet = int(id_digipos_outlet.strip())
                    except:
                        return await message.answer("id digipos outlet harusnya berupa nomor")
                    valid.append('id digipos outlet')
                    proxy["complain_vf_id_digipos_outlet"] = id_digipos_outlet
                if 'nomor pelanggan :' in search_data[index]:
                    nomor_pelanggan = item.replace('Nomor Pelanggan : ', '')
                    if len(nomor_pelanggan.strip()) > 29:
                        return await message.answer(f"Nomor Pelanggan tidak boleh lebih dari 29 karakter")
                    try:
                        nomor_pelanggan = int(nomor_pelanggan.strip())
                    except:
                        return await message.answer("Nomor Pelanggan harusnya berupa nomor")
                    valid.append('nomor pelanggan')
                    proxy["complain_vf_nomor_pelanggan"] = nomor_pelanggan
                if 'serial number (12digit) :' in search_data[index]:
                    serial_number = item.replace('Serial Number (12Digit) : ', '')
                    if len(serial_number.strip()) > 29:
                        return await message.answer(f"Serial Number tidak boleh lebih dari 29 karakter")
                    try:
                        serial_number = int(serial_number.strip())
                    except:
                        return await message.answer("Serial Number harusnya berupa nomor")
                    valid.append('serial number')
                    proxy["complain_vf_serial_number"] = serial_number
                if 'tanggal inject voucher :' in search_data[index]:
                    tanggal_inject_voucher = item.replace('Tanggal Inject Voucher : ', '')
                    if len(tanggal_inject_voucher.strip()) > 149:
                        return await message.answer(f"Tanggal Inject Voucher  : tidak boleh lebih dari 149 karakter")
                    valid.append('tanggal inject voucher')
                    proxy["complain_vf_tgl_inject_voucher"] = tanggal_inject_voucher.strip()
                if 'paket :' in search_data[index]:
                    paket = item.replace('Paket : ', '')
                    if len(paket.strip()) > 149:
                        return await message.answer(f"Paket tidak boleh lebih dari 149 karakter")
                    valid.append('paket')
                    proxy["complain_vf_paket"] = paket.strip()
                if 'masalah :' in search_data[index]:
                    masalah = item.replace('Masalah : ', '')
                    if len(masalah.strip()) > 149:
                        return await message.answer(f"Masalah tidak boleh lebih dari 149 karakter")
                    valid.append('masalah')
                    proxy["complain_vf_masalah"] = masalah.strip()
            proxy['complain_vf_valid'] = 'harus_pilih_tombol'
            if pertanyaan == valid:
                return await upload_bukti_ask(message)
            return await message.answer(
                "GAGAL, harus ada spasi di antar titik dua `(:)` atau mungkin anda tidak memasukkan info yang lengkap",
                reply_markup=types.ReplyKeyboardRemove()
            )
        elif proxy['complain_vf_valid'] == 'harus_pilih_tombol':
            return await message.answer(
                "[PERINGATAN] Pilih opsi !!",
                reply_markup=types.ReplyKeyboardRemove()
            )
        return await message.answer(
            "Terimakasih",
            reply_markup=types.ReplyKeyboardRemove()
        )
