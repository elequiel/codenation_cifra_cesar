import requests
import json
import hashlib

# load token
with open('.\\json_decode_auth.json', 'r') as token_file:
    load = json.load(token_file)
    token = load['token']

# Request dados do codenation
with requests.Session() as s:
    resp = s.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={}'.format(token))
    data = resp.json()

# Salva requsicao num arquivo JSON
with open('.\\answer.json', mode='w', encoding='utf8') as jsonfile:
    json.dump(data, jsonfile)

# Abre o JSON para trabalhar
with open('.\\answer.json', 'r') as json_file:
    dadosEnvio = json.load(json_file)
    enconding = json_file.encoding

# Funcao encriptar mensagem
def encrypt(texto_encrypt, key):

    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    cipher_text = ''
    texto_encrypt = texto_encrypt.upper()
    for ch in texto_encrypt:
        if ch in letters:
            idx = letters.find(ch) + key
            if idx >= 26:
                idx -= 26
            cipher_text += letters[idx]
    return cipher_text.lower()

# Funcao decriptar mensagem
def decrypt(texto_cifrado,  key):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    plain_text = ''
    texto_cifrado = texto_cifrado.upper()
    for ch in texto_cifrado:
        if ch in letters:
            idx = letters.find(ch) - key
            plain_text += letters[idx]
        else:
            plain_text += ch
    return plain_text.lower()

# Adicionar a mensagem decriptada ao JSON
dadosEnvio['decifrado'] = decrypt(dadosEnvio['cifrado'], dadosEnvio['numero_casas'])

# Cria o resumo Sha1
resumo = hashlib.sha1(dadosEnvio['decifrado'].encode(enconding)).hexdigest()
dadosEnvio['resumo_criptografico'] = resumo

# Salva o conteudo no arquivo resposta
with open('.\\answer.json', mode='w', encoding='utf8') as jsonfile:
    json.dump(dadosEnvio, jsonfile)

# Envia a resposta via POST para pagina solicitada
with requests.Session() as s:
    answer = {'answer': open('.\\answer.json', 'rb')}
    url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={}'.format(token)
    resp = s.post(url, files=answer)
