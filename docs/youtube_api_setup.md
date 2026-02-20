# YouTube API 配置指南

## 📋 配置步骤

### 第一步：创建Google Cloud项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 点击顶部导航栏的项目选择器
3. 点击"新建项目"
4. 输入项目名称（例如：`Zzy_Personal_Agent`）
5. 点击"创建"

### 第二步：启用YouTube Data API v3

1. 在Google Cloud Console中，选择你刚创建的项目
2. 点击左侧菜单的"API和服务" → "库"
3. 在搜索框中输入"YouTube Data API v3"
4. 点击"YouTube Data API v3"
5. 点击"启用"按钮

### 第三步：创建API密钥

1. 点击左侧菜单的"API和服务" → "凭据"
2. 点击顶部的"创建凭据" → "API密钥"
3. API密钥会自动生成并显示
4. **重要**：点击"限制密钥"以提高安全性

### 第四步：配置API密钥限制（推荐）

1. 在API密钥编辑页面：
   - **名称**：给密钥起一个有意义的名字（如"YouTube Agent Key"）
   - **应用程序限制**：
     - 选择"IP地址"（如果是服务器部署）
     - 或选择"HTTP引荐来源网址"（如果是Web应用）
     - 或选择"无"（仅用于开发测试）
   - **API限制**：
     - 选择"限制密钥"
     - 在下拉列表中选择"YouTube Data API v3"

2. 点击"保存"

### 第五步：复制API密钥

1. 复制生成的API密钥（格式类似：`AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）
2. 将密钥保存到安全的地方

### 第六步：配置到项目中

编辑 `.env` 文件：

```bash
# YouTube API配置
YOUTUBE_API_KEY=你的API密钥
```

例如：
```bash
YOUTUBE_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 📊 配额和限制

### 默认配额

YouTube Data API v3 的默认配额：

- **每日配额**：10,000 单位/天
- **每秒查询数（QPS）**：3,000 单位/100秒 = 30 QPS

### 配额使用情况

不同操作消耗的配额单位：

| 操作 | 配额单位 |
|------|---------|
| search.list | 100 单位 |
| videos.list | 1 单位 |
| channels.list | 1 单位 |
| playlistItems.list | 1 单位 |

### 示例计算

- 每天可以执行约 **100次搜索**（100 × 100 = 10,000）
- 每天可以获取约 **10,000个视频详情**（10,000 × 1）

### 申请更高配额

如果需要更高配额：

1. 访问 [YouTube API配额申请表单](https://forms.gle/HGf7nUvXPyvYvM5H9)
2. 填写申请表，说明你的使用场景
3. 等待Google审核（通常需要几个工作日）

## 🔧 使用方法

### 安装依赖

```bash
cd /Users/andreazhuo/AI/Zzy_Personal_Agent
source venv/bin/activate
pip install google-api-python-client
```

### 测试API连接

```python
from googleapiclient.discovery import build
import os

api_key = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

# 测试搜索
request = youtube.search().list(
    part='snippet',
    q='Python编程',
    maxResults=5
)
response = request.execute()

for item in response['items']:
    print(item['snippet']['title'])
```

## 🛡️ 安全最佳实践

### 1. 限制API密钥

- ✅ 设置IP地址白名单
- ✅ 限制只能访问特定API
- ✅ 定期轮换API密钥

### 2. 不要泄露密钥

- ❌ 不要将密钥提交到Git仓库
- ❌ 不要在前端代码中暴露密钥
- ✅ 使用环境变量存储密钥
- ✅ 在 `.gitignore` 中添加 `.env` 文件

### 3. 监控使用情况

- 定期检查API使用统计
- 设置预算提醒
- 监控异常流量

## 🚨 常见问题

### 问题1：API密钥无效

**错误信息**：`API key not valid. Please pass a valid API key.`

**解决方法**：
1. 检查API密钥是否正确复制
2. 确认YouTube Data API v3已启用
3. 检查API密钥是否被限制

### 问题2：配额超限

**错误信息**：`The request cannot be completed because you have exceeded your quota.`

**解决方法**：
1. 等待配额重置（每天太平洋时间午夜）
2. 申请更高配额
3. 优化API调用，减少不必要的请求

### 问题3：权限被拒绝

**错误信息**：`Access Not Configured. YouTube Data API has not been used in project`

**解决方法**：
1. 确认已启用YouTube Data API v3
2. 等待几分钟让更改生效
3. 检查项目是否正确选择

## 📝 配置检查清单

- [ ] 创建Google Cloud项目
- [ ] 启用YouTube Data API v3
- [ ] 创建API密钥
- [ ] 配置API密钥限制
- [ ] 将API密钥添加到 `.env` 文件
- [ ] 安装 `google-api-python-client`
- [ ] 测试API连接

## 🔗 相关链接

- [YouTube Data API 官方文档](https://developers.google.com/youtube/v3)
- [Google API Python客户端](https://github.com/googleapis/google-api-python-client)
- [API配额计算器](https://developers.google.com/youtube/v3/determine_quota_cost)
- [配额申请表单](https://forms.gle/HGf7nUvXPyvYvM5H9)

## 💡 提示

1. **开发阶段**：可以暂时不设置API密钥限制，使用 `youtube-search` 库作为备用方案
2. **生产环境**：务必设置API密钥限制，防止密钥被滥用
3. **成本控制**：监控API使用量，避免超出配额
4. **缓存策略**：对频繁请求的数据进行缓存，减少API调用

---

**配置完成后，运行测试脚本验证：**

```bash
python quick_test_youtube.py
```
