

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
            "nome":     linha["Nome do Produto"],
            "total":    para_float(linha["Valor Total"]),
            "qtd":      para_float(linha["Quantidade"]),
            "unidade":  linha["Unidade de Medida"],
            "unitario": para_float(linha["Valor Unitário"]),
            "data":     linha["Data da Compra"],
            "local":    linha["Local da Compra"],
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
    from teste import texto_teste1

    texto_csv = texto_teste1
    # --- uso ---
    itens = parsear_csv(texto_csv)

    # processar um a um
    for item in itens:
        print(item)
        print("---")

    # converter de volta para string CSV
    print(para_csv(itens))
