# -*- coding: utf-8 -*-
import os
import os.path
import urllib.request
import shutil
import base64
from webwhatsapi.objects.chat import GroupChat
from random import randint
from driver.storage import DriversStorage

HOST = "http://127.0.0.1:5000/"

# Main class that handle the comunications with WhatsApp
class WPDriver:
    def __init__(self):
        self.drivers_storage = DriversStorage()

    # Start driver
    def start(self, user):
        driver = self.drivers_storage.new(user)

        return driver

    # Close driver
    def close(self, user):
        driver = self.drivers_storage.get(user)
        driver["obj"].close()

    # Start the login process, return the QR Code if
    # not logedin and the status 2 if already logedin
    def start_login(self, user):
        driver = self.drivers_storage.get(user)
        response = {}

        loaded = False
        i = 0
        while not loaded:
            i += 1
            if i >= 4:
                loaded = True
                response["status"] = 0
            try:
                response["status"] = 2
                if not driver["obj"].get_status() == "LoggedIn":
                    b64 = driver["obj"].get_qr_base64()
                    loaded = True

                    response["qr_code"] = b64
                    response["status"] = 1

            except:
                print("exception")

        return response

    # Check if is logedin
    # Logedin: status = 2
    # Not logedin: status = 3 or 4
    def check_login(self, user):
        driver = self.drivers_storage.get(user)
        response = {}

        response["status"] = 4
        if driver is not None:
            loaded = False

            while not loaded:
                try:
                    response["status"] = 3
                    if driver["obj"].get_status() == "LoggedIn":
                        response["status"] = 2
                    loaded = True
                    driver["obj"].save_firefox_profile()
                except:
                    continue

        return response

    # Return al contacts ( not chats )
    def get_contacts(self, user):
        driver = self.drivers_storage.get(user)
        response = {}

        response["status"] = 4
        if driver is not None:
            retry = True
            while retry:
                try:
                    contact_objs = driver["obj"].get_contacts()
                    retry = False
                except:
                    continue

            def get_contact_with_image(contact):
                contact = {"id": obj.id, "safe_name": obj.get_safe_name(), "img": None}

                try:
                    contact["img"] = contact.profile_pic
                except:
                    pass

                return contact

            contacts = list(map(get_contact_with_image, contact_objs))

            response["contacts"] = contacts

        return response

    # Return all open chats on device
    def get_all_chats(self, user):
        driver = self.drivers_storage.get(user)
        response = {}

        response["status"] = 4
        response["drivers"] = str(self.drivers_storage.drivers)
        if driver is not None:
            retry = True
            while retry:
                try:
                    chats_objs = driver["obj"].get_all_chats()
                    retry = False
                except:
                    continue

            def get_chat_obj(chat):
                name = driver["obj"].get_contact_from_id(c.id).get_safe_name()
                unreads = driver["obj"].get_unread_messages_in_chat(
                    c.id, include_me=True, include_notifications=True
                )
                unreads = len(unreads)
                obj = {
                    "id": c.id,
                    "name": name,
                    "unreads": unreads,
                    "uri": "%schat/%s/?user=%s" % (HOST, c.id, driver["user"]),
                    "is_group": isinstance(c, GroupChat),
                }

                return obj

            chats = list(map(get_chat_obj, chats_objs))
            response["chats"] = chats
            response["status"] = 0

        return response

    # Get an especific chat by id
    # Limit parameter not working quite well
    def get_chat(self, user, chat_id, limit):
        driver = self.drivers_storage.get(user)
        response = {}

        if driver == None:
            response["status"] = 4
        else:
            retry = True
            while retry == True:
                try:
                    chat = driver["obj"].get_chat_from_id(chat_id)
                    messages_ids = driver["obj"].get_all_message_ids_in_chat(
                        chat, include_me=True
                    )
                    retry = False
                except:
                    continue

            messages_ids = messages_ids[-(limit):]

            messages = []
            for id in messages_ids:
                retry = True
                while retry == True:
                    try:
                        m = driver["obj"].get_message_by_id(id)
                        retry = False
                    except:
                        continue

                if m.type == "chat":
                    obj = {
                        "type": m.type,
                        "id": m.id,
                        "sender": m.sender.get_safe_name(),
                        "timestamp": m.timestamp,
                        "content": m.content,
                    }
                    messages.append(obj)
                if m.type == "audio":
                    try:
                        img_location = m.save_media("media/%s/" % driver["user"])
                    except:
                        pass
                    audio_url = "%smedia/%s/%s" % (HOST, driver["user"], m.filename)

                    # os.rename("media/%s/%s" % (driver["user"], m.filename), "media/%s/%s.mp3" % (driver["user"], m.filename))
                    obj = {
                        "type": m.type,
                        "id": m.id,
                        "sender": m.sender.get_safe_name(),
                        "timestamp": m.timestamp,
                        "content": audio_url,
                    }
                    messages.append(obj)
                if m.type == "image":
                    img_location = m.save_media("media/%s/" % driver["user"])
                    img_url = "%smedia/%s/%s" % (HOST, driver["user"], m.filename)

                    obj = {
                        "type": m.type,
                        "id": m.id,
                        "sender": m.sender.get_safe_name(),
                        "timestamp": m.timestamp,
                        "content": img_url,
                    }
                    try:
                        obj["caption"] = m.caption
                    except:
                        pass
                    messages.append(obj)
                if m.type == "video":
                    video_location = m.save_media("media/%s/" % driver["user"])
                    video_url = "%smedia/%s/%s" % (HOST, driver["user"], m.filename)

                    obj = {
                        "type": m.type,
                        "id": m.id,
                        "sender": m.sender.get_safe_name(),
                        "timestamp": m.timestamp,
                        "content": video_url,
                    }
                    try:
                        obj["caption"] = m.caption
                    except:
                        pass
                    messages.append(obj)

            chat = {
                "id": chat_id,
                "safe_name": driver["obj"].get_contact_from_id(chat_id).get_safe_name(),
            }

            response["chat"] = chat
            response["messages"] = messages
            response["status"] = 0

        return response

    # Get the profile pic of a contact by wpid
    # Not working yet
    def get_profile_pic(self, user, wpid):
        driver = self.drivers_storage.get(user)
        response = {}

        if driver == None:
            response["status"] = 4
        elif wpid:
            b64_pic = driver["obj"].get_profile_pic_from_id(wpid)
            # import pdb; pdb.set_trace()
            if isinstance(b64_pic, bool):
                response["profile_pic"] = b64_pic
            else:
                response["profile_pic"] = base64.b64encode(b64_pic).decode("ascii")
            response["status"] = 1

        return response

    # Delete a chat by its given id
    def delete_chat(self, user, wpid):
        driver = self.drivers_storage.get(user)
        response = {}

        if driver == None:
            response["status"] = 4
        elif wpid:
            status = driver["obj"].delete_chat(wpid)
            response["status"] = status

        return response

    # Send a message to the given number
    def send_message(self, user, number, message):
        driver = self.drivers_storage.get(user)
        response = {}

        if driver == None:
            response["status"] = 4
        elif number and message:
            if not number[-5] == "@":
                id = number + "@c.us"
            else:
                id = number
            retry = True
            while retry == True:
                try:
                    sent = driver["obj"].send_message_to_id(id, message)
                    retry = False
                except:
                    continue

            if sent:
                chat = self.get_chat(user, id, 1)
                message_finder = {
                    "id": chat["messages"][0]["id"],
                    "chat_id": chat["chat"]["id"],
                }
                response["message"] = message_finder
                response["status"] = 5

            else:
                response["status"] = 6
        else:
            response["status"] = 7

        return response

    # Send a media file to the given number
    def send_media(self, user, number, url, caption=""):
        driver = self.drivers_storage.get(user)
        response = {}

        if driver == None:
            response["status"] = 4
        elif number and url:
            file_name = url.split("/")[5]
            file_path = "./%s%s" % (driver["media_location"], file_name)

            urllib.request.urlretrieve(url, file_path)

            print(file_path)

            if not number[-5] == "@":
                id = number + "@c.us"
            else:
                id = number
            retry = True

            tries = 0
            while retry == True:
                print("Sending media...")
                tries += 1
                if tries == 3:
                    retry = False
                    sent = False

                try:
                    sent = driver["obj"].send_media(file_path, id, caption)
                    retry = False
                except:
                    continue

            if sent:
                chat = self.get_chat(user, id, 20)
                message_finder = {
                    "id": chat["messages"][0]["id"],
                    "chat_id": chat["chat"]["id"],
                }
                response["message"] = message_finder
                response["status"] = 5
            else:
                response["status"] = 6
        else:
            response["sta"]

        return response

    # Return all contacts from all groups
    def get_contacts_from_groups(self, user):
        driver = self.drivers_storage.get(user)
        response = {}

        if driver == None:
            response["status"] = 4
        else:
            chats = driver["obj"].get_all_chats()
            response["groups"] = []
            for chat in chats:
                contacts = []
                if isinstance(chat, GroupChat):
                    participants = chat.get_participants()
                    for p in participants:
                        contacts.append(
                            {"name": p.get_safe_name(), "number": p.id.split("@")[0]}
                        )

                    response["groups"].append(
                        {
                            "name": chat.name,
                            "participants_count": len(contacts),
                            "contacts": contacts,
                        }
                    )

        return response

    # Get the status of a message by the given message id
    def get_sended_message_status(self, user, message_id):
        driver = self.drivers_storage.get(user)
        response = {}

        if driver == None:
            response["status"] = 4
        elif message_id:
            message = driver["obj"].get_message_by_id(message_id)
            if not isinstance(message, bool):
                status = message._js_obj["ack"]
            else:
                status = -1

            status_str = ""
            if status == -1:
                status_str = "Mensagem não encontrada no dispositivo"
            if status == 0:
                status_str = "Mensagem não enviada"
            elif status == 1:
                status_str = "Mensagem enviada"
            elif status == 2:
                status_str = "Mensagem entregue"
            elif status == 3:
                status_str = "Mensagem lida"

            response["message"] = {
                "id": message_id,
                "status": status,
                "status_str": status_str,
            }
            response["status"] = 2
        else:
            response["status"] = "Falha"

        return response

    # Check if the given wpid is a valid whatsapp contact
    def check_number(self, user, wpid):
        driver = self.drivers_storage.get(user)
        response = {"status": 1}

        check = driver["obj"].check_number_status(wpid)
        if check.status == 200:
            response["is_wp"] = True
        else:
            response["is_wp"] = False

        return response

    # Get data from a recently sended message in a chat
    def reg_sent(self, user, chat_id):
        driver = self.drivers_storage.get(user)
        reg = {}
        try:
            chat = driver["obj"].get_chat_from_id(chat_id)
            messages_ids = driver["obj"].get_all_message_ids_in_chat(chat)

            if len(messages_ids) > 1:
                i = len(messages_ids) - 1
            elif len(messages_ids) == 1:
                i = 0
            else:
                i = -1
            # import pdb; pdb.set_trace()
            if i >= 0:
                msg = driver["obj"].get_message_by_id(messages_ids[i])

                if (
                    msg.sender.get_safe_name() == "You"
                    or msg.sender.get_safe_name() == "Voc"
                ):
                    reg["id"] = messages_ids[i]
                    reg["chat_id"] = chat_id

            # import pdb; pdb.set_trace()
        except Exception:
            pass

        return reg
