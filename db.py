import sqlite3
from datetime import date


DB_PATH = "mercado.db"


def criar_banco(db_path: str = DB_PATH) -> None:
    """
    Cria o banco de dados e as tabelas necessárias se não existirem.
    :param db_path: caminho do arquivo SQLite (string)
    """
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS precos (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                produto           TEXT    NOT NULL,
                unidade_medida    TEXT    NOT NULL,
                preco_por_unidade REAL,
                preco_pago        REAL    NOT NULL,
                quantidade        REAL    NOT NULL,
                data_compra       TEXT    NOT NULL,
                local_compra      TEXT    NOT NULL,
                data_insercao     TEXT    DEFAULT (date('now'))
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_produto_data
            ON precos (produto, data_compra)
        """)
        conn.commit()
    print(f"[DB] Banco inicializado em '{db_path}'.")


def inserir_preco(
    produto: str,
    unidade_medida: str,
    preco_por_unidade: float | None,
    preco_pago: float,
    quantidade: float,
    data_compra: str,
    local_compra: str,
    db_path: str = DB_PATH
) -> None:
    """
    Insere um registro de preço no banco de dados.
    :param produto: nome genérico do produto (string)
    :param unidade_medida: KG, L ou UN (string)
    :param preco_por_unidade: R$/kg, R$/L ou R$/UN — None se não calculável (float | None)
    :param preco_pago: valor total pago na nota (float)
    :param quantidade: quantidade comprada (float)
    :param data_compra: data no formato DD/MM/AAAA (string)
    :param local_compra: nome do estabelecimento (string)
    :param db_path: caminho do arquivo SQLite (string)
    """
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            INSERT INTO precos 
                (produto, unidade_medida, preco_por_unidade, preco_pago, quantidade, data_compra, local_compra)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (produto, unidade_medida, preco_por_unidade, preco_pago, quantidade, data_compra, local_compra))
        conn.commit()


def tabela2_para_tabela3(
    linhas: list[str],
    local_compra: str,
    db_path: str = DB_PATH
) -> None:
    """
    Recebe a lista de linhas CSV do PROMPT_PROCESSAR_TABELA já processadas,
    calcula o preço por unidade e insere todas no banco.
    :param linhas: lista de strings CSV no formato: Produto,Quantidade,Unidade_Medida,Peso_Unitario_g,Preco_Pago,Data_Compra
    :param local_compra: nome do estabelecimento extraído da nota (string)
    :param db_path: caminho do arquivo SQLite (string)
    """
    from processador import calcular_preco_por_kg

    criar_banco(db_path)
    inseridos = 0
    erros = 0

    for linha in linhas:
        try:
            partes = linha.strip().split(",")
            if len(partes) != 6:
                print(f"[AVISO] Linha ignorada — formato inesperado: {linha}")
                erros += 1
                continue

            produto, quantidade, unidade, peso_unitario_g, preco_pago, data_compra = partes

            quantidade    = float(quantidade)
            preco_pago    = float(preco_pago)

            preco_por_unidade = calcular_preco_por_kg(
                produto       = produto,
                quantidade    = quantidade,
                unidade       = unidade,
                peso_unitario_g = peso_unitario_g.strip(),
                preco_pago    = preco_pago
            )

            inserir_preco(
                produto           = produto.strip(),
                unidade_medida    = unidade.strip(),
                preco_por_unidade = preco_por_unidade,
                preco_pago        = preco_pago,
                quantidade        = quantidade,
                data_compra       = data_compra.strip(),
                local_compra      = local_compra,
                db_path           = db_path
            )
            inseridos += 1

        except Exception as e:
            print(f"[ERRO] Falha ao inserir linha '{linha}': {e}")
            erros += 1

    print(f"[DB] Inserção concluída — {inseridos} registros inseridos, {erros} erros.")


def consultar_precos(produto: str, db_path: str = DB_PATH) -> list[dict]:
    """
    Consulta o histórico de preços de um produto.
    :param produto: nome do produto a consultar (string)
    :param db_path: caminho do arquivo SQLite (string)
    :return: lista de dicionários com os registros encontrados
    """
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT produto, unidade_medida, preco_por_unidade, preco_pago,
                   quantidade, data_compra, local_compra
            FROM precos
            WHERE produto = ?
            ORDER BY data_compra DESC
        """, (produto,))
        return [dict(row) for row in cursor.fetchall()]


def media_precos(produto: str, db_path: str = DB_PATH) -> float | None:
    """
    Retorna o preço médio por unidade de um produto no histórico.
    :param produto: nome do produto (string)
    :param db_path: caminho do arquivo SQLite (string)
    :return: média do preco_por_unidade (float) ou None se não houver registros
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("""
            SELECT AVG(preco_por_unidade)
            FROM precos
            WHERE produto = ? AND preco_por_unidade IS NOT NULL
        """, (produto,))
        resultado = cursor.fetchone()[0]
        return round(resultado, 2) if resultado else None