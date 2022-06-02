from distutils.command.build import build
from telethon import TelegramClient, events, Button
import requests
import os 
from config import*

bot = TelegramClient( 
    'github', api_id=config.API_ID, api_hash=config.API_HASH).start(bot_token =config.TOKEN ) 


# Comando /start
@bot.on(events.NewMessage(pattern='/start'))
async def dl(app: events.NewMessage.Event):
    await app.reply('Bienvenido a Github.App',
    # boton que ejecute el comando /help
    buttons=[
        [Button.inline('❕Ayuda❕', data='help')],
        [Button.inline('💰Donar💰', data='donar')],
        [Button.url('🤖 Desarrollador 🤖', 'https://t.me/JeanNetwork')],
    ])

# Comando data de boton /start
@bot.on(events.CallbackQuery(data='start'))
async def help(app: events.CallbackQuery.Event):
    await app.edit('Bienvenido a Github.App',
    buttons=[
        [Button.inline('❕Ayuda❕', data='help')],
        [Button.inline('💰Donar💰', data='donar')],
        [Button.url('🤖 Desarrollador 🤖', 'https://t.me/JeanNetwork')],
    ])


# Comando data de boton /help
@bot.on(events.CallbackQuery(data='help'))
async def help(app: events.CallbackQuery.Event):
    await app.edit('/dl [url] - Descarga el repositorio de la url dada.\n/repos [usuario] - Muestra repositorios del usuario dado.\n/search [termino] - Busca repositorios con la palabra dada.\n/user [usuario] - Muestra informacion del usuario dado.',
    buttons=[
        [Button.inline('⬅️Regresar', data='start')]
    ])

# Comando Help
@bot.on(events.NewMessage(pattern='/help'))
async def help(app: events.NewMessage.Event):
    await app.reply('/dl [url] - Descarga el repositorio de la url dada.\n/repos [usuario] - Muestra repositorios del usuario dado.\n/search [termino] - Busca repositorios con la palabra dada.\n/user [usuario] - Muestra informacion del usuario dado.')


# Comando Donar
@bot.on(events.NewMessage(pattern='/donar'))
async def dl(app: events.NewMessage.Event):
    await app.reply('Si gustas puedes ayudar al desarrollador con una pequeña donación. 👍🏻\n\nPulsa sobre el siguiente botón para dirigirte a mis métodos de pago 😁',
    buttons=[
        [Button.url('Donar', 'https://paynest.app/JeanPssss')]
    ])

# Comando data de boton /donar
@bot.on(events.CallbackQuery(data='donar'))
async def help(app: events.CallbackQuery.Event):
    await app.edit('Si gustas puedes ayudar al desarrollador con una pequeña donación. 👍🏻\n\nPulsa sobre el siguiente botón para dirigirte a mis métodos de pago 😁',
    buttons=[
        [Button.url('Donar', 'https://paynest.app/JeanPssss')],
        [Button.inline('⬅️Regresar', data='start')]
        

    ])


# Descargar repositorio pasando la url de el como argumento
@bot.on(events.NewMessage(pattern='/dl'))
async def repo(app: events.NewMessage.Event):
    msg = await app.reply('⏬Descargando...')
    repo_url = app.message.text.split(' ')[1]
    repo_name = repo_url.split('/')[-1]
    repo_name = repo_name.split(".")[0]
    
    url = 'https://api.github.com/repos/' + repo_url.split('/')[-2] + '/' + repo_name + '/zipball'
    reponse = requests.get(url)
    if reponse.status_code == 200:
        file = open(repo_name + '.zip', 'wb')
        file.write(reponse.content)
        file.close()
        await msg.delete()
        await bot.send_file(app.chat.id, repo_name + '.zip')
        os.remove(repo_name + '.zip')
    else:
        await msg.edit('‼️Error en la descarga‼️')


#Obtener todos los repositorios de un perfil pasandole como argumento el nombre de usuario
@bot.on(events.NewMessage(pattern='/repos'))
async def repos(app: events.NewMessage.Event):
    msg = await app.reply('🔍Analizando...')
    repo = app.message.text.split(' ')[1]
    r = requests.get(f'https://api.github.com/users/{repo}/repos')
    if r.status_code == 200:
        if r.json() == []:
            await msg.edit('‼️El usuario no tiene repositorios‼️')
        else:
            await msg.delete()
            for i in range(20):
                await msg.delete()
                await app.reply(f'🔖:{r.json()[i]["name"]}\n📦:{r.json()[i]["html_url"]}')
    else: 
        await msg.edit('💢Usuario no encontrado💢')


#Obtener información de un perfil pasandole el usuario como argumento
@bot.on(events.NewMessage(pattern='/user'))
async def user(app: events.NewMessage.Event):
    msg = await app.reply('🔍Analizando...')
    user = app.message.text.split(' ')[1]
    r = requests.get('https://api.github.com/users/' + user)
    if r.status_code == 200:
        await msg.delete()
        await app.reply(f'🔖 Nombre: {r.json()["name"]}\n\n🫂 Siguiendo: {r.json()["following"]}\n\n👥 Seguidores: {r.json()["followers"]}\n\n📦 Repositorios: {r.json()["public_repos"]}\n\n🔗 URL: {r.json()["html_url"]}')
        

#Buscar repositorios pasando como argumento el termino de busqueda
@bot.on(events.NewMessage(pattern='/search'))
async def search(app: events.NewMessage.Event):
    msg = await app.reply('🔍Analizando...')
    repo = app.message.text.split(' ')[1]
    r = requests.get(f'https://api.github.com/search/repositories?q={repo}')
    if r.status_code == 200:
        if r.json()['total_count'] == 0:
            await msg.edit('💢No se encontraron resultados💢')
        else:
            for i in range(20):
                await msg.delete()
                await app.reply(f'{r.json()["items"][i]["name"]} - {r.json()["items"][i]["html_url"]}')
    else:
        await msg.edit('💢Error💢')






print('App Run...')
bot.loop.run_forever()