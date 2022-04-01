import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
import time
import random
import math

window = tk.Tk()
window.title("Hopfield")

select_train_button = object
select_test_button = object
train_button = object
test_button = object
previous_button = object
next_button = object
reset_button = object
train_file_label = object
test_file_label = object
total_label = object
current_label = object
canvas = object
canvas_test = object
canvas_predict = object
hopfield = object

train_filename = ""
test_filename = ""
train_dataset = list()
test_dataset = list()
predict_dataset = list()
total_num = 0
current_num = 0
canvas_width = 300
canvas_height = 300
dim_x = 0
dim_y = 0
iteration = 1000
trained = False
draw_test = False
draw_predict = False

class Hopfield():
    def __init__(self, data_size):
        self.data_size = data_size
        self.w = [[0 for i in range(self.data_size)] for j in range(self.data_size)]
        self.theta = list()

    def predict(self, data):
        predict_data = data.copy()
        count = 0
        for it in range(iteration):
            tmp = predict_data.copy()
            for i in range(len(self.w)):
                u = 0
                for j in range(len(predict_data)):
                    u += self.w[i][j] * predict_data[j]
                if u > self.theta[i]:
                    predict_data[i] = 1
                elif u < self.theta[i]:
                    predict_data[i] = -1
            if predict_data == tmp:
                count += 1
            else:
                count = 0
            if count > 10:
                break
        return predict_data

    def train(self, dataset):
        for data in dataset:
            for i in range(len(data)):
                for j in range(len(data)):
                    self.w[j][i] += data[i] * data[j]
        for i in range(len(self.w)):
            for j in range(len(self.w[i])):
                if i == j:
                    self.w[i][j] /= self.data_size
                    self.w[i][j] -= (len(dataset) / len(dataset[0]))
                else:
                    self.w[i][j] /= self.data_size
        for i in range(len(self.w)):
            self.theta.append(sum(self.w[i]))

