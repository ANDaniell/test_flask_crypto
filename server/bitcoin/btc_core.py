import os

from bipwallet.utils import *

def gen_seed():
    from bipwallet import wallet

    # generate 12 word mnemonic seed
    seed = wallet.generate_mnemonic()
    return seed

def gen_address(index):
    # Ваша seed фраза
    seed = 'inhale eager parrot choose weapon section kidney danger entire patrol exhaust evolve'
    # Мастер ключ из seed фразы
    master_key = HDPrivateKey.master_key_from_mnemonic(seed)
    # public_key из мастер ключа по пути 'm/44/0/0/0'
    root_keys = HDKey.from_path(master_key, "m/44'/0'/0'/0")[-1].public_key.to_b58check()
    # Extended public key
    xpublic_key = str(root_keys)
    # Адрес дочернего кошелька в зависимости от значения index
    address = Wallet.deserialize(xpublic_key, network='BTC').get_child(index, is_prime=False).to_address()

    rootkeys_wif = HDKey.from_path(master_key, f"m/44'/0'/0'/0/{index}")[-1]

    # Extended private key
    xprivatekey = str(rootkeys_wif.to_b58check())

    # Wallet import format
    wif = Wallet.deserialize(xprivatekey, network='BTC').export_to_wif()

    return address, str(wif)

def gen_qr_wallet(address):
    import qrcode as qrcode
    img = qrcode.make(address)
    folder_path = os.path.abspath(os.path.dirname(__file__)).split('server')[0]+'server\\static\\img\\'
    img.save(f'{folder_path}{address}.jpg')
    return f'{address}.jpg'

#print(gen_address(0))
if __name__ == '__main__':
    print()