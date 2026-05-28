# 上传本地文件获取临时URL

在调用多模态、图像、视频或音频模型时，通常需要传入文件的 URL。为此，阿里云百炼提供了**免费**临时存储空间，您可将本地文件上传至该空间并获得 URL（**有效期为 48 小时**）。

## **使用限制**

-   **文件与模型绑定**：文件上传时必须指定模型名称，且该模型须与后续调用的**模型一致**，不同模型无法共享文件。此外，不同模型对文件大小有不同限制，超出限制将导致上传失败。
    
-   **文件与主账号绑定**：文件上传与模型调用所使用的 API Key 必须**属于同一个阿里云主账号**，且上传的文件仅限该主账号及其对应模型使用，无法被其他主账号或其他模型共享。
    
-   **文件有效期限制**：文件上传后**有效期48小时**，超时后文件将被自动清理，请确保在有效期内完成模型调用。
    
-   **文件使用限制**：文件一旦上传，不可查询、修改或下载，仅能**通过URL参数在模型调用时使用**。
    
-   **文件上传限流**：文件上传凭证接口的调用限流按照“阿里云主账号+模型”维度为**100QPS**，**超出限流将导致请求失败**。
    

**重要**

-   临时 URL 有效期48小时，过期后无法使用，**请勿用于生产环境。**
    
-   文件上传凭证接口限流为 100 QPS 且不支持扩容，**请勿用于生产环境、高并发及压测场景。**
    
-   生产环境建议使用[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss) 等稳定存储，确保文件长期可用并规避限流问题。
    

## **使用方式**

