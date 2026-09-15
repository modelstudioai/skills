# 人像风格重绘

人像风格重绘模型可以将您提供的人物照片，转换为多种预设或自定义的艺术风格。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 模型概览

**模型名称**

**计费单价**

**限流（主账号与RAM子账号共享）**

**免费额度**[（查看）](raw/model-user-guide/test-1/new-free-quota.md)

**任务下发接口QPS限制**

**同时处理中任务数量**

wanx-style-repaint-v1

0.12元/张

2

1

500张

## 快速开始

#### 前提条件

您需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

#### 示例代码

本模型**仅提供 HTTP API**，请参考curl示例代码。

#### curl

**说明**HTTP调用新手指南请参见[Postman](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

由于图像生成耗时较长，API 采用异步模式，调用流程分两步：

##### 步骤1：创建任务获取任务ID

此接口将返回唯一的任务ID（task\_id）。

**请求示例**

#### 使用预置风格

设置style\_index（不能设为-1）。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wanx-style-repaint-v1",
    "input": {
        "image_url": "https://vigen-video.oss-cn-shanghai.aliyuncs.com/demo_image/image_demo_input.png",
        "style_index": 3
    }
}'
```

#### 使用自定义风格

设置style\_ref\_url（风格参考图），并将 style\_index 设为 -1。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wanx-style-repaint-v1",
    "input": {
        "image_url": "https://vigen-video.oss-cn-shanghai.aliyuncs.com/demo_image/input_example.png",
        "style_ref_url": "https://vigen-video.oss-cn-shanghai.aliyuncs.com/demo_image/style_example.png",
        "style_index": -1
    }
}'
```

**响应示例**

`task_id`查询有效期为24小时。

```
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

##### 步骤2：查询任务结果

使用 `task_id` 轮询任务状态，直至完成并获取生成的图像URL。

**请求示例**

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```
**响应示例**

> 图像URL有效期为24小时，请及时下载图像。

```
{
    "request_id": "f7fee4f1-1f68-9f17-85df-xxxxx",
    "output": {
        "task_id": "316c7af0-e91f-476f-99bd-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-08-12 10:55:43.768",
        "scheduled_time": "2025-08-12 10:55:43.799",
        "end_time": "2025-08-12 10:55:48",
        "error_message": "Success",
        "start_time": "2025-08-12 10:55:43",
        "style_index": 0,
        "error_code": 0,
        "results": [
            {
                "url": "http://oss.aliyuncs.com/xxx/abc.jpg"
            }
        ]
    },
    "usage": {
        "image_count": 1
    }
}
```

#### Python

**说明**

-   如需集成至现有项目，需自行实现对应语言的 HTTP 调用逻辑，如 Python、Java、Node.js 等。
-   本文仅提供 Python 示例（非官方 SDK，仅为基于 HTTP 的调用实现参考）。

**环境配置**

-   推荐使用Python 3.9及以上版本。
-   请安装必要的依赖包。

