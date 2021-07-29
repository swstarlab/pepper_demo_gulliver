import time
from naoqi import ALProxy

from data_list import *
from cameras import take_photo
from functions import updown
from functions.play_music import *
from motion import photo_motion


aas_configuration = {"bodyLanguageMode": "contextual"}


class Transition:
    def __init__(self):
        pass

    def get_html_address(self, file_name):
        name = file_name
        if len(name) > 5 and name[-5:] == '.html':
            name = name[:-5]
        return "http://198.18.0.1/apps/bi-html/" + name + '.html'

    def tour_robot(self, srv):
        next_scene = 'tour_hsr1'
        srv['tts'].setParameter("defaultVoiceSpeed", 100)
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        srv['aas'].say(
            "Let me explain the robots in our lab. First, HSR, a human helper robot, is a mobile operation robot.",
            aas_configuration)

        next_scene = 'tour_hsr2'
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        srv['aas'].say(
            "It is about 1 meter tall and is a versatile robot that can recognize objects through various cameras and pick them up with a gripper. But is it ugly than me?",
            aas_configuration)

        next_scene = 'tour_blitz'
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        srv['aas'].say(
            "The next robot, Blitz. It is a robot made by combining a base robot, which is specialized in moving objects, and a UR5 robot that picks up objects. In addition, it is a mobile operation robot that is equipped with sound and camera sensors, capable of recognizing objects and gripping them with a gripper.",
            aas_configuration)

        next_scene = 'tour_pepper1'
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        srv['aas'].say(
            "The last robot to be introduced is me, Pepper. I am a humanoid robot made by Softbank, and I can use artificial intelligence.",
            aas_configuration)

        next_scene = 'tour_pepper2'
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        srv['aas'].say(
            "I have a cute appearance, and has been introduced in various fields such as finance, bookstores, medical care, and distribution fields in Korea. In addition, it is used as a standard robot in S, S, P, L, among the world robot competitions, Robo Cup League.",
            aas_configuration)

        srv['tts'].setParameter("defaultVoiceSpeed", 70)
        next_scene = 'tour'
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        return next_scene

    def tour_lab(self, srv):
        next_scene = 'tour_ourlab1'
        srv['tts'].setParameter("defaultVoiceSpeed", 100)
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        srv['aas'].say(
            "Let me introduce our lab. Our bio-intelligence lab is conducting the following studies. First, we are conducting interdisciplinary research in various fields such as artificial intelligence, psychology, and cognitive science to develop human-level artificial intelligence such as Baby Mind and VTT. We are also actively conducting research on robots on various platforms, such as home robots that work with humans and Robocup, a world robot competition.",
            aas_configuration)

        next_scene = 'tour_ourlab2'
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        srv['aas'].say(
            "If you have any other questions or inquiries, please refer to the following website or contact us.",
            aas_configuration)

        srv['tts'].setParameter("defaultVoiceSpeed", 70)
        next_scene = 'tour'
        srv['tablet'].showWebview(self.get_html_address(next_scene))
        return next_scene

    def updown_game(self, srv, input_ret):
        updown.UpDown(srv).play(input_ret)
        return SCENES['entertain2']

    # initial screen
    def home(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next menu")
                return SCENES[next_scene]

        elif input_ret['type'] == 'speech':
            if input_ret['word'] == 'hello':
                next_scene = 'first_menu'
                srv['aas'].say("Hello, Nice to meet you!", aas_configuration)
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                return SCENES[next_scene]

            elif input_ret['word'] == 'pepper':
                next_scene = 'home'
                srv['aas'].say("Yep! Hello?!", aas_configuration)
                return SCENES[next_scene]

            elif input_ret['word'] == 'cheese':
                # srv['tts'].say("Say cheese")
                photo_test = take_photo.Photo(srv)
                photo_test.take()
                next_scene = 'photo_screen'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                time.sleep(3)
                srv['tablet'].showWebview(self.get_html_address('home'))
                pass

    def first(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_LEFT':
                next_scene = 'tour'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                # srv['tts'].say("next menu")
                srv['aas'].say("What would you like me to introduce?")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_RIGHT':
                next_scene = 'entertain'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("What should we do? Please choose one")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say("To the initial screen")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                next_scene = 'first_menu'
                srv['tts'].setParameter("defaultVoiceSpeed", 100)
                srv['aas'].say(
                    "Are you curious about me? I am Pepper. It is a humanoid robot made by Softbank, and can use artificial intelligence. It is characterized by a cute appearance, and is introduced in various fields such as finance, bookstore, medical care, and distribution fields in Korea")
                srv['tts'].setParameter("defaultVoiceSpeed", 70)
                return SCENES[next_scene]

        elif input_ret['type'] == 'speech':
            say = None
            if input_ret['word'] == 'back':
                next_scene = 'home'
            elif input_ret['word'] == 'who':
                next_scene = 'first_menu'
            elif input_ret['word'] == 'tour':
                next_scene = 'tour'
                say = "What would you like me to introduce?"
            elif input_ret['word'] == 'play':
                next_scene = 'entertain'
                say = "What should we do? Please choose one"
            else:
                next_scene = 'first_menu'

            srv['tablet'].showWebview(self.get_html_address(next_scene))
            if say is not None:
                srv['aas'].say(say)
            return SCENES[next_scene]

    def tour(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_RIGHT':
                next_scene = self.tour_robot(srv)

            elif input_ret['touch_position'] == 'BUTTON_LEFT':
                next_scene = self.tour_lab(srv)

            elif input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say("To the initial screen", aas_configuration)

            elif input_ret['touch_position'] == 'BUTTON_LEFT_DOWN':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("previous menu")

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                next_scene = 'tour'
                srv['tts'].setParameter("defaultVoiceSpeed", 110)
                srv['aas'].say(
                    "Are you curious about me? I am Pepper. It is a humanoid robot made by Softbank, and can use artificial intelligence. It is characterized by a cute appearance, and is introduced in various fields such as finance, bookstore, medical care, and distribution fields in Korea",
                    aas_configuration)
                srv['tts'].setParameter("defaultVoiceSpeed", 70)

            else:
                next_scene = 'tour'

            return SCENES[next_scene]

        elif input_ret['type'] == 'speech':
            if input_ret['word'] == 'robot':
                next_scene = self.tour_robot(srv)

            elif input_ret['word'] == 'lab':
                next_scene = self.tour_lab(srv)

            elif input_ret['word'] == 'back':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say("Okay. What should we do then?")

            else:
                next_scene = 'tour'

            return SCENES[next_scene]

    def do_elephant(self, srv):
        file_path = "/opt/aldebaran/www/apps/bi-sound/elephant.ogg"
        # srv['tts'].post.say('yes')
        player = ALProxy("ALAudioPlayer", PEPPER_IP, 9559)
        player.post.playFileFromPosition(file_path, 0)
        entertain.elephant(srv)
        player.post.stopAll()

    def play_music(self, srv, mode):
        try:
            player = Play(srv, mode, PEPPER_IP)
            player.motion()
        except KeyError:
            print("KeyError occurs.")  # for debugging
            return

    def entertain(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("To the initial screen")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT_DOWN':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("previous menu")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT':
                self.do_elephant(srv)

            elif input_ret['touch_position'] == 'BUTTON_RIGHT':
                self.play_music(srv, "disco")

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                next_scene = 'entertain2'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next menu")
                return SCENES[next_scene]
            
        elif input_ret['type'] == 'speech':
            if input_ret['word'] == 'elephant':
                self.do_elephant(srv)

            elif input_ret['word'] == 'music':
                # self.play_music(srv, "disco")
                next_scene = 'dance_1'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next menu")
                return SCENES[next_scene]

            elif input_ret['word'] == 'back':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['aas'].say("Okay. What should we do then?")
                return SCENES[next_scene]

    # fix after implementation
    def entertain2(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("To the initial screen")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT_DOWN':
                next_scene = 'first_menu'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("previous menu")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT':
                pass  # need to implement this

            elif input_ret['touch_position'] == 'BUTTON_RIGHT':
                srv['tts'].say("You must say the number in English." \
                               + "Other languages are not allowed.")
                time.sleep(1)  # wait for a second
                next_scene = 'updown'
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                next_scene = 'entertain'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next menu")
                return SCENES[next_scene]

    def dance1(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("To the initial screen")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT_DOWN':
                next_scene = 'entertain'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("previous menu")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT':
                self.play_music(srv, "disco")

            elif input_ret['touch_position'] == 'BUTTON_RIGHT':
                self.play_music(srv, "bang")

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                next_scene = 'dance_2'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("next menu")
                return SCENES[next_scene]

    def dance2(self, srv, input_ret):
        if input_ret['type'] == 'touch':
            if input_ret['touch_position'] == 'BUTTON_MIDDLE_DOWN':
                next_scene = 'home'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("To the initial screen")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT_DOWN':
                next_scene = 'dance_1'
                srv['tablet'].showWebview(self.get_html_address(next_scene))
                srv['tts'].say("previous menu")
                return SCENES[next_scene]

            elif input_ret['touch_position'] == 'BUTTON_LEFT':
                self.play_music(srv, "guitar")

            elif input_ret['touch_position'] == 'BUTTON_RIGHT':
                self.play_music(srv, "saxophone")

            elif input_ret['touch_position'] == 'BUTTON_RIGHT_DOWN':
                pass  # need to implement this

    # return the object of the next scene
    def switch(self, srv, scene, input_ret):
        if scene == "home":
            return self.home(srv, input_ret)
        elif scene == "first_menu":
            return self.first(srv, input_ret)
        elif scene == "tour":
            return self.tour(srv, input_ret)
        elif scene == "entertain":
            return self.entertain(srv, input_ret)
        elif scene == "entertain2":
            return self.entertain2(srv, input_ret)
        elif scene == "updown":
            return self.updown_game(srv, input_ret)
