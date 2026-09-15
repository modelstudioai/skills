# 图像编辑-万相2.5至2.7

万相图像编辑模型系列支持多图输入与多图输出，通过文本指令实现图像编辑、多图融合、主体特征保持、目标检测与分割等能力。

## 快速开始

本示例将演示如何使用`wan2.7-image-pro`模型，基于2张输入图片和提示词生成编辑后的图像。

> 提示词：把图2的涂鸦喷绘在图1的汽车上

**输入图像1**

**输入图像2**

**输出图像（wan2.7-image-pro）**

![umbrella](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039710.webp)

![input2](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039712.webp)

![1774509357\_902b1408-2026-03-30-16-12-31](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1063463.webp)

在调用前，先[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如需通过SDK进行调用，请[安装DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)。

#### 同步调用

**重要****请确保 DashScope Python SDK 版本不低于**`1.25.15`**， DashScope Java SDK 版本不低于**`2.22.13`**。**

#### Python

### 请求示例

```
import os
import base64
import mimetypes
import urllib.request
import dashscope
from dashscope.aigc.image_generation import ImageGeneration
from dashscope.api_entities.dashscope_response import Message

# 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# --- Base64编码函数 ---
# base64编码格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明：
以下提供了三种图片输入方式，三选一即可
1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""
# 【方式一】使用公网图片 URL
image_1 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"
image_2 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# image_1 = "file:///path/to/your/car.png"
# image_2 = "file:///path/to/your/paint.png"

# 【方式三】使用Base64编码的图片
# image_1 = encode_file("/path/to/your/car.png")
# image_2 = encode_file("/path/to/your/paint.png")

message = Message(
    role="user",
    content=[
        {"text": "把图2的涂鸦喷绘在图1的汽车上"},
        {"image": image_1},
        {"image": image_2},
    ],
)
print("----sync call, please wait a moment----")
rsp = ImageGeneration.call(
    model="wan2.7-image-pro",
    api_key=api_key,
    messages=[message],
    watermark=False,
    n=1,
    size="2K",  # wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
)

# 提取结果图片URL并保存到本地
if rsp.status_code == 200:
    for i, choice in enumerate(rsp.output.choices):
        for j, content in enumerate(choice["message"]["content"]):
            if content.get("type") == "image":
                image_url = content["image"]
                file_name = f"output_{i}_{j}.png"
                # 结果URL有效期为24小时，请及时下载
                urllib.request.urlretrieve(image_url, file_name)
                print(f"Image saved to {file_name}")
else:
    print(f"Failed: status_code={rsp.status_code}, message={rsp.message}")
```

### 响应示例

> URL 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "81d868c6-6ce1-92d8-a90d-d2ee71xxxxxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "audio": null,
        "finished": true
    },
    "usage": {
        "input_tokens": 18790,
        "output_tokens": 2,
        "characters": 0,
        "image_count": 1,
        "size": "2985*1405",
        "total_tokens": 18792
    }
}
```

#### Java

### 请求示例

```
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * wan2.7-image-pro 图像编辑 - 同步调用示例
 */
public class Main {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // --- Base64编码函数 ---
    // base64编码格式为 data:{MIME_type};base64,{base64_data}
    public static String encodeFile(String filePath) throws IOException {
        byte[] fileContent = Files.readAllBytes(Paths.get(filePath));
        String base64String = Base64.getEncoder().encodeToString(fileContent);
        String mimeType = Files.probeContentType(Paths.get(filePath));
        return "data:" + mimeType + ";base64," + base64String;
    }

    public static void basicCall() throws ApiException, NoApiKeyException, UploadFileException, IOException {
        /*
         * 图像输入方式说明：
         * 以下提供了三种图片输入方式，三选一即可
         * 1. 使用公网URL - 适合已有公开可访问的图片
         * 2. 使用本地文件 - 适合本地开发测试
         * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
         */
        // 【方式一】使用公网图片 URL
        String image1 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp";
        String image2 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp";

        // 【方式二】使用本地文件（支持绝对路径和相对路径）
        // 格式要求：file:// + 文件路径
        // String image1 = "file:///path/to/your/car.png";
        // String image2 = "file:///path/to/your/paint.png";

        // 【方式三】使用Base64编码的图片
        // String image1 = encodeFile("/path/to/your/car.png");
        // String image2 = encodeFile("/path/to/your/paint.png");

        // 构建多图输入消息
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Arrays.asList(
                        // 支持多图输入，可以提供多张参考图片
                        Collections.singletonMap("text", "把图2的涂鸦喷绘在图1的汽车上"),
                        Collections.singletonMap("image", image1),
                        Collections.singletonMap("image", image2)
                )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.7-image-pro")
                .messages(Collections.singletonList(message))
                .n(1)
                .size("2K") // wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = null;
        try {
            System.out.println("---sync call for image editing, please wait a moment----");
            result = imageGeneration.call(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        // 提取结果图片URL并保存到本地
        for (int i = 0; i < result.getOutput().getChoices().size(); i++) {
            List<Map<String, Object>> contents = result.getOutput().getChoices().get(i)
                    .getMessage().getContent();
            for (int j = 0; j < contents.size(); j++) {
                if ("image".equals(contents.get(j).get("type"))) {
                    String imageUrl = (String) contents.get(j).get("image");
                    String fileName = "output_" + i + "_" + j + ".png";
                    // 结果URL有效期为24小时，请及时下载
                    try (InputStream in = new URL(imageUrl).openStream()) {
                        Files.copy(in, Paths.get(fileName), StandardCopyOption.REPLACE_EXISTING);
                    }
                    System.out.println("Image saved to " + fileName);
                }
            }
        }
    }

    public static void main(String[] args) throws ApiException, NoApiKeyException, UploadFileException, IOException {
        basicCall();
    }
}
```

### 响应示例

> URL 有效期24小时，请及时下载并保存图像。

```
{
    "requestId": "1bf6173a-e8de-9f75-94d3-5e618f875xxx",
    "usage": {
        "input_tokens": 18790,
        "output_tokens": 2,
        "total_tokens": 18792,
        "image_count": 1,
        "size": "2985*1405"
    },
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "finished": true
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

#### curl

##### 请求示例

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"},
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"},
                    {"text": "把图2的涂鸦喷绘在图1的汽车上"}
                ]
            }
        ]
    },
    "parameters": {
        "size": "2K",
        "n": 1,
        "watermark": false
    }
}'
```

##### 响应示例

```
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "content": [
                        {
                            "image": "https://dashscope-xxx.oss-xxx.aliyuncs.com/xxx.png?Expires=xxx",
                            "type": "image"
                        }
                    ],
                    "role": "assistant"
                }
            }
        ],
        "finished": true
    },
    "usage": {
        "image_count": 1,
        "input_tokens": 10867,
        "output_tokens": 2,
        "size": "1488*704",
        "total_tokens": 10869
    },
    "request_id": "71dfc3c6-f796-9972-97e4-bc4efc4faxxx"
}
```

#### 异步调用

**重要****请确保 DashScope Python SDK 版本不低于**`1.25.15`**， DashScope Java SDK 版本不低于**`2.22.13`**。**

#### Python

### 请求示例

```
import os
import base64
import mimetypes
import urllib.request
import dashscope
from dashscope.aigc.image_generation import ImageGeneration
from dashscope.api_entities.dashscope_response import Message
from http import HTTPStatus

