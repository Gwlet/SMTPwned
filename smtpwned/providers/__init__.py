from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def send_email(self, sender, to, subject, body, html=None):
        pass