import requests
import json
from bs4 import BeautifulSoup as BS
import telebot
import config
from telebot import types
import schedule
import time
from threading import Thread

bot = telebot.TeleBot(config.TOKEN)
for_everyone_zal = ''

lessons = [
    {'name': 'Іноземна мова 1-2 сем', 'code': '149868'},
    {'name': 'Українознавство', 'code': '157076'},
    {'name': 'Програмування та алгоритмічні мови', 'code': '157077'},
    {'name': 'Мікроекономіка', 'code': '157078'},
    {'name': 'Макроекономіка', 'code': '157079'},
    {'name': 'Математика 2', 'code': '157080'},
    {'name': 'Теорія ймовірності та математична статистика', 'code': '157089'}
]

def reloadPoints(zal, auth_url, s, message, reload_counter):
    auth_html = s.get(auth_url)
    auth_bs = BS(auth_html.content, 'html.parser')
    sesID = auth_bs.select('input[name=sesID]')[0]['value']
    answ = s.get('http://dekanat.kneu.edu.ua/cgi-bin/classman.cgi?n=7&sesID=' + sesID)
    answ_bs = BS(answ.content, 'html.parser')
    lessons_codes = answ_bs.select('.col-xs-12.col-sm-12.col-md-6>select[id="prt"]>option:not([value="-1"])')

    jsonFile = []
    # for code in lessons_codes:
    #     lessons.append({'name':code.getText(),'code':code['value']})
    iter = 0
    if reload_counter != 0:
        with open('points/'+zal+".json", "r") as read_file:
            data = json.load(read_file)
    for lesson in lessons:
        payload = {
            'grp': 'ІЕ-101',
            'n': '7',
            'sesID': sesID,
            'teacher': '0',
            'irc': '0',
            'tid': '0',
            'CYKLE': '-1',
            'prt': str(lesson['code']),
            'hlf': '1',
            'modeView': '0',
            'd1':'',
            'd2':'',
            'm': '-1',
            'grade': '0'
        }

        answ_get = s.post('http://dekanat.kneu.edu.ua/cgi-bin/classman.cgi?sesID='+sesID, data=payload)
        answ_get_bs = BS(answ_get.content, 'html.parser')
        dates = answ_get_bs.select('thead>tr>th[colspan="2"]')
        points = answ_get_bs.select('tbody>tr')[2]
        lesson_tr = answ_get_bs.select('tbody>tr')[1]
        lesson_bs = BS(str(lesson_tr), 'html.parser')
        points_bs = BS(str(points), 'html.parser')
        points_td = points_bs.select('td:not([class="fsdfhjh"])')
        lesson_type = lesson_bs.select('th[colspan="2"]')
        # print(lesson_type)
        # print(str(int(1+0.5))


        jsonFile.append({'lesson_code':lesson['code'], 'points':[], 'final-point':''})
        i = 1
        # print(lesson['name'])
        for date in dates:
            for v in range(0,2):
                if points_td[i].getText() != "":
                    # print(lesson_type[dates.index(date)].getText())
                    jsonFile[iter]['points'].append({'date':date.getText(), 'value':points_td[i].getText(), 'lesson_type':lesson_type[dates.index(date)].getText()})
                i+=1
        jsonFile[iter]['final-point']=points_td[i+1].getText();
        if reload_counter != 0:
            len_data = len(data[iter]['points'])
            len_json = len(jsonFile[iter]['points'])
            if len_data != len_json and reload_counter != 0:
                dif = len_json - len_data
                for j in range(1, dif+1):
                    bot.send_message(message.chat.id,"Новые баллы по " +lesson['name']+" "+jsonFile[iter]['points'][len_json-j]['value'])
        iter+=1

    with open('points/'+zal+".json", "w") as write_file:
        json.dump(jsonFile, write_file)
    print('refresh points ' + zal + ' the end')
    if reload_counter == 0:
        markup = types.InlineKeyboardMarkup(row_width=1)
        for lesson in lessons:
            item = types.InlineKeyboardButton(str(lesson['name']), callback_data=lesson['code']+' '+zal)
            markup.add(item)
        bot.send_message(message.chat.id, "Загрузка успешна")
        bot.send_message(message.chat.id, "Выберете предмет", reply_markup=markup)




