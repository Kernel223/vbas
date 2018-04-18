import sqlite3
from datetime import datetime
import vk_api
from math import ceil

def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


def main():
    login, password = '', ''
    vk_session = vk_api.VkApi(login, password, captcha_handler=captcha_handler)
    try:
        print("trt")
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    # Авторизация группы:
    # при передаче token вызывать vk_session.auth не нужно
    """
    vk_session = vk_api.VkApi(token='токен с доступом к сообщениям и фото')
    """
    tools = vk_api.VkTools(vk_session)
    # vk = vk_session.get_api()


    conn = sqlite3.connect('usrs.db')
    c = conn.cursor()
    t = []
    temp = []
    i = 0
    for row in  c.execute('''SELECT * FROM users''').fetchall():
        temp.append(str(row[0]))
        i += 1
        if i == 300:
            temp = ','.join(temp)
            t.append(temp)
            temp = []
            i = 0
        # t.append(row[0])
    del temp
    print(t)
    print(len(t))
    # exit()

    megaWords = ['муз','код','танц','рекл','звон']

    delit = 5
    # print(Fore.RED + 'Range pool: ' + str(ceil(len(members) / delit)) + Fore.RESET)
    allPool = int(ceil(len(t) / delit)) + 1
    #
    tt = []
    # print(t[0])
    print('AllPolls:',allPool)
    for poollt in range(1,allPool):

        with vk_api.VkRequestsPool(vk_session) as pool:
            user = pool.method_one_param(
                'users.get',  # Метод
                key='user_ids',  # Изменяющийся параметр
                values=t[(poollt - 1) * delit: poollt * delit],

                # Параметры, которые будут в каждом запросе
                # default_values={}
                default_values={'fields': 'sex,status,occupation,interests,about,quotes,bdate'}
            )



        for v in user.result.values():
            for vv in v:
                for m in megaWords:
                    if m.lower() in str(vv).lower():
                        # print(vv)
                        tt.append(vv)
                        break
                    # exit()

        print('Pool:',poollt)

    conn = sqlite3.connect('usrs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS goods
                                    (id INTEGER UNIQUE,first_name TEXT,last_name TEXT,sex INTEGER,status TEXT,occupation TEXT,interests TEXT,about TEXT, quotes Text, `bdate` TEXT)''')
    conn.commit()
    ti = 0
    keys = ['id','first_name','last_name','sex','status','occupation','interests','about','quotes','bdate']
    for i,t in enumerate(tt):
        try:

            for k in keys:
                if k in t.keys():
                    pass
                else:
                    t[k] = ""

            c.execute('INSERT INTO goods VALUES (?,?,?,?,?,?,?,?,?,?)',
                      [t['id'],t['first_name'],t['last_name'],t['sex'],str(t['status']),
                       str(t['occupation']),t['interests'],t['about'],t['quotes'],t['bdate']])
        except Exception as e:
            print(e,t)
            pass
        ti += 1
        # if ti - 10 == 0:
        #     print(i)
        #     ti = 0
    print(ti)
    conn.commit()
    conn.close()



if __name__ == '__main__':
    now = datetime.now()
    print(now)
    main()
    end = datetime.now()
    print(end - now)
