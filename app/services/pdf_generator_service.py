import markdown
from weasyprint import HTML
from io import BytesIO
import asyncio

class PDFGeneratorService:
    def __init__(self):
        # 初始化PDF生成服务
        # 设置默认的CSS样式，使PDF看起来更专业
        self.default_css = """
            @page {
                margin: 2cm;
                size: A4;
            }
            body {
                font-family: SimSun, Georgia, serif;
                line-height: 1.6;
                color: #333;
            }
            h1, h2, h3, h4, h5, h6 {
                color: #2c3e50;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }
            h1 {
                font-size: 2.5em;
                border-bottom: 2px solid #eee;
                padding-bottom: 0.3em;
            }
            h2 {
                font-size: 2em;
                border-bottom: 1px solid #eee;
                padding-bottom: 0.3em;
            }
            p {
                margin-bottom: 1em;
            }
            ul, ol {
                margin-bottom: 1em;
                padding-left: 1.5em;
            }
            code {
                font-family: 'Courier New', monospace;
                background-color: #f8f8f8;
                padding: 0.2em 0.4em;
                border-radius: 3px;
            }
            pre {
                background-color: #f8f8f8;
                padding: 1em;
                border-radius: 5px;
                overflow-x: auto;
                margin-bottom: 1em;
            }
            pre code {
                background-color: transparent;
                padding: 0;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 1em;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
            }
            th {
                background-color: #f2f2f2;
                text-align: left;
            }
        """
    
    def markdown_to_pdf(self, markdown_content: str, css: str = None) -> bytes:
        """
        将Markdown内容转换为PDF格式
        
        参数:
            markdown_content: Markdown格式的文本内容
            css: 可选的自定义CSS样式
        
        返回:
            包含PDF数据的字节数组
        """
        # 如果没有提供自定义CSS，使用默认样式
        if css is None:
            css = self.default_css
        
        # 将Markdown转换为HTML
        html_content = markdown.markdown(markdown_content)
        
        # 添加CSS样式到HTML
        full_html = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                {css}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>"""
        
        # 创建BytesIO对象来存储PDF数据
        pdf_buffer = BytesIO()
        
        # 使用WeasyPrint将HTML渲染为PDF
        HTML(string=full_html).write_pdf(pdf_buffer)
        
        # 获取PDF数据
        pdf_data = pdf_buffer.getvalue()
        pdf_buffer.close()
        
        return pdf_data
    
    async def markdown_to_pdf_async(self, markdown_content: str, css: str = None) -> bytes:
        """
        异步将Markdown内容转换为PDF格式
        
        参数:
            markdown_content: Markdown格式的文本内容
            css: 可选的自定义CSS样式
        
        返回:
            包含PDF数据的字节数组
        """
        # 使用线程池执行同步调用，避免阻塞事件循环
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,  # 使用默认线程池
            self.markdown_to_pdf,  # 要执行的同步函数
            markdown_content,  # 函数参数
            css  # 函数参数
        )