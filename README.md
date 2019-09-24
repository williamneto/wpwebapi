## wpwebapi

An web api for sending and receiving messages on WhatsApp, based on [WebWhatsapp-Wrapper](https://github.com/mukulhase/WebWhatsapp-Wrapper)

## Anti-spam policy and bans

Whatsapp has a strong anti spam policiy wich ban numbers after signs of spam dissemination. Its highly recomended only send messages to contacts that have your number saved.

## Dependencies
- [WebWhatsapp-Wrapper](https://github.com/mukulhase/WebWhatsapp-Wrapper)
- [Flask](https://github.com/pallets/flask)

Take atention on the installation of WebWhatsappWrapper. It depends on Firefox and other packages like geckodriver to work properly.

## Getting started

With flask and WebWhatsapp-Wrapper dependencies solved you wil be able to run the webapp 

`python3 webapi.py`

With the local server runing you will nedd to login with  Whatsapp scaning a QR Code, like in the Whatsapp Web. After that you are ready to send and read messages, get contacts and chats, etc.

## Endpoints

These are the main api endpoints. All requests nedd a user parameter, what is an username used iternaly to store diferents profiles (multiple whatsapps logedin).

- **start_login/?user=username** - start the login process, returning the QR Code in b64 if not logedin and the status 2 if already logedin.
- **check_login/?user=username** - verify if the given user is logedin whatsapp
- **contacts/?user=username** - return all whatsapp contacts
- **chats/?user=username** - return all current chats
- **chat/<id>/?user=username** - return messages from a given chat. require the chat id
- **send/?user=username&number=target_number&message=text_to_send** - send a message to a contact, requires a target number formated as wpid (ex: +5521987452144@c.us) and the text content for the message
- **send_media/?user=username&number=target_number&url=media_url&caption=media_caption** - send a media file to a contact, requires a target number formated as wp id (ex: +5521987452144@c.us), url of the media to be sent (.png, .jpg, .mp3, .mp4, etc) and a caption
- **delete_chat/?user=username&wpid=chat_id** - delete a chat by its given id
- **check_number/?user=username&wpid=number_to_check** - check if a number is a valid whatsapp contact. Must be formated as wpid (ex: +5521987452144@c.us)
