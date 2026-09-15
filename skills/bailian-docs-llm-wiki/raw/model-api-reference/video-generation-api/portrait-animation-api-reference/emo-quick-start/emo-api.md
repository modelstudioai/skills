# EMO 视频生成 API参考

EMO模型可基于人物肖像图片和人声音频，生成人脸动态视频。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 效果示例

**输入示例**

**输出示例**

人物肖像：

![上春山](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9239161571/p872312.png)

人声音频：

使用动作风格强度：参数 `style_level` 设置为 `'active'`。

更多效果示例请参见[模型效果示例](https://help.aliyun.com/zh/model-studio/emo-quick-start#3487e3ac6c4xh)。

**说明**请确保上传的图片、音频文件来源符合相关法律法规，且已获得相应内容的使用许可。

## 前提条件

-   需要[开通模型服务并获取API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   输入图像必须先通过[EMO图像检测API](raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)检测，并获得对应**人脸区域（face\_bbox）**和**动态区域（ext\_bbox）**的范围值作为入参。

## HTTP调用

### 步骤1：创建任务获取任务ID

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis
```

**说明**

-   创建任务后，系统将立即返回一个 `task_id`，用于“步骤2”查询任务结果。`task_id` 自创建起**有效期为24小时**。
-   新手指引请参见[Postman](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

#### 请求参数

##### 请求头（Headers）

**X-DashScope-Async**`string`**（必选）**

异步处理配置参数。HTTP请求只支持异步，**必须设置为**`enable`。

**重要**缺少此请求头将报错：“current user api does not support synchronous calls”。

**Authorization**`string`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

**Content-Type**`string`**（必选）**

请求内容类型。此参数必须设置为`application/json`。

##### 请求体（Request Body）

**model** `string` **（必选）**

模型名称。示例值：emo-v1。

**说明**若调用独立部署模型，则填入**部署成功的模型名称**

**input** `object` **（必选）**

输入的基本信息。

属性

**image\_url** `string` **（必选）**

用户上传的图片 URL。模型将根据[EMO图像检测API](raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)返回的 ext\_bbox 参数，对原始图片进行裁剪。裁剪后区域的宽高比直接决定了输出视频的画幅比例与分辨率。

-   若 ext\_bbox 宽高比为1:1，则生成512×512的头像视频；若为3:4，则生成512×704的半身像视频。
-   图像要求最小边长 ≥ 400像素，最大边长 ≤ 7000像素。
-   格式支持：jpg，jpeg，png，bmp，webp。
-   示例值：[](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250911/yhdvfg/emo.png)[https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250911/yhdvfg/emo.png](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250911/yhdvfg/emo.png)。
-   上传文件支持HTTP或HTTPS链接方式，不支持本地链接方式。您也可在此[获取临时公网URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

**audio\_url** `string` **（必选）**

用户上传的音频文件 URL， 用于EMO模型推理的输入。

-   需包含清晰人声，并尽可能去除环境噪音、背景音乐等干扰。
-   文件大小 ≤ 15 MB，时长 ≤ 60 s。
-   格式支持：wav、mp3。
-   示例值：[](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250825/aejgyj/input_audio.mp3)[https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250825/aejgyj/input\_audio.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250825/aejgyj/input_audio.mp3)。
-   上传文件支持HTTP或HTTPS链接方式，不支持本地链接方式。您也可在此[获取临时公网URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

**face\_bbox** `array`**（必选）**

图片中人脸区域bbox的像素坐标，应输入[EMO图像检测API](raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)出参中同名字段的值。坐标格式\[x1,y1,x2,y2\]，分别对应左上和右下两个点的坐标。示例值：\[302,286,610,593\]。

> 图像左上角为坐标原点(0,0)，x轴向右为正，y轴向下为正。

**ext\_bbox** `array`**（必选）**

图片中动态区域bbox的像素坐标，应输入[EMO图像检测API](raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)出参中同名字段的值。该区域的宽高比为1:1或3:4。坐标格式\[x1,y1,x2,y2\]，分别对应左上和右下两个点的坐标。示例值：\[71,9,840,778\]。

**parameters** `object`（可选）

属性

**style\_level** `string` （可选）默认值：normal

可选择动作风格强度控制人物的运动姿态和幅度，当前支持3种：normal、calm、active，分别对应人物动作风格适中、平静、活泼。默认为normal。

bash

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "emo-v1",
    "input": {
        "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251225/onmomb/emo.png",
        "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250825/aejgyj/input_audio.mp3",
        "face_bbox":[302,286,610,593],
        "ext_bbox":[71,9,840,778]
        },
    "parameters": {
        "style_level": "normal"
        }
    }'
```

python

```
import requests
import os

# 1. 从环境变量获取 API Key
api_key = os.getenv("DASHSCOPE_API_KEY")

# 2. 准备请求信息
url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis'

headers = {
    'X-DashScope-Async': 'enable',
    'Authorization': f'Bearer {api_key}',
}

payload = {
    "model": "emo-v1",
    "input": {
        "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251225/onmomb/emo.png",
        "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250825/aejgyj/input_audio.mp3",
        "face_bbox": [302, 286, 610, 593],
        "ext_bbox": [71, 9, 840, 778]
    },
    "parameters": {
        "style_level": "normal"
    }
}

# 3. 发送 POST 请求
#    使用 'json' 参数，requests会自动处理JSON序列化和'Content-Type'头
response = requests.post(url, headers=headers, json=payload)

# 4. 打印服务器返回的原始JSON响应
#    如果请求成功，会打印任务ID等信息。
#    如果请求失败，会打印服务器返回的错误信息。
print(response.json())
```

java

```
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.stream.Collectors;
/**
 * 要求：
 * - Java 8 或更高版本。
 * - 运行时需要设置环境变量 DASHSCOPE_API_KEY。
 **/
public class DashScopeApiDemo {

    public static void main(String[] args) throws IOException {
        // 1. 从环境变量获取 API Key
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        // 2. 准备请求信息
        String urlString = "https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis";
        String payload = "{"
                + "\"model\": \"emo-v1\","
                + "\"input\": {"
                +     "\"image_url\": \"https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251225/onmomb/emo.png\","
                +     "\"audio_url\": \"https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250825/aejgyj/input_audio.mp3\","
                +     "\"face_bbox\": [302, 286, 610, 593],"
                +     "\"ext_bbox\": [71, 9, 840, 778]"
                + "},"
                + "\"parameters\": {"
                +     "\"style_level\": \"normal\""
                + "}"
                + "}";
        // 3. 发送 POST 请求
        URL url = new URL(urlString);
        // noinspection StartSSRFNetHookCheckingInspection
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Authorization", "Bearer " + apiKey);
        connection.setRequestProperty("X-DashScope-Async", "enable");
        connection.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
        connection.setRequestProperty("Accept", "application/json");
        connection.setDoOutput(true);
        // 获取输出流并写入请求体数据
        try (OutputStream os = connection.getOutputStream()) {
            byte[] input = payload.getBytes(StandardCharsets.UTF_8);
            os.write(input, 0, input.length);
        }
        // 4. 获取并打印服务器响应
        int statusCode = connection.getResponseCode();
        System.out.println("Status Code: " + statusCode);
        // 根据状态码选择输入流（正常流或错误流）
        InputStream inputStream = (statusCode >= 200 && statusCode < 300)
                ? connection.getInputStream()
                : connection.getErrorStream();
        String responseBody;
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8))) {
            responseBody = reader.lines().collect(Collectors.joining("\n"));
        }
        System.out.println("Response Body: " + responseBody);
        connection.disconnect();
    }
}
```

javascript

```
// 需要安装node-fetch包
// npm install node-fetch@2

// 导入 node-fetch 库
const fetch = require('node-fetch');
// 1. 从环境变量获取 API Key
const apiKey = process.env.DASHSCOPE_API_KEY;
// 2. 准备请求信息
const url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis';

const headers = {
    'X-DashScope-Async': 'enable',
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json' // 使用 fetch 时需要手动指定
};

const payload = {
    "model": "emo-v1",
    "input": {
        "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251225/onmomb/emo.png",
        "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250825/aejgyj/input_audio.mp3",
        "face_bbox": [302, 286, 610, 593],
        "ext_bbox": [71, 9, 840, 778]
    },
    "parameters": {
        "style_level": "normal"
    }
};

// 3. 发送 POST 请求并处理响应
fetch(url, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(payload) // 必须将 JS 对象转换为 JSON 字符串
})
.then(response => response.json()) // 将响应体解析为 JSON
.then(data => {
    // 4. 打印服务器返回的 JSON 数据
    console.log(data);
});
```

#### 响应参数

**output**`object`

任务输出信息。

属性

**task\_id**`string`

提交异步任务的任务ID，实际任务结果需要通过异步任务查询接口获取。示例值：a8532587-fa8c-4ef8-82be-xxxxxx。

**task\_status** `string`

提交异步任务后的任务状态。示例值：“PENDING”。

**request\_id**`string`

请求唯一标识。可用于请求明细溯源和问题排查。

**code** `string`

请求失败时返回的错误码，详情请参见[状态码说明](https://help.aliyun.com/zh/model-studio/emo-api#933856b630hez)。

**message**`string`

请求失败时返回的详细错误信息，详情请参见[状态码说明](https://help.aliyun.com/zh/model-studio/emo-api#933856b630hez)。

响应成功示例

```
{
    "output": {
        "task_id": "a8532587-fa8c-4ef8-82be-xxxxxx",
        "task_status": "PENDING"
    },
    "request_id": "7574ee8f-38a3-4b1e-9280-11c33ab46e51"
}
```

响应异常示例

```
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

### 步骤2：根据任务ID查询结果

使用上一步获取的 `task_id`，轮询任务状态和结果。请将 URL 中的`{task_id}` 替换为您的实际任务ID。

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

**说明**

-   **task\_id 有效期**：自创建起**有效期24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
-   **任务状态流转**：一般正常处理的任务流转状态为 PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
-   **任务结果获取**：视频生成过程约需数分钟，查询接口默认QPS为20。建议[配置异步任务回调](raw/model-api-reference/more-about-models/async-task-api.md)获取结果，或者采用轮询方式并设置合理的查询间隔（如 15 秒）来获取结果。
-   **video\_url 有效期**：自任务成功时刻起**有效期为 24 小时。建议在获取链接后立即下载并转存至永久存储**（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
-   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

#### 请求参数

##### 请求头（Headers）

**Authorization**`string`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

##### URL路径参数（Path parameters）

**task\_id** `string`**（必选）**

需要查询任务的task\_id。示例值：a8532587-fa8c-4ef8-82be-xxxxxx。

bash

```
curl -X GET \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

python

```
import requests
import os

# 1. 从环境变量获取 API Key
api_key = os.getenv("DASHSCOPE_API_KEY")

# 2. 请替换为您真实需要查询的任务 ID
task_id = "a8532587-fa8c-4ef8-82be-xxxxxx"

# 3. 准备请求信息
# 使用 f-string 将 task_id 拼接到 URL 中
url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"

headers = {
    'Authorization': f'Bearer {api_key}'
}

# 4. 发送 GET 请求
response = requests.get(url, headers=headers)

# 5. 打印服务器返回的 JSON 响应
# 这将显示任务的状态（如 "RUNNING", "SUCCEEDED", "FAILED"）和结果
print(response.json())
```

java

```
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.stream.Collectors;
/**
 * 要求：
 * - Java 8 或更高版本。
 * - 运行时需要设置环境变量 DASHSCOPE_API_KEY。
 **/
public class TaskStatusChecker {

    public static void main(String[] args) throws IOException {
        // 1. 从环境变量获取 API Key
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        // 2. 请替换为您真实需要查询的任务 ID
        String taskId = "a8532587-fa8c-4ef8-82be-xxxxxx"; // 替换为你的任务ID
        // 3. 准备请求信息 (动态拼接 URL)
        String urlString = "https://dashscope.aliyuncs.com/api/v1/tasks/" + taskId;
        // 4. 创建连接并发送 GET 请求
        URL url = new URL(urlString);
        // noinspection StartSSRFNetHookCheckingInspection
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");
        // 设置请求头
        connection.setRequestProperty("Authorization", "Bearer " + apiKey);
        // 5. 获取并打印服务器响应
        int statusCode = connection.getResponseCode();
        System.out.println("Status Code: " + statusCode);
        InputStream inputStream = (statusCode >= 200 && statusCode < 300)
                ? connection.getInputStream()
                : connection.getErrorStream();
        String responseBody;
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8))) {
            responseBody = reader.lines().collect(Collectors.joining("\n"));
        }
        System.out.println("Response Body: " + responseBody);
        connection.disconnect();
    }
}
```

javascript

```
// 需要安装node-fetch包
// npm install node-fetch@2

// 导入 node-fetch 库
const fetch = require('node-fetch');
// 1. 从环境变量获取 API Key
const apiKey = process.env.DASHSCOPE_API_KEY;
// 2. 请替换为您真实需要查询的任务 ID
const taskId = "a8532587-fa8c-4ef8-82be-xxxxxx"; // <-- 在这里替换您的任务 ID
// 3. 准备请求信息
// 使用模板字符串将 taskId 拼接到 URL 中，这等同于 Python 的 f-string
const url = `https://dashscope.aliyuncs.com/api/v1/tasks/${taskId}`;

const headers = {
    'Authorization': `Bearer ${apiKey}`
};

// 4. 发送 GET 请求
// fetch 默认的请求方法就是 GET，所以可以省略 method: 'GET'
fetch(url, {
    headers: headers
})
.then(response => response.json()) // 将响应体解析为 JSON
.then(data => {
    // 5. 打印服务器返回的 JSON 响应
    // 这将显示任务的状态（如 "RUNNING", "SUCCEEDED"）和结果
    console.log(data);
});
```

#### 响应参数

**request\_id**`string`

请求唯一标识。可用于请求明细溯源和问题排查。

**output**`object`

任务输出信息。

属性

**task\_id**`string`

查询任务的 task\_id。示例值：a8532587-fa8c-4ef8-82be-xxxxxx。

**task\_status** `string`

任务状态。

枚举值

-   PENDING：任务排队中
-   RUNNING：任务处理中
-   SUCCEEDED：任务执行成功
-   FAILED：任务执行失败
-   CANCELED：任务已取消
-   UNKNOWN：任务不存在或状态未知

**submit\_time** `string`

任务提交时间，时区为UTC+8，示例值：2025-09-11 14:33:38.716。

**scheduled\_time** `string`

任务被安排计划开始执行的时间，时区为UTC+8，示例值：2025-09-11 14:33:53.089。

**end\_time** `string`

任务执行结束时间，时区为UTC+8，示例值：2025-09-11 14:35:51.541。

**results** `object`

任务执行结果。

属性

**video\_url** `string`

平台输出的视频结果，**video\_url有效期为任务完成后24小时，请及时下载并保存视频文件。**示例值：[](http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?Expires=xxxx)[http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?Expires=xxxx](http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?Expires=xxxx)。

**code** `string`

请求失败时返回的错误码，详情请参见[状态码说明](https://help.aliyun.com/zh/model-studio/emo-api#933856b630hez)。

**message**`string`

请求失败时返回的详细错误信息，详情请参见[状态码说明](https://help.aliyun.com/zh/model-studio/emo-api#933856b630hez)。

**usage** `object`

属性

**video\_duration** `float`

本次请求生成视频时长，单位：秒，示例值：13.93。

**video\_ratio** `string`

本次请求生成视频的画幅比例，该值为1:1或3:4。

响应成功示例

```
{
    "request_id": "8190395f-ca1b-4703-9656-xxxxxx",
    "output": {
        "task_id": "a8532587-fa8c-4ef8-82be-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-09-11 14:33:38.716",
        "scheduled_time": "2025-09-11 14:33:53.089",
        "end_time": "2025-09-11 14:35:51.541",
        "results": {
            "video_url": "http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?Expires=xxxx"
        }
    },
    "usage": {
        "video_duration": 13.93,
        "video_ratio": "1:1"
    }
}
```

响应异常示例

```
{
    "output": {
        "task_id": "a8532587-fa8c-4ef8-82be-xxxxxx",
        "task_status": "FAILED",
        "code": "InvalidURL",
        "message": "Required URL is missing or invalid, please check the request URL."
    },
    "request_id": "4d687387-580a-4b49-a1f8-4691289e09a3"
}
```

## 计费与限流

**模式**

**模型名称**

**单价**

**免费额度**[**（查看）**](raw/model-user-guide/test-1/new-free-quota.md)

**任务下发接口QPS限制**

**同时处理中任务数量**

调用百炼模型API

emo-v1

后付费，按照输出视频的实际时长计费：

-   生成1:1画幅比例视频：0.08元/秒
    
-   生成3:4画幅比例视频：0.16元/秒
    

1800秒

5

1

（超出任务将排队）

独立部署模型

独立部署成功后将生成唯一的模型名称

预付费：

-   10000元/算力单元/月
    
-   20元/算力单元/小时
    

需部署成功后调用，仅收取部署费用。

无

5

1算力单元支持1并发

## 状态码说明

大模型服务平台通用状态码请查阅：[错误码](raw/model-api-reference/preparations/error-code.md)。
