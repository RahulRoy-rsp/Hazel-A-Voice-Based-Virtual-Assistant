import ctypes
import os
import datetime
import speech_recognition as sr
import playsound
import pyttsx3
import webbrowser
import random
import time
# from googletranslation import Translator
from googletrans import Translator
from playsound import playsound
from word2number import w2n
import wikipedia
from lang_list import lan_2,lan_3
from f2 import *
import urllib.request
import re
from dno import email_list, api_key, api_secret_key, access_token_secret, access_token

# from fb import facebook

from em import send_email
from validate_email import validate_email
#from verify_email import verify_email
import tweepy

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0')
rate = engine.getProperty('rate')
engine.setProperty('rate', 250)

speech = sr.Recognizer()

wikipedia_dict = {"wikipedia:wikipedia"}
open_launch_dict = {'open': 'open', 'launch': 'launch'}
social_media_dict = {'facebook': 'https://www.facebook.com', 'twitter': 'https://www.twitter.com'}
chat_dict = {'chat': 'chat', "chatting": 'chatting', 'conversation': 'conversation'}
social_post_dict = {'post': 'post'}

google_searches_dict = {'what': 'what', 'why': 'why', 'who': 'who', 'which': 'which'}

translator = Translator()

t_engine = pyttsx3.init('sapi5')
t_voices = t_engine.getProperty('voices')
t_engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0')
t_rate = t_engine.getProperty('rate')
t_engine.setProperty('rate', 150)

c_engine = pyttsx3.init('sapi5')
c_voices = c_engine.getProperty('voices')
c_engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0')
c_rate = c_engine.getProperty('rate')
c_engine.setProperty('rate', 200)

sad_life = 0
talk = True

def t_speak(t_cmd):
    t_engine.say(t_cmd)
    t_engine.runAndWait()

def c_speak(c_cmd):
    c_engine.say(c_cmd)
    c_engine.runAndWait()

def speak(cmd):
    engine.say(cmd)
    engine.runAndWait()


def to_be_posted(voice_note):
    for key in social_media_dict.keys():
        if key in voice_note:
            return key


def get_key(val):
    for key, value in lan_3.items():
        if val == value:
            return key


def is_valid_google_search(phrase):
    if (google_searches_dict.get(phrase.split(' ')[0]) == phrase.split(' ')[0]):
        return True


def play_sound(mp3_list):
    mp3 = random.choice(mp3_list)
    playsound(mp3)


def greet_user():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("A very Good Morning to you!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon! lets make your day special . ")

    else:
        speak("Good Evening! i hope you having a good day . ")

    speak("I am Hazel . I am here to help you . You can ask me anything .")


def read_email_cmd():
    email_text = ''
    print('Listening... ')

    try:
        with sr.Microphone() as source:
            audio = speech.listen(source=source, timeout=7, phrase_time_limit=10)
        email_text = speech.recognize_google(audio)
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print('Network error.')
    except sr.WaitTimeoutError:
        pass
    return email_text


def read_voice_cmd():
    voice_text = ''
    print('Listening...')

    try:
        with sr.Microphone() as source:
            audio = speech.listen(source=source, timeout=10, phrase_time_limit=5)
        voice_text = speech.recognize_google(audio)
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        speak('''I could see that you have been disconnected to the internet
              Please connect with the internet''')
        print('Network error.')
    except sr.WaitTimeoutError:
        pass
    return voice_text


def is_valid_note(greet_dict, voice_note):
    for key, value in greet_dict.items():
        try:
            if value == voice_note.split(' ')[0]:
                return True
            elif key == voice_note.split(' ')[1]:
                return True
        except IndexError:
            pass
    return False


def youtube_search():
    print("What do you want me to search on youtube ?")
    speak("What do you want me to search on youtube ?")
    y_search = str(read_voice_cmd().lower())
    print(f"To be searched : {y_search}")
    print(f"Searching : {y_search} on Youtube . ")
    speak(f"Searching : {y_search} on Youtube . ")
    t_y_search = y_search.replace(" ", "")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + t_y_search)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    #print("https://www.youtube.com/watch?v=" + video_ids[0])
    webbrowser.open("https://www.youtube.com/watch?v=" + video_ids[0])
    speak("Here is your result")


