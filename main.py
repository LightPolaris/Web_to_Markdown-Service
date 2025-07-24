from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import html2text
import time
import logging
import uvicorn
from selenium.common.exceptions import WebDriverException, TimeoutException

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    filename='/fast_api/logs/8203/warm.log', 
    )
logger = logging.getLogger(__name__)

# 初始化FastAPI应用
app = FastAPI(
    title="网页转Markdown服务",
    description="将动态网页内容转换为Markdown格式的API服务",
    version="1.0.0"
)

# 请求模型
class UrlRequest(BaseModel):
    url: str
    wait_time: float = 2.0  # 默认等待2秒

# 浏览器实例初始化为None
driver = None

@app.on_event("startup")
async def startup_event():
    """启动时初始化浏览器"""
    global driver
    try:
        logger.info("正在初始化Chrome浏览器...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)  # 设置全局超时时间·
        logger.info("Chrome浏览器初始化完成")
    except Exception as e:
        logger.error(f"浏览器初始化失败: {str(e)}")
        raise RuntimeError(f"浏览器初始化失败: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    """关闭时清理浏览器"""
    global driver
    if driver is not None:
        logger.info("正在关闭浏览器...")
        try:
            driver.quit()
        except Exception as e:
            logger.error(f"关闭浏览器时出错: {str(e)}")
        finally:
            driver = None
            logger.info("浏览器已关闭")

def convert_webpage_to_md(url: str, wait_time: float = 2.0) -> str:
    """将网页转换为Markdown"""
    global driver
    if driver is None:
        raise RuntimeError("浏览器未初始化")
    
    try:
        logger.info(f"正在访问URL: {url}")
        try:
            driver.get(url)
            time.sleep(wait_time)  # 等待页面加载完成
            
            html_content = driver.page_source
            
            converter = html2text.HTML2Text()
            converter.ignore_links = False
            converter.ignore_images = False
            converter.images_as_html = False
            converter.wrap_links = False
            
            markdown_content = converter.handle(html_content)
            markdown_content = markdown_content.replace("\\_", "_")
            
            logger.info(f"成功转换URL: {url}")
            return markdown_content
            
        except TimeoutException:
            logger.warning(f"页面加载超时，但继续处理已加载的内容")
            html_content = driver.page_source
            converter = html2text.HTML2Text()
            return converter.handle(html_content)
            
    except WebDriverException as e:
        logger.error(f"浏览器操作失败: {str(e)}")
        raise RuntimeError(f"浏览器操作失败: {str(e)}")
    except Exception as e:
        logger.error(f"转换失败: {str(e)}")
        raise RuntimeError(f"转换失败: {str(e)}")

@app.post("/convert", response_class=PlainTextResponse)
async def convert_url_to_md(request: UrlRequest):
    """将网页转换为Markdown的API端点"""
    try:
        if not request.url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="URL必须以http://或https://开头")
            
        start_time = time.time()
        md_text = convert_webpage_to_md(request.url, request.wait_time)
        elapsed_time = time.time() - start_time
        
        logger.info(f"转换完成，用时: {elapsed_time:.2f}秒")
        return md_text
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API调用失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"转换失败: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)