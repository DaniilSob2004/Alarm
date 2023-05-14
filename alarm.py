import threading
import re
import pygame

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from datetime import *
from PIL import Image, ImageTk
from tkcalendar import *
from time import time
import babel.numbers


WIDTH = 530
HEIGHT = 280
pygame.init()


class Alarm(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title("Будильник")
        self.resizable(False, False)
        self["bg"] = "khaki1"
        x = int(self.winfo_screenwidth() / 2 - WIDTH / 2)
        y = int(self.winfo_screenheight() / 2 - HEIGHT / 2)
        self.geometry("{0}x{1}+{2}+{3}".format(WIDTH, HEIGHT, x, y))
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.begin_settings()
        self.load_obj()
        self.read_file()
        self.clear_list("")
        self.sort_alarm_value(False)
        self.get_list_all_alarm()
        self.add_label()
        self.add_button()
        self.load_alarm()
        self.start_alarm()

        self.iconbitmap(r"image\alarm.ico")

    def begin_settings(self):
        self.root_run = None
        self.dict_months = {"Янв": 1, "Фев": 2, "Март": 3, "Апр": 4, "Май": 5, "Июнь": 6, "Июль": 7, "Авг": 8, "Сент": 9, "Окт": 10, "Нояб": 11, "Дек": 12}
        self.listCheck = []  # список: StringVar() для получения значения Checkbutton
        self.dict_dataFrames = {}  # словарь дат фреймов: ключ - объект фрейм, значение - размещение этого фрейма(индекс, row)
        self.keys, self.values = [], []  # даты, и все будильники
        self.list_alarmFrames = []  # список всех будильников фреймов (Размещены как в self.values)
        self.SpinVar = []  # список StringVar() для получения значения Spinbox
        self.all_spin = [[Spinbox(), ""], [Spinbox(), ""], [Spinbox(), ""]]  # все объекты Spinbox и их значения
        self.sort_data = []  # рассположение всех будильников по убыванию (Размещены как в self.values), затем копируем в self.values
        self.list_all_alarm = []  # обычный список всех будильников(Даты)
        self.start = False  # для бесконечного работающего будильника
        self.is_work_alarm = False
        calendar = ""  # значение выбранной даты

    def load_obj(self):
        self.img_add = ImageTk.PhotoImage(Image.open(r"image\add.png").resize((38, 38), Image.ANTIALIAS))
        self.img_delete = ImageTk.PhotoImage(Image.open(r"image\delete.png").resize((31, 31), Image.ANTIALIAS))
        self.img_delete_all = ImageTk.PhotoImage(Image.open(r"image\delete_all.png").resize((30, 30), Image.ANTIALIAS))
        self.img_exit = ImageTk.PhotoImage(Image.open(r"image\exit.png").resize((38, 38), Image.ANTIALIAS))
        self.img_send = ImageTk.PhotoImage(Image.open(r"image\send.png").resize((29, 29), Image.ANTIALIAS))
        self.img_search = ImageTk.PhotoImage(Image.open(r"image\search.png").resize((25, 25), Image.ANTIALIAS))
        self.main_frame = LabelFrame()  # самый главный фрейм
        self.today_date = datetime.today()  # сегодняшняя дата
        self.canvas = Canvas()
        self.lbl_empty = Label()  # пустая метка
        self.text = Entry()  # текст будильника
        self.music = Entry()  # путь к музыке в поле ввода виджета Entry()
        self.text_music = "Egor Kreed - Cosmoboy.mp3"  # путь к музыке (По умолчанию)

    def start_alarm(self):
        if len(self.list_all_alarm) > 0:
            self.start = True
            threading.Thread(target=self.start_alarm_2()).start()

    def start_alarm_2(self):
        if self.start:
            second_now = time()
            d = datetime(int(self.list_all_alarm[0][6:10]),
                         int(self.list_all_alarm[0][3:5]),
                         int(self.list_all_alarm[0][0:2]),
                         int(self.list_all_alarm[0][11:13]),
                         int(self.list_all_alarm[0][14:16]),
                         int(self.list_all_alarm[0][17:]))

            if second_now > int(d.timestamp()):
                self.start = False
                self.is_work_alarm = True
                self.play_sound()
                self.message_run_alarm()
            else:
                self.after(500, self.start_alarm_2)
        else:
            self.add_alarm()
            if len(self.list_all_alarm) > 0:
                self.start = True
                self.after(500, self.start_alarm_2)

    def play_sound(self):
        pygame.mixer.music.load(self.values[0][0][0])
        pygame.mixer.music.play()

    def click_run_btn(self, event):
        self.is_work_alarm = False

        if len(self.values[0]) == 1:
            del self.keys[0]
            del self.values[0]
        else:
            del self.values[0][0]

        self.root_run.destroy()
        pygame.mixer.music.stop()
        self.start_alarm_2()

    def message_run_alarm(self):
        self.root_run = Tk()
        self.root_run.title("Будильник")
        self.root_run.resizable(False, False)
        self.root_run["bg"] = "khaki1"
        width, height = 320, 150
        x = int(self.root_run.winfo_screenwidth() / 2 - WIDTH / 2)
        y = int(self.root_run.winfo_screenheight() / 2 - HEIGHT / 2)
        self.root_run.geometry("{0}x{1}+{2}+{3}".format(width, height, x, y))
        self.root_run.iconbitmap(r"image\run.ico")
        self.root_run.focus_force()
        self.root_run.wm_attributes("-topmost", 1)

        if len(self.values[0][0][1]) <= 15:
            text = self.values[0][0][1]
        else:
            text = self.values[0][0][1][:13] + "..."

        lab_go = Label(self.root_run, text="Время пришло!!!", font=("Tahoma", 15, "bold"), bg="khaki1", fg="red")
        lab_text = Label(self.root_run, text='"{}"'.format(text), font=("Tahoma", 14, "bold"), bg="khaki1")
        lab_time = Label(self.root_run, text='Время:  "{}"'.format(self.values[0][0][-1]), font=("Tahoma", 13, "bold"), bg="khaki1")
        btn_ok = Button(self.root_run, text="ok", font=("Tahoma", 10, "bold"), bg="khaki1", bd=3, width=6, activebackground="red", cursor="hand2", command=lambda event="": self.click_run_btn(event))
        lab_go.place(relx=0.5, rely=0.1, anchor="center")
        lab_text.place(relx=0.5, rely=0.35, anchor="center")
        lab_time.place(relx=0.5, rely=0.6, anchor="center")
        btn_ok.place(relx=0.5, rely=0.85, anchor="center")
        self.root_run.bind("<Return>", self.click_run_btn)

    def read_file(self):
        first_index = 0
        index, length = [], []

        with open(r"file\keys.txt", "r", encoding="utf-8") as file:
            self.keys = [line.strip() for line in file]
        with open(r"file\values.txt", "r", encoding="utf-8") as file:
            list1 = [line.strip() for line in file]

        if len(self.list_all_alarm) > 0:
            list1 = self.check_file_data(list1)

        for l in range(len(self.keys)):
            self.values.append([])
            length.append(0)
        for i in range(len(self.keys)):
            for v in list1:
                if v[0:10] == self.keys[i]:
                    length[i] += 1
                    self.values[i] = [[]] * length[i]
                    index.append(0)

        q = 0
        for l in range(len(length)):
            for m in range(len(self.values[l])):
                first_index += int(length[l] / length[l] * 3)
                index[q] = first_index
                q += 1

        q = 0
        for l in range(len(self.values)):
            for i in range(len(self.values[l])):
                if l == 0:
                    if i == 0:
                        val = list1[0:index[q]]
                    else:
                        val = list1[index[q - 1]:index[q]]
                else:
                    val = list1[index[q - 1]:index[q]]
                self.values[l][i] = val
                q += 1

        self.get_list_all_alarm()

    def write_file(self):
        key = open(r"file\keys.txt", "w", encoding="utf-8")
        value = open(r"file\values.txt", "w", encoding="utf-8")

        for k in range(len(self.keys)):
            key.write(self.keys[k] + "\n")
            for l in range(len(self.values[k])):
                for v in self.values[k][l]:
                    value.write(v + "\n")

        key.close()
        value.close()

    def check_file_data(self, values):
        new_sec = []
        second_now = time()

        for d in range(2, len(values), 3):
            d = datetime(int(values[d][6:10]), int(values[d][3:5]), int(values[d][0:2]), int(values[d][11:13]), int(values[d][14:16]), int(values[d][17:]))
            if int(d.timestamp()) > second_now:
                d = str(datetime.fromtimestamp(int(d.timestamp())))
                data = "{0}/{1}/{2} {3}".format(d[8:10], d[5:7], d[:4], d[-8:])
                new_sec.append(data)

        index = values.index(new_sec[0])
        index_data = self.keys.index(new_sec[0][:10])
        self.keys = self.keys[index_data:]
        return values[index - 2:]

    def style_menu(self):
        self.main_frame = LabelFrame(self, text="Расписание", bg="khaki1", bd=3)
        self.canvas = Canvas(self, borderwidth=0, bg="khaki1", highlightbackground="khaki1")
        self.scroll = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.canvas["yscrollcommand"] = self.scroll.set
        self.main_frame.place(relx=0.01, rely=0.01, width=WIDTH - 65, height=HEIGHT - 50)

        if len(self.list_all_alarm) < 4:
            if len(self.values) == 0:
                self.lbl_empty = Label(self.main_frame, text="Пусто", font=("Tahoma", 10), bg="khaki1")
                self.lbl_empty.place(relx=0.5, rely=0.45, anchor="center")
            self.canvas.place(relx=0, rely=0, width=1, height=1)
            self.scroll.place(relx=0.849, rely=0.044, height=218)
        else:
            self.canvas.place(relx=0.015, rely=0.06, width=WIDTH - 72, height=HEIGHT - 68)
            self.scroll.place(relx=0.848, rely=0.046, height=218)
            self.frame = Frame(self.canvas, bg="khaki1", width=WIDTH - 72, height=HEIGHT - 68)
            self.canvas.create_window((1, 1), window=self.frame, anchor="nw")
            self.frame.bind("<Configure>", self.on_frame_configure)
            self.main_frame = self.frame

    def load_alarm(self):
        for k in range(len(self.keys)):
            lbl_data = Label(self.main_frame, text=self.keys[k], bg="khaki1", fg="navy", font=("Tahoma", 8, "bold"))
            data_frames = LabelFrame(self.main_frame, labelwidget=lbl_data, bg="khaki1", width=WIDTH, bd=3)
            data_frames.grid(row=k, column=0, sticky="w")
            self.dict_dataFrames.update({data_frames: k})

            for i in range(len(self.values[k])):
                if len(self.values[k][i][1]) <= 15:
                     text = self.values[k][i][1]
                else:
                    text = self.values[k][i][1][:13] + "..."

                alarm_frame = LabelFrame(data_frames, bg="khaki1", width=WIDTH, bd=2)
                alarm_frame.grid(row=i, column=0, pady=2, sticky="w")
                self.list_alarmFrames[k][i] = alarm_frame
                lab_data = Label(alarm_frame, text="{0}) {1}".format(i + 1, self.values[k][i][-1][11:]), bg="khaki1")
                lab_text = Label(alarm_frame, text=text, bg="khaki1", width=15)
                lab_data.grid(row=i, column=0)
                lab_text.grid(row=i, column=1, padx=104)
                choice = StringVar()
                check = Checkbutton(alarm_frame, variable=choice, onvalue="{}.{}".format(k, i), offvalue="-1", bg="khaki1", selectcolor="khaki1", activebackground="khaki1")
                check.grid(row=i, column=2, padx=15)
                check.deselect()
                self.listCheck.append(choice)

    def add_alarm(self):
        self.start = False
        self.canvas.destroy()
        self.scroll.destroy()
        self.clear_list("")
        self.get_list_all_alarm()
        self.style_menu()
        self.load_alarm()
        self.start = True

    def del_alarm(self):
        self.start = False
        del_index = []

        for i in range(len(self.listCheck)):
            if self.listCheck[i].get() != "-1":
                index = self.listCheck[i].get().find(".")
                k = int(self.listCheck[i].get()[:index])
                v = int(self.listCheck[i].get()[index + 1:])
                del_index.append(self.values[k][v])

        for del1 in range(len(del_index)):
            for k in range(len(self.keys)):
                for v in range(len(self.values[k])):
                    if self.values[k][v] == del_index[del1]:
                        self.values[k][v] = "0"
                        try:
                            for z in range(len(self.values[k])):
                                int(self.values[k][z])
                        except TypeError:
                            pass
                        else:
                            self.keys[k] = "0"
                            self.values[k] = ["0"]
                        break

        new_values = self.clear_list("del_alarm")
        new_keys = []
        for i in range(len(self.keys)):
            if self.keys[i] != "0":
                new_keys.append(self.keys[i])

        dict1 = {}
        for k in range(len(self.keys)):
            if self.keys[k] != "0":
                for v in range(len(self.values[k])):
                    if self.values[k][v] != "0":
                        data = re.search(r"\d{2}/\d{2}/\d{4}", self.values[k][v][-1]).group(0)
                        index = new_keys.index(data)
                        if str(index) in dict1:
                            dict1[str(index)].append(self.values[k][v])
                        else:
                            dict1.update({str(index): [self.values[k][v]]})

        key = list(dict1.keys())
        for k in range(len(key)):
            for i in range(len(dict1[str(k)])):
                new_values[k].append(dict1[str(k)][i])

        self.values = new_values[:]
        self.keys = new_keys[:]
        self.add_alarm()
        self.start = True

    def del_all_alarm(self):
        self.start = False
        self.canvas.destroy()
        self.scroll.destroy()
        self.begin_settings()
        self.style_menu()

    def create_btn(self, img, x, y, tag, window):
        if tag == "send" or tag == "search":
            window = window
        else:
            window = self

        btn = Button(window, image=img, bd=0, bg="khaki1", cursor="hand2", text=tag)
        btn.place(relx=x, rely=y)
        btn.bind("<Enter>", self.enter_btn)
        btn.bind("<Leave>", self.leave_btn)
        btn.bind("<Button-1>", self.click_btn)

    def create_label(self, x, y, text, window):
        lbl = Label(window, text=text, bg="khaki1", font=("Tahoma", 9, "bold"), fg="navy")
        lbl.place(relx=x, rely=y)

    def add_label(self):
        lab_time = Label(self, text="Время", bg="khaki1", font=("Tahoma", 10, "bold"), fg="navy")
        lab_text = Label(self, text="Текст", bg="khaki1", font=("Tahoma", 10, "bold"), fg="navy")
        lab_choice = Label(self, text="Выбор", bg="khaki1", font=("Tahoma", 10, "bold"), fg="navy")
        lab_time.place(relx=0.03, rely=0.84)
        lab_text.place(relx=0.4, rely=0.84)
        lab_choice.place(relx=0.755, rely=0.84)

        lab_data = Label(self, text="Дата: {0}.{1}.{2}".format(self.today_date.day, self.today_date.month, self.today_date.year), font=("Tahoma", 8, "bold"), bg="khaki1", fg="red")
        lab_data.place(relx=0.9, rely=0.97, anchor="center")

        self.style_menu()

    def add_button(self):
        self.create_btn(img=self.img_add, x=0.91, y=0.06, tag="add", window=self)
        self.create_btn(img=self.img_delete, x=0.915, y=0.28, tag="del", window=self)
        self.create_btn(img=self.img_delete_all, x=0.915, y=0.49, tag="del_all", window=self)
        self.create_btn(img=self.img_exit, x=0.91, y=0.66, tag="exit", window=self)

    def add_alarm_window(self):
        self.root = Toplevel()
        self.root.title("Создание будильника")
        self.root.resizable(False, False)
        self.root["bg"] = "khaki1"
        width, height = 340, 200
        x = int(self.root.winfo_screenwidth() / 2 - WIDTH / 2)
        y = int(self.root.winfo_screenheight() / 2 - HEIGHT / 2)
        self.root.geometry("{0}x{1}+{2}+{3}".format(width, height, x, y))
        self.root.iconbitmap(r"image\add.ico")
        self.root.focus_force()
        self.root.protocol("WM_DELETE_WINDOW", self.close_window_alarm)

        frame = LabelFrame(self.root, text="Настройки", width=width - 5, height=height - 45, bd=3, bg="khaki1")
        frame.place(relx=0.01, rely=0.01)

        xy = ((0.01, 0.01, "Часы"), (0.32, 0.01, "Минут:"), (0.65, 0.01, "Секунд:"), (0.01, 0.26, "Выберите дату:"), (0.01, 0.52, "Выбрать музыку:"), (0.01, 0.77, "Введите текст:"))
        for i in range(len(xy)):
            self.create_label(x=xy[i][0], y=xy[i][1], text=xy[i][2], window=frame)

        self.calendar = DateEntry(frame, width=15, background="darkblue", foreground="red", borderwidth=3, state="readonly", date_pattern="dd/mm/yyyy")
        self.calendar.place(relx=0.35, rely=0.26)
        self.calendar.bind("<<DateEntrySelected>>", self.check_error_data)

        self.music = Entry(frame, font=("Tahoma", 9, "bold"), width=19, state="normal")
        self.music.place(relx=0.37, rely=0.55)
        self.music.insert(0, "По умолчанию")
        self.music.configure(state="readonly")

        self.create_btn(img=self.img_search, x=0.87, y=0.5, tag="search", window=frame)
        self.create_btn(img=self.img_send, x=0.485, y=0.81, tag="send", window=self.root)

        self.text = Entry(frame, font=("Tahoma", 9, "bold"), width=24)
        self.text.place(relx=0.37, rely=0.775)

        self.create_spinbox(frame)

    def create_spinbox(self, window):
        self.SpinVar = [StringVar(), StringVar(), StringVar()]
        values = ((0.14, 0.02, 6, 23), (0.48, 0.02, 0, 59), (0.83, 0.02, 0, 59))

        for i in range(3):
            spin = Spinbox(window, from_=values[i][2], to=values[i][3], font=("Tahoma", 9, "bold"), width=5, textvariable=self.SpinVar[i], command=self.get_value_spinbox, state="readonly")
            spin.place(relx=values[i][0], rely=values[i][1])
            self.all_spin[i][0] = spin

        for i in range(3):
            self.all_spin[i][1] = self.SpinVar[i].get()

    def get_value_spinbox(self, a=None, b=None, c=None):
        for i in range(3):
            self.all_spin[i][1] = self.SpinVar[i].get()

    def find_music(self):
        filename = askopenfilename(title="Открыть файл", initialdir="/", filetypes=(("Файл mp3", "*.mp3"),))
        start = filename.rfind("/")

        if filename:
            self.text_music = filename
            self.music.configure(state="normal")
            self.music.delete(0, "end")
            self.music.insert(0, filename[start + 1:])
            self.music.configure(state="readonly")

        self.root.focus_force()

    def write_dict_alarm(self):
        hour, min, sec = self.add_zero_in_time()

        if len(self.keys) == 0:
            self.keys.append(self.calendar.get())
            self.values.append([[self.text_music, self.text.get().strip(), self.calendar.get() + " " + hour + ":" + min + ":" + sec]])
        else:
            for key in self.keys:
                if key != self.calendar.get():
                    continue
                index = self.keys.index(self.calendar.get())
                self.values[index].extend([[self.text_music, self.text.get().strip(), self.calendar.get() + " " + hour + ":" + min + ":" + sec]])
                break
            else:
                self.keys.append(self.calendar.get())
                self.sort_alarm_key()
                index = self.keys.index(self.calendar.get())
                self.values.insert(index, [[self.text_music, self.text.get().strip(), self.calendar.get() + " " + hour + ":" + min + ":" + sec]])

        self.sort_alarm_value(True)
        self.root.destroy()
        self.focus_force()

    def sort_alarm_key(self):
        d1 = ""
        sec = []

        for i in range(len(self.keys)):
            d1 = datetime(int(self.keys[i][6:10]), int(self.keys[i][3:5]), int(self.keys[i][0:2]))
            sec.append(int(d1.timestamp()))

        sec.sort()
        self.keys.clear()

        for i in range(len(sec)):
            d2 = str(d1.fromtimestamp(sec[i]))
            data = "{0}/{1}/{2}".format(d2[8:10], d2[5:7], d2[:4])
            self.keys.append(data)

    def sort_alarm_value(self, start):
        if start:
            self.clear_list("sort")

        for k in range(len(self.keys)):
            for i in range(len(self.values[k])):
                data = self.values[k][i][-1]
                d = datetime(int(data[6:10]), int(data[3:5]), int(data[0:2]), int(data[11:13]), int(data[14:16]), int(data[17:]))
                self.sort_data[k][i] = int(d.timestamp())

        all_data = self.sort_data[:]
        list_new_sort_data = self.sort_data[:]
        for k in range(len(self.keys)):
            s1 = sorted(all_data[k])
            self.sort_data[k] = s1

        for k in range(len(self.keys)):
            for i in range(len(self.values[k])):
                d = str(datetime.fromtimestamp(self.sort_data[k][i]))
                data = "{0}/{1}/{2} {3}".format(d[8:10], d[5:7], d[:4], d[-8:])
                self.sort_data[k][i] = data

        for k in range(len(self.keys)):
            for i in range(len(self.values[k])):
                try:
                    index = self.sort_data[k].index(self.values[k][i][-1])
                    list_new_sort_data[k][index] = self.values[k][i]
                except ValueError:
                    pass

        self.values = list_new_sort_data[:]

    def get_list_all_alarm(self):
        self.list_all_alarm.clear()
        for key in range(len(self.keys)):
            for val in range(len(self.values[key])):
                self.list_all_alarm.append(self.values[key][val][-1])

    def add_zero_in_time(self):
        if int(self.all_spin[0][1]) < 10:
            hour = "0" + self.all_spin[0][1]
        else:
            hour = self.all_spin[0][1]

        if int(self.all_spin[1][1]) < 10:
            min = "0" + self.all_spin[1][1]
        else:
            min = self.all_spin[1][1]

        if int(self.all_spin[2][1]) < 10:
            sec = "0" + self.all_spin[2][1]
        else:
            sec = self.all_spin[2][1]

        return hour, min, sec

    def check_error_data(self, event):
        self.today_date = datetime.today()
        data = self.calendar.get()

        if int(data[:2]) == self.today_date.day and int(data[3:5]) == self.today_date.month and int(data[6:]) == self.today_date.year:
            return True
        if (int(data[6:]) < self.today_date.year) or \
           (int(data[6:]) <= self.today_date.year and int(data[3:5]) < self.today_date.month) or \
           (int(data[:2]) < self.today_date.day and int(data[3:5]) <= self.today_date.month and int(data[6:]) <= self.today_date.year):
            messagebox.showerror("Ошибка!", "Выбранной даты уже не существует!\nИзмените свой выбор!")
            self.change_data()

    def change_data(self):
        day = self.today_date.day
        if len(str(self.today_date.day)) == 1:
            day = "0{}".format(self.today_date.day)

        month = self.today_date.month
        if self.today_date.month < 10:
            month = "0" + str(self.today_date.month)

        self.root.focus_force()
        self.calendar["state"] = "normal"
        self.calendar.delete(0, "end")
        self.calendar.insert(0, "{0}/{1}/{2}".format(day, month, self.today_date.year))
        self.calendar["state"] = "readonly"

        for i in range(3):
            self.all_spin[i][0]["state"] = "normal"
            self.all_spin[i][0].delete(0, "end")
            if i == 0:
                self.all_spin[i][0].insert(0, 6)
            else:
                self.all_spin[i][0].insert(0, 0)
            self.all_spin[i][0]["state"] = "readonly"

    def check_same_data(self):
        self.today_date = datetime.today()
        data = self.calendar.get()
        hour, min, sec = self.add_zero_in_time()
        h_now, m_now, s_now = self.today_date.hour, self.today_date.minute, self.today_date.second

        for key in range(len(self.keys)):
            for i in range(len(self.values[key])):
                if data == self.keys[key] and self.values[key][i][-1][11:] == "{0}:{1}:{2}".format(hour, min, sec):
                    messagebox.showwarning("Предупреждение!", "Выбранная дата уже не существует!\nИзмените свой выбор!")
                    self.root.focus_force()
                    return True

        error = self.check_error_data("")

        if error:
            if int(hour) < h_now:
                messagebox.showerror("Ошибка!", "Выбранного времени уже не существует!\nИзмените свой выбор!")
                self.change_data()
                self.root.focus_force()
                return True
            if int(hour) <= h_now and int(min) < m_now:
                messagebox.showerror("Ошибка!", "Выбранного времени уже не существует!\nИзмените свой выбор!")
                self.change_data()
                self.root.focus_force()
                return True
            if int(hour) <= h_now and int(min) <= m_now and int(sec) < s_now:
                messagebox.showerror("Ошибка!", "Выбранного времени уже не существует!\nИзмените свой выбор!")
                self.change_data()
                self.root.focus_force()
                return True

    def clear_list(self, style):
        if style == "sort":
            self.sort_data.clear()
            for l in range(len(self.keys)):
                self.sort_data.append([])
            for i in range(len(self.keys)):
                for l in range(len(self.values[i])):
                    self.sort_data[i] = [[]] * len(self.values[i])

        elif style == "del_alarm":
            new_values = []
            for k in range(len(self.keys)):
                if self.keys[k] != "0":
                    new_values.append([])
            return new_values

        else:
            self.dict_dataFrames.clear()
            self.list_alarmFrames.clear()
            self.listCheck.clear()
            self.sort_data.clear()
            for l in range(len(self.keys)):
                self.list_alarmFrames.append([])
                self.sort_data.append([])
            for i in range(len(self.keys)):
                for l in range(len(self.values[i])):
                    self.list_alarmFrames[i] = [[]] * len(self.values[i])
                    self.sort_data[i] = [[]] * len(self.values[i])

    def click_btn(self, event):
        if self.is_work_alarm:
            self.click_run_btn("")
            self.is_work_alarm = False

        event.widget["state"] = ACTIVE
        event.widget["activebackground"] = "red"

        if event.widget["text"] == "del":
            if messagebox.askyesno("Удаление", "Вы действительно хотите\nудалить выбранные будильники?"):
                self.del_alarm()

        elif event.widget["text"] == "del_all":
            if messagebox.askyesno("Удаление", "Вы действительно хотите\nудалить все будильники?"):
                self.del_all_alarm()

        elif event.widget["text"] == "search":
            self.find_music()

        elif event.widget["text"] == "send":
            if self.check_same_data():
                pass
            else:
                self.write_dict_alarm()
                self.text_music = "Egor Kreed - Cosmoboy.mp3"
                self.add_alarm()
                if len(self.list_all_alarm) == 1:
                    self.start_alarm_2()

        elif event.widget["text"] == "add":
            self.add_alarm_window()

        elif event.widget["text"] == "exit":
            if messagebox.askokcancel("Выход из программы", "Вы действительно хотите выйти?"):
                self.quit()
            else:
                try:
                    self.root.focus_force()
                except:
                    pass

        try:
            event.widget["activebackground"] = "khaki1"
        except:
            pass

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def enter_btn(self, event):
        event.widget["bg"] = "khaki"
        event.widget["activebackground"] = "khaki"

    def leave_btn(self, event):
        event.widget["bg"] = "khaki1"

    def close_window_alarm(self):
        if messagebox.askyesno("Выход из настройки", "Хотите выйти?"):
            self.root.destroy()
        else:
            self.root.focus_force()

    def close_window(self):
        ask = messagebox.askyesnocancel("Выход из программы", "Сохранить все изменения?")
        if ask:
            self.write_file()
            self.quit()
        elif ask == None:
            pass
        else:
            self.quit()


Alarm().mainloop()