s = requests.Session()

# zal = input('Введите номер зачетки: ')
# name = input('Введите фамилию: ')

auth = [{'name':'Климов', 'zal':'190200', 'url':'https://kneu.edu.ua/j.php?190200-149868-1-1b459c69'},
    {'name':'Андрущенко', 'zal':'190112', 'url':'https://kneu.edu.ua/j.php?190112-149876-1-86c60278'},
    {'name':'Василенко', 'zal':'190194', 'url':'https://kneu.edu.ua/j.php?190194-149868-1-ae87040'},
    {'name':'Глебець', 'zal':'190108', 'url':'https://kneu.edu.ua/j.php?190108-149868,149878,149887,149896,149923-1-bc2a4211'},
    {'name':'Коновалова', 'zal':'190199', 'url':'https://kneu.edu.ua/j.php?190199-149868,149878,149887,149896,149923-1-b4312bfd'},
    {'name':'Красноусова', 'zal':'190125', 'url':'https://kneu.edu.ua/j.php?190125-149868-1-d1a46f5e'},
    {'name':'Кузьменко', 'zal':'190123', 'url':'https://kneu.edu.ua/j.php?190123-149868-1-cd4e1fbc'},
    {'name':'Миколюк', 'zal':'190195', 'url':'https://kneu.edu.ua/j.php?190195-149868-1-7ac61891'},
    {'name':'Мороз', 'zal':'190127', 'url':'https://kneu.edu.ua/j.php?190127-149868,149878,149887,149896,149923-1-c03b08ac'},
    {'name':'Настаулова', 'zal':'190113', 'url':'https://kneu.edu.ua/j.php?190113-149868-1-6573eff7'},
    {'name':'Семенюк', 'zal':'190115', 'url':'https://kneu.edu.ua/j.php?190115-149868-1-2c574255'},
    {'name':'Степаненко', 'zal':'190120', 'url':'https://kneu.edu.ua/j.php?190120-149868-1-c454cc6a'},
    {'name':'Стрельцов', 'zal':'190116', 'url':'https://kneu.edu.ua/j.php?190116-149868-1-92fea2f0'},
    {'name':'Ткачук', 'zal':'190111', 'url':'https://kneu.edu.ua/j.php?190111-149868-1-e0f8944d'},
    {'name':'Ярош', 'zal':'190197', 'url':'https://kneu.edu.ua/j.php?190197-149868-1-f9cf2fb0'},
    {'name':'Волочай', 'zal':'190109', 'url':'https://kneu.edu.ua/j.php?190109-149868-1-b60f54ab'},
]

# for auth_ac in auth:
#     if(auth_ac['name'] == name and auth_ac['zal'] == zal):
#         url = auth_ac['url']
# reloadPoints(zal, url, s)
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Введите номер зачетки и фамилию\nВ формате "123456 Фамилия"')
@bot.message_handler(content_types=['text'])
def lalala(message):
    try:
        zal, name = message.text.split()
        for_everyone_zal = zal
        url = ''
        for auth_ac in auth:
            if(auth_ac['name'] == name and auth_ac['zal'] == zal):
                url = auth_ac['url']
        if url == '':
            raise IOError("Неверные данные")
        bot.send_message(message.chat.id, "Загрузка оценок с сервера,\nв первый раз это может занять неокторое время")
        # print(message.chat.id)
        schedule.clear(message.chat.id)
        schedule.every(1).hour.do(reloadPoints, zal =zal, auth_url=url, s=s, message=message, reload_counter=1).tag(message.chat.id)
        reloadPoints(zal, url, s, message, 0)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Неверно введены данные')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data.split()[0] == 'cancel':
                markup = types.InlineKeyboardMarkup(row_width=1)
                for lesson in lessons:
                    item = types.InlineKeyboardButton(str(lesson['name']), callback_data=lesson['code']+' '+call.data.split()[1])
                    markup.add(item)
                bot.send_message(call.message.chat.id, "Выберете предмет", reply_markup=markup)
            else:
                code, zal = call.data.split()
                message_text = ''
                print(zal)
                with open('points/'+zal+".json", "r") as read_file:
                    data = json.load(read_file)

                for data_lesson in data:
                    if data_lesson['lesson_code'] == code:
                        for lesson in lessons:
                            if lesson['code'] == code:
                                name = lesson['name']
                        message_text+='<strong>'+name+" : </strong>"+data_lesson['final-point'] +"\n"
                        for point in data_lesson['points']:
                            message_text+=point['date']+'   <strong>'+point['value']+"</strong>    "+point['lesson_type']+"\n"
                markup = types.InlineKeyboardMarkup(row_width=1)
                item = types.InlineKeyboardButton("Назад", callback_data='cancel '+zal)
                markup.add(item)
                # bot.send_message(message.chat.id, "Выберете предмет", reply_markup=markup)
                bot.send_message(call.message.chat.id, message_text, parse_mode='html', reply_markup=markup)
            # if call.data == 'good':
            #     bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            # elif call.data == 'bad':
            #     bot.send_message(call.message.chat.id, 'Бывает 😢')
            #
            # # remove inline buttons
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
            #     reply_markup=None)
            #
            # # show alert
            # bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
            #     text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))

