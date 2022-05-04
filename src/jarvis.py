import os # noqa
import re # noqa
from subprocess import check_output # noqa

import pyttsx3
import speech_recognition as sr # noqa
from selenium import webdriver # noqa
from pydantic.dataclasses import dataclass


@dataclass
class Jarvis:
    def __post_init__(self) -> None:
        """
        Inicializa a classe de interpretação de voz do python.
        """
        self.speaker = pyttsx3.init()
        self.speaker.setProperty('rate', 150)
        self.speaker.setProperty('volume', 0.7)
        self.speaker.setProperty('voice', 'brazil')

    def __get_pid(self, app: str) -> int:
        pass

    def __say_string(self, speech: str) -> None:
        pass

    def __stop_app(self, app: str) -> bool:
        pass

    def __search_google(self, command: str) -> bool:
        pass

    def __play_spotify(self, command: str) -> bool:
        pass

    def __open_project(self, command: str) -> bool:
        pass

    def __start_program(self, command: str) -> bool:
        pass

    def __stop_program(self, command: str) -> bool:
        pass

    def __volume(self, command: str) -> bool:
        pass

    def __work(self, command: str) -> bool:
        pass

    def __run(self) -> None:
        pass
