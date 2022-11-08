#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position

# lib for work with trans audio to text and some OS stuff
import os
import speech_recognition as sr
from lib import get_large_audio_transcription

# libs for TG bot's work
from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters

TOKEN = ":"
whitelist_id = ['', '']   # my dudes

# creating folders
folder_names = ["audio-chunks", "audio-raw"]
for folder in folder_names:
    if not os.path.isdir(folder):
        os.mkdir(folder)

path = "audio-raw/audio.ogg"
r = sr.Recognizer()


# fun for main (and one!) handler
def get_voice(update: Update, context: CallbackContext) -> None:
    # check users - is it in witeliste?
    if str(update.message.chat_id) in whitelist_id:
        new_file = context.bot.get_file(update.message.voice.file_id)
        new_file.download(path)
        text = str(get_large_audio_transcription(path, r))

        if text != "":
            print("Send text message to:", update.message.chat_id)
            context.bot.send_message(str(update.message.chat_id),
                                     text)
        else:
            print("Message is empty")
            exit
    else:
        context.bot.send_message(str(update.message.chat_id),
                                 "I will be the silence for you")


updater = Updater(TOKEN)

# Add handler for voice messages
updater.dispatcher.add_handler(MessageHandler(Filters.voice, get_voice))

updater.start_polling()
updater.idle()