def wiki_search():
    speak('what do you want me to search on wikipedia ?')
    wiki_search = str(read_voice_cmd().lower())
    print("wiki_search : " + wiki_search)
    con_wiki_search = wiki_search.replace(" ", "_")

    speak(f'''If you want me to tell you about {wiki_search} then give me command : Voice
                     and if you want me to open browser then give command : Browser''')
    wiki_style = str(read_voice_cmd().lower())
    print("wiki_style : " + wiki_style)
    if 'browser' in wiki_style:
        speak(f'Searching {wiki_search} on Wikipedia...')
        webbrowser.open('https://en.wikipedia.org/wiki/{}'.format(con_wiki_search))
        speak(f"here you got your result for {wiki_search}")

    elif 'voice' in wiki_style:
        # wiki_search = wiki_search.replace(" ", "")
        # print('v :'+wiki_search)
        speak(f"How many sentences should i say about {wiki_search}")
        no_of_sent = str(read_voice_cmd().lower())
        print('Sentence(s) : ' + no_of_sent)
        # conv_sent = w2n.word_to_num(no_of_sent)
        # print(conv_sent)
        speak("According to Wikipedia !")
        results = wikipedia.summary(con_wiki_search, sentences=no_of_sent)
        print(results)
        speak(results)

    else:
        er_ = "Please try to search again as i am not able to recognize your query "
        print(er_)
        speak(er_)


def tweet():
    print('What do you want me tweet on your timeline ?')
    speak('What do you want me tweet on your timeline ?')
    my_consumer_key = api_key
    my_consumer_secret = api_secret_key
    my_access_token = access_token
    my_access_token_secret = access_token_secret
    my_auth = tweepy.OAuthHandler(my_consumer_key, my_consumer_secret)
    # Authentication of access token and secret
    my_auth.set_access_token(my_access_token, my_access_token_secret)
    my_api = tweepy.API(my_auth)

    tweet_message = str(read_voice_cmd().lower())
    print(f"Tweeting : {tweet_message}")
    speak(f"Tweeting : {tweet_message}")
    my_api.update_status(tweet_message)
    print("Tweet has been tweeted succesfully !")
    speak("Tweet has been tweeted succesfully !")


if __name__ == "__main__":
    greet_user()

    while True:
        voice_read = read_voice_cmd().lower()

        print('cmd : {}'.format(voice_read))

        if 'wikipedia' in voice_read:
            wiki_search()
            continue

        elif is_valid_google_search(voice_read):
            speak(f" Searching : {voice_read}")
            print('in google search...')
            webbrowser.open('https://www.google.co.in/search?q={}'.format(voice_read))
            # google_search_result(voice_read)
            continue

        elif is_valid_note(open_launch_dict, voice_read):
            #speak(f"Opening : {voice_read}")
            print("Opening .....")
            if (is_valid_note(social_media_dict, voice_read)):
                key = voice_read.split(' ')[1]
                webbrowser.open(social_media_dict.get(key))
            else:
             #   speak(f"Opening : {voice_read}")
                w = str(format(voice_read.replace('open', '').replace('launch', '')))
                os.system(f'explorer C:\\{w.lstrip()}')
            continue

        elif is_valid_note(chat_dict, voice_read):
            print("IN CHATTING MODE")
            c_speak("okay ! lets begin !")
            print("okay ! lets begin !")
            while talk == True:
                # inp = input("You: ")
                inp = str(read_voice_cmd().lower())
                if inp.lower() == "quit":
                    # print(random.choice(bye_list))
                    bye_sp = random.choice(bye_list)
                    c_speak(bye_sp)
                    talk = False

                else:
                    results = model.predict([bag_of_words(inp, words)])[0]
                    results_index = numpy.argmax(results)
                    tag = labels[results_index]
                    # print(tag)

                    if tag == 'sad':
                        sad_life += 1

                    if sad_life < 3:
                        if results[results_index] > 0.5:
                            for tg in data["intents"]:
                                if tg['tag'] == tag:
                                    responses = tg['responses']

                            res = random.choice(responses)
                            #                    print(random.choice(responses))
                            c_speak(res)
                        else:
                            not_und = random.choice(not_understand_list)
                            c_speak(not_und)
                    #                    print(random.choice(not_understand_list))
                    else:
                        c_speak('''I think you are feeling very low right now .
                                You shouldn't be feeling like this !
                                I want you tob see this , it would make you feel good a bit !
                                ''')
                        webbrowser.open('https://www.youtube.com/watch?v=PLSq7OJCZOQ')
                        # print("Very SAD")
                        exit()
