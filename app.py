#coding=gbk
import re
import PySimpleGUI as sg
from photozip import *
from concurrent.futures import ThreadPoolExecutor

threadpool = ThreadPoolExecutor(5)
menu_def = []
img_kb = [[
        sg.T('ѹ����',k='ys_a'),
        sg.I(k='ys_n',size=4,enable_events=True),
        sg.T('kb',k='ys_b'),
        sg.B('ȷ��',k='ys_btn',bind_return_key=True),
             sg.Checkbox('���߳�','dxc',key='dxc',expand_x=True)]]
img_ls = [[
        sg.T('����ֱ���:',k='fbl'),sg.I(k='fbl_x',size=4),
        sg.T('*',k='z'),sg.I(k='fbl_y',size=4),
        sg.B('ȷ��',k='fbl_btn',visible=True,font=10,bind_return_key=True)]]
img_cj = [[
        sg.T('�ϱ߾�:',k='up'),sg.I(k='up_n',size=4),
        sg.T('�±߾�:',k='dowm'),sg.I(k='down_n',size=4),
        sg.T('��߾�:',k='life'),sg.I(k='life_n',size=4),
        sg.T('�ұ߾�:',k='right'),sg.I(k='right_n',size=4),
        sg.B('ȷ��',k='cj_btn',bind_return_key=True)
]]
img_jz = [[
        sg.T('����ֱ���:',visible=True,k='jzfbl'),sg.I(k='jzfbl_x',size=4,visible=True),
        sg.T('*',visible=True,k='jzz'),sg.I(k='jzfbl_y',size=4,visible=True),
        sg.B('ȷ��',k='jzfbl_btn',visible=True,font=10,bind_return_key=True)]]
layout = [ [sg.MenubarCustom(menu_def,key='-MENU-', font='Courier 15', tearoff=True)],
                [sg.Text('ͼƬ������',background_color='#64778d',expand_x=True,pad=((0,0),(0,10)), justification='center', font=("Helvetica", 14), relief=sg.RELIEF_RIDGE, k='errortext', enable_events=True)]]
layout +=[[sg.TabGroup([[sg.Tab('��Сkb', img_kb,k='dakb',pad=100),
                               sg.Tab('����ͼƬ', img_ls,k='lstp',border_width=0),
                               sg.Tab('�ü�ͼƬ', img_cj,k='cjtp'),
                               sg.Tab('���вü�ͼƬ',img_jz,k='jzcjtp')]],font=20,border_width=1, key='-TAB GROUP-', expand_x=True)]]
layout += [
            [sg.T('֧��jpg,png,bmp��ʽ')],
            [sg.LBox([], size=(80,10), key='-FILESLB-',expand_x=True,no_scrollbar=True)],
            [sg.Input(visible=False, key='-IN-',enable_events=True),
            sg.FilesBrowse('ѡȡͼƬ'),sg.T(key='-NUM-',text_color='blue')]
            ]
layout += [
            [sg.ML(size=(40,5),key='errortext2',write_only=False,text_color='blue',visible=True,border_width=0,no_scrollbar=True,background_color='#64778d',expand_x=True)],]

windows = sg.Window("ͼƬ�޸Ĺ���",layout,resizable=True)

#�ж��Ƿ���ͼƬ��ʽ
def is_image(s):
    tmp=[]
    for i in s.split(';'):
        if re.findall('(\.jpg|\.png|\.jpge|\.bmp)$',i,re.I):
            tmp.append(i)
    return tmp
#�ж��Ƿ�������
def is_num(*args):
    #print(type(args),args)
    tmp=0
    for i in args:
        if re.findall('^\d+$',i) or i=='':
            tmp+=1
        else:
            tmp=0
    return True if tmp == len(args) else False
#��Сkb
def changekb():
    if event == 'ys_btn':
        if value['ys_n'] == '' or is_num(value['ys_n'])==False:
            windows['errortext'].update('����������!', text_color='blue',background_color='#64778d')
        elif value['-IN-'] == '':
            windows['errortext'].update('��ѡȡͼƬ!', text_color='blue',background_color='#64778d')
        else:
            imglist = is_image(value['-IN-'])
            errorstr=''
            if value['dxc']:
                for imgfile in imglist:
                    threadpool.submit(compress_image,r'%s' % imgfile, mb=int(value['ys_n']))
                    #errorstr+=compress_image(r'%s' % imgfile, mb=int(value['ys_n']))+'\n'
            else:
                for imgfile in imglist:
                    #threadpool.submit(compress_image,r'%s' % imgfile, mb=int(value['ys_n']))
                    errorstr+=compress_image(r'%s' % imgfile, mb=int(value['ys_n']))+'\n'
            windows['errortext2'].update(errorstr.strip())
            windows['errortext'].update('ִ�����!',text_color='blue', background_color="yellow")
            windows['ys_n'].update('')
            windows['-FILESLB-'].update('')
            windows['-IN-'].update('')
            windows['-NUM-'].update('')

