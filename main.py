import sys
from datetime import datetime
import babel.numbers



from utils.enum import tableG029
from utils.mask_cnpj import mask_cnpj

file_import = sys.argv[1]
file_export = sys.argv[2]

arquivo = open(file_import, 'r')
arquivo_string = arquivo.read()
arquivo.close()

data = arquivo_string.split("\n")

list_registro_detalhe = []
for line in data:
    if len(line) > 1:
        if line[7] == '0':
            header_arquivo = line
            #print('header_arquivo')
        elif line[7] == '1':
            header_lote = line
            #print('header_lote')
        elif line[7] == '3':
            list_registro_detalhe.append(line)
            #print('registro_detalhe')
        elif line[7] == '5':
            trailer_lote = line
            #print('trailer_lote')
        elif line[7] == '9':
            trailer_arquivo = line
            #print('trailer_arquivo')
        else:
            print('linha não mapeada')
    else:
        print('linha não possui qtd de caracteres suficientes')



def getRegistros():
    html_string = ''
    for registros in list_registro_detalhe:
        price = registros[119:134]
        print(price)
        html_string += (f'''<tr>
        <td>{registros[43:73]}</td>
        <td>{datetime(int(registros[97:101]), int(registros[95:97]), int(registros[93:95])).strftime('%d/%m/%Y')}</td>
        <td>{babel.numbers.format_currency(price[:13] + '.' + price[13:], 'BRL', locale='pt_BR')}</td>
        <td>{registros[73:93]}</td>
        <td>{tableG029[header_lote[11:13]]}</td>
        </tr>''')
    else:
        return html_string


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
                <td>{header_arquivo[72:102]}</td>
                <td>{mask_cnpj(header_arquivo[18:32])}</td>
                <td>{header_arquivo[102:132]}</td>
				<td>{header_lote[142:172]}</td>
				<td>{header_lote[172:177]}</td>
				<td>{header_lote[192:212]}</td>
				<td>{header_lote[212:217]}-{header_lote[217:220]}</td>
				<td>{header_lote[220:222]}</td>
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
           {getRegistros()}
        </table>
    </body>
</html>
''')

arq_html = open(file_export, 'w')

arq_html.write(codigo_html)

arq_html.close()
