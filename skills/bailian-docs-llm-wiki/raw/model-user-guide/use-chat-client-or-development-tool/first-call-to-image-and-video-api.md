# 使用Postman或cURL调用图像/视频生成API

本文介绍使用**Postman**和**cURL**调用阿里云百炼的图像或视频生成 API。以“[文生图](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)”为例，演示从创建任务到获取结果的完整流程。

-   Postman：一款界面化的 HTTP 测试工具，操作直观，**推荐初学者使用**。
    
-   cURL：一个强大的命令行工具，适用于熟悉命令行的开发者。
    

**说明**

Postman 和 cURL仅适用于快速测试与功能验证。对于生产环境，建议您使用官方 SDK 或自行实现 HTTP 调用。

## **API异步调用机制**

由于图像与视频生成任务耗时较长（十几秒到数分钟不等），为避免长时间的HTTP连接等待和超时，API采用异步调用机制。整个调用过程分为两步：

1.  **创建任务**：调用 API 创建任务，服务会同步返回一个任务 ID（task\_id）。
    
2.  **查询结果**：使用该 task\_id，通过轮询方式查询任务状态，直到任务完成并获取最终的图像或视频 URL。
    

**HTTP调用示例（文生图）**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4178421871/CAEQZRiBgICJ0seH1xkiIDgzYWE2MTBkZjkzODRkNDA5NzczNTE0NjBiMGE1Y2Nm5274221_20250627113930.173.svg)

## **方式一：使用Postman发送请求（推荐）**

#### 如何根据 cURL 配置 Postman？

将 cURL 示例转换为 Postman 请求时，各参数存在以下对应关系：

**cURL参数**

**Postman 界面**

**说明**

`curl -X POST`或`curl -X GET`

请求方法下拉框

选择 HTTP 请求方法

`https://<api-endpoint-url>`

URL 输入框

API 的请求地址

`-H 'Key: Value'`

Headers标签页

配置请求头，以 键 (Key) - 值 (Value) 的形式展示。

`-d '{...}'`

Body标签页

配置请求体

### **前提条件**