#����ͼƬ
def changels():
    if event == 'fbl_btn':
        if value['fbl_x'] == '' and value['fbl_y'] == '' \
                or is_num(value['fbl_x'],value['fbl_y'])==False:
            # print("����������!")
            windows['errortext'].update('����������!', text_color='blue',background_color='#64778d')
        elif value['-IN-'] == '':
            # print("��ѡȡͼƬ!")
            windows['errortext'].update('��ѡȡͼƬ!', text_color='blue',background_color='#64778d')
        else:
            f1 = int(value['fbl_x']) if value['fbl_x'] != '' else 0
            f3 = int(value['fbl_y']) if value['fbl_y'] != '' else 0
            imglist = is_image(value['-IN-'])
            errorstr=''
            for imgfile in imglist:
                errorstr+=resize_image(r'%s' % imgfile, x_s=f1, y_s=f3)+'\n'
            windows['errortext2'].update(errorstr.strip())
            windows['errortext'].update('ִ�����!', text_color='blue', background_color="yellow")
            windows['fbl_x'].update('')
            windows['fbl_y'].update('')
            windows['-FILESLB-'].update('')
            windows['-IN-'].update('')
            windows['-NUM-'].update('')
#�ü�ͼƬ
def changecj():
    if event == 'cj_btn':
        if value['up_n'] == '' or value['up_n'] == '' \
                or value['life_n'] == '' or value['right_n'] == '' \
                or is_num(value['up_n'], value['up_n'], value['life_n'], value['right_n']) == False:
            # print("����������!")
            windows['errortext'].update('����������!', text_color='blue',background_color='#64778d')
        elif value['-IN-'] == '':
            # print("��ѡȡͼƬ!")
            windows['errortext'].update('��ѡȡͼƬ!', text_color='blue',background_color='#64778d')
        else:
            up_n = int(value['up_n'])
            down_n = int(value['down_n'])
            life_n = int(value['life_n'])
            right_n = int(value['right_n'])
            trupe_crop =[up_n,down_n,life_n,right_n]
            imglist = is_image(value['-IN-'])
            errorstr=''
            for imgfile in imglist:
                errorstr+=crop_img(imgfile, trupe_crop)+'\n'
            windows['errortext2'].update(errorstr.strip())
            windows['errortext'].update('ִ�����!', text_color='blue', background_color="yellow")
            windows['up_n'].update('')
            windows['down_n'].update('')
            windows['life_n'].update('')
            windows['right_n'].update('')
            windows['-FILESLB-'].update('')
            windows['-IN-'].update('')
            windows['-NUM-'].update('')
#���вü�ͼƬ
def changejzcj():
    if event == 'jzfbl_btn':
        if value['jzfbl_x'] == '' and value['jzfbl_y'] == '' \
            or is_num(value['jzfbl_x'], value['jzfbl_y']) == False:
            # print("����������!")
            windows['errortext'].update('������ֱ���!', text_color='blue',background_color='#64778d'
                                        )
        elif value['-IN-'] == '':
            # print("��ѡȡͼƬ!")
            windows['errortext'].update('��ѡȡͼƬ!', text_color='blue',background_color='#64778d')
        else:
            jzfbl_x = int(value['jzfbl_x']) if value['jzfbl_x'] != '' else 0
            jzfbl_y = int(value['jzfbl_y']) if value['jzfbl_y'] != '' else 0
            imglist = is_image(value['-IN-'])
            trupe_crop=(jzfbl_x,jzfbl_y)
            errorstr=''
            for imgfile in imglist:
                errorstr+=crop_img2(imgfile, trupe_crop)+'\n'
            windows['errortext2'].update(errorstr.strip())
            windows['errortext'].update('ִ�����!', text_color='blue', background_color="yellow")
            windows['jzfbl_x'].update('')
            windows['jzfbl_y'].update('')
            windows['-FILESLB-'].update('')
            windows['-IN-'].update('')
            windows['-NUM-'].update('')
while True:
    event,value = windows.read(timeout=100)
    if event in (sg.WIN_CLOSED,'Exit'):
        break
    if event=='-IN-':
        #print(len(is_image(value['-IN-'])))
        img_list=is_image(value['-IN-'])
        #��ЧͼƬ·��
        windows['-FILESLB-'].update(tm for tm in img_list)
        windows['-NUM-'].update('һ��'+str(len(img_list))+'��ͼƬ',visible=True)
    changekb()
    changels()
    changecj()
    changejzcj()
    #print(event,value,sg.theme_background_color())
threadpool.shutdown(True)
windows.close()