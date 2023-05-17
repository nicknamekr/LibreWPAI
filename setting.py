"""
(C) Nicknamekr
You can use this Program and Code free.
Attribution required

이 코드와 프로그램을 무료로 사용할 수 있습니다.
저작권 표기가 요구됩니다.
"""
from googletrans import Translator
translator = Translator()

url = '' # Example : https://example.blog/xmlrpc.php
id = '' # Example : libre
pw = '' # Example : 1q2w3e4r5t6y7u8i9o0p!A

delay = int('1800') # 몇 초 주기로 글을 작성할까요? (기본값 1800)
autoDelayMode = False # autoDelayMode는 AI 탐지를 우회할 수 있습니다. delay 시간보다 10분 내외의 시간 차이를 둡니다. (기본값 "False")

Topic = '' # 주제를 설정하세요.
Topic_English = translator.translate(Topic).text # Unsplash용 영문 주제 (기본값 : 자동번역)
category = [Topic] # 카테고리를 설정하세요. (기본 값 : Topic)

OpenAI_Key = 'pk-FcRodAetTQBBbNwvAWlKoHYdRxvGeFyHBZHARdQskUlBOxiX' # OpenAI 키를 입력하세요 (For now, we supports freegpt key)

txtSaveMode = True # TXT 파일 세이브를 할 지 선택합니다. (기본값 "True")
txtSaveDirectory = '/' # 슬래쉬 또는 역슬래쉬를 정합니다. Mac, Linux는 슬래쉬(/)이고 Windows는 역슬래쉬(\)입니다. (기본값 '/')