在调用API之前，您需要[根据地域获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，下载[Postman](https://www.postman.com/downloads/)到本地。

### **步骤1：创建任务**

我们将根据下面的 cURL 命令来配置 Postman。

> 以下为北京地域的base\_url，不同地域需配置对应的 base\_url。

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.6-t2i",
    "input": {
        "prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"
    },
    "parameters": {
        "size": "1024*1024",
        "n": 1
    }
}'
```

1.  在 Postman 中，单击**new**或`+` 按钮创建一个新请求，请求类型选择**HTTP**。
    
2.  在请求方法下拉菜单中选择**POST**，并根据您的模型所在地域填入对应的 URL：
    
    -   华北2（北京）：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`
        
    -   新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`，请将`WorkspaceId`替换为真实的[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)
        
    -   美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`
        
    
    > 各地域支持的模型请参见百炼控制台，当前地域与服务部署范围为[系统预设绑定关系](https://help.aliyun.com/zh/model-studio/regions/#6e9530261dv6q)，不支持自由组合。
    
3.  点击**Headers**标签页，添加以下三个键值对。
    
    **Key**
    
    **Value**
    
    **说明**
    
    在 Postman 的 **Headers** 标签页中，配置以下关键请求头：**X-DashScope-Async** 设置为 `enable`，**Authorization** 设置为 `Bearer <your-api-key>`，**Content-Type** 设置为 `application/json`。
    
    X-DashScope-Async
    
    enable
    
    启用异步调用
    
    Authorization
    
    Bearer sk-xxx（请将sk-xxx替换为阿里云百炼API Key）
    
    身份验证凭证
    
    Content-Type
    
    application/json
    
    声明请求体为JSON格式
    
4.  配置请求体 (Body)
    
    -   点击 **Body** 标签页，选中 **raw** 单选框，然后在右侧的格式下拉菜单中选择**JSON**，将cURL示例中的 `-d` 后面的 JSON 内容粘贴到输入框。
        
        ```
        {
            "model": "wan2.5-t2i-preview",
            "input": {
                "prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"
            },
            "parameters": {
                "size": "1024*1024",
                "n": 1
            }
        }
        ```
        
    -   （可选）点击页面右侧的 `**Beautify**`，可以格式化JSON格式，使其更易阅读。
        
    
5.  点击**Send**发送请求，并获取 `task_id`。有效期 24 小时，过期后无法查询，请及时获取结果。
    
    ```
    {
        "request_id": "896b2ccd-a0cd-40a8-a557-bb73cee5cf95",
        "output": {
            "task_id": "42442de9-917d-4c41-80a7-37fb7ad25ed2",
            "task_status": "PENDING"
        }
    }
    ```
    

### **步骤2：根据task\_id查询结果**

获取到 task\_id 后，需要通过查询接口来获取最终结果。

-   华北2（北京）：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`
    
-   新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`，请将`WorkspaceId`替换为真实的[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)
    
-   美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`
    

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

1.  在 Postman 中配置查询请求：
    
    1.  新建一个HTTP请求。
        
    2.  配置请求方法为**GET** 。
        
    3.  根据地域，填入查询URL，将URL中的 `{task_id}` 替换为在步骤1中获取的真实 task\_id。
        
    4.  在**Headers**标签页中，添加 Authorization 键，其值与步骤1中使用的 API Key 相同。
        
    5.  点击**Send**发送请求。
        
    
2.  检查返回结果。重复发送此请求（轮询），直到 task\_status 变为 SUCCEEDED，获取图像的URL。图像URL有效期为**24小时**，请及时下载。
    
    ```
    "results": [
                {
                    "orig_prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵",
                    "actual_prompt": "一间温馨雅致的花店，外墙装饰着精致的雕花窗户，窗框为浅色木质，镶嵌着透明玻璃，透出店内柔和的光线。花店正门是一扇漂亮的实木门，表面保留了天然木纹，配以黄铜门把手和复古门牌，显得古朴而有质感。门前台阶两侧和店内窗台、门口处错落有致地摆放着各式鲜花——包括玫瑰、百合、绣球、郁金香等，色彩缤纷、生机盎然。部分花束用牛皮纸包裹，系着麻绳，散发出自然清新的气息。背景为宁静的欧洲小镇街景，石板路与绿植相映成趣。整体画面采用写实摄影风格，光线柔和，色调温暖，突出花店的精致与浪漫氛围。",
                    "url": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/1d/3a/20251203/7a2bee47/42442de9-917d-4c41-80a7-37fb7ad25ed2.png?xxx"
                }
            ]
    ```
    

## **方式二：使用cURL发送请求**

熟悉命令行的开发者可使用cURL快速测试API。

### **前提条件**

在执行cURL命令之前，您需要：

-   已[开通模型服务并获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    
-   确保您的系统中已安装 cURL，并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，方便后续直接引用`$DASHSCOPE_API_KEY`变量。
    
    **检查是否已安装cURL**
    
    运行以下命令，检查 cURL 是否已安装。
    
    ```
    curl --version
    ```
    
    如果看到类似如下输出，说明cURL已安装：
    
    ```
    curl 8.x.x (x86_64-apple-darwin23.0) libcurl/8.x.x (SecureTransport) LibreSSL/3.3.6 zlib/1.2.12 nghttp2/1.58.0
    Release-Date: 2023-10-11
    Protocols: dict file ftp ftps gopher gophers http https imap imaps ldap ldaps mqtt pop3 pop3s rtsp smb smbs smtp smtps telnet tftp
    Features: alt-svc AsynchDNS GSS-API HSTS HTTP2 HTTPS-proxy IPv6 Kerberos Largefile libz MultiSSL NTLM NTLM_WB SPNEGO SSL threadsafe UnixSockets
    ```
    
    如果没有安装，可能会给出以下类似提示：
    
    -   Windows: `'curl' 不是内部或外部命令，也不是可运行的程序或批处理文件`。
        
    -   Linux/macOS: `command not found: curl`。
        
    
    请访问[curl下载](https://curl.se/download.html)页面进行安装，
    

### **步骤1：创建任务**

-   在终端执行以下命令：
    
    > 以下为北京地域的base\_url，不同地域需配置对应的 base\_url。
    
    ```
    curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
        -H 'X-DashScope-Async: enable' \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H 'Content-Type: application/json' \
        -d '{
        "model": "wan2.5-t2i-preview",
        "input": {
            "prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"
        },
        "parameters": {
            "size": "1024*1024",
            "n": 1
        }
    }'
    ```
    
-   成功请求后将返回`task_id`。有效期 24 小时，过期后无法查询。请及时获取结果。
    
    ```
    curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
        -H 'X-DashScope-Async: enable' \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H 'Content-Type: application/json' \
        -d '{
        "model": "wan2.5-t2i-preview",
        "input": {
            "prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"
        },
        "parameters": {
            "size": "1024*1024",
            "n": 1
        }
    }'
    {"request_id":"ca3b5224-bc60-4e47-80f4-2790040e9e55","output":{"task_id":"2de3f7e1-52ce-4cf4-a466-f2d318061c43","task_status":"PENDING"}}
    ```
    

### **步骤2：根据task\_id查询结果**

-   将以下命令中的 `{task_id}` 替换为步骤 1 中获取的任务 ID，复制命令到终端并执行。
    
    > 以下为北京地域的base\_url，不同地域需配置对应的 base\_url。
    
    ```
    curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
    
