

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


def calcular_preco_por_kg(
    produto: str,
    quantidade: float,
    unidade: str,
    peso_unitario_g: str,
    preco_pago: float
) -> float | None:
    """
    Calcula o preço por kg do produto para permitir comparação justa entre embalagens diferentes.
    :param produto: nome do produto (string)
    :param quantidade: quantidade original (float)
    :param unidade: unidade de medida, ex: "UN", "KG" (string)
    :param peso_unitario_g: peso unitário em gramas extraído pelo modelo, ou "N/A" (string)
    :param preco_pago: valor total pago (float)
    :return: preço por kg (float) ou None se não for possível calcular
    """
    try:
        if unidade.upper() == "KG":
            # já está em kg, só divide
            return round(preco_pago / quantidade, 2)

        if unidade.upper() == "UN" and peso_unitario_g != "N/A":
            peso_kg = float(peso_unitario_g) / 1000
            quantidade_total_kg = quantidade * peso_kg
            return round(preco_pago / quantidade_total_kg, 2)

        # UN sem peso conhecido — não é possível calcular
        print(f"[AVISO] Não foi possível calcular preço/kg para '{produto}' — sem peso unitário.")
        return None

    except (ValueError, ZeroDivisionError) as e:
        print(f"[ERRO] Falha ao calcular preço/kg para '{produto}': {e}")
        return None


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
