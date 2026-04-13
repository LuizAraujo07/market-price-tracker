import lmstudio as lms

from teste import texto_teste1, nota_docling_teste, json_teste1
from processador import processar_pdf_com_modelo, processar_texto_tabela1, processar_nota_tab1, processar_pdf_json






if __name__ == "__main__":
    model = lms.llm("google/gemma-4-e2b",
                     config={"temperature": 0.0,
                             "contextLength": 98468})

    comando = input(
        "Pressione 1 para processar tabela de produtos\n"
        "2 para processar tabela de notas\n"
        "3 para processar PDF para JSON\n" 
        "4 para processar PDF completo\n"
        "Digite o número correspondente ao comando desejado: "
        )
    if comando == "1":
        tabela_produtos = processar_texto_tabela1(texto_teste1, model)
        print("Resposta tabela produtos:\n********************************")
        print(f"\n\n{tabela_produtos}\n********************************\n\n")
    elif comando == "2":
        tabela_notas = processar_nota_tab1(json_teste1, model)
        print("Resposta tabela notas:\n********************************")
        print(f"\n\n{tabela_notas}\n********************************\n\n")
    elif comando == "3":
        caminho_pdf = "documents/nota1.pdf"
        tabela_notas_json = processar_pdf_json(caminho_pdf, model)
        print("Resposta tabela notas JSON:\n********************************")
        print(f"\n\n{tabela_notas_json}\n********************************\n\n")
    elif comando == "4":
        caminho_pdf = "documents/nota1.pdf"
        resposta = processar_pdf_com_modelo(caminho_pdf, model)
        print("Resposta tabela notas JSON:\n********************************")
        print(f"\n\n{resposta}\n********************************\n\n")
    