from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend

def conversor_pdf_simples(arquivo_pdf, extrair_imagens=False):
    """
    Versão simplificada do conversor de PDF.
    
    Args:
        arquivo_pdf (str): Caminho para o arquivo PDF
        extrair_imagens (bool): Se deve extrair imagens do documento
    
    Returns:
        str: Documento convertido em formato Markdown
    """
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.generate_picture_images = extrair_imagens
    
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                backend=PyPdfiumDocumentBackend
            )
        }
    )
    
    resultado = converter.convert(arquivo_pdf)

    return resultado.document.export_to_markdown()