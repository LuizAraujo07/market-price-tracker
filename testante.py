import lmstudio as lms

from teste import texto_teste1, nota_docling_teste, json_teste1
from processador import processar_texto_tabela1, processar_nota_tab1, procesar_pdf_json






if __name__ == "__main__":
    model = lms.llm("google__gemma-4-e4b-it@q8_0")
    comando = input("Pressione 1 para processar tabela de produtos\n" "2 para processar tabela de notas\n" "3 para processar PDF para JSON\n" "Digite o número correspondente ao comando desejado: ")
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
        tabela_notas_json = procesar_pdf_json(caminho_pdf, model)
        print("Resposta tabela notas JSON:\n********************************")
        print(f"\n\n{tabela_notas_json}\n********************************\n\n")
    