def drawData(canvas, dataset):
    global current_num
    canvas.delete("all")
    for j in range(len(dataset[0])):
        x0 = (canvas_width // dim_x) * (j % dim_x)
        y0 = (canvas_height // dim_y) * (j // dim_x)
        x1 = (canvas_width // dim_x) * ((j % dim_x) + 1)
        y1 = (canvas_height // dim_y) * ((j // dim_x) + 1)

        if dataset[current_num][j] == 1:
            canvas.create_rectangle(x0, y0, x1, y1, fill="black")
        else:
            canvas.create_rectangle(x0, y0, x1, y1, fill="white")

def readTrainFile(file, canvas):
    global train_dataset, total_num, current_num, dim_x, dim_y
    f = open(file, "r")
    train_dataset.append(list())
    data_num = 0
    dim_y = 0
    for i in f.readlines():
        dim_x = 0
        if i != "\n":
            dim_y += 1
            for blank in i:
                dim_x += 1
                if blank == " ":
                    train_dataset[data_num].append(-1)
                elif blank == "1":
                    train_dataset[data_num].append(1)
        else:
            train_dataset.append(list())
            data_num += 1
            dim_y = 0
    total_num = data_num + 1
    drawData(canvas, train_dataset)
    total_label.config(text="Total data = {}".format(total_num))
    current_label.config(text="Current data = {}".format(current_num + 1))
    f.close()

def readTestFile(file, canvas):
    global test_dataset, current_num, draw_test
    f = open(file, "r")
    test_dataset.append(list())
    data_num = 0
    for i in f.readlines():
        if i != "\n":
            for blank in i:
                if blank == " ":
                    test_dataset[data_num].append(-1)
                elif blank == "1":
                    test_dataset[data_num].append(1)
        else:
            test_dataset.append(list())
            data_num += 1
    drawData(canvas, test_dataset)
    draw_test = True
    f.close()

def selectTrainDataset():
    global train_filename
    file = filedialog.askopenfilename(title="Select Train Data", filetypes=(("text files (*.txt)", "*.txt"), ("all files", "*.*")))
    if file:
        readTrainFile(file, canvas)
        train_filename = file.split("/")[-1]
        train_file_label.config(text="{}".format(train_filename))
        select_train_button.config(state="disabled")
        select_test_button.config(state="normal")
        train_button.config(state="normal")
        reset_button.config(state="normal")
        previous()
    else:
        tk.messagebox.showinfo(title="Notice", message="No file selected")

def selectTestDataset():
    global test_filename, test_dataset
    file = filedialog.askopenfilename(title="Select Test Data", filetypes=(("text files (*.txt)", "*.txt"), ("all files", "*.*")))
    if file:
        readTestFile(file, canvas_test)
        test_filename = file.split("/")[-1]
        test_file_label.config(text="{}".format(test_filename))
        select_test_button.config(state="disabled")
    else:
        tk.messagebox.showinfo(title="Notice", message="No file selected")
    if draw_test and trained:
        test_button.config(state="normal")

def training():
    global hopfield, train_dataset, trained
    hopfield = Hopfield(len(train_dataset[0]))
    hopfield.train(train_dataset)
    tk.messagebox.showinfo(title="Notice", message="Train Success!")
    trained = True
    if draw_test and trained:
        test_button.config(state="normal")

def testing():
    global test_dataset, predict_dataset, draw_predict
    draw_predict = True
    predict_dataset = test_dataset.copy();
    for i in range(len(predict_dataset)):
        predict_dataset[i] = hopfield.predict(predict_dataset[i])
    drawData(canvas_predict, predict_dataset)

def drawAllData():
    global draw_test, draw_predict
    drawData(canvas, train_dataset)
    if draw_test:
        drawData(canvas_test, test_dataset)
    if draw_predict:
        drawData(canvas_predict, predict_dataset)

def previous():
    global current_num
    if current_num - 1 >= 0:
        current_num -= 1
        drawAllData()
        current_label.config(text="Current data = {}".format(current_num + 1))

    previous_button.config(state="normal")
    next_button.config(state="normal")
    if current_num - 1 < 0:
        previous_button.config(state="disabled")

def next():
    global total_num, current_num
    if current_num + 1 < total_num:
        current_num += 1
        drawAllData()
        current_label.config(text="Current data = {}".format(current_num + 1))

    previous_button.config(state="normal")
    next_button.config(state="normal")
    if current_num + 1 >= total_num:
        next_button.config(state="disabled")

def resetState():
    global train_dataset, test_dataset, predict_dataset, total_num, current_num, trained, draw_test, draw_predict
    train_dataset = list()
    test_dataset = list()
    predict_dataset = list()
    total_num = 0
    current_num = 0
    trained = False
    draw_test = False
    draw_predict = False
    select_train_button.config(state="normal")
    select_test_button.config(state="disabled")
    train_button.config(state="disabled")
    test_button.config(state="disabled")
    previous_button.config(state="disabled")
    next_button.config(state="disabled")
    reset_button.config(state="disabled")
    train_file_label.config(text="{}".format(""))
    test_file_label.config(text="{}".format(""))
    total_label.config(text="Total data = {}".format(total_num))
    current_label.config(text="Current data = {}".format(current_num))
    canvas.delete("all")
    canvas_test.delete("all")
    canvas_predict.delete("all")

def GUI():
    global select_train_button, select_test_button, train_button, test_button, previous_button, next_button, reset_button
    global train_file_label, test_file_label, total_label, current_label
    global canvas, canvas_test, canvas_predict

    select_train_button = tk.Button(window, text="select train data", command=selectTrainDataset, width=15)
    select_train_button.grid(row=0, column=0)
    select_test_button = tk.Button(window, text="select test data", command=selectTestDataset, state="disabled", width=15)
    select_test_button.grid(row=1, column=0)
    train_button = tk.Button(window, text="start training", command=training, state="disabled", width=15)
    train_button.grid(row=2, column=0)
    test_button = tk.Button(window, text="start testing", command=testing, state="disabled", width=15)
    test_button.grid(row=3, column=0)
    previous_button = tk.Button(window, text="previous", command=previous, state="disabled", width=15)
    previous_button.grid(row=4, column=0)
    next_button = tk.Button(window, text="next", command=next, state="disabled", width=15)
    next_button.grid(row=5, column=0)
    reset_button = tk.Button(window, text="reset all", command=resetState, state="disabled", width=15)
    reset_button.grid(row=6, column=0)

    train_file_label = tk.Label(window, text="{}".format(train_filename), width=20)
    train_file_label.grid(row=0, column=1)
    test_file_label = tk.Label(window, text="{}".format(test_filename), width=20)
    test_file_label.grid(row=1, column=1)
    total_label = tk.Label(window, text="Total data = {}".format(total_num), width=15)
    total_label.grid(row=4, column=1)
    current_label = tk.Label(window, text="Current data = {}".format(current_num), width=15)
    current_label.grid(row=5, column=1)

    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='white')
    canvas.grid(row=0, column=2, rowspan=7, padx=5)
    canvas_test = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='white')
    canvas_test.grid(row=0, column=3, rowspan=7, padx=5)
    canvas_predict = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='white')
    canvas_predict.grid(row=0, column=4, rowspan=7, padx=5)

    tk.mainloop()

if __name__ == "__main__":
    GUI()