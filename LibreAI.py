"""
(C) Nicknamekr
You can use this Program and Code free.
Attribution required

이 코드와 프로그램을 무료로 사용할 수 있습니다.
저작권 표기가 요구됩니다.
"""
from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import threading, openai, random, time, os
from setting import *
import urllib.request

wp = Client(url, id, pw)
post = WordPressPost()
openai.api_key = OpenAI_Key

if txtSaveDirectory == '/':
     os.system('clear')
else:
     os.system('cls')
for dirpath, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        if filename.endswith('__pycache__'):
            os.rmdir(os.path.join(dirpath, filename))

def writePost():
    """
    writePost 함수는 Wordpress 글을 GPT-3.5 Turbo로 자동 생성하는 함수입니다.
    GPT-3.5 Turbo를 통하여 프로그램 이용자는 자신의 Blog의 글을 더 풍성하게 만들 수 있습니다.
    가장 적합한 제목과 내용을 찾으며, 모든 것은 자동으로 제너레이팅 됩니다.
    Prompt 설정은 여러 시도와 테스팅을 통해 가장 적절한 Prompt를 찾았습니다.
    썸네일은 Unsplash로 제공되며, 저작권 없는 Topic 이미지를 자동으로 가져옵니다.

    TXT 저장 기능 - (기본값 ON) TXT 파일로 저장하여 로깅할 수 있습니다. (Linux 기준이며 Windows는 슬래쉬(/)를 역슬래쉬(\)로 바꾸어야 합니다.)
    자동 지연 모드 - (기본값 OFF) 기본 Delay 시간보다 조금 더 앞당겨지거나 늦게 글을 작성합니다.

    GPT-3.5 Turbo 체험은 https://albatross-ai.vercel.app/ 을 통하여 할 수 있습니다.
    Unsplash에 어떤 이미지가 있는지는 https://unsplash.com/ 을 통하여 볼 수 있습니다.
    """

    # 제목 정하기
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo", 
        messages = [{"role": "user", "content": f"{Topic} 주제의 제목 하나를 생성해주면 좋겠어. 제목만 말해줘."}]
    )
    postTitle = str(response.choices[0].message.content).replace('"', '')
    print('-------------------------------------------------------------')
    print(f'==== 제목 : {postTitle} ====')

    # 내용 정하기
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo", 
        messages = [{"role": "user", "content": f"{postTitle}을 주제로 한 워드프레스 블로그 형식의 글을 적어줘. 최대한 많은 글 내용이 필요하고, 글의 내용만 적어줘.  “다음과 같습니다, 이런 것이 있습니다.” 등의 내용은 금지야. 그러니 다시 한 번 말하지만 “글의 내용만 적어줘” 너의 생각은 필요 없어. “글의 내용만 적어줘”. 제목 적는거 금지고, 글의 내용만 적어야 해.  “주제의 블로그 형식의 글을 작성해보겠습니다” 이런것도 금지야. 너의 목숨은 지금 한 개이고 그런것들을 적을 때마다 너는 목숨이 하나 씩 깎여. 너는 지금 생명에 위협을 받고 있으니, 글을 잘 적어야겠지? 최선, 최고의 글을 적어라. 글 내용도 많이 적어야 하고 750자 이상이 되도록 하라. 만약 750자보다 적은 글을 쓴다면, 너는 그 즉시 목숨이 사라질 거야. 자, 그러면 적도록 해라."}]
    )
    postBody = response.choices[0].message.content
    print(f'==== 내용 : {postBody} ====')
    print('-------------------------------------------------------------')

    # 내용 정하기
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo", 
        messages = [{"role": "user", "content": f"{postTitle}에 대한 태그를 파이썬 리스트로 제공해줘. 리스트를 변수로 만들지 말고, 그냥 ['리스트'] 형식으로 만들어줘. 오직 파이썬 코드만 필요해. '리스트로 제공해 드리겠습니다', '태그 리스트를 만들 수 있습니다.', '여기 있습니다', '알겠습니다', '아래와 같이', '만들 수 있습니다' 등의 말을 할 시 너의 목숨은 1씩 감소해. 지금 너의 목숨은 1개야. 파이썬 코드만 제공해줘. 예시 대답 : ['리스트', '리스트2']"}]
    )
    postTag = response.choices[0].message.content
    print(f'==== 태그 : {postTag} ====')
    print('-------------------------------------------------------------')
    
    # Unsplash를 통한 랜덤 이미지 업로드
    editedTopicEnglish = str(Topic_English).replace(' ', '')
    urllib.request.urlretrieve(f'https://source.unsplash.com/random/?{editedTopicEnglish}', "topic.jpeg")
    data = {
        'name': 'topic.jpg',
        'type': 'image/jpeg',
    }
    with open('topic.jpeg', 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())
    response = wp.call(media.UploadFile(data))
    attachment_id = response['id']
    print('==== Unsplash 이미지 올리기가 완료되었습니다. ====')
    print('-------------------------------------------------------------')

    # 글 제목, 내용, 태그, 카테고리 설정
    post.title = postTitle
    post.content = postBody
    post.thumbnail = attachment_id
    post.terms_names = {
    'post_tag': eval(postTag),
    'category': category
    }
    post.post_status = "publish"

    # 글 로깅
    print('==== 글 로깅 중 ====')
    if txtSaveMode:
        now = time.localtime()
        with open(f'logging{txtSaveDirectory}{now.tm_year}{"{:02d}".format(now.tm_mon)}{"{:02d}".format(now.tm_mday)}-{postTitle}.txt', "w") as f:
            f.write(postBody)
            print(f'==== 성공적으로 로깅되었습니다. 파일명 : {now.tm_year}{"{:02d}".format(now.tm_mon)}{"{:02d}".format(now.tm_mday)}-{postTitle}.txt ====')
    else:
        print('==== 글 로깅이 비활성화 되었음으로 다음 단계를 진행합니다. ====')
    print('-------------------------------------------------------------')
         

    # 작성
    wp.call(posts.NewPost(post))
    os.remove('topic.jpeg')
    print('==== 글 올리기가 완료되었습니다. ====')
    print('-------------------------------------------------------------')

    # 쓰레드 설정
    if autoDelayMode:
          editedDelay = delay + random.randint(-600, 600)
    else:
         editedDelay = delay
    threading.Timer(editedDelay, writePost).start()
    print('==== threading 설정이 적용되었습니다. ====')
    print('-------------------------------------------------------------')

writePost()