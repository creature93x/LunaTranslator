from translator.basetranslator import basetrans
import re
import socket
from thefuzz import fuzz
import pickle


class My_socket():

    def __init__(self) -> None:
        self.client_socket = None

    def _create_socket(self):
        # Create a socket object if not already created
        if self.client_socket is None:
            self.client_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', 9444))

    def _close_socket(self):
        # Close the socket if it exists
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None

    def send(self, message):
        try:
            self._create_socket()  # Ensure socket is created before sending
            # Send the message to the server
            self.client_socket.send(pickle.dumps(message))
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self._close_socket()  # Close the socket after sending


class TS(basetrans):

    def langmap(self):
        return {"zh": "zh-CN", "cht": "zh-TW"}

    def translate(self, content):
        global client_socket

        headers = {
            'authority': 'translate.google.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://translate.google.com/m',
            'sec-ch-ua': '"Microsoft Edge";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"105.0.1343.53"',
            'sec-ch-ua-full-version-list': '"Microsoft Edge";v="105.0.1343.53", "Not)A;Brand";v="8.0.0.0", "Chromium";v="105.0.5195.127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-ch-ua-wow64': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53',
        }
        params = {
            'sl': self.srclang,
            'tl': self.tgtlang,
            'hl': 'zh-CN',
            'q':  content,
        }

        response = self.session.get(
            'https://translate.google.com/m', params=params, verify=False, headers=headers)

        res = re.search(
            '<div class="result-container">([\\s\\S]*?)</div>', response.text).groups()

        client_socket.send({"content": content, "translation": res[0]})
        return '\u200F'+res[0]


global client_socket
client_socket = My_socket()
