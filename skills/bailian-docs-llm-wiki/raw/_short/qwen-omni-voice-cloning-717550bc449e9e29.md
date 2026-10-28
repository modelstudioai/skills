# 声音复刻API参考

使用创建、查询和删除接口管理 Qwen-Omni 与 Qwen-Omni-Realtime 的复刻音色。本文列出请求参数、响应和错误说明。

复刻步骤、完整示例、音频要求和费用见[声音复刻用户指南](raw/model-user-guide/model-experience/omni-modal/qwen-omni-voice-cloning-user-guide.md)。

**重要**本文档专用于千问Omni和千问Omni-Realtime声音复刻接口；若您使用的是语音合成模型，请参见[语音合成](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：

-   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

使用不同 API 时，请确保使用同一账号进行操作。

## 请求头

**Authorization** `string` **（必选）**

鉴权令牌，格式为`Bearer <your_api_key>`，使用时，将“`<your_api_key>`”替换为实际的API Key。

先[获取并配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再将其传入 `Authorization` 请求头。cURL、Python 和 Java 示例均读取 `DASHSCOPE_API_KEY` 环境变量。

**Content-Type** `string` **（必选）**

请求体中传输的数据的媒体类型。固定为`application/json`。

## 创建音色

上传用于复刻的音频，创建自定义音色。

输入音频支持 WAV（16bit）、MP3、M4A，推荐 10～20 秒，最长 60 秒，文件小于 10 MB，采样率不低于 24 kHz，且为单声道。音频必须包含至少 3 秒连续清晰朗读，停顿不超过 2 秒；整段音频应避免背景音乐、噪音或其他人声。请使用正常说话音频，不要上传歌曲或唱歌音频。支持的语种与方言见下方 `language` 参数；录制建议见[音频要求](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#fe3daa6c3f7jw)。

#### 华北2（北京）

```
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization
```

#### 新加坡

```
POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization
```

### 请求体

**model** `string` **（必选）**

声音复刻模型，固定为`qwen-voice-enrollment`。

**input** `object` **（必选）**

属性

**action** `string` **（必选）**

操作类型，固定为`create`。

**target\_model** `string` **（必选）**

驱动音色的全模态模型：

-   qwen3.8-omni-flash-realtime
-   qwen3.5-omni-plus-realtime
-   qwen3.5-omni-flash-realtime
-   qwen3.5-omni-plus
-   qwen3.5-omni-flash

必须与后续调用全模态接口时使用的模型一致，否则合成会失败。

**preferred\_name** `string` **（必选）**

为音色指定一个便于识别的名称（仅允许数字、大小写字母和下划线，不超过16个字符）。建议选用与角色、场景相关的标识。

> 该关键字会在复刻的音色名中出现，例如关键字为“guanyu”，最终音色名为“qwen-omni-vc-guanyu-voice-20250812105009984-838b”

**audio** `object` **（必选）**

属性

**data** `string` **（必选）**

用于复刻的音频（录制时需遵循[录音操作指南](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#8d342f3949vge)，音频需满足[音频要求](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#fe3daa6c3f7jw)）。

可通过以下两种方式提交音频数据：

1.  [Data URL](https://www.rfc-editor.org/rfc/rfc2397)
    
    格式：`data:<mediatype>;base64,<data>`
    
    -   `<mediatype>`：MIME类型
        
        -   WAV：`audio/wav`
        -   MP3：`audio/mpeg`
        -   M4A：`audio/mp4`
    -   `<data>`：音频转成的Base64编码的字符串
        
        Base64编码会增大体积，请控制原文件大小，确保编码后仍小于10MB
        
    -   示例：`data:audio/wav;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//PAxABQ/BXRbMPe4IQAhl9`
        
2.  音频URL（推荐将音频[上传至OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)）
    
    -   文件大小不超过10MB
    -   URL必须公网可访问且无需鉴权

Data URL 编码示例

python

```
import base64, pathlib

# input.mp3为用于声音复刻的本地音频文件，请替换为自己的音频文件路径，确保其符合音频要求
file_path = pathlib.Path("input.mp3")
base64_str = base64.b64encode(file_path.read_bytes()).decode()
data_uri = f"data:audio/mpeg;base64,{base64_str}"
```

java

```
import java.nio.file.*;
import java.util.Base64;

public class Main {
    /**
     * filePath为用于声音复刻的本地音频文件，请替换为自己的音频文件路径，确保其符合音频要求
     */
    public static String toDataUrl(String filePath) throws Exception {
        byte[] bytes = Files.readAllBytes(Paths.get(filePath));
        String encoded = Base64.getEncoder().encodeToString(bytes);
        return "data:audio/mpeg;base64," + encoded;
    }

    // 使用示例
    public static void main(String[] args) throws Exception {
        System.out.println(toDataUrl("input.mp3"));
    }
}
```

**text** `string` **（可选）**

与`audio.data`音频内容相匹配的文本。

传入该参数后，服务端会对比音频与该文本的差异，若差异过大，将返回Audio.PreprocessError。

**language** `string` **（可选）**

`audio.data`音频对应的语种。

支持`zh`（中文）、`en`（英文）、`de`（德语）、`it`（意大利语）、`pt`（葡萄牙语）、`es`（西班牙语）、`ja`（日语）、`ko`（韩语）、`fr`（法语）、`ru`（俄语）、`th`（泰语）、`id`（印尼语）、`ar`（阿拉伯语）、`cs`（捷克语）、`da`（丹麦语）、`nl`（荷兰语）、`fi`（芬兰语）、`he`（希伯来语）、`hi`（印地语）、`is`（冰岛语）、`ms`（马来语）、`no`（挪威语）、`fa`（波斯语）、`pl`（波兰语）、`sv`（瑞典语）、`tl`（他加禄语）、`tr`（土耳其语）、`ur`（乌尔都语）、`vi`（越南语）。

中文方言：`Dongbei`（东北话）、`Shannxi`（陕西话）、`Sichuan`（四川话）、`Henan`（河南话）、`Changsha`（长沙话）、`Tianjin`（天津话）、`Hangzhou`（杭州话）、`Liaoning`（辽宁话）、`Shenyang`（沈阳话）、`Anshan`（鞍山话）。

若使用该参数，设置的语种要和实际用于复刻的音频的语种一致。

**parameters** `object`

属性

**voice\_clone\_mode** `string` **（条件必选）**

声音复刻模式。使用qwen3.8-omni系列模型时必传，不传时默认回退到qwen3.5-omni talker system instruct模式（兼容旧服务）。

可选值：

-   `normal`：普通模式
-   `dialect`：方言模式
-   `crosslingual`：跨语言模式

该参数需放在`parameters`中。

**skip\_audio\_process** `boolean` **（可选）**

默认值：`false`。

是否跳过音频预处理。默认为`false`。该参数需放在`parameters`中。

**重要**注意区分如下参数：

-   `model`：声音复刻模型，固定为`qwen-voice-enrollment`
-   `target_model`：驱动音色的全模态模型，须和后续调用 Omni 接口时使用的模型一致，否则合成会失败

**重要**`parameters`中的`voice_clone_mode`参数在使用qwen3.8-omni系列模型时必传。不传该字段时，默认回退到qwen3.5-omni talker system instruct模式（兼容旧服务）。

### 请求示例

cURL 示例使用音频 URL，请将 `https://xxx.wav` 替换为实际地址。Python 和 Java 示例读取本地音频，请将 `input.mp3` 替换为实际文件路径。

cURL

```
# 未配置环境变量时，将下方 $DASHSCOPE_API_KEY 替换为实际 API Key。
# ======= 重要提示 =======
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-voice-enrollment",
    "input": {
        "action": "create",
        "target_model": "qwen3.8-omni-flash-realtime",
        "preferred_name": "chinese",
        "audio": {
            "data": "https://xxx.wav"
        }
    },
    "parameters": {
        "skip_audio_process": false,
        "voice_clone_mode": "normal"
    }
}'
```

Python

```
import os
import requests
import base64, pathlib

target_model = "qwen3.8-omni-flash-realtime"
preferred_name = "guanyu"
audio_mime_type = "audio/mpeg"

file_path = pathlib.Path("input.mp3")
base64_str = base64.b64encode(file_path.read_bytes()).decode()
data_uri = f"data:{audio_mime_type};base64,{base64_str}"

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
api_key = os.getenv("DASHSCOPE_API_KEY")
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization"

payload = {
    "model": "qwen-voice-enrollment", # 不要修改这个值
    "parameters": {"voice_clone_mode": "normal"},
    "input": {
        "action": "create",
        "target_model": target_model,
        "preferred_name": preferred_name,
        "audio": {
            "data": data_uri
        }
    }
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 发送 POST 请求
resp = requests.post(url, json=payload, headers=headers)

if resp.status_code == 200:
    data = resp.json()
    voice = data["output"]["voice"]
    print(f"生成的 voice 参数为: {voice}")
else:
    print("请求失败:", resp.status_code, resp.text)
```

Java

```
import com.google.gson.Gson;
import com.google.gson.JsonObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.*;
import java.util.Base64;

public class Main {
    private static final String TARGET_MODEL = "qwen3.8-omni-flash-realtime";
    private static final String PREFERRED_NAME = "guanyu";
    private static final String AUDIO_FILE = "input.mp3";
    private static final String AUDIO_MIME_TYPE = "audio/mpeg";

    public static String toDataUrl(String filePath) throws Exception {
        byte[] bytes = Files.readAllBytes(Paths.get(filePath));
        String encoded = Base64.getEncoder().encodeToString(bytes);
        return "data:" + AUDIO_MIME_TYPE + ";base64," + encoded;
    }

    public static void main(String[] args) {
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx";
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        String apiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization";

        try {
            // 构造 JSON 请求体（注意内部的引号需转义）
            String jsonPayload =
                    "{"
                            + "\"model\": \"qwen-voice-enrollment\"," // 不要修改该值
                            + "\"parameters\": {\"voice_clone_mode\": \"normal\"},"
                            + "\"input\": {"
                            +     "\"action\": \"create\","
                            +     "\"target_model\": \"" + TARGET_MODEL + "\","
                            +     "\"preferred_name\": \"" + PREFERRED_NAME + "\","
                            +     "\"audio\": {"
                            +         "\"data\": \"" + toDataUrl(AUDIO_FILE) + "\""
                            +     "}"
                            + "}"
                            + "}";

            HttpURLConnection con = (HttpURLConnection) new URL(apiUrl).openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Authorization", "Bearer " + apiKey);
            con.setRequestProperty("Content-Type", "application/json");
            con.setDoOutput(true);

            // 发送请求体
            try (OutputStream os = con.getOutputStream()) {
                os.write(jsonPayload.getBytes("UTF-8"));
            }

            int status = con.getResponseCode();
            InputStream is = (status >= 200 && status < 300)
                    ? con.getInputStream()
                    : con.getErrorStream();

            StringBuilder response = new StringBuilder();
            try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
                String line;
                while ((line = br.readLine()) != null) {
                    response.append(line);
                }
            }

            System.out.println("HTTP 状态码: " + status);
            System.out.println("返回内容: " + response.toString());

            if (status == 200) {
                // 解析 JSON
                Gson gson = new Gson();
                JsonObject jsonObj = gson.fromJson(response.toString(), JsonObject.class);
                String voice = jsonObj.getAsJsonObject("output").get("voice").getAsString();
                System.out.println("生成的 voice 参数为: " + voice);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### 响应体

**output** `object`

属性

**voice** `string`

音色名称，可用于后续 Omni 接口的 `voice` 参数。

**target\_model** `string`

驱动音色的全模态模型：

-   qwen3.8-omni-flash-realtime
    
-   qwen3.5-omni-plus-realtime
    
-   qwen3.5-omni-flash-realtime
    
-   qwen3.5-omni-plus
    
-   qwen3.5-omni-flash
    

必须与后续调用全模态接口时使用的模型一致，否则合成会失败。

**usage** `object`

属性

**count** `integer`

本次请求实际计入费用的“创建音色”次数，本次请求的费用为 count × 0.01元。

创建音色时，count恒为1。

**request\_id** `string`

Request ID。

### 响应示例

#### 响应结构

```
{
    "output": {
        "voice": "yourVoice",
        "target_model": "qwen3.8-omni-flash-realtime"
    },
    "usage": {
        "count": 1
    },
    "request_id": "yourRequestId"
}
```

#### 返回示例

```
{"output":{"target_model":"qwen3.8-omni-flash-realtime","voice":"qwen-omni-vc-chinese-voice-20260911161744020-3f9d"},"usage":{"count":1},"request_id":"7a36a3cb-be34-9be8-a127-df2449d51ab2"}
```

## 查询音色列表

分页查询已创建的音色列表。

#### 华北2（北京）

```
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization
```

#### 新加坡

```
POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization
```

### 请求体

**model** `string` **（必选）**

声音复刻模型，固定为`qwen-voice-enrollment`。

**input** `object` **（必选）**

属性

**action** `string` **（必选）**

操作类型，固定为`list`。

**page\_index** `integer` **（可选）**

默认值：`0`。

页码索引。取值范围：\[0, 1000000\]。

**page\_size** `integer` **（可选）**

默认值：`10`。

每页包含数据条数。取值范围：\[0, 1000000\]。

**重要**`model`：声音复刻模型，固定为`qwen-voice-enrollment`，请勿修改。

### 请求示例

cURL

```
# 未配置环境变量时，将下方 $DASHSCOPE_API_KEY 替换为实际 API Key。
# ======= 重要提示 =======
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# === 执行时请删除该注释 ===

curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen-voice-enrollment",
    "input": {
        "action": "list",
        "page_size": 10,
        "page_index": 0
    }
}'
```

Python

```
import os
import requests

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
api_key = os.getenv("DASHSCOPE_API_KEY")
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization"

payload = {
    "model": "qwen-voice-enrollment", # 不要修改该值
    "input": {
        "action": "list",
        "page_size": 10,
        "page_index": 0
    }
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("HTTP 状态码:", response.status_code)

if response.status_code == 200:
    data = response.json()
    voice_list = data["output"]["voice_list"]

    print("查询到的音色列表：")
    for item in voice_list:
        print(f"- 音色: {item['voice']}  创建时间: {item['gmt_create']}  模型: {item['target_model']}")
else:
    print("请求失败:", response.text)
```

Java

```
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class Main {
    public static void main(String[] args) {
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx";
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        String apiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization";

        // JSON 请求体（旧版本 Java 无 """ 多行字符串）
        String jsonPayload =
                "{"
                        + "\"model\": \"qwen-voice-enrollment\"," // 不要修改该值
                        + "\"input\": {"
                        +     "\"action\": \"list\","
                        +     "\"page_size\": 10,"
                        +     "\"page_index\": 0"
                        + "}"
                        + "}";

        try {
            HttpURLConnection con = (HttpURLConnection) new URL(apiUrl).openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Authorization", "Bearer " + apiKey);
            con.setRequestProperty("Content-Type", "application/json");
            con.setDoOutput(true);

            try (OutputStream os = con.getOutputStream()) {
                os.write(jsonPayload.getBytes("UTF-8"));
            }

            int status = con.getResponseCode();
            BufferedReader br = new BufferedReader(new InputStreamReader(
                    status >= 200 && status < 300 ? con.getInputStream() : con.getErrorStream(), "UTF-8"));

            StringBuilder response = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                response.append(line);
            }
            br.close();

            System.out.println("HTTP 状态码: " + status);
            System.out.println("返回 JSON: " + response.toString());

            if (status == 200) {
                Gson gson = new Gson();
                JsonObject jsonObj = gson.fromJson(response.toString(), JsonObject.class);
                JsonArray voiceList = jsonObj.getAsJsonObject("output").getAsJsonArray("voice_list");

                System.out.println("\n 查询到的音色列表：");
                for (int i = 0; i < voiceList.size(); i++) {
                    JsonObject voiceItem = voiceList.get(i).getAsJsonObject();
                    String voice = voiceItem.get("voice").getAsString();
                    String gmtCreate = voiceItem.get("gmt_create").getAsString();
                    String targetModel = voiceItem.get("target_model").getAsString();

                    System.out.printf("- 音色: %s  创建时间: %s  模型: %s\n",
                            voice, gmtCreate, targetModel);
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### 响应体

**output** `object`

属性

**voice\_list** `array<object>`

属性

**voice** `string`

音色名称，可用于后续 Omni 接口的 `voice` 参数。

**gmt\_create** `string`

创建音色的时间。

**target\_model** `string`

驱动音色的全模态模型：

-   qwen3.8-omni-flash-realtime
    
-   qwen3.5-omni-plus-realtime
    
-   qwen3.5-omni-flash-realtime
    
-   qwen3.5-omni-plus
    
-   qwen3.5-omni-flash
    

必须与后续调用全模态接口时使用的模型一致，否则合成会失败。

**usage** `object`

属性

**count** `integer`

本次请求实际计入费用的“创建音色”次数，本次请求的费用为count × 0.01元。

查询音色不计费，因此`count`恒为0。

**request\_id** `string`

Request ID。

### 响应示例

```
{
    "output": {
        "voice_list": [
            {
                "voice": "yourVoice1",
                "gmt_create": "2025-08-11 17:59:32",
                "target_model": "qwen3.5-omni-plus-realtime"
            },
            {
                "voice": "yourVoice2",
                "gmt_create": "2025-08-11 17:38:10",
                "target_model": "qwen3.5-omni-plus-realtime"
            }
        ]
    },
    "usage": {
        "count": 0
    },
    "request_id": "yourRequestId"
}
```

## 删除音色

删除指定音色，释放对应额度。

#### 华北2（北京）

```
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization
```

#### 新加坡

```
POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization
```

### 请求体

**model** `string` **（必选）**

声音复刻模型，固定为`qwen-voice-enrollment`。

**input** `object` **（必选）**

属性

**action** `string` **（必选）**

操作类型，固定为`delete`。

**voice** `string` **（必选）**

待删除的音色。

**重要**`model`：声音复刻模型，固定为`qwen-voice-enrollment`，请勿修改。

### 请求示例

将 `yourVoice` 替换为要删除的音色名称。

cURL

```
# 未配置环境变量时，将下方 $DASHSCOPE_API_KEY 替换为实际 API Key。
# ======= 重要提示 =======
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# === 执行时请删除该注释 ===

curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen-voice-enrollment",
    "input": {
        "action": "delete",
        "voice": "yourVoice"
    }
}'
```

Python

```
import os
import requests

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
api_key = os.getenv("DASHSCOPE_API_KEY")
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization"

voice_to_delete = "yourVoice"  # 要删除的音色（替换为真实值）

payload = {
    "model": "qwen-voice-enrollment", # 不要修改该值
    "input": {
        "action": "delete",
        "voice": voice_to_delete
    }
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("HTTP 状态码:", response.status_code)

if response.status_code == 200:
    data = response.json()
    request_id = data["request_id"]

    print(f"删除成功")
    print(f"Request ID: {request_id}")
else:
    print("请求失败:", response.text)
```

Java

```
import com.google.gson.Gson;
import com.google.gson.JsonObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class Main {
    public static void main(String[] args) {
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx";
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        String apiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization";
        String voiceToDelete = "yourVoice"; // 要删除的音色（替换为真实值）

        // 构造 JSON 请求体（字符串拼接，兼容 Java 8）
        String jsonPayload =
                "{"
                        + "\"model\": \"qwen-voice-enrollment\"," // 不要修改该值
                        + "\"input\": {"
                        +     "\"action\": \"delete\","
                        +     "\"voice\": \"" + voiceToDelete + "\""
                        + "}"
                        + "}";

        try {
            // 建立 POST 连接
            HttpURLConnection con = (HttpURLConnection) new URL(apiUrl).openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Authorization", "Bearer " + apiKey);
            con.setRequestProperty("Content-Type", "application/json");
            con.setDoOutput(true);

            // 发送请求体
            try (OutputStream os = con.getOutputStream()) {
                os.write(jsonPayload.getBytes("UTF-8"));
            }

            int status = con.getResponseCode();
            BufferedReader br = new BufferedReader(new InputStreamReader(
                    status >= 200 && status < 300 ? con.getInputStream() : con.getErrorStream(), "UTF-8"));

            StringBuilder response = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                response.append(line);
            }
            br.close();

            System.out.println("HTTP 状态码: " + status);
            System.out.println("返回 JSON: " + response.toString());

            if (status == 200) {
                Gson gson = new Gson();
                JsonObject jsonObj = gson.fromJson(response.toString(), JsonObject.class);
                String requestId = jsonObj.get("request_id").getAsString();

                System.out.println("删除成功");
                System.out.println("Request ID: " + requestId);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### 响应体

**usage** `object`

属性

**count** `integer`

本次请求实际计入费用的“创建音色”次数，本次请求的费用为count × 0.01元。

删除音色不计费，因此`count`恒为0。

**request\_id** `string`

Request ID。

### 响应示例

```
{
    "usage": {
        "count": 0
    },
    "request_id": "yourRequestId"
}
```

## 错误信息

如遇报错问题，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行排查。

## 用户指南

-   [音频与语言要求](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#fe3daa6c3f7jw)
-   [复刻流程与完整示例](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#bb60d81324wsu)
-   [配额与自动清理](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#4bd111d07d16t)
-   [计费说明](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#b819f697047nb)
-   [版权与合法性](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#8d2900c951llr)
-   [录音建议](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#8d342f3949vge)
