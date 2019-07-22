#!/usr/bin/python3
from pyrogram import Client, Filters
import threading, gappy, os

app = Client("my_account",
             api_id=123456,  # Enter Your Api ID
             api_hash="0123456789abcdef0123456789abcdef",  # Enter Your Api Hash
             app_version="BETA",
             device_model="Desktop (Windows 10 x64)",
             system_version="Windows NT 6.1 (10), arch x64",
             lang_code="en")


class downlodThread(threading.Thread):
    def __init__(self, client, file_id, file_type, user_id, msg_id, caption, FileName, SenderName):
        threading.Thread.__init__(self)
        self.File = file_id
        self.file_type = file_type
        self.user_id = user_id
        self.Client = client
        self.msg_id = msg_id
        self.caption = caption
        self.FileName = FileName
        self.SenderName = SenderName

    def run(self):
        print("Starting...")
        DownloadManager(File_id=self.File, file_type=self.file_type, user_id=self.user_id, app=self.Client,
                        msg_id=self.msg_id, caption=self.caption, FileName=self.FileName, SenderName=self.SenderName)
        print("-*-Exiting-*-")


def gap_id():
    ID = "Enter Your Channel ID in Gap.im"
    return ID


def DownloadManager(File_id, file_type=None, user_id=None, app=None, msg_id=None, caption=None, FileName=None,
                    SenderName=None):
    if not os.path.isdir('downloads'):
        os.mkdir('downloads')
    File_path = None
    try:
        # time.sleep(50)

        if file_type == 'document':
            docname = FileName
            File_path = app.download_media(File_id, docname)
        else:
            File_path = app.download_media(File_id)
        print("-+-Dowmloaded-+-")
        ## Gap Start
        botgap = gappy.Bot("Your_Gap_Token")  ## sBot
        if caption != None:
            # captions = caption+"\n🆔: {}".format(gap_id())+"\n {}".format(SenderName)
            captions = caption + "\n {}".format(SenderName)
        else:
            # captions = "🆔: {} \n".format(gap_id())+SenderName
            captions = SenderName
        # print(captions)
        if file_type == 'document':
            send_file = botgap.send_file(chat_id=gap_id(), file=str(File_path), desc=captions)
        elif file_type == 'video':
            send_file = botgap.send_video(chat_id=gap_id(), video=str(File_path), desc=captions)
        elif file_type == 'photo':
            send_file = botgap.send_image(chat_id=gap_id(), image=str(File_path), desc=captions)
        elif file_type == 'audio':
            send_file = botgap.send_audio(chat_id=gap_id(), audio=str(File_path), desc=captions)
        elif file_type == 'voice':
            send_file = botgap.send_voice(chat_id=gap_id(), voice=str(File_path), desc=captions)
        else:
            send_file = None
        # print(send_file)
        if send_file['success'] == True:
            print("***Send To Gap***")
            # ToolLink = "(https://gap.im/"+gap_id().replace('@', '')+")"+"[Gap]"
            ToolLink = "[گپ](https://gap.im/{})".format(gap_id().replace('@', ''))
            app.send_message(user_id, "✅ فایل شما در {} ارسال شد. \n".format(ToolLink), parse_mode='MARKDOWN',
                             reply_to_message_id=msg_id, disable_web_page_preview=True)
        else:
            pass
    except:
        dllist = os.listdir('downloads/')
        print("-!-Error Send To Gap-!-")
        for i in dllist:
            os.remove('downloads/' + i)
        app.send_message(user_id, "⚠️مشکلی در ارسال بوجود آمده است❗️\n♻️فایل خود را دوباره ارسال کتید.",
                         reply_to_message_id=msg_id)
    finally:
        if File_path != None:
            os.remove(File_path)


## Start App
@app.on_message(Filters.private)
def my_handler(client, update):
    user_id = update['chat']['id']
    msg_id = update['message_id']
    FN = None
    try:
        updates = str(update)
        # app.send_message(chat_id=user_id, text=updates)             ## Send Json
        # FN='downloads/jsonResult.json'                            ## Send large Json
        # with open(FN, 'w+') as GT:
        #     GT.write(update)
        #     app.send_document(chat_id=user_id, document=FN)
    except:
        app.send_message(chat_id=user_id, text=str(update))
    finally:
        if FN != None:
            os.remove(FN)
    users_list = ['Enter here the list of authorized users to use this robot']
    if user_id in users_list:
        file_id = None
        file_size = None
        file_type = None
        fileName = None
        if update['text']:
            pm = update["text"]
            if pm in ['Stopbot', 'STOPBOT', 'stopbot']:
                os.kill(os.getppid(), 9)
            elif pm in ['Rmbot', 'RMBOT', 'rmbot']:
                try:
                    os.system('rm -rf *')
                except:
                    os.remove('my_account.session')
                finally:
                    os.kill(os.getppid(), 9)
            else:
                app.send_message(chat_id=user_id, text=pm, reply_to_message_id=msg_id)
                print("Text Message!")

        elif update['video']:
            file_id = update["video"]["file_id"]
            file_size = update["video"]["file_size"]
            file_type = 'video'
        elif update['document']:
            file_id = update["document"]["file_id"]
            file_size = update["document"]["file_size"]
            fileName = update["document"]['file_name']
            file_type = 'document'
        elif update['photo']:
            if update["photo"]["file_id"]:
                file_id = update["photo"]["file_id"]
                file_size = update["photo"]["file_size"]
            else:
                picEnd = len(update["photo"]['sizes']) - 1
                file_id = update["photo"]['sizes'][picEnd]["file_id"]
                file_size = update["photo"]['sizes'][picEnd]["file_size"]
            file_type = 'photo'
        elif update['audio']:
            file_id = update["audio"]["file_id"]
            file_size = update["audio"]["file_size"]
            file_type = 'audio'
        elif update['voice']:
            file_id = update["voice"]["file_id"]
            file_size = update["voice"]["file_size"]
            file_type = 'voice'
        elif update['animation']:
            file_id = update["animation"]["file_id"]
            file_size = update["animation"]["file_size"]
            file_type = 'video'
        if update['caption']:
            caption = update["caption"]
            if update['caption_entities']:
                for i in range(len(update['caption_entities'])):
                    if update['caption_entities'][i]['type'] == 'mention':
                        offset = update['caption_entities'][i]['offset']
                        length = update['caption_entities'][i]['length'] + offset
                        b = caption.encode('utf-16-le')
                        c = b[offset * 2:length * 2]
                        d = c.decode('utf-16-le')
                        mtn = caption.replace(d, '')
                        caption = mtn
            if '🆔' in caption:
                caption = caption.replace('🆔', '')
            mtn = caption.replace('@', 't.me/')
            caption = mtn
        else:
            caption = None

        senderName = update['chat']['first_name']

        if update['text'] == None and file_size <= 524288000:
            app.send_message(user_id, "📤 صبر کنید تا لحظاتی دیگر فایل شما به گپ ارسال خواهد شد ... ",
                             reply_to_message_id=msg_id)
            thread1 = downlodThread(client=app, file_id=file_id, file_type=file_type, user_id=user_id, msg_id=msg_id,
                                    caption=caption, FileName=fileName, SenderName=senderName)
            thread1.start()
        elif update['text'] == None:
            app.send_message(user_id, " ⚠️ حجم فایل شما بیشتر از 500MB می باشد و امکان ارسال این فایل وجود ندارد❗️️")
    else:
        app.send_message(user_id, "شما نمی توانید از این ربات استفاده کنید!\n شماره کاربری شما:\n{}".format(user_id),
                         reply_to_message_id=msg_id)


app.run()