#            print(sad_life)
            break

        elif 'time' in voice_read:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f" the current time is {strTime}")
            speak(f" the current time is {strTime}")
            continue

        elif 'youtube' in voice_read:
            youtube_search()
            continue

        elif 'play music' in voice_read:
            print('PLay mode ')
            speak('''If you want me to play local music then give me command : Local.
                  And if you want me to play music online then give me command : Online ''')
            music_choice = str(read_voice_cmd().lower())
            print(music_choice)
            if music_choice == 'local':
                print('Playing system songs')
                music_dir = 'C:\\Users\\Rahul Roy\\Desktop\\my_ai\\mp3\\Alyssa'
                songs = os.listdir(music_dir)
                ran_song = random.choice(songs)
                speak(f" Now Playing : {ran_song}")
                print(f" Now Playing : {ran_song}")
                os.startfile(os.path.join(music_dir, ran_song))
            else:
                print('Playing online')
                speak("please give me a song name to play for you . ")
                music_name = str(read_voice_cmd().lower())
                print("Music name : " + music_name)
                t_music_name = music_name.replace(" ", "")
                print(t_music_name)
                speak(f"Searching : {music_name} ")
                html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + t_music_name)
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                print("https://www.youtube.com/watch?v=" + video_ids[0])
                print(f"Playing : {music_name}")
                webbrowser.open("https://www.youtube.com/watch?v=" + video_ids[0])
            continue

        elif 'translate' in voice_read:

            from_lang = 'en'
            print('What do you want me to translate ?')
            speak('What do you want me to translate ?')
            to_be_translate = str(read_email_cmd().lower())
            print(f"Text : {to_be_translate} ")
            print(f"In which language you want me to translate {to_be_translate} ")
            speak(f"In which language you want me to translate {to_be_translate} ")
            dest_lang = str(read_voice_cmd().lower())
            print(f'Translation language : {dest_lang}')
            lan_code = get_key(dest_lang)
            print(f'Translation language Code : {lan_code}')
            spell = translator.translate(to_be_translate, src=from_lang, dest=lan_code)
            print(spell)
            print(spell.text)
            t_speak(spell.text)

            # if spell.pronunciation == 'None' or spell.pronunciation == '':
            #     print(spell.pronunciation)
            #     t_speak(spell.text)
            # else:
            #     print(spell.text)
            #     t_speak(spell.text)


        elif 'reminder' in voice_read:
            print("What shall I remind you about?")
            speak("What shall I remind you about?")
            rem_about = str(read_voice_cmd())
            print(rem_about)
            print(f"In how many minutes should i remind about {rem_about}?")
            speak(f"In how many minutes should i remind about {rem_about}?")
            try:
                local_time = (str(read_voice_cmd()))
