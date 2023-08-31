from yolo_opencv import make_prediction
import PySimpleGUI as sg
import os.path
import cv2
from PIL import Image
import os


file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
        sg.Button('Guess Object', enable_events = True, key = '-PREDICT-')
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]



image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]


layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]


window = sg.Window("Object Detection", layout)


while True:
    event, values = window.read()
    print(event)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif", ".jpg"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            print(filename)
            pil_image = Image.open(filename)
            pil_image.thumbnail((600, 600))
            filename = f"{values['-FOLDER-']}/output.png"
            pil_image.save(filename)
            window["-TOUT-"].update(values["-FILE LIST-"][0])
            window["-IMAGE-"].update(filename)
            #window["-IMAGE-"].update(filename=filename)
        except:
            pass
    elif event == "-PREDICT-": # predict requested
        try:
            config = "yolov3.cfg"
            weights = "yolov3.weights"
            classes = "yolov3.txt"
            current_dir = os.path.dirname(os.path.realpath(__file__))
            object_list = make_prediction(filename, config, weights, classes, current_dir)

            filename = os.path.join(
                current_dir, "object-detection.png"
            )
            window["-TOUT-"].update("object-detection.png")
            window["-IMAGE-"].update(filename)
        except:
            pass

window.close()