```
pip install -U requests
```
**请求示例**
```
import os
import requests
import time
from http import HTTPStatus

# 从环境变量获取阿里云百炼API Key，或直接在代码中赋值
api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    raise ValueError("请设置环境变量 DASHSCOPE_API_KEY")

def submit_task():
    """提交一个风格重绘任务"""
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"  # 异步调用
    }

    # --- 使用预置风格 ---
    # style_index: 0=复古漫画, 1=3D童话, 2=二次元, 3=小清新, 4=未来科技...
    body = {
        "model": "wanx-style-repaint-v1",
        "input": {
            "image_url": "https://vigen-video.oss-cn-shanghai.aliyuncs.com/demo_image/image_demo_input.png",
            "style_index": 3  # 示例：选择“小清新”风格
        }
    }

    # --- 使用自定义风格 ---
    # body = {
    #     "model": "wanx-style-repaint-v1",
    #     "input": {
    #         "image_url": "https://vigen-video.oss-cn-shanghai.aliyuncs.com/demo_image/input_example.png",
    #         "style_ref_url": "https://vigen-video.oss-cn-shanghai.aliyuncs.com/demo_image/style_example.png",
    #         "style_index": -1
    #     }
    # }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == HTTPStatus.OK:
        task_id = response.json().get('output', {}).get('task_id')
        print(f"任务提交成功，任务ID为: {task_id}")
        return task_id
    else:
        print(f"任务提交失败，状态码: {response.status_code}, 响应: {response.text}")
        return None

def query_task_result(task_id):
    """根据任务ID轮询查询结果"""
    if not task_id:
        return

    url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    print("开始查询任务状态...")
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code != HTTPStatus.OK:
            print(f"查询失败，状态码: {response.status_code}, 响应: {response.text}")
            break

        response_data = response.json()
        task_status = response_data.get('output', {}).get('task_status')

        if task_status == 'SUCCEEDED':
            print("任务成功完成！")
            print(f"任务成功响应数据: {response_data}")
            results = response_data.get('output', {}).get('results', [])
            for i, result in enumerate(results):
                print(f"生成图片_{i + 1} URL: {result.get('url')}")
            break
        elif task_status == 'FAILED':
            print(f"任务失败。错误信息: {response_data}")
            break
        else:
            print(f"任务正在处理中，当前状态: {task_status}...")
            time.sleep(5)  # 等待5秒后再次查询

if __name__ == '__main__':
    task_id = submit_task()
    if task_id:
        query_task_result(task_id)
```
**响应示例**
```
任务提交成功，任务ID为: b6496481-4fdc-476b-b20f-xxxxxx
开始查询任务状态...
任务正在处理中，当前状态: RUNNING...
任务成功完成！
任务成功响应数据: {'request_id': 'ec3a682b-4d67-96f2-937d-xxxxxx', 'output': {'task_id': 'b6496481-4fdc-476b-b20f-xxxxxx', 'task_status': 'SUCCEEDED', 'submit_time': '2025-08-12 17:52:56.439', 'scheduled_time': '2025-08-12 17:52:56.466', 'end_time': '2025-08-12 17:53:01', 'error_message': 'Success', 'start_time': '2025-08-12 17:52:56', 'style_index': 3, 'error_code': 0, 'results': [{'url': 'https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/1d/e0/20250812/b1be3297/20250812175256936406_style3_w52l3kpz6i.jpg?Expires=xxxx'}]}, 'usage': {'image_count': 1}}
  生成图片_1 URL: https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/1d/e0/20250812/b1be3297/20250812175256936406_style3_w52l3kpz6i.jpg?Expires=xxxx
```

## 输入图像限制

#### 人物图像

-   图片分辨率：分辨率不小于`256*256`，不超过`5760*3240`。长短边比例不超过 2:1。
    
-   图片质量：确保生成质量，请上传脸部清晰照片，人脸比例不宜过小，并避免夸张姿势和表情。
    
-   图片格式：JPEG，PNG，JPG，BMP，WEBP。
    
-   图片大小：不超过10M。
    
