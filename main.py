import sys
from ReadingFile import *
from CreateReport import *


def main():

    file_import = sys.argv[1]
    file_export = sys.argv[2]

    reading_file = ReadingFile(file_import)

    data = reading_file.readFile()
    list_registro_detalhe = []
    header_lote = ''
    header_arquivo = ''
    print('Obtendo as linhas do arquivo lido e separando-as de acordo com o tipo de cada uma.')
    for line in data:
        if len(line) > 1:
            if line[7] == '0':
                header_arquivo = line
            elif line[7] == '1':
                header_lote = line
            elif line[7] == '3':
                list_registro_detalhe.append(line)
            elif line[7] == '5':
                trailer_lote = line
            elif line[7] == '9':
                trailer_arquivo = line
            else:
                print('linha não mapeada')
        else:
            print('linha não possui qtd de caracteres suficientes')

    create_report = CreateReport(list_registro_detalhe, header_lote, header_arquivo, file_export)
    create_report.generateByExtension()


if __name__ == "__main__":
    main()