# 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# --- Base64编码函数 ---
# base64编码格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明：
以下提供了三种图片输入方式，三选一即可
1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""
# 【方式一】使用公网图片 URL
image_1 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"
image_2 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# image_1 = "file:///path/to/your/car.png"
# image_2 = "file:///path/to/your/paint.png"

# 【方式三】使用Base64编码的图片
# image_1 = encode_file("/path/to/your/car.png")
# image_2 = encode_file("/path/to/your/paint.png")

# 创建异步任务
def create_async_task():
    print("Creating async task...")
    message = Message(
        role="user",
        content=[
            {"text": "把图2的涂鸦喷绘在图1的汽车上"},
            {"image": image_1},
            {"image": image_2},
        ],
    )
    response = ImageGeneration.async_call(
        model="wan2.7-image-pro",
        api_key=api_key,
        messages=[message],
        watermark=False,
        n=1,
        size="2K",  # wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
    )

    if response.status_code == 200:
        print("Task created successfully:", response)
        return response
    else:
        raise Exception(f"Failed to create task: {response.code} - {response.message}")

# 等待任务完成
def wait_for_completion(task_response):
    print("Waiting for task completion...")
    status = ImageGeneration.wait(task=task_response, api_key=api_key)

    if status.output.task_status == "SUCCEEDED":
        print("Task succeeded!")
        # 提取结果图片URL并保存到本地
        for i, choice in enumerate(status.output.choices):
            for j, content in enumerate(choice["message"]["content"]):
                if content.get("type") == "image":
                    image_url = content["image"]
                    file_name = f"output_{i}_{j}.png"
                    # 结果URL有效期为24小时，请及时下载
                    urllib.request.urlretrieve(image_url, file_name)
                    print(f"Image saved to {file_name}")
    else:
        raise Exception(f"Task failed with status: {status.output.task_status}")

# 获取异步任务信息
def fetch_task_status(task):
    print("Fetching task status...")
    status = ImageGeneration.fetch(task=task, api_key=api_key)

    if status.status_code == HTTPStatus.OK:
        print("Task status:", status.output.task_status)
        print("Response details:", status)
    else:
        print(f"Failed to fetch status: {status.code} - {status.message}")

# 取消异步任务
def cancel_task(task):
    print("Canceling task...")
    response = ImageGeneration.cancel(task=task, api_key=api_key)

    if response.status_code == HTTPStatus.OK:
        print("Task canceled successfully:", response.output.task_status)
    else:
        print(f"Failed to cancel task: {response.code} - {response.message}")

# 主执行流程
if __name__ == "__main__":
    task = create_async_task()
    wait_for_completion(task)
```

### 响应示例

1、创建任务的响应示例

```
{
    "status_code": 200,
    "request_id": "4fb3050f-de57-4a24-84ff-e37ee5xxxxxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": null,
        "audio": null,
        "task_id": "127ec645-118f-4884-955d-0eba8dxxxxxx",
        "task_status": "PENDING"
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "characters": 0
    }
}
```

2、查询任务结果的响应示例

> URL 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "3b99aae5-d26f-9059-8dd0-ee9ca4804xxx",
    "code": null,
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "audio": null,
        "task_id": "127ec645-118f-4884-955d-0eba8dxxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-03-31 22:58:47.646",
        "scheduled_time": "2026-03-31 22:58:47.683",
        "end_time": "2026-03-31 22:58:59.642",
        "finished": true
    },
    "usage": {
        "input_tokens": 18711,
        "output_tokens": 2,
        "characters": 0,
        "size": "2985*1405",
        "total_tokens": 18713,
        "image_count": 1
    }
}
```

#### Java

### 请求示例

```
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * wan2.7-image-pro 图像编辑 - 异步调用示例
 */
public class Main {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // --- Base64编码函数 ---
    // base64编码格式为 data:{MIME_type};base64,{base64_data}
    public static String encodeFile(String filePath) throws IOException {
        byte[] fileContent = Files.readAllBytes(Paths.get(filePath));
        String base64String = Base64.getEncoder().encodeToString(fileContent);
        String mimeType = Files.probeContentType(Paths.get(filePath));
        return "data:" + mimeType + ";base64," + base64String;
    }

    public static void asyncCall() throws ApiException, NoApiKeyException, UploadFileException, IOException {
        /*
         * 图像输入方式说明：
         * 以下提供了三种图片输入方式，三选一即可
         * 1. 使用公网URL - 适合已有公开可访问的图片
         * 2. 使用本地文件 - 适合本地开发测试
         * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
         */
        // 【方式一】使用公网图片 URL
        String image1 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp";
        String image2 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp";

        // 【方式二】使用本地文件（支持绝对路径和相对路径）
        // 格式要求：file:// + 文件路径
        // String image1 = "file:///path/to/your/car.png";
        // String image2 = "file:///path/to/your/paint.png";

        // 【方式三】使用Base64编码的图片
        // String image1 = encodeFile("/path/to/your/car.png");
        // String image2 = encodeFile("/path/to/your/paint.png");

        // 构建多图输入消息
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Arrays.asList(
                        // 支持多图输入，可以提供多张参考图片
                        Collections.singletonMap("text", "把图2的涂鸦喷绘在图1的汽车上"),
                        Collections.singletonMap("image", image1),
                        Collections.singletonMap("image", image2)
                )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.7-image-pro")
                .n(1)
                .size("2K") // wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
                .messages(Arrays.asList(message))
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = null;
        try {
            System.out.println("---async call for image editing, creating task----");
            result = imageGeneration.asyncCall(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        System.out.println("任务创建结果:");
        System.out.println(JsonUtils.toJson(result));

        String taskId = result.getOutput().getTaskId();
        // 等待任务完成
        waitTask(taskId);
    }

    public static void waitTask(String taskId) throws ApiException, NoApiKeyException, IOException {
        ImageGeneration imageGeneration = new ImageGeneration();
        System.out.println("\n---waiting for task completion----");
        ImageGenerationResult result = imageGeneration.wait(taskId, apiKey);
        // 提取结果图片URL并保存到本地
        for (int i = 0; i < result.getOutput().getChoices().size(); i++) {
            List<Map<String, Object>> contents = result.getOutput().getChoices().get(i)
                    .getMessage().getContent();
            for (int j = 0; j < contents.size(); j++) {
                if ("image".equals(contents.get(j).get("type"))) {
                    String imageUrl = (String) contents.get(j).get("image");
                    String fileName = "output_" + i + "_" + j + ".png";
                    // 结果URL有效期为24小时，请及时下载
                    try (InputStream in = new URL(imageUrl).openStream()) {
                        Files.copy(in, Paths.get(fileName), StandardCopyOption.REPLACE_EXISTING);
                    }
                    System.out.println("Image saved to " + fileName);
                }
            }
        }
    }

    public static void main(String[] args) throws ApiException, NoApiKeyException, UploadFileException, IOException {
        asyncCall();
    }
}
```

### 响应示例

1、创建任务的响应示例

