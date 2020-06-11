import tkinter as tk
from report import createReport
from tkinter import filedialog, ttk, StringVar


class reportAnalysis():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('ADnálisis')
        self.window.geometry('200x200')

        self.labelTop = tk.Label(self.window, text='Selecciona un video')
        self.labelTop.place(relx=0.05, rely=0.05)
        self.video = tk.Button(
            self.window, text='Buscar', command=self.uploadAction)
        self.video.place(relx=0.05, rely=0.15)

        self.labelMed = tk.Label(self.window, text='Idioma del video')
        self.labelMed.place(relx=0.05, rely=0.30)
        self.lang = ttk.Combobox(self.window, width=18, values=[
            'Español', 'Inglés', 'Catalán', 'Euskera', 'Gallego'], state="readonly")
        self.lang.current(0)
        self.lang.place(relx=0.05, rely=0.4)

        self.labelBot = tk.Label(self.window, text='Elige un título')
        self.labelBot.place(relx=0.05, rely=0.55)
        self.title = tk.Entry(self.window, width=20)
        self.title.place(relx=0.05, rely=0.65)

        self.report = tk.Button(
            self.window, text='Análisis', command=self.reportAd)
        self.report.place(relx=0.05, rely=0.80)

        self.window.mainloop()

    def uploadAction(self, event=None):
        self.filename = filedialog.askopenfilename(title='Seleccionar archivo')

    def filename(self, event=None):
        return self.filename

    def reportAd(self, event=None):
        self.cReport = createReport(
            self.filename, self.title.get(), self.lang.get())


if __name__ == "__main__":
    ra = reportAnalysis()
