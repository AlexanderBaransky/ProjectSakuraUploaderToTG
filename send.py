from telethon.sync import TelegramClient
import os
import sys

args = sys.argv

# Change these to needed values if you want to use saved profile
api_id = None
api_hash = None
phone = None

os.chdir('./vendor/lineage/build/tools/uploader')


if 'current.session' in os.listdir() and api_id and api_hash and phone:
    result = input('Do you want to use saved profile? (Y/N)\n>>> ')
    if result == 'N' or result == 'n':
        os.remove('current.session')
        api_id = input(
            'Enter account api_id\nTo get it go to my.telegram.org, log in > API development tools > fill needed fields\n>>> ')
        api_hash = input(
            'Enter account api_hash\nTo get it go to my.telegram.org, log in > API development tools\n>>> ')
        phone = input('Enter your account phone number\n>>> ')
    elif result == 'Y' or result == 'y':
        pass
else:
    api_id = input(
        'Enter account api_id\n'
        'To get it go to my.telegram.org, log in > API development tools > fill needed fields\n>>> ')
    api_hash = input('Enter account api_hash\nTo get it go to my.telegram.org, log in > API development tools\n>>> ')
    phone = input('Enter your account phone number\n>>> ')

client = TelegramClient('current-session', int(api_id), api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, code=input('Enter code sent to paired account\n>>> '))

chat = input('Enter chat link or public chat name\n>>> ')

print('Starting...')


device = None
build_date_temp = None
rom_status = None
rom_type = None
if 'OFFICIAL' in args[2] and 'VANILLA' in args[2]:
    device = args[2][40:-13]
    build_date_temp = args[2][26:-19 - len(device)]
    rom_status = 'Official'
    rom_type = 'Vanilla'
elif 'OFFICIAL' in args[2] and 'GAPPS' in args[2]:
    device = args[2][38:-13]
    build_date_temp = args[2][24:-19 - len(device)]
    rom_status = 'Official'
    rom_type = 'GApps'
elif 'OFFICIAL' in args[2] and 'MICROG' in args[2]:
    device = args[2][39:-13]
    build_date_temp = args[2][25:-19 - len(device)]
    rom_status = 'Official'
    rom_type = 'MicroG'
elif 'UNOFFICIAL' in args[2] and 'VANILLA' in args[2]:
    device = args[2][40:-15]
    build_date_temp = args[2][26:-21 - len(device)]
    rom_status = 'Unofficial'
    rom_type = 'Vanilla'
elif 'UNOFFICIAL' in args[2] and 'GAPPS' in args[2]:
    device = args[2][38:-15]
    build_date_temp = args[2][24:-21 - len(device)]
    rom_status = 'Unofficial'
    rom_type = 'GApps'
elif 'UNOFFICIAL' in args[2] and 'MICROG' in args[2]:
    device = args[2][39:-15]
    build_date_temp = args[2][25:-21 - len(device)]
    rom_status = 'Unofficial'
    rom_type = 'MicroG'

build_date = build_date_temp[6:] + '/' + build_date_temp[4:-2] + '/' + build_date_temp[:-4]
version = args[2][14:-(len(args[2])-17)]
android_version = version[2:]

text = f'<b>Project Sakura {version}</b>\n\n' \
       f'<b>Android:</b> {android_version}\n' \
       f'<b>Device:</b> {device}\n' \
       f'<b>Build date:</b> {build_date}\n' \
       f'<b>Status:</b> {rom_status}\n' \
       f'<b>Type:</b> {rom_type}'


def callback(current, total):
    print('Uploading... [{:.2%}]'.format(current/total))


rom = client.upload_file(args[1], progress_callback=callback)
md5 = client.upload_file(args[3], progress_callback=callback)

client.send_file(chat, [rom, md5], caption=text, parse_mode='HTML', progress_callback=callback)
