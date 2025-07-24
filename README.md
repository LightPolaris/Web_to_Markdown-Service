# 网页转Markdown服务

一个基于FastAPI和Selenium的高性能网页转换服务，能够将动态网页内容转换为Markdown格式。

## 🚀 功能特性

- **动态网页解析**：支持JavaScript渲染的动态网页内容
- **高质量转换**：使用html2text库确保转换质量
- **RESTful API**：提供简洁的HTTP API接口
- **自定义等待时间**：支持设置页面加载等待时间
- **完整的日志系统**：详细记录操作日志，便于调试和监控
- **错误处理**：完善的异常处理机制

## 📋 技术栈

- **FastAPI**：现代、快速的Web框架
- **Selenium**：浏览器自动化工具
- **html2text**：HTML到Markdown的转换器
- **Chrome WebDriver**：无头浏览器驱动
- **Uvicorn**：ASGI服务器

## 🛠️ 安装与配置

### 环境要求

- Python 3.7+
- Chrome/Chromium浏览器
- Chrome WebDriver（自动下载管理）

### 安装依赖

```bash
pip install fastapi selenium html2text uvicorn webdriver-manager
```

### 创建日志目录

```bash
mkdir -p /fast_api/logs/8203
```

## 🔧 使用方法

### 启动服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动。

### API文档

启动服务后，访问以下地址查看自动生成的API文档：

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### API接口

#### POST /convert

将指定URL的网页转换为Markdown格式。

**请求体**：
```json
{
  "url": "https://example.com",
  "wait_time": 2.0
}
```

**参数说明**：
- `url` (必填)：要转换的网页URL，必须以`http://`或`https://`开头
- `wait_time` (可选)：页面加载等待时间，默认2秒

**响应**：
- **状态码 200**：转换成功，返回Markdown格式文本
- **状态码 400**：请求参数错误
- **状态码 500**：服务器内部错误

**示例请求**：
```bash
curl -X POST "http://localhost:8000/convert" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com", "wait_time": 3.0}'
```

## 📝 使用示例

### Python客户端示例

```python
import requests

# 转换网页
response = requests.post(
    "http://localhost:8000/convert",
    json={
        "url": "https://example.com",
        "wait_time": 2.0
    }
)

if response.status_code == 200:
    markdown_content = response.text
    print(markdown_content)
else:
    print(f"转换失败: {response.text}")
```

### JavaScript客户端示例

```javascript
const convertWebpage = async (url, waitTime = 2.0) => {
    try {
        const response = await fetch('http://localhost:8000/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: url,
                wait_time: waitTime
            })
        });
        
        if (response.ok) {
            const markdown = await response.text();
            return markdown;
        } else {
            throw new Error(`转换失败: ${response.statusText}`);
        }
    } catch (error) {
        console.error('请求失败:', error);
        throw error;
    }
};

// 使用示例
convertWebpage('https://example.com', 3.0)
    .then(markdown => console.log(markdown))
    .catch(error => console.error(error));
```

## 🔍 日志

日志文件位置：`/fast_api/logs/8203/warm.log`

日志级别：INFO

日志内容包括：
- 浏览器初始化状态
- URL访问记录
- 转换成功/失败信息
- 错误详情和异常堆栈

## ⚙️ 配置选项

### Chrome浏览器选项

服务使用以下Chrome选项以确保在服务器环境中稳定运行：

- `--headless`：无头模式运行
- `--disable-gpu`：禁用GPU加速
- `--no-sandbox`：禁用沙箱模式
- `--disable-dev-shm-usage`：禁用/dev/shm使用

### 超时设置

- 页面加载超时：30秒（全局设置）
- 自定义等待时间：通过API参数控制

## 🚨 错误处理

服务包含完善的错误处理机制：

1. **URL格式验证**：确保URL格式正确
2. **浏览器状态检查**：确保浏览器正常初始化
3. **超时处理**：页面加载超时时仍会处理已加载内容
4. **异常捕获**：详细记录所有异常信息

## 🔧 故障排除

### 常见问题

1. **浏览器初始化失败**
   - 确保已安装Chrome浏览器
   - 检查系统权限设置
   - 查看日志文件获取详细错误信息

2. **页面加载超时**
   - 增加`wait_time`参数值
   - 检查网络连接
   - 确认目标网站可访问

3. **转换结果异常**
   - 检查目标网页是否为动态内容
   - 调整等待时间
   - 查看日志了解具体错误

### 日志查看

```bash
tail -f /fast_api/logs/8203/warm.log
```

## 📄 许可证

[在此添加许可证信息]

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 📞 支持

如有任何问题或建议，请通过以下方式联系：

- 创建Issue：[项目Issues页面]
- 邮箱：[联系邮箱]

---

**注意**：本服务需要在具有Chrome浏览器的环境中运行，建议在生产环境中使用Docker容器部署以确保环境一致性。
