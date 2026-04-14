PROMPT_EXTRAIR_COMPRAS = """
Você receberá um JSON de uma NFC-e brasileira já estruturado.
Converta os itens para uma tabela CSV com as colunas abaixo, sem introduções ou comentários.

**Colunas:**
Nome_Produto, Quantidade, Unidade_Medida, Valor_Unitario, Valor_Total, Data_Compra, Local_Compra

**Regras:**
1. `Nome_Produto`: use o campo `descricao` do JSON. Não inclua o código do produto.
2. `Data_Compra`: extraia do campo `emissao`, formato DD/MM/AAAA.
3. `Local_Compra`: use o campo `emitente.nome`.
4. Valores numéricos com ponto como separador decimal (ex: 10.90).
5. Se algum campo estiver ausente no JSON, preencha com "N/A".
6. Responda SOMENTE com o CSV, sem blocos de código ou markdown.
"""




PROMPT_PROCESSAR_TABELA = """
Você receberá uma linha de CSV de compras de supermercado.
Processe e devolva apenas uma linha CSV normalizada, sem cabeçalho.

**Colunas de saída:** Produto, Quantidade, Unidade_Medida, Peso_Unitario_g, Preco_Pago, Data_Compra

**Regras:**
1. `Produto`: mantenha apenas o nome genérico do produto. Remova marcas, tamanhos, pesos e adjetivos.
   - ✅ "Linguica" | ❌ "Linguica Frimesa 250g"
   - ✅ "Macarrao" | ❌ "Macarrao Todeschini 500g"
   - ✅ "Suco Laranja" | ❌ "Suco Kapo Laranja"
   - ✅ "Biscoito" | ❌ "Bisc Renata 112g"
   - Para frutas e verduras, mantenha a variedade: "Batata Monalisa" → "Batata".
   - Sem acentos, sem abreviações.

2. `Quantidade`: mantenha o valor original da entrada, sem calcular nada.

3. `Unidade_Medida`: mantenha a unidade original (UN ou KG). Não converta.

4. `Peso_Unitario_g`: extraia o peso ou volume unitário mencionado no nome do produto, em gramas ou ml.
   - "Salsicha Frimesa 400g" → 400
   - "Macarrao 500g" → 500
   - "Leite 1L" → 1000
   - Se não houver peso/volume no nome, preencha com N/A.

5. `Preco_Pago`: use o Valor_Total da linha de entrada.

6. Valores numéricos com ponto como separador decimal.

7. Responda SOMENTE com a linha CSV, sem cabeçalho e sem explicações.
   - ❌ Errado: Produto,Quantidade,...\\nSalsicha,2.0,...
   - ✅ Certo:   Salsicha,2.0,UN,400,17.98,30/09/2025
"""


PROMPT_NOTA_JSON = """
Você receberá o conteúdo em Markdown de uma NFC-e brasileira.
Extraia todos os itens em JSON com os campos:
- codigo (string)
- descricao (string)
- quantidade (número)
- unidade (string, ex: "KG", "UN")
- valor_unitario (número)
- valor_total (número)

Também extraia os campos da nota:
- emitente (nome, cnpj, endereco)
- numero, serie, emissao (datetime)
- valor_total, desconto, valor_pagar
- forma_pagamento
- chave_acesso
- cpf_consumidor

Responda SOMENTE com JSON válido, sem explicações.
"""


PROMPT_VERIFICAR_RESPOSTA = """
**Papel:** Você é um avaliador de qualidade de respostas geradas por modelos de linguagem.
**Objetivo:** Avaliar a qualidade e a precisão da resposta gerada pelo modelo.
**Instruções:**
1. Analise a resposta gerada pelo modelo.
2. Verifique se a resposta é relevante e útil.
3. Determine se a resposta está de acordo com as diretrizes fornecidas.
4. Responda com "Resposta adequada" se for o caso, ou "Resposta inadequada" caso contrário.
"""