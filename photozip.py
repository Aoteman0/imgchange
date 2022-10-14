from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog

def get_size(file):
    size = os.path.getsize(file)
    return size / 1024
def get_outfile(infile,outfile,name_tmp="new"):
    if outfile:
        return outfile
    file_name=os.path.basename(infile)  # 返回文件名
    dir, suffix = os.path.splitext(file_name) #分离名称和后缀
    dir_name=os.path.dirname(infile)  # 返回目录路径
    dir_new_name=dir_name+'/image_new/'
    if os.path.exists(dir_new_name)==False:
        os.mkdir(dir_new_name)
    #print(os.path.join('root', 'test', 'runoob.txt'))  # 将目录和文件名合成一个路径
    #print(file_name,dir_name,dir)
    outfile = '{}{}_{}{}'.format(dir_new_name,dir,name_tmp,suffix)
    #print(outfile)
    return outfile

def compress_image(infile, outfile='', mb=100,tmp=1,quality=95):
    o_size = get_size(infile)
    if o_size <= mb:
        return ('图片小于设置'+'\n'+infile)
    outfile = get_outfile(infile, outfile)
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality-tmp<0:
            break
        quality-=tmp
        o_size = get_size(outfile)
    return ''


def thumbnail_img(infile, outfile='', width=0):
    with Image.open(infile) as im:
        width,height=im.size
        im.thumbnail()

def compress_image_list(infile, outfile='', mb=100,tmp=1,quality=95):
    pass
def resize_image(infile, outfile='', x_s="",y_s=""):
    """修改图片尺寸
    :param infile: 图片源文件
    :param outfile: 重设尺寸文件保存地址
    :param x_s: 设置的宽度
    :return:
    """
    im = Image.open(infile)
    x, y = im.size
    try:
        if y_s==0 and x_s!=0:
            y_s = int(y * x_s / x)
            out = im.resize((x_s, y_s),resample=Image.Resampling.HAMMING,reducing_gap=3)
            outfile = get_outfile(infile, outfile,name_tmp=x_s)
        elif x_s==0 and y_s!=0:
            x_s = int(x * y_s / y)
            out = im.resize((x_s, y_s),resample=Image.Resampling.HAMMING,reducing_gap=3)
            outfile = get_outfile(infile, outfile,name_tmp=y_s)
        elif x_s!=0 and y_s!=0:
            out = im.resize((x_s, y_s),resample=Image.Resampling.HAMMING,reducing_gap=3)
            outfile = get_outfile(infile, outfile, name_tmp="new")

    except:
        pass
    out.save(outfile)
    return ''
def ChangeImage(infile):
    im = Image.open(infile)
    image=im.convert('RGB')
    dir, suffix = os.path.splitext(infile)
    outfile = '{}_{}{}'.format(dir, "new",".jpg")
    image.save(outfile)
    return ''

#裁剪图片 根据边距进行裁剪
def crop_img(infile,list1=[], outfile=''):
    x1, y1, x2, y2=list(map(lambda x: int(x), list1))
    outfile = get_outfile(infile,outfile)

    with Image.open(infile) as im:
        width,heigth = im.size
        if x1>heigth or y1>heigth or x2>width or y2>width:
            return ('输入的值不能大于图片像素'+'\n'+infile)
        elif x1+y1>heigth or x2+y2>width:
            return ('边距和不能大于图片像素'+'\n'+infile)
        x1,y1=y1,x1
        x2=width-y2
        y2=heigth-y1
        img_tuple = tuple((x1, y1, x2, y2))
        new_image = im.crop(img_tuple)
        #new_image.show()
        new_image.save(outfile)
        return ''