#                print(local_time)
                conv_time = w2n.word_to_num(local_time)
                print(conv_time)
                conv_time = conv_time * 60
 #               print(conv_time)
                time.sleep(conv_time)
                print(f'Reminder alert ! Its time for {rem_about}')
                speak(f'Reminder alert ! Its time for {rem_about}')
                break
            except ValueError:
                speak(f'Please tell me a valid number of minute to remind you about {rem_about}')

            continue


        elif 'twitter' in voice_read:
            tweet()

            continue

        elif 'send email' in voice_read:
            print('is this person on your registered email list ?')
            speak('is this person on your registered email list ?')
            em_ans = str(read_voice_cmd())
            print(em_ans)
            if 'yes' in em_ans:
                print("Give me the name of that person .")
                speak("Give me the name of that person .")
                name = str(read_voice_cmd()).lower()
                receiver = email_list[name]
                print(receiver)
                print('What is the subject of your email?')
                speak('What is the subject of your email?')
                subject = str(read_email_cmd())
                print(f"Subject : {subject}")
                print("Tell me the content of your email")
                speak('Tell me the content of your email')
                message = str(read_email_cmd())
                print(f'Message : {message}')
                send_email(receiver, subject, message)
                print('Congratulations ! Your email has been sent successfully .')
                speak('Congratulations ! Your email has been sent successfully .')
            elif 'no' in em_ans:
                print("Please tell me the user name of receiver")
                speak("Please tell me the user name of receiver")
                new_receiver = str(read_voice_cmd()).lower()
                print(f"Now please tell me the email id of {new_receiver}")
                speak(f"Now please tell me the email id of {new_receiver}")
                new_receiver_email = str(read_email_cmd()).lower()
                new_receiver_email = new_receiver_email.strip()
                new_receiver_email = new_receiver_email.replace("dot", ".")
                new_receiver_email = new_receiver_email.replace("at the rate", "@")
                new_receiver_email = new_receiver_email.replace("to", "2")
                new_receiver_email = new_receiver_email.replace(" ", "")
                speak(f"Do you want me to send email to {new_receiver_email} ")
                print(f"Do you want me to send email to {new_receiver_email}")
                new_em_ans = str(read_voice_cmd()).lower()
                print(new_em_ans)
                if 'yes' in new_em_ans:
                    # if verify_email(new_receiver_email):
                    if validate_email(email_address=new_receiver_email):
                        print('What is the subject of your email?')
                        speak('What is the subject of your email?')
                        new_subject = str(read_email_cmd())
                        print(f"Subject : {new_subject}")
                        print('Tell me the content of your email')
                        speak('Tell me the content of your email')
                        new_message = str(read_email_cmd())
                        print(f'Content : {new_message}')
                        send_email(new_receiver_email, new_subject, new_message)
                        print('Congratulations ! Your email has been sent successfully .')
                        speak('Congratulations ! Your email has been sent successfully .')
                    else:
                        print('''OHH sorry ! 
                        but this is not a valid email address 
                        I'm much more smarter than you think''')
                        speak('''OHH sorry ! 
                        but this is not a valid email address 
                        I'm much more smarter than you think''')
                elif 'no' in em_ans:
                    print("Please again say the email id :")
                    speak("Please again say the email id :")
                    new_receiver_email = str(read_email_cmd()).lower()
                    new_receiver_email = new_receiver_email.strip()
                    new_receiver_email = new_receiver_email.replace("dot", ".")
                    new_receiver_email = new_receiver_email.replace("at the rate", "@")
                    new_receiver_email = new_receiver_email.replace("to", "2")
                    new_receiver_email = new_receiver_email.replace(" ", "")
                    speak(f"Do you want me to send email to {new_receiver_email} ")
                    print(f"Do you want me to send email to {new_receiver_email}")
                    n_em_ans = str(read_voice_cmd()).lower()
                    print(n_em_ans)
                    if 'yes' in n_em_ans:
                        if validate_email(email_address=new_receiver_email):
                            speak('What is the subject of your email?')
                            new_subject = str(read_email_cmd())
                            speak('Tell me the content of your email')
                            new_message = str(read_email_cmd())
                            send_email(new_receiver_email, new_subject, new_message)
                            speak('Congratulations ! Your email has been sent successfully .')
                        else:
                            print('''OHH sorry ! 
                            but this is not a valid email address 
                            I'm much more smarter then you think''')
                            speak('''OHH sorry ! 
                            but this is not a valid email address 
                            I'm much more smarter then you think''')
                    else:
                        print('''I am Sorry for this ,
                         but i am not able to recognise this email id
                         So you have  to enter the email id manually ''')
                        speak('''I am Sorry for this ,
                         but i am not able to recognise this email id
                         So you have enter the email id manually ''')
                        new_receiver_email = str(input("Enter the email id : "))
                        if new_receiver_email == '':
                            print("Sorry , but you did not entered the e-mail id ")
                            t_speak("Sorry , but you did not entered the e-mail id ")
                            break
                        else:
                            if validate_email(email_address=new_receiver_email):
                                print('What is the subject of your email?')
                                speak('What is the subject of your email?')
                                new_subject = str(read_email_cmd())
                                print(f"Subject : {new_subject}")
                                print('Tell me the content of your email')
                                speak('Tell me the content of your email')
                                new_message = str(read_email_cmd())
                                print(f"Message : {new_message}")
                                send_email(new_receiver_email, new_subject, new_message)
                                print("Congratulations ! Your email has been sent successfully .")
                                speak('Congratulations ! Your email has been sent successfully .')
                            else:
                                print('''OHH sorry ! 
                                but this is not a valid email address 
                                I'm much more smarter then you think''')
                                speak('''OHH sorry ! 
                                but this is not a valid email address 
                                I'm much more smarter then you think''')
            else:
                pass


        elif 'lock' in voice_read:
            print("Do you want me turn on the sleep mode of your system ?")
            speak("Do you want me turn on the sleep mode of your system ?")
            lock_confirmation = str(read_voice_cmd()).lower()
            print(lock_confirmation)
            if 'yes' in lock_confirmation:
                print("Sleep mode has been turned on . Byee !")
                speak("Sleep mode has been turned on . Byee !")
                for value in ['pc', 'system', 'windows']:
                    ctypes.windll.user32.LockWorkStation()
                exit()
            else:
                print("What can i do for you")
                speak("What can i do for you")
                continue

        elif 'thank you' in voice_read:
            print("It was my pleasure to help you !")
            speak("It was my pleasure to help you !")
            continue

        elif 'bye' in voice_read:
            print("It was pleasure to help you . Bye !")
            speak("It was pleasure to help you . Bye !")
            exit()
