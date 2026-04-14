def calcular_preco_por_kg(
    produto: str,
    quantidade: float,
    unidade: str,
    peso_unitario_g: str,
    preco_pago: float
) -> float | None:
    """
    Docstring for calcular_preco_por_kg

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
            
            return round(preco_pago / quantidade, 2)

        if unidade.upper() == "UN" and peso_unitario_g != "N/A":
            peso_kg = float(peso_unitario_g) / 1000
            quantidade_total_kg = quantidade * peso_kg
            return round(preco_pago / quantidade_total_kg, 2)

        
        print(f"[AVISO] Não foi possível calcular preço/kg para '{produto}' — sem peso unitário.")
        return None

    except (ValueError, ZeroDivisionError) as e:
        print(f"[ERRO] Falha ao calcular preço/kg para '{produto}': {e}")
        return None