from aiogram import types


async def registrasi_perdana_complain_format_model_handler(message: types.Message, state, reset_proxy, default_proxy):
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
            'complain_rp_msisdn_or_nomor_kartu': None,
            'complain_rp_nama_lengkap': None,
            'complain_rp_tempat_lahir': None,
            'complain_rp_tanggal_lahir': None,
            'complain_rp_nik': None,
            'complain_rp_no_kk': None,
            'complain_rp_valid': None,
            'complain_rp_photo_ktp': False,
            'complain_rp_photo_perdana': False,
        })
        # print(message.text)
        data: list = message.text.split('\n')
        search_data: list = message.text.lower().split('\n')
        pertanyaan: list = [
            'msisdn_or_nomor_kartu',
            'nama_lengkap',
            'tempat_lahir',
            'tanggal_lahir',
            'nik',
            'no_kk'
        ]
        valid: list = []
        if not proxy['complain_rp_valid']:
            for index, item in enumerate(data):
                if 'msisdn/nomor kartu :' in search_data[index]:
                    msisdn_or_nomor_kartu = item.replace('MSISDN/Nomor Kartu : ', '')
                    if regex_special_character.search(msisdn_or_nomor_kartu):
                        karakter = msisdn_or_nomor_kartu[regex_special_character.search(msisdn_or_nomor_kartu).span()[0]]
                        return await message.answer(f"MSISDN/Nomor Kartu tidak boleh memiliki special karakter {karakter}")
                    if len(msisdn_or_nomor_kartu.strip()) > 20:
                        return await message.answer(f"MSISDN/Nomor Kartu tidak boleh lebih dari 20 karakter")
                    try:
                        msisdn_or_nomor_kartu = int(msisdn_or_nomor_kartu.strip())
                    except:
                        return await message.answer("MSISDN/Nomor Kartu harusnya berupa nomor")
                    valid.append('msisdn_or_nomor_kartu')
                    proxy["complain_rp_msisdn_or_nomor_kartu"] = msisdn_or_nomor_kartu
                if 'nama lengkap :' in search_data[index]:
                    nama_lengkap = item.replace('Nama Lengkap : ', '')
                    if len(nama_lengkap.strip()) > 100:
                        return await message.answer(f"Nama Lengkap tidak boleh lebih dari 100 karakter")
                    valid.append('nama_lengkap')
                    proxy["complain_rp_nama_lengkap"] = nama_lengkap.strip().lower()
                if 'tempat lahir :' in search_data[index]:
                    tempat_lahir = item.replace('Tempat Lahir : ', '')
                    if len(tempat_lahir.strip()) > 100:
                        return await message.answer(f"Tempat Lahir : tidak boleh lebih dari 100 karakter")
                    valid.append('tempat_lahir')
                    proxy["complain_rp_tempat_lahir"] = tempat_lahir.strip()
                if 'tanggal lahir :' in search_data[index]:
                    tanggal_lahir = item.replace('Tanggal Lahir : ', '')
                    if len(tanggal_lahir.strip()) > 29:
                        return await message.answer(f"Tanggal Lahir Outlet tidak boleh lebih dari 29 karakter")
                    valid.append('tanggal_lahir')
                    proxy["complain_rp_tanggal_lahir"] = tanggal_lahir
                if 'nik :' in search_data[index]:
                    nik = item.replace('NIK : ', '')
                    if len(nik.strip()) > 29:
                        return await message.answer(f"NIK tidak boleh lebih dari 29 karakter")
                    try:
                        nik = int(nik.strip())
                    except:
                        return await message.answer("NIK harusnya berupa nomor")
                    valid.append('nik')
                    proxy["complain_rp_nik"] = nik
                if 'no kk :' in search_data[index]:
                    no_kk = item.replace('No KK : ', '')
                    if len(no_kk.strip()) > 29:
                        return await message.answer(f"No KK tidak boleh lebih dari 29 karakter")
                    try:
                        no_kk = int(no_kk.strip())
                    except:
                        return await message.answer("No KK harusnya berupa nomor")
                    valid.append('no_kk')
                    proxy["complain_rp_no_kk"] = no_kk
            proxy['complain_rp_valid'] = 'harus_pilih_tombol'
            if pertanyaan == valid:
                proxy['complain_rp_photo_ktp'] = True
                return await message.answer(
                    "Silahkan upload KTP.",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            return await message.answer(
                "GAGAL, Kirana Bingung, Format yang kamu masukkan salah,\n\n "
                "Pastikan kamu telah mengikuti sesuai dengan contoh yang kirana berikan ya",
                reply_markup=types.ReplyKeyboardRemove()
            )
        elif type(proxy['complain_rp_photo_ktp']) == bool and proxy['complain_rp_photo_ktp']:
            return await message.answer(
                "Upload Foto KTP !!",
                reply_markup=types.ReplyKeyboardRemove()
            )
        elif type(proxy['complain_rp_photo_perdana']) == bool and proxy['complain_rp_photo_perdana']:
            return await message.answer(
                "Upload Foto Kartu Perdana !!",
                reply_markup=types.ReplyKeyboardRemove()
            )
        return await message.answer(
            "Inputan tidak sesuai",
            reply_markup=types.ReplyKeyboardRemove()
        )