```
{
    "requestId": "ccf4b2f4-bf30-9e13-9461-3a28c6a7bxxx",
    "output": {
        "task_id": "8811b4a4-00ac-4aa2-a2fd-017d3b90cxxx",
        "task_status": "PENDING"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

2、查询任务结果的响应示例

> URL 有效期24小时，请及时下载并保存图像。

```
{
    "requestId": "60a08540-f1c1-9e76-8cd3-d5949db8cxxx",
    "usage": {
        "input_tokens": 18711,
        "output_tokens": 2,
        "total_tokens": 18713,
        "image_count": 1,
        "size": "2985*1405"
    },
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "task_id": "8811b4a4-00ac-4aa2-a2fd-017d3b90cxxx",
        "task_status": "SUCCEEDED",
        "finished": true,
        "submit_time": "2026-03-31 19:57:58.840",
        "scheduled_time": "2026-03-31 19:57:58.877",
        "end_time": "2026-03-31 19:58:11.563"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

#### curl

### 步骤1：创建任务获取任务ID

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "X-DashScope-Async: enable" \
--data '{
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"},
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"},
                    {"text": "把图2的涂鸦喷绘在图1的汽车上"}
                ]
            }
        ]
    },
    "parameters": {
        "size": "2K",
        "n": 1,
        "watermark": false
    }
}'
```
**响应示例**
```
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

#### 步骤2：根据任务ID查询结果

使用上一步获取的 `task_id`，通过接口轮询任务状态，直到 `task_status` 变为 SUCCEEDED 或 FAILED。

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```
**响应示例**

> 图像URL有效期为24小时，请及时下载图像。

```
{
    "request_id": "810fa5f5-334c-91f3-aaa4-ed89cf0caxxx",
    "output": {
        "task_id": "a81ee7cb-014c-473d-b842-76e98311cxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-03-26 17:16:01.663",
        "scheduled_time": "2026-03-26 17:16:01.716",
        "end_time": "2026-03-26 17:16:22.961",
        "finished": true,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-xxx.oss-xxx.aliyuncs.com/xxx.png?Expires=xxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ]
    },
    "usage": {
        "size": "2976*1408",
        "total_tokens": 11017,
        "image_count": 1,
        "output_tokens": 2,
        "input_tokens": 11015
    }
}
```

wan2.5-i2i-preview使用不同的API端点和参数传入方式，其调用示例如下：

点击查看wan2.5-i2i-preview调用示例

#### 同步调用

**重要****请确保 DashScope Python SDK 版本不低于**`1.25.2`**， DashScope Java SDK 版本不低于**`2.22.2`**。**

若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装或升级SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

#### Python

本示例支持三种图像输入方式：**公网URL、Base64编码、本地文件路径**。

##### 请求示例

```
import base64
import mimetypes
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import dashscope
import requests
from dashscope import ImageSynthesis
import os

# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# --- 输入图片：使用 Base64 编码 ---
# base64编码格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明：
以下提供了三种图片输入方式，三选一即可

1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""

# 【方式一】使用公网图片 URL
image_url_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"
image_url_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# 格式要求：file:// + 文件路径
# 示例（绝对路径）：
# image_url_1 = "file://" + "/path/to/your/image_1.png"     # Linux/macOS
# image_url_2 = "file://" + "C:/path/to/your/image_2.png"  # Windows
# 示例（相对路径）：
# image_url_1 = "file://" + "./image_1.png"                 # 以实际路径为准
# image_url_2 = "file://" + "./image_1.png"                # 以实际路径为准

# 【方式三】使用Base64编码的图片
# image_url_1 = encode_file("./image_1.png")               # 以实际路径为准
# image_url_2 = encode_file("./image_2.png")              # 以实际路径为准

print('----sync call, please wait a moment----')
rsp = ImageSynthesis.call(api_key=api_key,
                          model="wan2.5-i2i-preview",
                          prompt="将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                          images=[image_url_1, image_url_2],
                          negative_prompt="",
                          n=1,
                          # size="1280*1280",
                          prompt_extend=True,
                          watermark=False,
                          seed=12345)
print('response: %s' % rsp)
if rsp.status_code == HTTPStatus.OK:
    # 在当前目录下保存图片
    for result in rsp.output.results:
        file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
        with open('./%s' % file_name, 'wb+') as f:
            f.write(requests.get(result.url).content)
else:
    print('sync_call Failed, status_code: %s, code: %s, message: %s' %
          (rsp.status_code, rsp.code, rsp.message))
```

##### 响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "8ad45834-4321-44ed-adf5-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "3aff9ebd-35fc-4339-98a3-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
                "orig_prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                "actual_prompt": "将图1中的蓝色闹钟放置在图2餐桌的花瓶右侧，靠近桌布边缘的位置，保持闹钟朝向镜头，与桌面平行，阴影自然投射于桌面。"
            }
        ],
        "submit_time": "2025-10-23 16:18:16.009",
        "scheduled_time": "2025-10-23 16:18:16.040",
        "end_time": "2025-10-23 16:19:09.591",
        "task_metrics": {
            "TOTAL": 1,
            "FAILED": 0,
            "SUCCEEDED": 1
        }
    },
    "usage": {
        "image_count": 1
    }
}
```

#### Java

本示例支持三种图像输入方式：公网URL、Base64编码、本地文件路径。

##### 请求示例

```
// Copyright (c) Alibaba, Inc. and its affiliates.
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

public class Image2Image {

    static {
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * 图像输入方式说明：三选一即可
     *
     * 1. 使用公网URL - 适合已有公开可访问的图片
     * 2. 使用本地文件 - 适合本地开发测试
     * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
     */

    //【方式一】公网URL
    static String imageUrl_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp";
    static String imageUrl_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp";

    //【方式二】本地文件路径（file://+绝对路径 or file:///+绝对路径）
    // static String imageUrl_1 = "file://" + "/your/path/to/image_1.png";    // Linux/macOS
    // static String imageUrl_2 = "file:///" + "C:/your/path/to/image_2.png";  // Windows

    //【方式三】Base64编码
    // static String imageUrl_1 = encodeFile("/your/path/to/image_1.png");
    // static String imageUrl_2 = encodeFile("/your/path/to/image_2.png");

    // 设置待编辑的图片列表
    static List<String> imageUrls = new ArrayList<>();
    static {
        imageUrls.add(imageUrl_1);
        imageUrls.add(imageUrl_2);
    }

    public static void syncCall() {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.5-i2i-preview")
                        .prompt("将图1中的闹钟放置到图2的餐桌的花瓶旁边位置")
                        .images(imageUrls)
                        .n(1)
                         //.size("1280*1280")
                        .negativePrompt("")
                        .parameters(parameters)
                        .build();

        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = imageSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
    }

    /**
     * 将文件编码为Base64字符串
     * @param filePath 文件路径
     * @return Base64字符串，格式为 data:{MIME_type};base64,{base64_data}
     */
    public static String encodeFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) {
            throw new IllegalArgumentException("文件不存在: " + filePath);
        }
        // 检测MIME类型
        String mimeType = null;
        try {
            mimeType = Files.probeContentType(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法检测文件类型: " + filePath);
        }
        if (mimeType == null || !mimeType.startsWith("image/")) {
            throw new IllegalArgumentException("不支持或无法识别的图像格式");
        }
        // 读取文件内容并编码
        byte[] fileBytes = null;
        try{
            fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法读取文件内容: " + filePath);
        }

        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
    }

    public static void main(String[] args) {
        syncCall();
    }
}
```