def polling():
    bot.polling(none_stop=True)
def while_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

thread1 = Thread(target=polling)
thread2 = Thread(target=while_schedule)

thread1.start()
thread2.start()
thread1.join()
thread2.join()




# auth_html = s.get(url)
# auth_bs = BS(auth_html.content, 'html.parser')
# sesID = auth_bs.select('input[name=sesID]')[0]['value']
# answ = s.get('http://dekanat.kneu.edu.ua/cgi-bin/classman.cgi?n=7&sesID=' + sesID)
# answ_bs = BS(answ.content, 'html.parser')
# lessons_codes = answ_bs.select('.col-xs-12.col-sm-12.col-md-6>select[id="prt"]>option:not([value="-1"])')
# lessons = []
# for code in lessons_codes:
#     lessons.append({'name':code.getText(),'code':code['value']})
# print(lessons)
#
# lesson_name = input('Введите предмет: ')
# for lesson in lessons:
#     if lesson['name'] == lesson_name:
#         prt = lesson['code']
#         print('Найден')
#     else:
#         print('Не Найден')
# print(prt)
# # print(answ_bs)
# payload = {
#     'grp': 'ІЕ-101',
#     'n': '7',
#     'sesID': sesID,
#     'teacher': '0',
#     'irc': '0',
#     'tid': '0',
#     'CYKLE': '-1',
#     'prt': str(prt),
#     'hlf': '1',
#     'modeView': '0',
#     'd1':'',
#     'd2':'',
#     'm': '-1',
#     'grade': '0'
# }
#
# answ_get = s.post('http://dekanat.kneu.edu.ua/cgi-bin/classman.cgi?sesID='+sesID, data=payload)
# answ_get_bs = BS(answ_get.content, 'html.parser')
# dates = answ_get_bs.select('thead>tr>th[colspan="2"]')
# points = answ_get_bs.select('tbody>tr')[2]
# points_bs = BS(str(points), 'html.parser')
# points_td = points_bs.select('td:not([class = ""])')
#
#
# jsonFile = [{'lesson_name':lesson_name, 'points':[]}]
# i = 1
# print(lesson_name)
# for date in dates:
#     for v in range(0,2):
#         # points = answ_get_bs.select('td', data_item=str(dates.index(date)+1))
#         # print(points_td[i]['data-item'])
#         # print(points_td.count())
#         if points_td[i].getText() != "":
#             jsonFile[0]['points'].append({'date':date.getText(), 'value':points_td[i].getText()})
#             print (date.getText() + " " +  points_td[i].getText())
#         i+=1
# with open(zal+".json", "w") as write_file:
#     json.dump(jsonFile, write_file)
#
#
# with open(zal+".json", "r") as read_file:
#     data = json.load(read_file)
#
# print("Общий балл " + points_td[i+1].getText())
# print(data[0]['lesson_name'])
