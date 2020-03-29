# To design a UI
# by citrus in 2020/3
import tkinter
from tkinter import *
from tkinter import ttk
import json


# Def a func to read the file:'scraped_data.json'

def json_reader():
    with open('./scraped_data.json', 'r') as f:
        data = json.load(f)
    return data


# Def a func to get all the tags with a list returned

def tag_dealer(data):
    tag_list = []
    key = 'tag'
    repeat = 0
    for dict_items in data:
        for tag_items in tag_list:
            if tag_items == dict_items[key]:
                repeat = 1
                break
        if repeat == 0:  # no repeat or do nothing otherwise
            tag_list.append(dict_items[key])
        else:
            repeat = 0
    return tag_list


# Def a func to get the specific tag and its inf

def tag_finder(tag, data):
    key = 'tag'
    res_list = []
    book_list = []
    note_list = []
    ret_list = []

    for dict_items in data:
        if tag == dict_items[key]:
            num = 0
            for items in dict_items['book_name']:
                book_list.append(items)
            for items in dict_items['resource']:
                res_list.append(items)
            for items in dict_items['note']:
                if items.find("360") == -1:  # not 360 cloud
                    note_list.append(items)
            while len(note_list) < len(res_list):
                note_list.append('无需提取码')

    for index in range(len(book_list)):
        ret_list.append(tag)
        ret_list.append(book_list[index])
        ret_list.append(res_list[index])
        ret_list.append(note_list[index])

    return ret_list


def set_treeview(win, tv, ww, wh):
    tv.column("标签", width=150, anchor='center')
    tv.column("书名", width=250, anchor='center')
    tv.column("资源", width=250, anchor='center')
    tv.column("备注", width=150, anchor='center')
    tv.heading("标签", text="标签")
    tv.heading("书名", text="书名")
    tv.heading("资源", text="资源")
    tv.heading("备注", text="备注")

    # add scroll bar
    vbar = ttk.Scrollbar(win, orient=VERTICAL, command=tv.yview)
    tv.configure(yscrollcommand=vbar.set)
    tv.place(x=(ww / 2 - 250), y=(wh / 4), height=wh / 2)
    vbar.place(x=(ww / 2 + 550), y=(wh / 4), height=wh / 2)


def set_label(win, ww, wh):
    label_main = tkinter.Label(
        win,
        text="书籍信息采集结果 BY CITRUS",
        font=("宋体", 18)
    )
    label_main.place(x=(ww / 2 - 150), y=(wh / 2 - 300))

    label_select = tkinter.Label(
        win,
        text="选择书籍分类（可多选）",
        font=("宋体", 11)
    )
    label_select.place(x=ww / 8, y=wh / 4 - 30)
    label_result = tkinter.Label(
        win,
        text="查询结果",
        font=("宋体", 11)
    )
    label_result.place(x=ww/2+110, y=wh/4-30)


# Def a func to as the event when choosing a tag


def tag_chosen(tag_list, data, treeview,lb):
    # clean up tree view
    x = treeview.get_children()
    for item in x:
        treeview.delete(item)
    chosen_list = lb.curselection()
    row = 0
    for chosen_items in chosen_list:
        temp_list = tag_finder(tag_list[chosen_items], data)
        lenth_by4 = int(len(temp_list)/4)
        for num in range(lenth_by4):
            i = num*4
            treeview.insert('', row, values=(temp_list[i], temp_list[i+1], temp_list[i+2], temp_list[i+3]))
            row = row + 1


def main():

    win = tkinter.Tk()

    win.title("SYSTEM UI BY CITRUS")
    # Set parameters for windows
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    ww = sw*2/3
    wh = sh*2/3
    offsetx = (sw - ww) / 2
    offsety = (sh - wh) / 2

    win.geometry("%dx%d+%d+%d" % (ww, wh, offsetx, offsety))

    # Preparation of basic data
    book_data = json_reader()  # main data
    tag_list1 = tag_dealer(book_data)  # all of the tags
    columns1 = ('标签', '书名', '资源', '备注')
    tv = ttk.Treeview(win, show="headings", columns=columns1)

    # Tag list in the left side

    sb1 = Scrollbar(win)
    sb1.place(x=ww/4, y=wh/4, height=wh/2)

    # Initialize the list
    lb = Listbox(win, selectmode=MULTIPLE, yscrollcommand=sb1.set)

    for tag_items in tag_list1:
        lb.insert(END, tag_items)

    lb.place(x=(ww/8), y=(wh/4), height=wh/2, width=ww/8)
    lb.bind('<<ListboxSelect>>', lambda event: tag_chosen(tag_list1, book_data, tv,lb))
    # Combine the scroll
    sb1.config(command=lb.yview)

    # Info tree view in the right side

    set_label(win, ww, wh)
    set_treeview(win, tv, ww, wh)

    # cannot change size of windows
    win.resizable(0, 0)

    win.mainloop()


if __name__ == "__main__":
    main()