##### 响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "request_id": "d362685b-757f-4eac-bab5-xxxxxx",
    "output": {
        "task_id": "bfa7fc39-3d87-4fa7-b1e6-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "orig_prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                "actual_prompt": "将图1中的蓝色闹钟放置在图2餐桌的花瓶右侧，靠近桌布边缘的位置，保持闹钟正面朝向镜头，与花瓶平行摆放。",
                "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx"
            }
        ],
        "task_metrics": {
            "TOTAL": 1,
            "SUCCEEDED": 1,
            "FAILED": 0
        }
    },
    "usage": {
        "image_count": 1
    }
}
```

#### 异步调用

**重要****请确保 DashScope Python SDK 版本不低于**`1.25.2`**， DashScope Java SDK 版本不低于**`2.22.2`**。**

若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装或升级SDK](raw/model-api-reference/preparations/install-sdk.md)进行更新。

#### Python

本示例使用公网URL方式传入图片。

### 请求示例

```
import os
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import dashscope
import requests
from dashscope import ImageSynthesis

# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# 使用公网图片 URL
image_url_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"
image_url_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"

def async_call():
    print('----create task----')
    task_info = create_async_task()
    print('----wait task----')
    wait_async_task(task_info)

# 创建异步任务
def create_async_task():
    rsp = ImageSynthesis.async_call(api_key=api_key,
                                    model="wan2.5-i2i-preview",
                                    prompt="将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                                    images=[image_url_1, image_url_2],
                                    negative_prompt="",
                                    n=1,
                                    # size="1280*1280",
                                    prompt_extend=True,
                                    watermark=False,
                                    seed=12345)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))
    return rsp

# 等待异步任务结束
def wait_async_task(task):
    rsp = ImageSynthesis.wait(task=task, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        # save file to current directory
        for result in rsp.output.results:
            file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            with open('./%s' % file_name, 'wb+') as f:
                f.write(requests.get(result.url).content)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

# 获取异步任务信息
def fetch_task_status(task):
    status = ImageSynthesis.fetch(task=task, api_key=api_key)
    print(status)
    if status.status_code == HTTPStatus.OK:
        print(status.output.task_status)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (status.status_code, status.code, status.message))

# 取消异步任务，只有处于PENDING状态的任务才可以取消
def cancel_task(task):
    rsp = ImageSynthesis.cancel(task=task, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.task_status)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    async_call()
