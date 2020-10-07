import pandas as pd

class InfoFile():
    def __init__(self, path, engine):
        self.file = pd.read_excel(path, engine=engine).set_index('Name')
    def get_info(self):
        return self.file.loc['Kate Sheppard','Text']

if __name__ == "__main__":
    InfoFile('media/texts.ods', 'odf').get_info()
