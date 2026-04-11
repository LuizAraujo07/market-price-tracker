from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend

def _criar_conversor(extrair_imagens: bool) -> DocumentConverter:
    """Cria e configura o DocumentConverter."""
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.generate_picture_images = extrair_imagens

    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                backend=PyPdfiumDocumentBackend
            )
        }
    )


def conversor_pdf_simples(arquivo_pdf: str | Path, extrair_imagens: bool = False) -> str:
    """
    Converte um arquivo PDF para formato Markdown.

    Args:
        arquivo_pdf: Caminho para o arquivo PDF.
        extrair_imagens: Se True, extrai imagens do documento.

    Returns:
        Conteúdo do documento em formato Markdown.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se o arquivo não for um PDF.
        RuntimeError: Se a conversão falhar.
    """
    caminho = Path(arquivo_pdf)

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    if caminho.suffix.lower() != ".pdf":
        raise ValueError(f"O arquivo deve ser um PDF, recebido: {caminho.suffix!r}")

    try:
        converter = _criar_conversor(extrair_imagens)
        resultado = converter.convert(str(caminho))
        return resultado.document.export_to_markdown()
    except Exception as e:
        raise RuntimeError(f"Falha ao converter '{caminho.name}': {e}") from e