```

### 响应示例

1、创建任务的响应示例

```
{
	"status_code": 200,
	"request_id": "31b04171-011c-96bd-ac00-f0383b669cc7",
	"code": "",
	"message": "",
	"output": {
		"task_id": "4f90cf14-a34e-4eae-xxxxxxxx",
		"task_status": "PENDING",
		"results": []
	},
	"usage": null
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

```
{
    "status_code": 200,
    "request_id": "8ad45834-4321-44ed-adf5-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "3aff9ebd-35fc-4339-98a3-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
                "orig_prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                "actual_prompt": "将图1中的蓝色闹钟放置在图2餐桌的花瓶右侧，靠近桌布边缘的位置，保持闹钟朝向镜头，与桌面平行，阴影自然投射于桌面。"
            }
        ],
        "submit_time": "2025-10-23 16:18:16.009",
        "scheduled_time": "2025-10-23 16:18:16.040",
        "end_time": "2025-10-23 16:19:09.591",
        "task_metrics": {
            "TOTAL": 1,
            "FAILED": 0,
            "SUCCEEDED": 1
        }
    },
    "usage": {
        "image_count": 1
    }
}
```

#### Java

本示例默认使用公网URL方式传入图片。

### 请求示例

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisListResult;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.task.AsyncTaskListParam;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Image2Image {
    static {
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    //公网URL
    static String imageUrl_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp";
    static String imageUrl_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp";

    // 设置待编辑的图片列表
    static List<String> imageUrls = new ArrayList<>();
    static {
        imageUrls.add(imageUrl_1);
        imageUrls.add(imageUrl_2);
    }

    public static void asyncCall() {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.5-i2i-preview")
                        .prompt("将图1中的闹钟放置到图2的餐桌的花瓶旁边位置")
                        .images(imageUrls)
                        .n(1)
                        //.size("1280*1280")
                        .negativePrompt("")
                        .parameters(parameters)
                        .build();
        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            System.out.println("---async call, please wait a moment----");
            result = imageSynthesis.asyncCall(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }

        System.out.println(JsonUtils.toJson(result));

        String taskId = result.getOutput().getTaskId();

        System.out.println("taskId=" + taskId);

        try {
            result = imageSynthesis.wait(taskId, apiKey);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
        System.out.println(JsonUtils.toJson(result.getOutput()));
    }

    public static void listTask() throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        AsyncTaskListParam param = AsyncTaskListParam.builder().build();
        param.setApiKey(apiKey);
        ImageSynthesisListResult result = is.list(param);
        System.out.println(result);
    }

    public void fetchTask(String taskId) throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        // 如果已设置 DASHSCOPE_API_KEY 为环境变量，apiKey 可为空。
        ImageSynthesisResult result = is.fetch(taskId, apiKey);
        System.out.println(result.getOutput());
        System.out.println(result.getUsage());
    }

    public static void main(String[] args) {
        asyncCall();
    }
}
```

### 响应示例

1、创建任务的响应示例

```
{
	"request_id": "5dbf9dc5-4f4c-9605-85ea-542f97709ba8",
	"output": {
		"task_id": "7277e20e-aa01-4709-xxxxxxxx",
		"task_status": "PENDING"
	}
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图片。

```
{
    "request_id": "d362685b-757f-4eac-bab5-xxxxxx",
    "output": {
        "task_id": "bfa7fc39-3d87-4fa7-b1e6-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "orig_prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                "actual_prompt": "将图1中的蓝色闹钟放置在图2餐桌的花瓶右侧，靠近桌布边缘的位置，保持闹钟正面朝向镜头，与花瓶平行摆放。",
                "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx"
            }
        ],
        "task_metrics": {
            "TOTAL": 1,
            "SUCCEEDED": 1,
            "FAILED": 0
        }
    },
    "usage": {
        "image_count": 1
    }
}
```

#### curl

本示例包含创建任务和查询结果两个步骤。

**说明**

-   异步调用必须设置 Header 参数`X-DashScope-Async` 为`enable`。
-   异步任务的 `task_id` 查询有效期为 24 小时，过期后任务状态将变为 `UNKNOWN`。
-   新手建议使用 [Postman](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)调用API。

#### 步骤1：发起创建任务请求

该请求会返回一个任务ID（`task_id`）。

##### 请求示例

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.5-i2i-preview",
    "input": {
        "prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
        "images": [
            "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp",
            "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"
        ]
    },
    "parameters": {
        "n": 1
    }
}'
```
**响应示例**
```
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

#### 步骤2：根据任务ID查询结果

使用上一步获取的 `task_id`，通过接口轮询任务状态，直到 `task_status` 变为 SUCCEEDED 或 FAILED。

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
    "request_id": "d1f2a1be-9c58-48af-b43f-xxxxxx",
    "output": {
        "task_id": "7f4836cd-1c47-41b3-b3a4-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-09-23 22:14:10.800",
        "scheduled_time": "2025-09-23 22:14:10.825",
        "end_time": "2025-09-23 22:15:23.456",
        "results": [
            {
                "orig_prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx"
            }
        ],
        "task_metrics": {
            "TOTAL": 1,
            "FAILED": 0,
            "SUCCEEDED": 1
        }
    },
    "usage": {
        "image_count": 1
    }
}
```

## 模型选型

-   **wan2.7-image-pro、wan2.7-image**（推荐）：适合对编辑精度要求高、或需要生成多张内容连贯图像的场景。
    
    -   [精准局部编辑](https://help.aliyun.com/zh/model-studio/wan-image-edit#f257e128e517d)：框选图中指定区域，对该区域的对象进行移动、替换或添加新元素，适用于电商修图、设计稿调整
    -   多格连续图生成：一次输出多张风格统一的图像，适用于漫画分镜、产品系列图、故事连环图
-   wan2.6-image：适合图文混排或带多张参考图的风格化编辑场景，支持在生成图像时生成对应文字内容，最多支持 4 张参考图输入。
    
-   wan2.5-i2i-preview：适合简单的图像编辑和多图融合。
    

各模型的输入和输出规格见[输入图像规格](https://help.aliyun.com/zh/model-studio/wan-image-edit#title-input-images)、[输出图像分辨率](https://help.aliyun.com/zh/model-studio/wan-image-edit#ebc41fe492cyx)。

## 效果展示

### 图生组图

**输入图像**

**输出图像**

![Wan\_图片生成\_一位 20 岁的东亚男性，头发是卷卷的半长发，文艺气质，五官立体，眉眼清秀，穿着简约白色 T 恤或浅蓝色衬衫，少年感，自然气质。-2026-03-31-19-26-24](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1064359.webp)

![output](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1064360.webp)

![wan\_image\_reqid\_57d7a71c-1932-4de8-8c32-be0f3fd5696f\_n1-2026-03-31-19-32-44](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1064362.webp)

![output](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1064361.webp)

点击查看提示词

案例1：摄影写真

```
基础人物设定：一位 20 岁的东亚男性，头发是卷卷的半长发，文艺气质，五官立体，眉眼清秀，穿着简约白色 T 恤或浅蓝色衬衫，少年感，自然气质。
1. 民国文人风 (Republic Era Scholar)
提示词：
[基础面部描述] 人物形象为参考图1，身穿深青色长衫，佩戴圆框金丝眼镜，手持一把折扇，背景是老旧的上海书房，木质书架，暖黄色调，复古胶片质感，柔和的侧光，尘埃在光束中飞舞，文化气息，沉静内敛，哈苏中画幅，85mm 镜头，高分辨率，电影感调色，王家卫风格。
道具： 折扇 / 线装书 / 圆框眼镜
色调： 暖黄 / 深青 / sepia
2. 英伦绅士风 (British Gentleman)
提示词：
[基础面部描述] 人物形象为参考图1，穿着深灰色粗花呢西装三件套，佩戴复古机械腕表，手持高脚红酒杯，并看向酒杯，背景是古典图书馆或私人俱乐部，深色皮革沙发，伦勃朗光，暗调氛围，优雅高贵，冷峻眼神，细节丰富，纹理清晰，英国贵族气质，8k 分辨率，时尚杂志大片。
道具： 红酒杯 / 烟斗 / 机械表
色调： 深灰 / 酒红 / 暗金
3. 90s 港风复古 (90s HK Retro)
提示词：
[基础面部描述] 人物形象为参考图1，穿着水洗牛仔夹克或花衬衫，头发微乱，双手抱胸，背景是夜晚的霓虹灯牌街道，模糊的光斑，高颗粒感，色彩浓郁，红蓝撞色，王家卫风格，情绪化，迷离眼神，闪光灯直出效果，怀旧氛围，【全身镜头】。
色调： 霓虹红 / 深蓝 / 胶片绿
4. 新中式禅意 (New Chinese Zen)
提示词：
[基础面部描述]人物形象为参考图1，人物淡淡露齿笑， 穿着改良式白色中式立领上衣，手持折枝梅花，背景是极简的留白墙面或竹林，阳光洒在墙面上留下斑驳光影，清冷色调，宁静致远，东方美学，皮肤通透，高颗粒感，哑光，构图简洁，光影层次丰富，高端摄影，禅意氛围。
道具： 梅花枝
色调： 白 / 墨绿 / 浅灰
5. 复古艺术家 (Vintage Artist)
提示词：
[基础面部描述] 人物形象为参考图1，穿着沾有颜料的白色衬衫，系着棕色皮围裙，手持画笔或调色板，背景是干净的工作室，光线明亮，色彩斑斓的光影，专注的神情，看向手中颜料，不看镜头，头发略显凌乱，艺术气息，印象派色调，质感强烈。
道具： 画笔 / 调色板 / 素描本
色调： 暖光 / 多彩颜料 / 棕色
6. 经典黑白电影 (Classic Noir B&W)
提示词：
[基础面部描述] 人物形象为参考图1，穿着黑色高领毛衣，手持一根香烟，戴着黑色礼帽，背景是阴影交错的楼梯或走廊，高对比度黑白摄影，硬光照明，强烈的阴影，神秘感，冷硬派侦探风格，面部轮廓分明，皮肤纹理极致清晰，经典电影剧照，永恒感，侧脸特写，艺术摄影。
道具： 手杖 / 礼帽 / 墨镜
色调： 黑白 / 高对比度
```

案例2：视觉设计

```
图1：一张商业级产品摄影主视觉封面图，正视全景构图，一款复古未来主义风格的无线头戴式耳机悬浮于几何石膏体之上，耳机呈现完全对称美学，材质为香槟金金属与奶油白外壳，背景为深度虚化的温暖室内光影，光线柔和地勾勒出产品轮廓，画面留白处具有极强的呼吸感，营造静谧的听觉暗示，8k超高清分辨率，极简高级感。
图2：100mm微距镜头拍摄的产品材质特写，极近距离聚焦于耳机的伸缩臂连接处，清晰展示香槟金拉丝铝合金的金属纹理与CNC精密精割倒角，一道锐利的侧逆光在金属边缘形成星芒高光，背景深暗以突出金属的工业精密感，画质极度锐利，无噪点。
图3：极近距离的微距材质特写，聚焦于摩卡色蛋白皮耳罩的表面，通过侧光展现皮革细腻的毛孔纹理、柔软的按压褶皱与透气孔细节，传达极致的亲肤佩戴舒适度与回弹感，光影层次丰富，色调温暖湿润，超高清微距摄影。
图4：艺术化的产品爆炸视图，将复古未来主义耳机的内部发声单元、降噪芯片、电池模块与外部的胡桃木装饰片、金属框架进行悬浮拆解展示，背景为深邃的科技蓝，内部元件呈现半透明的全息科技质感，强调内部精密工艺与现代科技的结合，高科技商业海报风格。
图5：35mm人文镜头拍摄的佩戴场景图，特写模特的下颌线与颈部，展示佩戴这款香槟金耳机时的完美贴合度，自然暖调夕阳光从侧后方射入形成轮廓光，发丝边缘透着金光，模特肤色呈现健康自然的质感，营造沉浸式听歌的松弛生活感，背景为模糊的居家环境。
图6：致敬建筑光影的静物摄影，将耳机放置于极简的灰色混凝土桌面上，午后阳光透过百叶窗投下条纹状的硬光影，光影切过哑光奶油白机身与香槟金框架，形成明暗强烈的几何构成，凸显机身的立体廓形与材质对比，冷暖色调对撞，极简主义构图。
图7：俯视平铺构图的色彩方案展示图，并排陈列该系列三款不同配色的耳机，分别为银白、黑金、蓝铜配色，背景为肌理感极强的灰色羊毛毡布，柔和顶光照明，强调CMF设计的多样性与材质的细腻触感，画面整洁有序，设计杂志风格。
图8：品牌生活方式的全家福静物摄影，复古未来主义耳机被收纳在配套的精致皮箱旁，桌面上摆放着黑胶唱片机、一张正在旋转的黑胶唱片与一杯冒着热气的咖啡，背景有暖色调的氛围灯渲染，深胡桃木色调为主，传递慢生活与高保真音质结合的品牌生活哲学，电影感叙事光影。
```

### 交互式编辑

**输入图像**

**输出图像**

![5eecdaf48460cde5f7fd58249809b192a118accde85283f275b8339e1c4c24831b75b38faadcd24bec177c308ebd5304463ca8e345548eb5f551b6ba01cd2c8d2d9b5606fa569ff7ba4077816ac9b801464f65aedbcf494f4fb4c8ed7016461c-combine](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1064355.webp)

![5eecdaf48460cde5f7fd58249809b192a118accde85283f275b8339e1c4c24831b75b38faadcd24bec177c308ebd530460436714d0283cee289325430893028097a53a8e5d630fb1c2d4c85d8cbb68a4387575c4b03700344fb4c8ed7016461c-2026-03-31-19-13-38](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1064356.webp)

将图1中框选的图案放置到图二中框选处

### 多图融合

**输入图像**

**输出图像**

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd5304e9d05d028a65a9ac270ee730e44b8c75c6634a9b9a7a70240d438b02b2f2153dc68966b442378d1d4fb4c8ed7016461c-combine](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039962.webp)

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd53044b9a1d72dee2f8507ee704b9cef3832907ff1182f52507c9bc4737520762d46a722e658f57cda6524fb4c8ed7016461c-2025-12-29-19-11-31](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039963.webp)

给图1的男生和图2的狗拍一张写真，男生搂着这只狗，人和狗都很开心，摄影棚柔和灯光，蓝色纹理背景

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd5304f060ec7a363e318af9bfaaa5e07be972cfc1ea4e21b47637fcdb2dfc53130c40a8efed5defc408a04fb4c8ed7016461c-combine](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039968.webp)

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd5304922cbdef3e3c42f83239de6d0f35a8b76f0e38934cc5170f7a908ec12140fb0af6590c72bcf1ba6f4fb4c8ed7016461c-2025-12-29-19-15-53](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039971.webp)

给图1的裙子按照图2鸟的颜色进行配色，充满艺术感，衣服款式不变，模特不变

### 主体特征保持

**输入图像**

**输出图像**

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd5304448a972b9f2ee7a7aadcc61495f4975a049f009e7721cbc833dc3a8005b1b026a54eaaec109d73484fb4c8ed7016461c-2025-12-29-20-00-21](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1040012.webp)

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd5304cc1b4a509823c5fb5e60999898811f8b51d7419220a118c9ff82110bc9525725a9ad7338f75985794fb4c8ed7016461c-2025-12-29-20-00-21](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1040013.webp)

请生成一套4宫格“季节变迁”主题的拍立得套图，共四张。每一张照片都是在同一个地点，公园里的一棵树下拍摄的，但分别展现了春夏秋冬四个季节的景象。人物的着装也需与季节相匹配，春天的薄外套、夏天的短袖、秋天的风衣、冬天的围巾和厚大衣。并将这组照片放在餐桌上。

### 检测和分割

**输入图像**

**输出图像**

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd5304b025e74206dc2cec5c2e587c3fe6fb135293836c9479220355470da15476dc934b26018061e9db0b4fb4c8ed7016461c-2025-12-29-19-54-33](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1040006.webp)

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd530451385eb561b49b0fe1f2169526b6a7e15bd78940def3c640c801511c349f6df35dceb72f4d3755f94fb4c8ed7016461c-2025-12-29-19-54-33](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1040007.webp)

检测图片中的笔记本电脑和闹钟，画框并标注“laptop”和“clock”

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd530440256f9add4113787af5d4f3a55469b38ef2422f018076640eb7cb552584c02ee729fcb23fec3bca4fb4c8ed7016461c-2025-12-29-19-54-33](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1040008.webp)

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd5304f0612d67f5c810ebef958385624ebd17323047aa5d00465d0e35257de5a2ea49d4b375d2e57693fa4fb4c8ed7016461c-2025-12-29-19-54-32](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1040009.webp)

分割图片中的玻璃杯

### 提取元素

**输入图像**

**输出图像**

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd53046b83761f1ab18c40e144f5db2b388e5f865ba9a5961d98b2710ce177c6a0f4baff63fe52259c44364fb4c8ed7016461c-2025-12-29-19-48-27](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1040000.webp)

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd53048e2a0d1d2805d92ba8d45a3bd1368528dd76f517b21ad1f545eb4097610838497cbdb5196da94ff54fb4c8ed7016461c-2025-12-29-19-48-27](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1040001.webp)

从上传照片中提取穿搭单品，将它们以平铺展示的方式排列在纯白背景上，保持真实细节与材质质感，时尚电商风格，适合服装展示。

### 文本编辑

**输入图像**

**输出图像**

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd530490f493eca22f34f0197173ddfdef17a04b34cb94813178b9d4eee36d246d3530a3e2fc6258cca0694fb4c8ed7016461c-2025-12-29-19-28-35](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039976.webp)

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd5304fe77776567f4ef79cb621289a6fdaa981f3364fe4c7c56265403b5d9d5ac43eaf5931f62db14952f4fb4c8ed7016461c-2025-12-29-19-28-35](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039977.webp)

去除全图水印

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd530476e971380812b1b9dbeac68272a27057175499fe84f0781c7b6fa6535f438c67f3556acc8c7324394fb4c8ed7016461c-2025-12-29-19-28-35](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039978.webp)

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd53047be52c6f41edecdefa77f0d93335d1492f1821b47dff7a1b08f60e99bdafcc84c31e3658fc593c904fb4c8ed7016461c-2025-12-29-19-28-35](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039979.webp)

用手在沙滩上随意的写上“Time for Holiday？”

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd5304fdb284f8d5c8ead814d11890da1a49411a6d9d41ad1bb2a4bf0b93d0bee5d792e8f5b419a3da9d534fb4c8ed7016461c-2025-12-29-19-28-34](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039980.webp)

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd5304df1c8787530497f4cc3bee0b84d3ba51d0353fceb8d0518ded6a25e8c0ddfec714f719154ac1c9354fb4c8ed7016461c-2025-12-29-19-28-34](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039981.webp)

把18改成29，把JUNE改成SEPTEMBER

### 镜头与视角编辑

**输入图像**

**输出图像**

![image (2)-2025-12-29-19-42-44](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039991.webp)

![image (3)-2025-12-29-19-42-44](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039992.webp)

保持人物的特征不变，生成正视图、侧视图和背视图

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd5304a53988b2efdd2fb6b95cb3b1b02701e6ff2c4902170b1ee230a9b4e3726a891c93646d68b821de294fb4c8ed7016461c-2025-12-29-19-42-43](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039995.webp)

![5eecdaf48460cde5544f9fac410016bc2fe4c1b4d23666c075b8339e1c4c24831b75b38faadcd24bec177c308ebd530428783dee341e41eb06234dfb75bd149d774f4850000123559a98bcd7ece97dc4a6c3cefa983ae8ac4fb4c8ed7016461c-2025-12-29-19-42-43](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9952205771/p1039996.webp)

用鱼眼镜头重新拍摄这张照片

## 输入说明

## 输入图像规格

**规格**

**wan2.7-image-pro、wan2.7-image**

**wan2.6-image**

**wan2.5-i2i-preview**

输入图像数量

0～9 张（0张对应文生图模式）

图像编辑 1～4 张 / 图文混排 0～1 张

1～3 张

图片格式

JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP

JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP

JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP

图片宽高范围

\[240, 8000\] 像素

\[240, 8000\] 像素

\[384, 5000\] 像素

文件大小

≤ 20MB

≤ 10MB

≤ 10MB

宽高比

\[1:8, 8:1\]

不限

\[1:4, 4:1\]

### 图像输入顺序

多图输入时，按照数组中的顺序定义图像顺序。因此，提示词引用的图像编号需要**与图像数组中的顺序一一对应**，例如：数组中的第一张图片为"图1"，第二张为"图2"，或者使用标记形式如"\[图1\]"、"\[图2\]"。

```
{
    "content": [
        {"text": "编辑指令，如：将图1中的闹钟放置到图2的餐桌的花瓶旁边位置"},
        {"image": "https://example.com/image1.png"},
        {"image": "https://example.com/image2.png"}
    ]
}
```

**输入图像**

**输出图像**

![image (19)-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8142593671/p1025838.webp)

图1

![image (20)-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7142593671/p1025839.webp)

图2

![04e0fc39-7ad6-41e0-9df9-1f69ac3ce825-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8142593671/p1021092.webp)

提示词：把图1移动到图2上

![36ed450d-bd54-4169-b13f-3d0f26d9d360-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8142593671/p1021093.webp)

提示词：把图2移动到图1上

### 图像传入方式

支持通过以下方式传入图像：

方式一：公网URL

-   提供一个公网可访问的图像地址，支持 HTTP 或 HTTPS 协议。
-   示例值：`https://xxxx/img.png`。
-   适用场景：图片已托管在对象存储（如OSS）或公开图床上。

