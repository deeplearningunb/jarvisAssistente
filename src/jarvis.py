import os  # noqa
import re  # noqa
import pickle  # noqa
import json
from subprocess import check_output  # noqa

import pyttsx3
import numpy as np
import speech_recognition as sr  # noqa
from selenium import webdriver  # noqa
from pydantic.dataclasses import dataclass
from tensorflow.keras.models import load_model

PATH = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(PATH, "playlist.json")) as f:
    PLAYLISTS = json.loads(f.read())


@dataclass
class Jarvis:
    def __post_init__(self) -> None:
        """
        Inicializa a classe de interpretação de voz do python.
        """
        self.speaker = pyttsx3.init()
        self.speaker.setProperty("rate", 150)
        self.speaker.setProperty("volume", 0.7)
        self.speaker.setProperty("voice", "brazil")
        self.path = PATH
        self.model = load_model(os.path.join(self.path, "model/result.h5"))
        with open(os.path.join(self.path, "model/encoders.pkl"), "rb") as f:
            self.encoders = pickle.load(f)

    def __get_pid(self, app: str) -> int:
        try:
            pids = [int(each) for each in check_output(["pidof", app]).split()]
        except Exception:
            pids = []
        return pids

    def __say_string(self, speech: str) -> None:
        self.speaker.say(speech)
        self.speaker.runAndWait()

    def __stop_app(self, app: str) -> bool:
        raise KeyboardInterrupt

    def __search_google(self, command: str) -> bool:
        driver = webdriver.Chrome(
            os.path.join(self.path, "chromedriver")
        )
        driver.get("http://www.google.com/")
        search_box = driver.find_element_by_name("q")
        search_box.send_keys("{}".format(" ".join(command.split(" ")[1:])))
        search_box.submit()
        return True

    def __play_spotify(self, command: str) -> bool:
        try:
            is_open = self.__get_pid("spotify")
            print(is_open)
            playlist = " ".join(command.lower().split(" ")[2:])
            if len(is_open) == 0:
                play_cmd = "(spotify 1>/dev/null 2>&1 &) && "
                play_cmd += "sleep 3 && "
                play_cmd += "qdbus org.mpris.MediaPlayer2.spotify "
                play_cmd += "/org/mpris/MediaPlayer2 "
                play_cmd += "org.mpris.MediaPlayer2.Player.OpenUri "
                play_cmd += PLAYLISTS[playlist] + " &"
            else:
                play_cmd = "qdbus org.mpris.MediaPlayer2.spotify "
                play_cmd += "/org/mpris/MediaPlayer2 "
                play_cmd += "org.mpris.MediaPlayer2.Player.OpenUri "
                play_cmd += PLAYLISTS[playlist] + " &"
            os.system(play_cmd)
            return True
        except KeyError:
            self.say_string("Playlist não encontrada !")
            return False

    def __start_program(self, command: str) -> bool:
        app = " ".join(command.split(" ")[2:]).lower()
        cmd = f"exec {app} &"
        if os.system(cmd):
            return True
        return False

    def __stop_program(self, command: str) -> bool:
        app = " ".join(command.split(" ")[2:]).lower()
        cmd = "pkill {}".format(app)
        if os.system(cmd):
            return True
        return False

    def __volume(self, command: str) -> bool:
        if re.match(r"(((a|A)umentar)|((s|S)ubir)|((a|A)lto))", command):
            cmd = "amixer -D pulse sset Master 10%+"
            os.system(cmd)
            return True

        elif re.match(r"(((a|A)baixar)|((d|D)iminuir)|((b|B)aixo))", command):
            cmd = "amixer -D pulse sset Master 10%-"
            os.system(cmd)
            return True
        return False

    def __controller(self, command) -> bool:
        if command in ["controle_play", "controle_pausa"]:
            cmd = "dbus-send --print-reply --dest=org.mpris.MediaPlayer2"
            cmd += ".spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2."
            cmd += "Player.PlayPause"
            os.system(cmd)
            return True

        elif command == "controle_prev":
            cmd = "dbus-send --print-reply --dest=org.mpris.MediaPlayer2"
            cmd += ".spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2."
            cmd += "Player.Previous"
            os.system(cmd)
            return True

        elif command == "controle_prox":
            cmd = "dbus-send --print-reply --dest=org.mpris.MediaPlayer2"
            cmd += ".spotify /org/mpris/MediaPlayer2 org.mpris."
            cmd += "MediaPlayer2.Player.Next"
            os.system(cmd)
            return True
        return False

    def __command_classify(self, command: str) -> str:
        x = self.encoders["vectorize"].transform([command])
        pred = self.model.predict(x)
        pred_label = self.encoders["encoder"].inverse_transform(
            [np.argmax(each) for each in pred]
        )
        return pred_label[0]

    def run(self) -> None:
        COMMANDS = {
            "volume": self.__volume,
            "controle_pausa": self.__controller,
            "controle_play": self.__controller,
            "controle_prox": self.__controller,
            "controle_prev": self.__controller,
            "spotify": self.__play_spotify,
            "fechar": self.__stop_program,
            "abrir": self.__start_program,
            "sair": self.__stop_app,
            "pesquisar": self.__search_google,
        }
        r = sr.Recognizer()
        m = sr.Microphone()
        try:
            self.__say_string("Bem vindo!")
            with m as source:
                r.adjust_for_ambient_noise(source)
            while True:
                with m as source:
                    audio = r.listen(source, phrase_time_limit=6)
                try:
                    command = r.recognize_google(audio, language="pt-BR")
                    print(f"Commando: {command}")
                    command_type = self.__command_classify(command)
                    print(f"Classificação: {command_type}")
                    if type(command) is bytes:
                        command = command.encode("utf-8")
                    if "controle" in command_type:
                        _ = COMMANDS[command_type](command_type)
                    else:
                        _ = COMMANDS[command_type](command)
                except sr.UnknownValueError:
                    self.__say_string("Não entendi!")
                except sr.RequestError as e:
                    print("uh oh! {}".format(e))
        except KeyboardInterrupt:
            self.__say_string("Até logo !")


if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()