-   当任务处理完成（`task_status` 为 `SUCCEEDED`）时，响应中将包含图像URL。图像URL有效期为**24小时**，请及时下载。
    
    > 由于模型处理时间较长（十几秒到几分钟不等），您可能需要轮询本接口。建议每隔3-5秒查询一次，直到 `task_status` 不为 `RUNNING`。
    
    ```
    curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/2de3f7e1-52ce-4cf4-a466-f2d3f8061c43 \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
    {"request_id":"24143559-9964-4898-8f9c-d968bba182b9","output":{"task_id":"2de3f7e1-52ce-4cf4-a466-f2d3f8061c43","task_status":"SUCCEEDED","submit_time":"2025-12-03 10:19:18.293","scheduled_time":"2025-12-03 10:19:18.320","end_time":"2025-12-03 10:19:31.890","results":[{"orig_prompt":"一间有着精致窗户的花店，漂亮的木质门，摆放着花朵","actual_prompt":"一间温馨雅致的花店，外墙装饰着精致的雕花窗户，窗框为深褐色木质结构，玻璃洁净透亮，透出店内柔和的光线。花店正门是一扇漂亮的实木门，表面保留天然木纹，配以黄铜门把手和复古门牌，散发出浓厚的手工艺气息。门前台阶两侧和店内窗台、门口区域错落有致地摆放着各式鲜花——有盛开的玫瑰、淡雅的绣球、清新的雏菊和翠绿的尤加利叶，色彩丰富而和谐。背景为宁静的欧洲小镇街景，石板路与爬满藤蔓的邻墙烘托出浪漫氛围。整体画面采用写实摄影风格，光线柔和自然，突出木质纹理与花卉细节。","url":"https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/1d/59/20251203/7a2bee47/2de3f7e1-52ce-4cf4-a466-f2d3f8061c43.png?Expires=1764814771&OSSAccessKeyId=xxx"}],"task_metrics":{"TOTAL":1,"FAILED":0,"SUCCEEDED":1}},"usage":{"image_count":1}}
    ```
    

## **下一步**

成功生成第一张图片后，您还可进行以下探索：

-   **深入了解API参数**：查看[文生图API](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)，了解更多输入输出参数。
    
-   **体验视频生成**：调用[首帧生视频API](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)，体验动态视频创作。
    
-   **浏览更多模型**：访问百炼控制台，查看阿里云百炼支持的所有图像/视频模型。
    
-   **在线体验**：前往[万相官网](https://tongyi.aliyun.com/wanxiang/creation)，在线体验更丰富的图像和视频生成功能。
    
    **说明**
    
    **关于官网与API的说明**
    
    -   万相官网的功能与 API 支持的能力可能存在差异，业务集成请以 API 文档为准。
        
    -   部分模型可能仅支持通过 API 调用，无法在官网在线体验。