方式二：Base64编码

将图像文件转换为 Base64 编码字符串，并按格式拼接：`data:{MIME_type};base64,{base64_data}`。

-   示例值：`data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABDg......`**（**因长度限制仅展示片段**）。**调用时，需传入完整字符串。
    
-   {base64\_data}：表示图像文件经过 Base64 编码后的字符串。
    
-   {MIME\_type}：表示图像的媒体类型，需与文件格式对应。
    
    **图像格式**
    
    **MIME Type**
    
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
    
-   适合场景：本地图片、私有图片或需要加密传输的场景。
    

代码示例：图像Base64编码

```
import os
import base64
import mimetypes

# 格式为 data:{mime_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

# 调用编码函数，请将 "/path/to/your/image.png" 替换为您的本地图片文件路径，否则无法运行
image = encode_file("/path/to/your/image.png")
```

方式三：本地文件路径（仅限SDK）

-   **Python SDK**：支持传入文件的**绝对路径和相对路径**。文件路径规则如下：
    
    **系统**
    
    **传入的文件路径**
    
    **示例（绝对路径）**
    
    **示例（相对路径）**
    
    Linux或macOS系统
    
    file://{文件的绝对路径或相对路径}
    
    file:///home/images/test.png
    
    file://./images/test.png
    
    Windows系统
    
    file://D:/images/test.png
    
    file://./images/test.png
    