-   图像URL：
    
    -   支持公网可访问的 HTTP/HTTPS 地址，URL 中不能包含中文字符；支持传入Base64编码字符串。
        
    -   对于本地文件，可通过以下两种方式获取合法参数值：
        
        -   获取URL：请参见[上传文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
        -   生成Base64编码字符串：请参见[图像Base64编码传值方式](https://help.aliyun.com/zh/model-studio/style-repaint#fa664addf5wph)。

#### 风格参考图

-   图片分辨率：分辨率不小于`256*256`，不超过`5760*3240`。为取得最佳效果，建议图像长短边比例不超过 2:1，否则可能影响生成或导致报错。
    
-   图片格式：JPEG，PNG，JPG，BMP，WEBP。
    
-   图片大小：不超过10M。
    
-   图像URL：
    
    -   支持公网可访问的 HTTP/HTTPS 地址，URL 中不能包含中文字符；支持传入Base64编码字符串。
        
    -   对于本地文件，可通过以下两种方式获取合法参数值：
        
        -   获取URL：请参见[上传文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
        -   生成Base64编码字符串：请参见[图像Base64编码传值方式](https://help.aliyun.com/zh/model-studio/style-repaint#fa664addf5wph)。

#### 图像Base64编码传值方式

将本地图片文件转换为 Base64 格式的字符串，并按格式拼接：`data:{MIME_type};base64,{base64_data}`。

-   {MIME\_type}：图像的媒体类型，需与文件格式对应。
    
-   {base64\_data}：图像文件经过 Base64 编码后的完整数据字符串。
    
-   图像格式与MIME 类型对应关系：
    
    图像格式
    
    MIME Type
    
    JPEG
    
    image/jpeg
    
    JPG
    
    image/jpeg
    
    PNG
    
    image/png
    
    BMP
    
    image/bmp
    
    WEBP
    
    image/webp
    
-   示例值：`"image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABDg......"`。
    
    注意：为便于展示，上述 Base64 字符串是截断的。在实际使用中，请务必传入完整的编码字符串。
    
-   示例代码：获取图像Base64编码字符串。
    

```
import base64
import mimetypes

# ---用于 Base64 编码 ---
# 格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

if __name__ == "__main__":
    print(encode_file("./image_demo_input.png"))
```

## 计费与限流

**计费规则**

-   计费项：按成功生成的 **图像张数** 计费，采用按量后付费模式。
    
-   计费公式：**费用 = 计费单价 × 图像张数**。
    
-   抵扣顺序：优先消耗免费额度。额度用尽后，默认转为按量付费。
    
    -   您可开启“免费额度用完即停”功能，以避免免费额度耗尽后产生额外费用。详情请参见[免费额度](raw/model-user-guide/test-1/new-free-quota.md)。
-   失败不计费：模型调用失败或处理错误不产生任何费用，也不消耗免费额度。
    

**免费额度**

关于免费额度的领取、查询、使用方法等详情，请参见[免费额度](raw/model-user-guide/test-1/new-free-quota.md)。

**调用量查询**

模型调用完约一小时后，请在[模型监控](https://bailian.console.aliyun.com/model/telemetry)页面，查看调用量、调用次数、成功率等指标。

**限流**

模型限流规则及常见问题，请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

## API参考

API的输入输出参数，请参见[人像风格重绘](raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)。

## 常见问题

##### Q: 如何处理本地图片？

A: 本API支持公网URL，支持 Base64 编码。若要使用本地文件，可通过以下两种方式获取合法参数值：

1.  获取URL：请将图片上传至对象存储（如阿里云OSS），或使用阿里云百炼提供的[临时存储](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
2.  生成Base64编码字符串：请参见[图像Base64编码传值方式](https://help.aliyun.com/zh/model-studio/style-repaint#fa664addf5wph)。

##### Q: 如何优化图片生成效果？

A: 好的输入决定了好的输出。请尝试以下方法：

-   提升人物照片质量：使用高清、光线好、五官清晰无遮挡的正面照。
-   挑选风格参考图：选择风格鲜明，且匹配人物主题的图片。

##### Q：预置风格和自定义风格可以同时使用吗？

A：不可以，两者互斥，需选择其中一种模式：

-   使用预置风格：请设置 style\_index（不为-1），枚举值请参见[人像风格重绘](raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)。
    
-   使用自定义风格：请提供风格参考图 URL（style\_ref\_url），并将 style\_index设置为 -1。
    
    > 若同时传入且未将 style\_index 设为 -1，系统可能默认采用预置风格，导致自定义风格不生效。
    

**Q：输出图像的尺寸是否与输入图像一致？**

A：**不一致。** 输出图像会保持输入图像的宽高比，但会将短边固定为 1536 像素，长边按比例缩放。
