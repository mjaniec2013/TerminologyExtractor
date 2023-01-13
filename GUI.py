from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
from TermEntry import *

class EntryGUI:
    '''GUI displaying list of terminology candidates and their related content, 
    i.e. definitions and context sentences.

    Attributes
    ----------
    root : Tk
        Main window of GUI, created using Tk() class from Tkinter. Serves as parent
        for all other widgets in GUI.

    Methods
    -------
    open_file(self):
        Opens .PDF file and prints out name of selected file
    candidates_list(self):
        Extracts terminology candidates from .PDF file and lists them out
    show_content(self, event):
        Prints out in the window terminology candidate, definition(s) and 
        related context sentences
    show_all_definitions(self):
        Opens a new window listing out all definitions for a terminology
        candidate
    show_all_context(self):
        Opens a new window listing out all context sentences for a 
        terminology candidate
    display_candidate(self):
        Binds functions for displaying content to 'Browse' button
    reset_window(self):
        Resets the window before showing output for a new .PDF file
    run(self):
        Runs GUI
    '''

    def __init__(self, root):
        '''Construct main window and widgets for GUI.

        Returns
        -------
        None
        '''
        # Main window
        self.root = root
        self.root.title('Terminology Extractor')
        self.root.state('zoomed')

        # Main canvas and widgets
        self.canvas = Canvas(self.root, highlightthickness=0, background='ghost white')
        self.canvas.place(relwidth=1, relheight=1)
        self.canvas.create_rectangle(0, 0, 2000, 55, fill='seashell2', outline='bisque4')
        self.canvas.create_rectangle(340, 121, 2000, 55, fill='NavajoWhite2', outline='sandy brown')
        self.canvas.create_rectangle(340, 122, 2000, 350, fill='ivory2', outline='pale goldenrod')
        self.canvas.create_rectangle(340, 351, 2000, 2000, fill='white smoke', outline='old lace')
        self.canvas.create_rectangle(0, 55, 350, 1000, fill='ghost white', outline='burlywood4')
        self.canvas.create_text(400, 150, text='Possible definition(s)', anchor='nw', fill='black', font=('Helvetica', 15, 'bold'))
        self.canvas.create_text(400, 370, text='Context sentence(s)', anchor='nw', fill='black', font=('Helvetica', 15, 'bold'))
        show_all_definitions = Button(self.canvas, text='Show all', highlightbackground='ivory2', font=('Helvetica', 14),
                             command=self.show_all_definitions)
        self.canvas.create_window(1200, 170, anchor='se', window=show_all_definitions)
        show_all_context = Button(self.canvas, text='Show all', highlightbackground='white smoke', font=('Helvetica', 14),
                             command=self.show_all_context)
        self.canvas.create_window(1200, 393, anchor='se', window=show_all_context)

        # 'Browse' button
        self.canvas.create_text(20, 20, text='Choose your file:', anchor='nw', fill='black', font=('Helvetica', 14))
        file_button = Button(self.canvas, text='Browse', highlightbackground='seashell2', font=('Helvetica', 14),
                             command=self.display_candidates)
        self.canvas.create_window(135, 12, anchor='nw', window=file_button)

        # Creates listbox to display terminology candidates
        self.listbox = Listbox(self.canvas, height=60, width=45, bg='ghost white', bd=1, fg='black', font=('Helvetica', 14))


    def open_file(self):
        '''Opens .PDF file, manages errors in case no file or a file with an extension different 
        from .PDF is selected, prints out name of selected file.

        Returns
        -------
        None
        '''
        # Gets file path and stores file name
        self.file_path = filedialog.askopenfilename()
        file_name = os.path.basename(self.file_path)

        # Checks whether file path is empty or extension is different from .pdf
        if self.file_path == '' or '.pdf' not in file_name:
            messagebox.showwarning(message='Please choose a .pdf file')
        else:
            # Prints out and updates file name
            self.canvas.delete('text')
            self.canvas.create_text(230, 20, text='Selected file: ' + file_name, tags='text', anchor='nw', fill='black',
                                    font=('Helvetica', 14))


    def candidates_list(self):
        '''Extracts terminology candidates from .PDF file and prints them out
        in a listbox.

        Returns
        -------
        None
        '''
        # Extracts term candidates from .PDF file
        self.entries = create_entry(self.file_path)
        candidates = []
        for entry in self.entries:
            candidates.append(entry.get_term_candidate())
        
        # Populates listbox
        for c in range(0, len(candidates)):
            self.listbox.insert(END, candidates[c])

        # Shows related content when clicking on a terminology candidate
        self.listbox.bind('<<ListboxSelect>>', self.show_content)

        # Sets listbox on canvas
        self.canvas.create_window(0, 55, anchor='nw', window=self.listbox)


    def show_content(self, event):
        '''Prints out terminology candidate, definition(s) and context sentences.

        Parameters
        ----------
        event : Event
            Event triggering function execution, in this case click of mouse's
            left button.

        Returns
        -------
        None
        '''
        # Prints out terminology candidate
        self.canvas.delete('text1')
        if self.listbox.curselection():
            term_cand = self.listbox.get(ANCHOR)
            self.canvas.create_text(400, 80, text=term_cand.upper(), tags='text1', 
                                    anchor='nw', fill='black', font=('Helvetica', 17, 'bold'))

        # Prints out 3 definitions one after the other
        selected_cand = self.listbox.get(ANCHOR)
        self.canvas.delete('text2')
        self.canvas.delete('text3')
        for entry in self.entries:
            if entry.get_term_candidate() == selected_cand:
                definition = entry.get_definition()
                y_coord1 = 180
                if len(definition) > 3 or len(definition[0]) > 300:
                    self.canvas.create_text(1150, 300, width=690, text='(...)', tags='text2', 
                                                anchor='nw', fill='black', font=('Helvetica', 17, 'bold'))
                for i, d in enumerate(definition):
                    if i < 3 and len(d) < 300:
                        self.canvas.create_text(400, y_coord1, width=690, text='{}. "{}"'.format(i+1,d.capitalize()), tags='text3', 
                                                anchor='nw', fill='black', font=('Helvetica', 15))
                        if i >= 1:
                            self.canvas.create_line(400, y_coord1, 1200, y_coord1, width=1, dash=(6,3), fill='ivory3')
                        y_coord1 += 50

        # Prints out 3 context sentences one after the other
        selected_cand = self.listbox.get(ANCHOR)
        self.canvas.delete('text4')
        self.canvas.delete('text5')
        for entry in self.entries:
            if entry.get_term_candidate() == selected_cand:
                context = entry.get_context()
                y_coord2 = 415
                if len(context) > 5 or len(context[0]) > 300:
                    self.canvas.create_text(1150, 680, width=690, text='(...)', tags='text2', 
                                                anchor='nw', fill='black', font=('Helvetica', 17, 'bold'))
                for i, c in enumerate(context):
                    if i < 5 and len(c) < 300:
                        self.canvas.create_text(400, y_coord2, width=690, text='• "' + c + '"', tags='text5', 
                                                anchor='nw', fill='black', font=('Helvetica', 14, 'italic'))
                        if i >= 1:
                            self.canvas.create_line(400, y_coord2, 1200, y_coord2, width=1, dash=(6,3), fill='ivory3')
                        y_coord2 += 60


    def show_all_definitions(self):
        '''Opens a new window listing out every definition found 
        for a terminology candidate.

        Returns
        -------
        None
        '''
        # Sets new window, label and text widget
        new_window = Toplevel(root)
        new_window.title('Show all possible definitions')
        new_window.geometry('500x600')
        label = Label(new_window, text="Possible definitions:", bg='white', fg='black', font=('Helvetica', 15, 'bold'))
        label.grid(row=0, column=0, sticky='nswe')
        textbox = Text(new_window, bg='white', fg='black', wrap=WORD, font=('Helvetica', 14))
        textbox.grid(row=1, column=0, sticky='nsew')
        new_window.rowconfigure(0, weight=1)
        new_window.rowconfigure(1, weight=3)
        new_window.columnconfigure(0, weight=1)

        # Lists out definitions
        selected_cand = self.listbox.get(ANCHOR)
        for entry in self.entries:
            if entry.get_term_candidate() == selected_cand:
                definition = entry.get_definition()
                for i, d in enumerate(definition):
                       textbox.insert(END, '• "' + d.capitalize() + '"\n\n')


    def show_all_context(self):
        '''Opens a new window listing out every context sentence found 
        for a terminology candidate.

        Returns
        -------
        None
        '''
        # Sets new window and text widget
        new_window = Toplevel(root)
        new_window.title('Show all context sentences')
        new_window.geometry('500x600')
        label = Label(new_window, text="Context sentences:", bg='white', fg='black', font=('Helvetica', 15, 'bold'))
        label.grid(row=0, column=0, sticky='nswe')
        textbox = Text(new_window, bg='white', fg='black',  wrap=WORD, font=('Helvetica', 14))
        textbox.tag_config('italic', font=('Helvetica', 14, 'italic'))
        textbox.grid(row=1, column=0, sticky='nsew')
        new_window.rowconfigure(0, weight=1)
        new_window.rowconfigure(1, weight=3)
        new_window.columnconfigure(0, weight=1)

        # Lists out context sentences 
        selected_cand = self.listbox.get(ANCHOR)
        for entry in self.entries:
            if entry.get_term_candidate() == selected_cand:
                context = entry.get_context()
                for i, c in enumerate(context):
                       textbox.insert(END, '• "' + c + '"\n\n', 'italic')


    def display_candidates(self):
        '''Binds functions for displaying content to 'Browse' button.

        Returns
        -------
        None
        '''
        self.reset_window()
        self.open_file()
        self.candidates_list()

            
    def reset_window(self):
        '''Resets listbox content before showing output for a new .PDF file.

        Returns
        -------
        None
        '''
        self.listbox.delete(0, END)


    def run(self):
        '''Runs GUI.

        Returns
        -------
        None
        '''
        self.root.mainloop()


root = Tk()
gui = EntryGUI(root)
gui.run()