-   **Java SDK**：仅支持传入文件的**绝对路径**。文件路径规则如下：
    
    **系统**
    
    **传入的文件路径**
    
    **示例（绝对路径）**
    
    Linux或macOS系统
    
    file://{文件的绝对路径}
    
    file:///home/images/test.png
    
    Windows系统
    
    file:///{文件的绝对路径}
    
    file:///D:/images/test.png
    
-   适用场景：适合在本地开发环境中快速测试。
    

## 关键能力

### 1\. 指令遵循（提示词）

参数：`messages.content.text`或`input.prompt`（必选）、`negative_prompt`（可选）。

-   **text \\ prompt（正向提示词）**：描述希望在画面中看到的内容、主体、场景、风格、光照和构图。
-   **negative\_prompt（反向提示词）**：描述不希望在画面中出现的内容，如“模糊”、“多余的手指”等。仅用于辅助优化生成质量。

**参数**

**wan2.7-image-pro、wan2.7-image**

**wan2.6-image**

**wan2.5-i2i-preview**

text

必选，最多5000字符

必选，最多2000字符

不支持

prompt

不支持

不支持

必选，最多2000字符

negative\_prompt

不支持

支持，最多500字符

支持，最多500字符

### 2\. 开启prompt智能改写

参数: `parameters.prompt_extend` (bool, **默认为 true**)。

此功能可自动扩展和优化较短的Prompt，提升输出图像效果。开启此功能会增加额外耗时。

实践建议：

-   建议开启：当输入 Prompt 较简洁或宽泛时，此功能可提升图像效果。
-   建议关闭：若需控制画面细节、或已提供详细描述，或对响应延迟敏感。请将参数 `prompt_extend` **显式设为**`false`。

**参数**

**wan2.7-image-pro、wan2.7-image**

**wan2.6-image**

**wan2.5-i2i-preview**

prompt\_extend

不支持

支持（仅图像编辑模式）

支持

### 3\. 设置输出图像分辨率

参数: `parameters.size` (string)，格式为 `"宽*高"`。

**重要**同名档位 `1K` 在不同模型中的定义不同：wan2.7 系列输出总像素接近 1024_1024，wan2.6-image 接近 1280_1280。切换模型时请注意输出分辨率的差异。

**参数**

**wan2.7-image-pro、wan2.7-image**

**wan2.6-image**

**wan2.5-i2i-preview**

size

**方式一：指定输出图片的分辨率（推荐）**

编辑模式（传入至少一张图片），可选的输出分辨率档位：`1K`、`2K`（默认）。

-   `1K`：输出总像素接近 1024\*1024，宽高比与最后一张输入图像一致。
-   `2K`：输出总像素接近 2048\*2048，宽高比与最后一张输入图像一致。

**方式二：指定生成图像的宽高像素值**

-   总像素在 \[768_768, 2048_2048\] 之间，宽高比范围为 \[1:8, 8:1\]。

> 仅文生图场景的wan2.7-image-pro支持4K分辨率

**方式一：参考输入图比例（推荐）**

编辑模式（`enable_interleave=false`），可选的输出分辨率档位：`1K`（默认）、`2K`。

-   `1K`：输出总像素接近 1280\*1280，宽高比与最后一张输入图像一致。
-   `2K`：输出总像素接近 2048\*2048，宽高比与最后一张输入图像一致。

**方式二：指定生成图像的宽高像素值**

-   总像素在 \[768_768, 2048_2048\] 之间，宽高比范围为 \[1:4, 4:1\]。

> 实际输出图像的像素值为接近指定值的16的倍数。

**仅支持指定生成图像的宽高像素值**

-   总像素在 \[768_768, 1280_1280\] 之间，宽高比范围为 \[1:4, 4:1\]。
-   若未指定`size`，系统将默认生成总像素为 `1280*1280` 的图像，宽高比与最后一张输入图像一致。

### 4\. 交互式精准编辑

参数 `parameters.bbox_list`，框选图中需要编辑的物品或位置，实现更准确的编辑效果，**仅wan2.7-image-pro、wan2.7-image支持**。

