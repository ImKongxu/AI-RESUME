from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
from typing import Optional
from app.services.deepseek_service import DeepSeekService
from app.services.pdf_generator_service import PDFGeneratorService

router = APIRouter(
    prefix="/api/resume",
    tags=["简历生成"],
)

# 请求模型定义
class ResumeGenerateRequest(BaseModel):
    content_request: str  # 用户的简历内容请求
    system_prompt: Optional[str] = None  # 可选的自定义系统提示词

# 响应模型定义
class ResumeGenerateResponse(BaseModel):
    success: bool
    generated_content: str  # 这里将包含Markdown格式的内容
    message: str

# 简历修改请求模型
class ResumeReviseRequest(BaseModel):
    resume_content: str    # 原始简历内容
    revision_request: str  # 修改请求

# Markdown到PDF转换请求模型
class MarkdownToPDFRequest(BaseModel):
    markdown_content: str  # Markdown格式的内容
    custom_css: Optional[str] = None  # 可选的自定义CSS样式

# 获取DeepSeek服务的依赖函数
def get_deepseek_service():
    return DeepSeekService()

# 获取PDF生成服务的依赖函数
def get_pdf_generator_service():
    return PDFGeneratorService()

@router.post("/generate", response_model=ResumeGenerateResponse)
async def generate_resume(
    request: ResumeGenerateRequest,
    deepseek_service: DeepSeekService = Depends(get_deepseek_service)
):
    """
    根据用户请求生成简历内容
    
    - **content_request**: 用户对简历内容的具体要求
    - **system_prompt**: 可选的系统提示词，用于定制AI的行为
    
    返回生成的Markdown格式简历内容
    """
    try:
        # 使用异步方法调用DeepSeek服务生成简历内容
        if request.system_prompt:
            # 如果提供了自定义系统提示词，则使用它
            generated_content = await deepseek_service.send_message_async(
                message=request.content_request,
                system_prompt=request.system_prompt
            )
        else:
            # 否则使用服务中的默认提示词
            generated_content = await deepseek_service.send_message_async(
                message=request.content_request
            )
        
        # 返回成功响应
        return ResumeGenerateResponse(
            success=True,
            generated_content=generated_content,
            message="简历内容生成成功（Markdown格式）"
        )
    
    except Exception as e:
        # 捕获并处理所有异常
        raise HTTPException(
            status_code=500,
            detail=f"生成简历内容时发生错误: {str(e)}"
        )

@router.post("/revise", response_model=ResumeGenerateResponse)
async def revise_resume(
    request: ResumeReviseRequest,
    deepseek_service: DeepSeekService = Depends(get_deepseek_service)
):
    """
    根据用户请求修改现有简历内容
    
    - **resume_content**: 原始简历内容
    - **revision_request**: 对简历的修改要求
    
    返回修改后的Markdown格式简历内容
    """
    try:
        # 构建完整的修改请求消息
        full_message = f"现有简历内容：{request.resume_content}\n\n修改要求：{request.revision_request}"

        # 使用异步方法调用DeepSeek服务进行修改，使用专用的修改提示词
        revised_content = await deepseek_service.send_message_async(
            message=full_message,
            system_prompt=deepseek_service.revise_system_prompt
        )

        # 返回成功响应
        return ResumeGenerateResponse(
            success=True,
            generated_content=revised_content,
            message="简历内容修改成功（Markdown格式）"
        )

    except Exception as e:
        # 捕获并处理所有异常
        raise HTTPException(
            status_code=500,
            detail=f"修改简历内容时发生错误: {str(e)}"
        )

@router.post("/markdown-to-pdf")
async def convert_markdown_to_pdf(
    request: MarkdownToPDFRequest,
    pdf_generator_service: PDFGeneratorService = Depends(get_pdf_generator_service)
):
    """
    将Markdown格式的内容转换为PDF文件
    
    - **markdown_content**: Markdown格式的文本内容
    - **custom_css**: 可选的自定义CSS样式
    
    返回生成的PDF文件
    """
    try:
        # 异步生成PDF
        pdf_data = await pdf_generator_service.markdown_to_pdf_async(
            markdown_content=request.markdown_content,
            css=request.custom_css
        )
        
        # 返回PDF文件作为响应
        return Response(
            content=pdf_data,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=resume.pdf"
            }
        )
    
    except Exception as e:
        # 捕获并处理所有异常
        raise HTTPException(
            status_code=500,
            detail=f"生成PDF时发生错误: {str(e)}"
        )