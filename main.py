import matplotlib.figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os.path
import config
from heart_algo import algorytm

# Konfiguracja DPI okienka zeby wykres nie byl nieczytelny
config.make_dpi_aware()



# Rysowanie wykresu na GUI
def draw_plot(canvas, plot):
    figure_canvas = FigureCanvasTkAgg(plot, canvas)
    figure_canvas.draw()
    figure_canvas.get_tk_widget().pack(side='top', fill='both')
    return figure_canvas

# Ustalanie osi elektrycznej serca
def define_meanaxis(meanaxis):
    axis = str(round(meanaxis, 5)) + chr(176)

    gram = ''

    if 0 < meanaxis <= 90:
       gram += 'Normogram'
    elif 90 < meanaxis <= 180:
        gram += 'Prawogram'
    elif -180 < meanaxis <= -90:
        gram += 'Oś niezdefiniowana'
    elif -90 < meanaxis <= 0:
        gram += 'Lewogram'

    return axis, gram

# Plotowanie wykresu w okienku na podstawie algorytmu heart_algo.py

def plot_heart_algo(filename: str, gui_window):
    data1, data2, axis = algorytm(filename)
    fig = matplotlib.figure.Figure(figsize=(5, 4))
    #fig, (ax1, ax2) = plt.subplots(2, constrained_layout=True)
    fig.add_subplot(111).plot(data1)
    fig.add_subplot(111).plot(data2)
    plt.plot()
    plt.grid(True)
    fig = plt.gcf()
    axis, gram = define_meanaxis(axis)
    gui_window['-MEANAXIS-'].update(axis)
    gui_window['-GRAM-'].update(gram)
    return fig


# Metoda do usuwania figury jeśli takowa sie znajduje w okienku

def delete_figure_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    plt.close('all')


def main() -> None:
    import PySimpleGUI as psg
    from gui_layout import layout

    # Tworzenie interfejsu
    gui_window = psg.Window("Aplikacja do liczenia osi elektrycznej serca", layout(),auto_size_text=True, default_element_size=(15,1), border_depth=5, auto_size_buttons=True,
                            font="Monospace 18", resizable=True, finalize=True)


    # Ustalanie figury jako nieistniejącej na początku programu
    fig_agg = None

    #Pętla wykonywania skryptów w GUI
    while True:
        #czytanie aktywnosci w okienku (przyciski, naciśniecia)
        event, values = gui_window.read()

        #jeśli klika się "QUIT" lub zamyka okienko to pętla jest przerywana i program się zamyka
        if event == "-QUIT-" or event == psg.WIN_CLOSED:
            break

        #oskryptowanie wybierania folderu
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []

            #list comprehension dla wybierania plików tylko z końcówką ".hea", który jest medycznym plikiem
            fnames = [
                f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".hea"))
            ]

            #Aktualizowanie okna GUI po wybraniu danego pliku
            gui_window['-FIRSTRUN-'].Update(visible=False)
            gui_window["-FILE LIST-"].Update(visible=True)
            gui_window["-FILE LIST-"].expand(True, True)
            gui_window["-FILE LIST-"].Update(fnames)


        #Oskryptowanie wybrania pliku i wykonania na danym pliku akcji liczenia oraz plotowania wykresu
        elif event == "-FILE LIST-":

            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                if fig_agg:
                    delete_figure_agg(fig_agg)

                filename = filename[:len(filename) - 4]
                fig = plot_heart_algo(filename, gui_window)
                fig_agg = draw_plot(gui_window['-PLOT-'].TKCanvas, fig)
                fig_agg.draw()


            except:
                pass



    gui_window.close()


if __name__ == '__main__':
    main()