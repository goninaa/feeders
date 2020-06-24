import attr
from pathlib import Path
import platform
import PySimpleGUI as sg

@attr.s
class bat_GUI:
    """Main GUI for Feeder analysis'.
    Recieves from user files/folder.
    Attributes: filelist.
    Methods: get_user_input, get_filelist, run.
    """
    filelist = attr.ib(default=attr.Factory(list))

    def get_user_input(self) -> bool:
        """GUI func to get input from GUI"""
        tag_list = ['1','2','3']
        #currnently only one file
        layout = [
            [sg.Text('Bat name:')],      
                 [sg.Input(key='-BAT NAME-')],
            [sg.Text('Tag')],
            [sg.Listbox(tag_list, size=(15, len(tag_list)), key='-TAG-')],
            # [sg.Listbox(values=tag_list, size=(20, 12), key='-LIST-', enable_events=False)],
            [sg.Text('Select files or a folder to analyze')],
            [sg.Text('Files', size=(8, 1)) ,sg.Input(), sg.FilesBrowse(file_types=(("txt Files", "*.txt"),)) if platform.system() == 'Windows' else sg.FilesBrowse()],
            [sg.Text('OR Folder', size=(8, 1)), sg.Input(), sg.FolderBrowse()],
            [sg.OK(size=(7,1)), sg.Cancel(size=(7,1))]
        ]

        window = sg.Window('Feeder analysis', layout)
        event, self.values = window.Read()
        window.Close()
        return True if event == 'OK' else False
    
    def get_filelist(self) -> None:
        """Extract filelist from GUI"""
        if self.values[0]:
            self.filelist = self.values[0].split(';')
            # print ('file found')
        elif self.values[1]:
            folder = Path(self.values[1])
            # print ('folder found')
            print (self.values[1])
            # self.filelist = [file for file in folder.glob('*.txt')] #check here
            self.filelist = [f for f in folder.resolve().glob('**/*') if f.is_file()] #scans through a folder with all of its subfolders
            # for name in folder.glob('*.txt'):
            #     print (name)
            # self.filelist = [file for file in folder.glob('*.*')] #check here
            print (self.filelist)
        else:
            raise Exception('Folder/files not found')

    def get_bat_name_tag(self):
        self.bat_name = self.values['-BAT NAME-'][0:]
        if self.values['-TAG-']:    # if something is highlighted in the list
            self.tag = {self.values['-TAG-'][0]}
            sg.Popup(f"analyzing {self.values['-BAT NAME-'][0:]}, tag: {self.values['-TAG-'][0]}")
    

    def run(self) -> bool:
        """Main function to run the GUI"""
        if not self.get_user_input():
            return False
        self.get_filelist()
        self.get_bat_name_tag()
        return True


if __name__ == "__main__":
    user_input=mass_GUI()
    assert user_input.run()
    print (f'bat: {user_input.bat_name}')
    print (f'tag: {user_input.tag}')
  