class ReadingFile:
    def __init__(self, filepath):
        self.filepath = filepath

    def readFile(self):
        print('Abrindo o arquivo e retornando  data (string do arquivo)')
        arquivo = open(self.filepath, 'r')

        arquivo_string = arquivo.read()
        arquivo.close()

        data = arquivo_string.split("\n")

        return data

