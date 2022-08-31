import PySimpleGUI as psg

def layout() -> list:

    #Tworzenie layoutu GUI

    #Kolumna z plikami
    file_column = [
        [
            psg.Text("Pliki"),
            psg.In(size=(20, 1), enable_events=True, key="-FOLDER-"),
            psg.FolderBrowse(),
            psg.Button("Quit",  key="-QUIT-", enable_events=True),

        ],
        [
            psg.Text("Wybierz folder", key="-FIRSTRUN-", visible=True),
            psg.Listbox(
                values=[],
                enable_events=True,
                size=(40, 20),
                key="-FILE LIST-",
                visible=False
            )

        ]

    ]
    #Kolumna z wykresem
    plot_viewer = [
        [
            psg.Canvas(key="-PLOT-")
        ],
        [
            psg.Text("Średnia oś elektryczna serca: "),
            psg.Text(key="-MEANAXIS-", text_color='Red'),
            psg.Text(key="-GRAM-")
        ]
    ]


    #Finalny layout okienka
    gui_layout = [
        [
            psg.Column(file_column),
            psg.VSeparator(pad=(0, 0)),
            psg.Column(plot_viewer)
        ]
    ]



    return gui_layout