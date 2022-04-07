from datetime import datetime
import babel.numbers
import csv
from utils.enum import tableG029
from utils.mask_cnpj import mask_cnpj

class CreateReport:
    def __init__(self, list_registro_detalhe, header_lote, header_arquivo, file_export):
        self.list_details_registry = list_registro_detalhe
        self.header_lote = header_lote
        self.header_arquivo = header_arquivo
        self.file_export = file_export

    def generateByExtension(self):
        if self.file_export[-4::] == 'html' :
            print(f'Gerando relatório: {self.file_export}')
            self.generate_html_report()
        elif self.file_export[-3::] == 'csv' :
            print(f'Gerando relatório: {self.file_export}')
            self.generate_csv_report()
        elif self.file_export[-3::] == 'txt' :
            print(f'Gerando relatório: {self.file_export}')
            self.generate_txt_report()

    def generate_txt_report(self):
        f   = open(self.file_export,"w+")

        f.write('------------------------------------------------------------------------------------------------------------------------------------------------------------ \n')
        f.write('Nome da Empresa | Numero de Inscricao da Empresa | Nome do Banco | Nome da Rua        | Numero do Local | Nome da Cidade       | CEP       | Sigla do Estado \n')
        f.write('------------------------------------------------------------------------------------------------------------------------------------------------------------ \n')
        f.write(f'{self.header_arquivo[72:102].rstrip()}   | {mask_cnpj(self.header_arquivo[18:32]).rstrip()}             | {self.header_arquivo[102:132].rstrip()}          | {self.header_lote[142:172].rstrip()} | {self.header_lote[172:177].rstrip()}             | {self.header_lote[192:212].rstrip()} | {self.header_lote[212:217].rstrip()}-{self.header_lote[217:220].rstrip()} | {self.header_lote[220:222].rstrip()} \n')
        f.write('------------------------------------------------------------------------------------------------------------------------------------------------------------ \n')
        f.write('-------------------------------------------------------------------------------------------------------------------------------------- \n')
        f.write('Nome do Favorecido   | Data de Pagamento | Valor do Pagamento | Numero do Documento Atribuido pela Empresa | Forma de Lancamento \n')
        f.write('-------------------------------------------------------------------------------------------------------------------------------------- \n')

        for registry in self.list_details_registry:
            price = registry[119:134]
            price_spaces = babel.numbers.format_currency(price[:13] + '.' + price[13:], 'BRL', locale='pt_BR') + (' ' * (19-len(babel.numbers.format_currency(price[:13] + '.' + price[13:], 'BRL', locale='pt_BR'))))
            csv_registry = f'''{registry[43:73].rstrip()} | {datetime(int(registry[97:101]), int(registry[95:97]), int(registry[93:95])).strftime('%d/%m/%Y').rstrip()}        | {price_spaces}| {registry[73:93].rstrip()}                                 | {tableG029[self.header_lote[11:13]]} \n'''
            f.write(csv_registry)

        f.write('-------------------------------------------------------------------------------------------------------------------------------------- \n')
        f.close()


    def generate_csv_report(self):
        #enconding utf-8 não estava reconhecendo caracteres como $ e acentos
        with open(self.file_export, 'w', encoding='latin1', newline='') as arq_csv:
            writer = csv.writer(arq_csv)

            header_1 = ['Nome da Empresa', 'Numero de Inscricao da Empresa', 'Nome do Banco', 'Nome da Rua', 'Numero do Local', 'Nome da Cidade', 'CEP', 'Sigla do Estado']
            writer.writerow(header_1)

            data_1 = [self.header_arquivo[72:102].rstrip(),mask_cnpj(self.header_arquivo[18:32]).rstrip(),self.header_arquivo[102:132].rstrip(),self.header_lote[142:172].rstrip(),self.header_lote[172:177].rstrip(),self.header_lote[192:212].rstrip(),self.header_lote[212:217] +'-'+self.header_lote[217:220], self.header_lote[220:222].rstrip()]
            writer.writerow(data_1)

            header_2 = ['Nome do Favorecido', 'Data de Pagamento', 'Valor do Pagamento','Numero do Documento Atribuido pela Empresa','Forma de Lancamento']
            writer.writerow(header_2)

            for registry in self.list_details_registry:
                price = registry[119:134]
                csv_registry = [registry[43:73].rstrip(),datetime(int(registry[97:101]), int(registry[95:97]), int(registry[93:95])).strftime('%d/%m/%Y').rstrip(), babel.numbers.format_currency(price[:13] + '.' + price[13:], 'BRL', locale='pt_BR') ,registry[73:93].rstrip(),tableG029[self.header_lote[11:13]]]
                writer.writerow(csv_registry)

            arq_csv.close()



    def generate_html_report(self):
            codigo_html = (f'''
                <html>
                    <body>
                        <table border="1">
                            <tr>
                                <th>Nome da Empresa</th>
                                <th>Numero de Inscricao da Empresa</th>
                                <th>Nome do Banco</th>
                                <th>Nome da Rua</th>
                                <th>Numero do Local</th>
                                <th>Nome da Cidade</th>
                                <th>CEP</th>
                                <th>Sigla do Estado</th>
                            </tr>
                            <tr>
                                <td>{self.header_arquivo[72:102]}</td>
                                <td>{mask_cnpj(self.header_arquivo[18:32])}</td>
                                <td>{self.header_arquivo[102:132]}</td>
                                <td>{self.header_lote[142:172]}</td>
                                <td>{self.header_lote[172:177]}</td>
                                <td>{self.header_lote[192:212]}</td>
                                <td>{self.header_lote[212:217]}-{self.header_lote[217:220]}</td>
                                <td>{self.header_lote[220:222]}</td>
                            </tr>
                        </table>
                        <br />
                        <table border="1">
                            <tr>
                                <th>Nome do Favorecido</th>
                                <th>Data de Pagamento</th>
                                <th>Valor do Pagamento</th>
                                <th>Numero do Documento Atribuido pela Empresa</th>
                                <th>Forma de Lancamento</th>
                            </tr>
                           {self.get_registry()}
                        </table>
                    </body>
                </html>
                ''')


            arq_html = open(self.file_export, 'w')

            arq_html.write(codigo_html)

            arq_html.close()


    def get_registry(self):
            html_string = ''
            for registry in self.list_details_registry:
                price = registry[119:134]
                html_string += (f'''<tr>
                        <td>{registry[43:73]}</td>
                        <td>{datetime(int(registry[97:101]), int(registry[95:97]), int(registry[93:95])).strftime('%d/%m/%Y')}</td>
                        <td>{babel.numbers.format_currency(price[:13] + '.' + price[13:], 'BRL', locale='pt_BR')}</td>
                        <td>{registry[73:93]}</td>
                        <td>{tableG029[self.header_lote[11:13]]}</td>
                        </tr>''')
            else:
                return html_string
