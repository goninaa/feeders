import attr
from pathlib import Path
import platform
import PySimpleGUI as sg

@attr.s
class csv_GUI:
    """Main GUI for Feeders Analysis.
    Recieves from user files/folder....(change here)
    Attributes: filelist.
    Methods: get_user_input, get_filelist, run.
    """
    filelist = attr.ib(default=attr.Factory(list))
    folder = attr.ib(default=attr.Factory(str))

    def get_user_input(self) -> bool:
        """GUI func to get input from GUI"""
        layout = [
            [sg.Text('Select files or a folder to analyze')],
            [sg.Text('Files', size=(8, 1)) ,sg.Input(), sg.FilesBrowse(file_types=(("csv Files", "*.csv"),)) if platform.system() == 'Windows' else sg.FilesBrowse()],
            [sg.Text('OR Folder', size=(8, 1)), sg.Input(), sg.FolderBrowse()],
            [sg.OK(size=(7,1)), sg.Cancel(size=(7,1))]
        ]

        window = sg.Window('Feeders Analysis', layout)
        event, self.values = window.Read()
        window.Close()
        return True if event == 'OK' else False
    
    def get_filelist(self) -> None:
        """Extract filelist from GUI"""
        if self.values[0]:
            self.filelist = self.values[0].split(';')
        elif self.values[1]:
            self.folder = Path(self.values[1])
            self.filelist = [file for file in self.folder.glob('**/*.csv')]
        else:
            raise Exception('Folder/files not found')


    
    def run(self) -> bool:
        """Main function to run the GUI"""
        if not self.get_user_input():
            return False
        self.get_filelist()
        return True


if __name__ == "__main__":
    user_input=csv_GUI()
    assert user_input.run()
    print (user_input.filelist)
    print (user_input.folder)