1.  获取文件 URL：请先通过[步骤一](#a363e01e741gu)上传文件（图片、视频或音频），获取以`oss://` 为前缀的临时 URL。
    
2.  调用模型：**请务必根据**[**步骤二**](#1c60469225ufa)**使用临时 URL 进行调用**。该步骤不能跳过，否则接口将报错。
    

## **步骤一：获取临时URL**

### **方式一：通过代码上传文件**

本文提供 Python 和 Java 示例代码，简化上传文件操作。您只需**指定模型和待上传的文件**，即可获取临时URL。

**前提条件**

在调用前，您需要[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

#### **示例代码**

## Python

**环境配置**

-   推荐使用Python 3.8及以上版本。
    
-   请安装必要的依赖包。
    

```
pip install -U requests
```

**输入参数**

-   api\_key：阿里云百炼API KEY。
    
-   model\_name：指定文件将要用于哪个模型，如`qwen-vl-plus`。
    
-   file\_path：待上传的本地文件路径（图片、视频等）。
    

```
import os
import requests
from pathlib import Path
from datetime import datetime, timedelta

def get_upload_policy(api_key, model_name):
    """获取文件上传凭证"""
    url = "https://dashscope.aliyuncs.com/api/v1/uploads"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    params = {
        "action": "getPolicy",
        "model": model_name
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to get upload policy: {response.text}")
    
    return response.json()['data']

def upload_file_to_oss(policy_data, file_path):
    """将文件上传到临时存储OSS"""
    file_name = Path(file_path).name
    key = f"{policy_data['upload_dir']}/{file_name}"
    
    with open(file_path, 'rb') as file:
        files = {
            'OSSAccessKeyId': (None, policy_data['oss_access_key_id']),
            'Signature': (None, policy_data['signature']),
            'policy': (None, policy_data['policy']),
            'x-oss-object-acl': (None, policy_data['x_oss_object_acl']),
            'x-oss-forbid-overwrite': (None, policy_data['x_oss_forbid_overwrite']),
            'key': (None, key),
            'success_action_status': (None, '200'),
            'file': (file_name, file)
        }
        
        response = requests.post(policy_data['upload_host'], files=files)
        if response.status_code != 200:
            raise Exception(f"Failed to upload file: {response.text}")
    
    return f"oss://{key}"

def upload_file_and_get_url(api_key, model_name, file_path):
    """上传文件并获取URL"""
    # 1. 获取上传凭证，上传凭证接口有限流，超出限流将导致请求失败
    policy_data = get_upload_policy(api_key, model_name) 
    # 2. 上传文件到OSS
    oss_url = upload_file_to_oss(policy_data, file_path)
    
    return oss_url

# 使用示例
if __name__ == "__main__":
    # 从环境变量中获取API Key 或者 在代码中设置 api_key = "your_api_key"
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise Exception("请设置DASHSCOPE_API_KEY环境变量")
        
    # 设置model名称
    model_name="qwen-vl-plus"

    # 待上传的文件路径
    file_path = "/tmp/cat.png"  # 替换为实际文件路径
    
    try:
        public_url = upload_file_and_get_url(api_key, model_name, file_path)
        expire_time = datetime.now() + timedelta(hours=48)
        print(f"文件上传成功，有效期为48小时，过期时间: {expire_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"临时URL: {public_url}")
        print("注意：使用oss://形式的临时URL时，必须在HTTP请求头（Header）中显式添加参数：X-DashScope-OssResourceResolve: enable，具体请参考：https://help.aliyun.com/zh/model-studio/get-temporary-file-url#http-call")

    except Exception as e:
        print(f"Error: {str(e)}")
```

**输出示例**

```
文件上传成功，有效期为48小时，过期时间: 2024-07-18 17:36:15
临时URL: oss://dashscope-instant/xxx/2024-07-18/xxx/cat.png
注意：使用oss://形式的临时URL时，必须在HTTP请求头（Header）中显式添加参数：X-DashScope-OssResourceResolve: enable，具体请参考：https://help.aliyun.com/zh/model-studio/get-temporary-file-url#http-call
```

**重要**

获取临时 URL 后，调用时**必须**在 HTTP 请求头（Header）中显式添加参数：`**X-DashScope-OssResourceResolve: enable**`，具体请参见[通过HTTP调用](#d6a1cb0f01h5k)。

## Java

**环境配置**

-   推荐使用JDK 1.8及以上版本。
    
-   请在Maven项目的`pom.xml`文件中导入以下依赖。
    

```
<dependencies>
        <dependency>
            <groupId>org.json</groupId>
            <artifactId>json</artifactId>
            <version>20230618</version>
        </dependency>
        <dependency>
            <groupId>org.apache.httpcomponents</groupId>
            <artifactId>httpclient</artifactId>
            <version>4.5.13</version>
        </dependency>
        <dependency>
            <groupId>org.apache.httpcomponents</groupId>
            <artifactId>httpmime</artifactId>
            <version>4.5.13</version>
        </dependency>
</dependencies>
```

**输入参数**

-   apiKey：阿里云百炼API KEY。
    
-   modelName：指定文件将要用于哪个模型，如`qwen-vl-plus`。
    
-   filePath：待上传的本地文件路径（图片、视频等）。
    

```
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.entity.ContentType;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.HttpStatus;
import org.apache.http.util.EntityUtils;
import org.json.JSONObject;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class PublicUrlHandler {

    private static final String API_URL = "https://dashscope.aliyuncs.com/api/v1/uploads";

    public static JSONObject getUploadPolicy(String apiKey, String modelName) throws IOException {
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpGet httpGet = new HttpGet(API_URL);
            httpGet.addHeader("Authorization", "Bearer " + apiKey);
            httpGet.addHeader("Content-Type", "application/json");

            String query = String.format("action=getPolicy&model=%s", modelName);
            httpGet.setURI(httpGet.getURI().resolve(httpGet.getURI() + "?" + query));

            try (CloseableHttpResponse response = httpClient.execute(httpGet)) {
                if (response.getStatusLine().getStatusCode() != 200) {
                    throw new IOException("Failed to get upload policy: " +
                            EntityUtils.toString(response.getEntity()));
                }
                String responseBody = EntityUtils.toString(response.getEntity());
                return new JSONObject(responseBody).getJSONObject("data");
            }
        }
    }

    public static String uploadFileToOSS(JSONObject policyData, String filePath) throws IOException {
        Path path = Paths.get(filePath);
        String fileName = path.getFileName().toString();
        String key = policyData.getString("upload_dir") + "/" + fileName;

        HttpPost httpPost = new HttpPost(policyData.getString("upload_host"));
        MultipartEntityBuilder builder = MultipartEntityBuilder.create();

        builder.addTextBody("OSSAccessKeyId", policyData.getString("oss_access_key_id"));
        builder.addTextBody("Signature", policyData.getString("signature"));
        builder.addTextBody("policy", policyData.getString("policy"));
        builder.addTextBody("x-oss-object-acl", policyData.getString("x_oss_object_acl"));
        builder.addTextBody("x-oss-forbid-overwrite", policyData.getString("x_oss_forbid_overwrite"));
        builder.addTextBody("key", key);
        builder.addTextBody("success_action_status", "200");
        byte[] fileContent = Files.readAllBytes(path);
        builder.addBinaryBody("file", fileContent, ContentType.DEFAULT_BINARY, fileName);

        httpPost.setEntity(builder.build());

        try (CloseableHttpClient httpClient = HttpClients.createDefault();
             CloseableHttpResponse response = httpClient.execute(httpPost)) {
            if (response.getStatusLine().getStatusCode() != HttpStatus.SC_OK) {
                throw new IOException("Failed to upload file: " +
                        EntityUtils.toString(response.getEntity()));
            }
            return "oss://" + key;
        }
    }

    public static String uploadFileAndGetUrl(String apiKey, String modelName, String filePath) throws IOException {
        JSONObject policyData = getUploadPolicy(apiKey, modelName);
        return uploadFileToOSS(policyData, filePath);
    }

    public static void main(String[] args) {
        // 获取环境变量中的API密钥
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            System.err.println("请设置DASHSCOPE_API_KEY环境变量");
            System.exit(1);
        }
        // 模型名称
        String modelName = "qwen-vl-plus";
        //替换为实际文件路径
        String filePath = "src/main/resources/tmp/cat.png";

        try {
            // 检查文件是否存在
            File file = new File(filePath);
            if (!file.exists()) {
                System.err.println("文件不存在: " + filePath);
                System.exit(1);
            }

            String publicUrl = uploadFileAndGetUrl(apiKey, modelName, filePath);
            LocalDateTime expireTime = LocalDateTime.now().plusHours(48);
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

            System.out.println("文件上传成功，有效期为48小时，过期时间: " + expireTime.format(formatter));
            System.out.println("临时URL: " + publicUrl);
            System.out.println("注意：使用oss://形式的临时URL时，必须在HTTP请求头（Header）中显式添加参数：X-DashScope-OssResourceResolve: enable，具体请参考：https://help.aliyun.com/zh/model-studio/get-temporary-file-url#http-call");
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
```

**输出示例**

```
文件上传成功，有效期为48小时，过期时间: 2024-07-18 17:36:15
临时URL: oss://dashscope-instant/xxx/2024-07-18/xxx/cat.png
注意：使用oss://形式的临时URL时，必须在HTTP请求头（Header）中显式添加参数：X-DashScope-OssResourceResolve: enable，具体请参考：https://help.aliyun.com/zh/model-studio/get-temporary-file-url#http-call
```

**重要**

获取临时 URL 后，调用时**必须**在 HTTP 请求头（Header）中显式添加参数：`**X-DashScope-OssResourceResolve: enable**`，具体请参见[通过HTTP调用](#d6a1cb0f01h5k)。

### **方式二：通过命令行工具上传文件**

对于熟悉命令行的开发者，可使用DashScope提供的命令行工具来上传文件。**执行命令后，即可获取临时URL**。

#### **前提条件**

1.  环境准备：推荐使用 Python 3.8 及以上版本。
    
2.  获取API-KEY：在调用前，您需要[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    
3.  安装SDK：请确保[DashScope Python SDK](https://help.aliyun.com/zh/model-studio/install-sdk) 版本不低于 `1.24.0`。执行以下命令进行安装或升级：
    

```
pip install -U dashscope
```

#### **方法1：使用环境变量（推荐）**

此方法更安全，可以避免API-KEY在命令历史或脚本中明文暴露。

前提条件：请确保已[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

执行上传命令：

```
dashscope oss.upload --model qwen-vl-plus --file cat.png
```

输出示例：

```
Start oss.upload: model=qwen-vl-plus, file=cat.png, api_key=None
Uploaded oss url: oss://dashscope-instant/xxxx/2025-08-01/xxxx/cat.png
```

**重要**

获取临时 URL 后，调用时**必须**在 HTTP 请求头（Header）中显式添加参数：`**X-DashScope-OssResourceResolve: enable**`，具体请参见[通过HTTP调用](#d6a1cb0f01h5k)。

#### **方法2：通过命令行参数指定API-KEY（临时使用）**

执行上传命令：

```
dashscope oss.upload --model qwen-vl-plus --file cat.png --api_key sk-xxxxxxx
```

输出示例：

```
Start oss.upload: model=qwen-vl-plus, file=cat.png, api_key=sk-xxxxxxx
Uploaded oss url: oss://dashscope-instant/xxx/2025-08-01/xxx/cat.png
```

**重要**

获取临时 URL 后，调用时**必须**在 HTTP 请求头（Header）中显式添加参数：`**X-DashScope-OssResourceResolve: enable**`，具体请参见[通过HTTP调用](#d6a1cb0f01h5k)。

#### **命令行参数说明**

**参数**

**是否必须**

**说明**

**示例**

oss.upload

是

dashscope的子命令，用于执行文件上传操作。

oss.upload

\--model

是

指定文件将要用于哪个模型。

qwen-vl-plus

\--file

是

本地文件的路径。可以是相对路径或绝对路径。

cat.png，/data/img.jpg

\--api\_key

否

阿里云百炼API-KEY。如已配置环境变量，无需填写此参数。

sk-xxxx

## **步骤二：使用临时URL调用模型**

#### **使用限制**

-   **文件格式**：临时URL须通过上述方式生成，且以 `oss://`为前缀的URL字符串。
    
-   **文件未过期**：文件URL仍在上传后的48小时有效期内。
    
-   **模型一致**：模型调用所使用的模型必须与文件上传时指定的模型完全一致。
    
-   **账号一致**：模型调用的API KEY必须与文件上传时使用的API KEY同属一个阿里云主账号。
    

#### **方式一：通过HTTP调用**

通过curl、Postman或任何其他HTTP客户端直接调用API，则**必须遵循以下规则**：

**重要**

-   使用临时URL，**必须**在请求的**Header**中添加参数：`**X-DashScope-OssResourceResolve: enable**`。
    
-   若缺失此Header，系统将无法解析`oss://`链接，请求将失败，报错信息请参考[错误码](#3b9b15a6a8qkl)。
    

## **请求示例**

本示例为调用 qwen-vl-plus 模型识别图片内容。

**说明**

请将 `oss://...`替换为真实的临时 URL，否则请求将失败。

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-OssResourceResolve: enable' \
-d '{
  "model": "qwen-vl-plus",
  "messages": [{
      "role": "user",
      "content": 
      [{"type": "text","text": "这是什么"},
       {"type": "image_url","image_url": {"url": "oss://dashscope-instant/xxx/2024-07-18/xxxx/cat.png"}}]
    }]
}'
```

## 响应示例

```
{
  "choices": [
    {
      "message": {
        "content": "这是一张描绘一只白色猫咪在草地上奔跑的图片。这只猫有蓝色的眼睛，看起来非常可爱和活泼。背景是模糊化的自然景色，强调了主体——那只向前冲跑的小猫。这种摄影技巧称为浅景深（或大光圈效果），它使得前景中的小猫变得清晰而锐利，同时使背景虚化以突出主题并营造出一种梦幻般的效果。整体上这张照片给人一种轻松愉快的感觉，并且很好地捕捉到了动物的行为瞬间。",
        "role": "assistant"
      },
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null
    }
  ],
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 1253,
    "completion_tokens": 104,
    "total_tokens": 1357
  },
  "created": 1739349052,
  "system_fingerprint": null,
  "model": "qwen-vl-plus",
  "id": "chatcmpl-cfc4f2aa-22a8-9a94-8243-44c5bd9899bc"
}
```

## 上传的本地图片示例

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5231249371/p915804.png)

#### **方式二：通过DashScope SDK调用**

您也可以使用阿里云百炼提供的 Python 或 Java SDK。

-   **直接传入 URL**：调用模型 SDK 时，直接将以`oss://`为前缀的URL字符串作为文件参数传入。
    
-   **无需关心 Header**：SDK 会自动添加必需的请求头，无需额外操作。
    

**注意**：并非所有模型都支持 SDK 调用，请以模型 API 文档为准。

> 不支持 OpenAI SDK。

## Python

**前提条件**

请[安装DashScope Python SDK](https://help.aliyun.com/zh/model-studio/install-sdk)，且DashScope Python SDK版本号 >=`1.24.0`。

**示例代码**

本示例为调用 qwen-vl-plus 模型识别图片内容。此代码示例仅适用于 qwen-vl 和 omni 系列模型。

## 请求示例

**说明**

请将 image 参数中的 `oss://...`替换为真实的临时 URL，否则请求将失败。

```
import os
import dashscope

messages = [
    {
        "role": "system",
        "content": [{"text": "You are a helpful assistant."}]
    },
    {
        "role": "user",
        "content": [
            {"image": "oss://dashscope-instant/xxx/2024-07-18/xxxx/cat.png"},
            {"text": "这是什么"}]
    }]

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
api_key = os.getenv('DASHSCOPE_API_KEY')

response = dashscope.MultiModalConversation.call(
    api_key=api_key,
    model='qwen-vl-plus',
    messages=messages
)

print(response)
```

## 响应示例

```
{
    "status_code": 200,
    "request_id": "ccd9dcfb-98f0-92bc-xxxxxx",
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
                            "text": "这是一张一只猫在草地上奔跑的照片。猫的毛色主要是白色，带有浅棕色的斑点，眼睛是蓝色的，显得非常可爱。背景是一个模糊的绿色草地和一些树木，阳光照射下来，给整个画面增添了一种温暖的感觉。猫的姿态显示出它正在快速移动，可能是在追逐什么或只是在享受户外活动的乐趣。整体来看，这是一幅充满活力和生机的图片。"
                        }
                    ]
                }
            }
        ]
    },
    "usage": {
        "input_tokens": 1112,
        "output_tokens": 91,
        "input_tokens_details": {
            "text_tokens": 21,
            "image_tokens": 1091
        },
        "prompt_tokens_details": {
            "cached_tokens": 0
        },
        "total_tokens": 1203,
        "output_tokens_details": {
            "text_tokens": 91
        },
        "image_tokens": 1091
    }
}
```

## Java

**前提条件**

请[安装DashScope Java SDK](https://help.aliyun.com/zh/model-studio/install-sdk)，且DashScope Java SDK版本号 >= `2.21.0`。

**示例代码**

本示例为调用 qwen-vl-plus 模型识别图片内容。此代码示例仅适用于 qwen-vl 和 omni 系列模型。

## 请求示例

**说明**

请将 `oss://...`替换为真实的临时 URL，否则请求将失败。

```
import com.alibaba.dashscope.aigc.multimodalconversation.*;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.Arrays;

public class MultiModalConversationUsage {

    private static final String modelName = "qwen-vl-plus";

    // 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void simpleMultiModalConversationCall() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessageItemText systemText = new MultiModalMessageItemText("You are a helpful assistant.");
        MultiModalConversationMessage systemMessage = MultiModalConversationMessage.builder()
                .role(Role.SYSTEM.getValue()).content(Arrays.asList(systemText)).build();
        MultiModalMessageItemImage userImage = new MultiModalMessageItemImage(
                "oss://dashscope-instant/xxx/2024-07-18/xxxx/cat.png");
        MultiModalMessageItemText userText = new MultiModalMessageItemText("这是什么");
        MultiModalConversationMessage userMessage =
                MultiModalConversationMessage.builder().role(Role.USER.getValue())
                        .content(Arrays.asList(userImage, userText)).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .model(MultiModalConversationUsage.modelName)
                .apiKey(apiKey)
                .message(systemMessage)
                .vlHighResolutionImages(true)
                .vlEnableImageHwOutput(true)
//                .incrementalOutput(true)
                .message(userMessage).build();
        MultiModalConversationResult result = conv.call(param);
        System.out.print(JsonUtils.toJson(result));

    }

    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException /*| IOException*/ e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }

}
```

## 响应示例

```
{
    "requestId": "b6d60f91-4a7f-9257-xxxxxx",
    "usage": {
        "input_tokens": 1112,
        "output_tokens": 91,
        "total_tokens": 1203,
        "image_tokens": 1091,
        "input_tokens_details": {
            "text_tokens": 21,
            "image_tokens": 1091
        },
        "output_tokens_details": {
            "text_tokens": 91
        }
    },
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "text": "这是一张一只猫在草地上奔跑的照片。猫的毛色主要是白色，带有浅棕色的斑点，眼睛是蓝色的，显得非常可爱。背景是一个模糊的绿色草地和一些树木，阳光照射下来，给整个画面增添了一种温暖的感觉。猫的姿态显示出它正在快速移动，可能是在追逐什么或只是在享受户外活动的乐趣。整体来看，这是一幅充满活力和生机的图片。"
                        },
                        {
                            "image_hw": [
                                [
                                    "924",
                                    "924"
                                ]
                            ]
                        }
                    ]
                }
            }
        ]
    }
}
```

## 附接口说明

在上述[获取临时URL](#a363e01e741gu)的两种方式中，代码调用和命令行工具已集成以下三个步骤，简化文件上传操作。以下是各步骤的接口说明。

#### **步骤1：获取文件上传凭证**

##### **前提条件**

您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

##### **请求接口**

```
GET https://dashscope.aliyuncs.com/api/v1/uploads
```

**重要**

文件上传凭证接口限流为 100 QPS（按“阿里云主账号+模型”维度），且临时存储不可扩容。生产环境或高并发场景请使用[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)等存储服务。

##### **入参描述**

**传参方式**

**字段**

**类型**

**必选**

**描述**

**示例值**

Header

Content-Type

_string_

是

请求类型：application/json 。

application/json

Authorization

_string_

是

阿里云百炼API Key，例如：Bearer sk-xxx。

Bearer sk-xxx

Params

action

_string_

是

操作类型，当前场景为`getPolicy`。

getPolicy

model

_string_

是

需要调用的模型名称。

qwen-vl-plus

##### **出参描述**

**字段**

**类型**

**描述**

**示例值**

request\_id

_string_

本次请求的系统唯一码。

7574ee8f-...-11c33ab46e51

data

_object_

\-

\-

data.policy

_string_

上传凭证。

eyJl...1ZSJ9XX0=

data.signature

_string_

上传凭证的签名。

g5K...d40=

data.upload\_dir

_string_

上传文件的目录。

dashscope-instant/xxx/2024-07-18/xxxx

data.upload\_host

_string_

上传的host地址。

https://dashscope-file-xxx.oss-cn-beijing.aliyuncs.com

data.expire\_in\_seconds

_string_

凭证有效期（单位：秒）。

**说明**

过期后，重新调用本接口获取新的凭证。

300

data.max\_file\_size\_mb

_string_

本次允许上传的最大文件的大小（单位：MB）。

该值与需要访问的模型相关。

100

data.capacity\_limit\_mb

_string_

同一个主账号每天上传容量限制（单位：MB）。

999999999

data.oss\_access\_key\_id

_string_

用于上传的access key。

LTAxxx

data.x\_oss\_object\_acl

_string_

上传文件的访问权限，`private`表示私有。

private

data.x\_oss\_forbid\_overwrite

_string_

文件同名时是否可以覆盖，`true`表示不可覆盖。

true

##### **请求示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/uploads?action=getPolicy&model=qwen-vl-plus' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

**说明**

若未配置阿里云百炼API Key到环境变量，请将`$DASHSCOPE_API_KEY`替换为实际API Key，例如：`--header "Authorization: Bearer sk-xxx"`。

#### **响应示例**

```
{
    "request_id": "52f4383a-c67d-9f8c-xxxxxx",
    "data": {
        "policy": "eyJl...1ZSJ=",
        "signature": "eWy...=",
        "upload_dir": "dashscope-instant/xxx/2024-07-18/xxx",
        "upload_host": "https://dashscope-file-xxx.oss-cn-beijing.aliyuncs.com",
        "expire_in_seconds": 300,
        "max_file_size_mb": 100,
        "capacity_limit_mb": 999999999,
        "oss_access_key_id": "LTA...",
        "x_oss_object_acl": "private",
        "x_oss_forbid_overwrite": "true"
    }
}
```

#### **步骤2：上传文件至临时存储空间**

#### **前提条件**

-   已获取文件上传凭证。
    
-   确保文件上传凭证在有效期内，若凭证过期，请重新调用步骤1的接口获取新的凭证。
    
    > 查看文件上传凭证有效期：步骤1的输出参数`data.expire_in_seconds`为凭证有效期，单位为秒。
    

#### **请求接口**

```
POST {data.upload_host}
```

**说明**

请将{data.upload\_host}替换为步骤1的输出参数`data.upload_host`对应的值。

#### **入参描述**

**传参方式**

**字段**

**类型**

**必选**

**描述**

**示例值**

Header

Content-Type

_string_

否

提交表单必须为`multipart/form-data`。

在提交表单时，Content-Type会以`multipart/form-data;boundary=xxxxxx`的形式展示。

> boundary 是自动生成的随机字符串，无需手动指定。若使用 SDK 拼接表单，SDK 也会自动生成该随机值。

multipart/form-data; boundary=9431149156168

form-data

OSSAccessKeyId

_text_

是

文件上传凭证接口的输出参数 `data.oss_access_key_id` 的值。

LTAm5xxx

policy

_text_

是

文件上传凭证接口的输出参数 `data.policy` 的值。

g5K...d40=

Signature

_text_

是

文件上传凭证接口的输出参数 `data.signature` 的值。

Sm/tv7DcZuTZftFVvt5yOoSETsc=

key

_text_

是

文件上传凭证接口的输出参数 `data.upload_dir` 的值拼接上`/_文件名_`。

例如，`upload_dir` 为 `dashscope-instant/xxx/2024-07-18/xxx`，需要上传的文件名为 `cat.png`，拼接后的完整路径为：

`dashscope-instant/xxx/2024-07-18/xxx/cat.png`

x-oss-object-acl

_text_

是

文件上传凭证接口的输出参数 `data.x_oss_object_acl` 的值。

private

x-oss-forbid-overwrite

_text_

是

文件上传凭证接口的输出参数中`data.x_oss_forbid_overwrite` 的值。

true

success\_action\_status

_text_

否

通常取值为 200，上传完成后接口返回 HTTP code 200，表示操作成功。

200

file

_text_

是

文件或文本内容。

**说明**

-   一次只支持上传一个文件。
    
-   file必须为最后一个表单域，除file以外的其他表单域并无顺序要求。
    

例如，待上传文件`cat.png`在Linux系统中的存储路径为`/tmp`，则此处应为`file=@"/tmp/cat.png"`。

#### **出参描述**

调用成功时，本接口无任何参数输出。

#### **请求示例**

```
curl --location 'https://dashscope-file-xxx.oss-cn-beijing.aliyuncs.com' \
--form 'OSSAccessKeyId="LTAm5xxx"' \
--form 'Signature="Sm/tv7DcZuTZftFVvt5yOoSETsc="' \
--form 'policy="eyJleHBpcmF0aW9 ... ... ... dHJ1ZSJ9XX0="' \
--form 'x-oss-object-acl="private"' \
--form 'x-oss-forbid-overwrite="true"' \
--form 'key="dashscope-instant/xxx/2024-07-18/xxx/cat.png"' \
--form 'success_action_status="200"' \
--form 'file=@"/tmp/cat.png"'
```

#### **步骤3：生成文件URL**

文件URL拼接逻辑：`**oss://**` + `**key**` （步骤2的入参`key`）。该URL有效期为 48 小时。

```
oss://dashscope-instant/xxx/2024-07-18/xxxx/cat.png
```

## **错误码**

如果接口调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

本文的API还有特定状态码，具体如下所示。

**HTTP状态码**

**接口错误码（code）**

**接口错误信息（message）**

**含义说明**

400

invalid\_parameter\_error

InternalError.Algo.InvalidParameter: The provided URL does not appear to be valid. Ensure it is correctly formatted.

无效URL，请检查URL是否填写正确。

> 若使用临时文件URL，需确保请求的 Header 中添加了参数 `X-DashScope-OssResourceResolve: enable`。

400

InvalidParameter.DataInspection

The media format is not supported or incorrect for the data inspection.

可能的原因有：

-   请求Header 缺少必要参数，请设置 `X-DashScope-OssResourceResolve: enable`**。**
    
-   上传的图片格式不符合模型要求，更多信息请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。
    

403

AccessDenied

Invalid according to Policy: Policy expired.

文件上传凭证已经过期。

请重新调用[文件上传凭证接口](#32db94982cllx)生成新凭证。

429

Throttling.RateQuota

Requests rate limit exceeded, please try again later.

调用频次触发限流。

[文件上传凭证接口](#32db94982cllx)限流为 100 QPS（按阿里云主账号 + 模型维度）。触发限流后，建议降低请求频率，或迁移至 OSS 等自有存储服务以规避限制。

## **常见问题**

#### **Q：使用** `**oss://**` **前缀的 URL 调用时报错，该如何处理？**

A：请按以下步骤排查：

1.  **检查请求头（Header）**：  
    若您通过 HTTP（如 Postman、curl）直接调用，**必须在** `**Header**` **中添加参数** `**X-DashScope-OssResourceResolve: enable**`。未添加该参数会导致服务端无法识别 OSS 内部协议。关于请求头配置，请参见[通过HTTP调用](#d6a1cb0f01h5k)。
    
2.  **检查 URL 有效性**：  
    `oss://` 链接为临时 URL，请确保该链接是48小时内生成的。如果链接已过期，请重新上传文件获取新的 URL。
    

#### **Q：文件上传与模型调用使用的API KEY可以不一样吗？**

A：文件存储和访问权限基于阿里云主账号管理，API Key 仅为主账号的访问凭证。

因此，同一阿里云主账号下的不同 API Key 可正常使用，不同主账号的 API Key因账号隔离，模型调用无法跨账号读取文件。

请确保文件上传与模型调用使用的 API Key 属于同一阿里云主账号。
