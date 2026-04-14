

import csv
import io



def para_float(valor):
    if valor == "N/A":
        return None
    return float(valor.replace(",", "."))

def parsear_csv(texto_csv):
    reader = csv.DictReader(io.StringIO(texto_csv))
    linhas = []
    for linha in reader:
        linhas.append({
            "nome":     linha["Nome_Produto"],
            "total":    para_float(linha["Valor_Total"]),
            "qtd":      para_float(linha["Quantidade"]),
            "unidade":  linha["Unidade_Medida"],
            "unitario": para_float(linha["Valor_Unitario"]),
            "data":     linha["Data_Compra"],
            "local":    linha["Local_Compra"],
        })
    return linhas

def para_csv(linhas):
    output = io.StringIO()
    campos = ["nome", "total", "qtd", "unidade", "unitario", "data", "local"]
    writer = csv.DictWriter(output, fieldnames=campos)
    writer.writeheader()
    writer.writerows(linhas)
    return output.getvalue()





if __name__ == "__main__":
    from tests.teste import texto_teste1

    texto_csv = texto_teste1
    # --- uso ---
    itens = parsear_csv(texto_csv)

    # processar um a um
    for item in itens:
        print(item)
        print("---")

    # converter de volta para string CSV
    print(para_csv(itens))