-   对应关系：列表长度必须与输入图片数量一致。若某张图片无需编辑，需要在对应位置传入空列表 `[]`。
-   坐标格式：`[x1, y1, x2, y2]`（左上角 x, 左上角 y, 右下角 x, 右下角 y），使用原图绝对像素坐标，左上角对应（0，0），x 轴向右，y 轴向下。若使用视觉模型（如 qwen3.6-plus）定位目标区域，其返回的是归一化坐标 \[0, 999\]，请先按下文辅助代码换算为绝对像素坐标后再传入。
-   数量限制：单张图片最多支持 2 个边界框。

示例：输入 3 张图片，其中第 2 张无框选，第 1 张有两个框选：

```
[
  [[0, 0, 12, 12], [25, 25, 100, 100]],
  [],
  [[10, 10, 50, 50]]
]
```

点击查看调用示例

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"image": "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"},
                    {"image": "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"},
                    {"text": "把图1的闹钟放在图2的框选的位置，保持场景和光线融合自然"}
                ]
            }
        ]
    },
    "parameters": {
        "bbox_list": [[],[[989, 515, 1138, 681]]],
        "size": "2K",
        "n": 1,
        "watermark": false
    }
}'
```

如何确定编辑区域坐标

**方法一：OpenCV 画框**

在图片上拖拽鼠标画框，精准直观：

```
# 安装依赖：pip install opencv-python
import cv2
import urllib.request

# 下载示例图片（替换为您自己的图片 URL 或本地路径）
image_url = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"
urllib.request.urlretrieve(image_url, "example.webp")

# 读取图片并弹出交互窗口
img = cv2.imread("example.webp")
# 在弹出的窗口中用鼠标拖拽画框，按 Enter 确认选区，按 Esc 取消
x, y, w, h = cv2.selectROI("Draw bounding box (Enter=confirm, Esc=cancel)", img)
cv2.destroyAllWindows()

# 将 OpenCV 返回的 (x, y, w, h) 转换为 bbox_list 所需的 [x1, y1, x2, y2] 格式
# 坐标系：原点在图片左上角，x 轴向右，y 轴向下，单位为像素
bbox = [x, y, x + w, y + h]
print(f"框选坐标: {bbox}")  # 将此坐标传入 parameters.bbox_list
```
**方法二：视觉理解模型**

通过 qwen3.6-plus 自动识别目标区域坐标，用自然语言描述目标即可获取坐标：

```
# 安装依赖：pip install dashscope pillow
import os
import json
from dashscope import MultiModalConversation
import dashscope
from PIL import Image
import urllib.request

dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

def get_bbox_list(image, prompt):
    """
    通过 qwen3.6-plus 识别图片中的目标区域，返回绝对像素坐标列表。

    Args:
        image: 图片 URL 或本地路径（本地路径格式为 "file:///absolute/path.png"）
        prompt: 自然语言描述，如 "咖啡杯"、"盘子里所有的水果"、"盘子正中间的水果"

    Returns:
        [[x1, y1, x2, y2], ...] 绝对像素坐标，可直接传入 bbox_list
    """
    # 将用户描述与返回格式指令拼接
    full_prompt = (
        prompt + "\n"
        "请根据以上描述，返回对应区域的坐标。\n"
        "最多返回2个区域，优先返回最匹配的目标。\n"
        "严格按照JSON二维列表格式返回：[[x1, y1, x2, y2], ...]\n"
        "每组坐标：[左上角x, 左上角y, 右下角x, 右下角y]\n"
        "坐标系以图片左上角为(0,0)，x轴向右，y轴向下。\n"
        "如果只有一个区域，也必须使用二维列表：[[x1, y1, x2, y2]]\n"
        "只返回JSON列表，不要返回其他任何内容。"
    )

    messages = [
        {'role': 'user',
         'content': [
             {'image': image},
             {'text': full_prompt}
         ]}
    ]

    response = MultiModalConversation.call(
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model='qwen3.6-plus',
        messages=messages,
    )

    text = response.output.choices[0].message.content[0]["text"]
    text = text.replace("```json", "").replace("```", "").strip()
    coords = json.loads(text)

    # 兼容模型返回一维列表 [x1,y1,x2,y2] 的情况
    if coords and not isinstance(coords[0], list):
        coords = [coords]

    # 获取图片尺寸，用于坐标转换
    if image.startswith("file://"):
        local_path = image[len("file://"):]
        img = Image.open(local_path)
    else:
        tmp_path = "temp_bbox_image"
        urllib.request.urlretrieve(image, tmp_path)
        img = Image.open(tmp_path)
    width, height = img.size

    # qwen3.6-plus 等 Qwen3-VL 系列模型返回归一化坐标 [0, 999]，此处转换为绝对像素坐标
    bbox_list = []
    for box in coords:
        bbox_list.append([
            int(box[0] / 1000 * width),
            int(box[1] / 1000 * height),
            int(box[2] / 1000 * width),
            int(box[3] / 1000 * height)
        ])

    return bbox_list

# === 使用示例 ===
image_url = "https://img.alicdn.com/imgextra/i3/O1CN01ewUWhg1eS3VqJ3wap_!!6000000003869-49-tps-2048-2048.webp"

# 按名称选取目标
bbox = get_bbox_list(image_url, "咖啡杯")           # [[x1, y1, x2, y2]]

# 按位置描述选取目标
bbox = get_bbox_list(image_url, "盘子正中间的水果")  # [[x1, y1, x2, y2]]

# 描述一个区域
bbox = get_bbox_list(image_url, "薰衣草盆栽")

# 结果可作为 bbox_list 数组中的元素
# 注意：单张图片最多支持 2 个边界框
```

## 计费与限流

-   模型免费额度和计费单价请参见[模型列表与价格](raw/model-user-guide/get-started-with-models/models.md)。
    
-   模型限流请参见[万相](https://help.aliyun.com/zh/model-studio/rate-limit#513e0a3df24v7)。
    
-   计费说明：
    
    -   按成功生成的 **图像张数** 计费。仅当接口返回`task_status`为`SUCCEEDED` 并成功生成图像后，才会计费。
    -   模型调用失败或处理错误不产生任何费用，也不消耗[免费额度](raw/model-user-guide/test-1/new-free-quota.md)。

## API参考

各模型使用不同的端点和请求结构：

**模型**

**端点****（以北京地域为例）**

`wan2.7-image` 、 `wan2.7-image-pro`、`wan2.6-image`

同步接口：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

异步接口：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

`wan2.5-i2i-preview`

异步接口：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis`

-   `wan2.7` / `wan2.6`：`messages` 格式，在 `messages[].content` 数组中，通过 `image` 传入图像，通过`text`传入提示词。
-   `wan2.5`：通过 `input.images`数组 传入图像，通过`input.prompt` 传入提示词

wan2.7-image-pro、wan2.7-image、wan2.6-image

```
"input": {
    "messages": [
        {
            "role": "user",
            "content": [
                {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"},
                {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"},
                {"text": "把图2的涂鸦喷绘在图1的汽车上"}
            ]
        }
    ]
}
```

wan2.5-i2i-preview

```
"input": {
    "prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
    "images": [
        "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp",
        "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"
    ]
}
```

输入和输出参数请参见[万相-图像生成与编辑2.7 API参考](raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)、[万相-图像生成与编辑2.6 API参考](raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)、[万相-通用图像编辑2.5 API参考](raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。