#裁剪图片 根据像素居中裁剪
def crop_img2(infile,list1=[], outfile=''):
    try:
        new_width,new_height=list(map(lambda x: int(x), list1))
        #print(outfile)
        with Image.open(infile) as im:
            width, heigth = im.size
            x1,y1,x2,y2=0,0,0,0
            if new_width>width or new_height>heigth:
                return ('输入的值不能大于图片像素'+'\n'+infile)
            if new_height == 0 and new_width != 0:
                new_height = int(heigth * new_width / width)
                y1 = int((heigth - new_height) / 2)
                y2 = y1 + new_height
            elif new_width == 0 and new_height != 0:
                new_width = int(width * new_height / heigth)
                x1 = int((width - new_width) / 2)
                x2 = x1 + new_width
            else:
                x1=int((width-new_width)/2)
                y1=int((heigth-new_height)/2)
                x2=x1+new_width
                y2=y1+new_height

            x1 = int((width - new_width) / 2)
            y1 = int((heigth - new_height) / 2)
            x2 = x1 + new_width
            y2 = y1 + new_height
            img_tuple = tuple((x1, y1, x2, y2))

            new_image = im.crop(img_tuple)
            outfile = get_outfile(infile, outfile, name_tmp=str(new_width) + "&" + str(new_height))
            #print(outfile)
            new_image.save(outfile)
            return ''
    except Exception as e:
        pass
        #print(e,e.__traceback__.tb_lineno)
def lst():#略缩图
    with Image.open('C:/Users/LXF/Desktop/新建文件夹/图片压缩/新建文件夹/123.jpg') as im:
        size=500,500
        im.thumbnail(size)
        im.save('C:/Users/LXF/Desktop/新建文件夹/图片压缩/新建文件夹/123_new.jpg')
        im.show()

def test():
    with Image.open('C:/Users/LXF/Desktop/中西餐前台销售/123.jpg') as im:
        width,height=im.size
        new_im=im.resize((1080,607),resample=Image.Resampling.HAMMING,reducing_gap=3)
        new_im.save('C:/Users/LXF/Desktop/中西餐前台销售/123_new5.jpg')
#格式转换
def change_img():
    with Image.open('C:/Users/LXF/Desktop/新建文件夹/图片压缩/新建文件夹/123.jpg') as im:
        #image = im.convert('RGB')
        size=1080,1000
        #print(type(size))
        im.thumbnail(size)
        im.save('C:/Users/LXF/Desktop/新建文件夹/图片压缩/新建文件夹/123_new.jpg')
        im.show()

def aaa():
    pass
    # root =tk.Tk()
    # try:
    #     root.withdraw() #tkinter 隐藏主窗口,只显示对话框
    #
    #      #拿到文件路径
    #     #print(type(Fpath))
    #     # print("\n1、按图片大小kb")
    #     # print("\n2、调整分辨率(拉伸图片)")
    #     # print("\n3、调整分辨率(裁剪图片)")
    #     # print("\n4、格式转换")
    #     # print("\n0、退出")
    #     # s_id = input("\n请输出操作编号：")
    #     if s_id=='1':
    #         Fpath_tuple = filedialog.askopenfilenames()
    #         quality_num = int(input("\n压缩到kb："))
    #         for Fpath in Fpath_tuple:
    #             #print(Fpath)
    #             compress_image(r'%s' % Fpath, mb=quality_num)
    #     elif s_id=='2':
    #         Fpath_tuple = filedialog.askopenfilenames()
    #         width_num = int(input("\n改变后的宽度："))
    #         height_num = int(input("\n改变后的高度："))
    #         for Fpath in Fpath_tuple:
    #             resize_image(r'%s' % Fpath,x_s=width_num,y_s=height_num)
    #     elif s_id == '3':
    #         print("\n1、根据边距裁剪图片")
    #         print("\n2、根据像素裁剪图片（居中裁剪）")
    #         s_id_1 = input("\n请输出操作编号：")
    #         if s_id_1=='1':
    #             Fpath_tuple = filedialog.askopenfilenames()
    #             trupe_crop = input("\n裁剪上下左右距离（如：10,20,30,40）：").split(',')
    #             for Fpath in Fpath_tuple:
    #                 #print('Fpath',type(trupe_crop),trupe_crop)
    #                 crop_img(Fpath,trupe_crop)
    #         elif s_id_1== '2':
    #             Fpath_tuple = filedialog.askopenfilenames()
    #             trupe_crop = input("\n裁剪后像素（如：1024，768）：").split(',')
    #             for Fpath in Fpath_tuple:
    #                 #print('Fpath',type(trupe_crop),trupe_crop)
    #                 crop_img2(Fpath, trupe_crop)
    #     elif s_id=="4":
    #         Fpath = filedialog.askopenfilename()
    #         ChangeImage(r'%s' % Fpath)
    # except:
    #     quit()


#if __name__ == '__main__':
    #aaa()
    #test()
    #change_img()
    #crop_img(100,100,100,100)
    
