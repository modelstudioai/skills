# 上传本地文件获取临时URL

在调用多模态、图像、视频或音频模型时，通常需要传入文件的 URL。为此，阿里云百炼提供了 免费 临时存储空间，您可将本地文件上传至该空间并获得 URL（ 有效期为 48 小时 ）。

<a id="使用限制"></a>

<a id="e5231784e4tdc"></a>

## 使用限制

-   **文件与模型绑定**：文件上传时必须指定模型名称，且该模型须与后续调用的**模型一致**，不同模型无法共享文件。
-   **文件大小限制**：接口上传文件大小不得超过**1GB**，超出限制将导致上传失败。此外，不同模型对输入文件大小有不同限制，超出限制将导致模型调用失败。
-   **文件与主账号绑定**：文件上传与模型调用所使用的 API Key 必须**属于同一个阿里云主账号**，且上传的文件仅限该主账号及其对应模型使用，无法被其他主账号或其他模型共享。
-   **文件有效期限制**：文件上传后**有效期48小时**，超时后文件将被自动清理，请确保在有效期内完成模型调用。
-   **文件使用限制**：文件一旦上传，不可查询、修改或下载，仅能**通过URL参数在模型调用时使用**。
-   **文件上传限流**：文件上传凭证接口的调用限流按照“阿里云主账号+模型”维度为**100QPS**，**超出限流将导致请求失败**。

> **重要**
>
> -   临时 URL 有效期48小时，过期后无法使用，**请勿用于生产环境。**
> -   文件上传凭证接口限流为 100 QPS 且不支持扩容，**请勿用于生产环境、高并发及压测场景。**
> -   生产环境建议使用[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss) 等稳定存储，确保文件长期可用并规避限流问题。

> **说明**
>
> 本功能支持**华北2（北京）**和**新加坡**地域。本文代码示例默认以**北京地域**为例；如需使用新加坡地域，请按示例中的注释将请求 URL 中的 `dashscope.aliyuncs.com` 替换为 `dashscope-intl.aliyuncs.com`，并使用新加坡地域的 API Key（两地域 API Key 不同，获取方式见[获取与配置 API Key](../preparations/get-api-key.md)）。

<a id="使用方式"></a>

<a id="b33e0ac80abq5"></a>

## 使用方式

1.  获取文件 URL：请先通过[步骤一](get-temporary-file-url.md#a363e01e741gu)上传文件（图片、视频或音频），获取以`oss://` 为前缀的临时 URL。
2.  调用模型：**请务必根据**[**步骤二**](get-temporary-file-url.md#1c60469225ufa)**使用临时 URL 进行调用**。该步骤不能跳过，否则接口将报错。

<a id="步骤一-获取临时url"></a>

<a id="a363e01e741gu"></a>

## 步骤一：获取临时URL

<a id="sec-tabs"></a>

<a id="方式一-通过代码上传文件"></a>

<a id="方式一-通过代码上传文件-h4"></a>

#### 方式一：通过代码上传文件

本文提供 Python 和 Java 示例代码，简化上传文件操作。您只需**指定模型和待上传的文件**，即可获取临时URL。

**前提条件**

在调用前，您需要[获取与配置 API Key](../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="c92b7d87ed5rs"></a>

#### 示例代码

<a id="sec-tabs-2"></a>

<a id="python"></a>

<a id="python-h4"></a>

#### Python

**环境配置**

-   推荐使用Python 3.9及以上版本。
-   请安装必要的依赖包。

<a id="code-block"></a>

```bash
pip install -U requests
```

**输入参数**

-   api\_key：阿里云百炼API KEY。
-   model\_name：指定文件将要用于哪个模型，如`qwen3-vl-plus`。
-   file\_path：待上传的本地文件路径（图片、视频等）。

<a id="code-block-2"></a>

```python
import os
import requests
from pathlib import Path
from datetime import datetime, timedelta

def get_upload_policy(api_key, model_name):
    """获取文件上传凭证"""
    # 北京与新加坡地域的 API Key 不同，请使用对应地域的 API Key
    # 以下为北京地域 url，若使用新加坡地域，需将 url 替换为：https://dashscope-intl.aliyuncs.com/api/v1/uploads
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
    model_name="qwen3-vl-plus"

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

<a id="code-block-3"></a>

```text
文件上传成功，有效期为48小时，过期时间: 2024-07-18 17:36:15
临时URL: oss://dashscope-instant/xxx/2024-07-18/xxx/cat.png
注意：使用oss://形式的临时URL时，必须在HTTP请求头（Header）中显式添加参数：X-DashScope-OssResourceResolve: enable，具体请参考：https://help.aliyun.com/zh/model-studio/get-temporary-file-url#http-call
```

> **重要**
>
> 获取临时 URL 后，调用时**必须**在 HTTP 请求头（Header）中显式添加参数：`X-DashScope-OssResourceResolve: enable`，具体请参见[通过HTTP调用](get-temporary-file-url.md#d6a1cb0f01h5k)。

<a id="java"></a>

<a id="java-h4"></a>

#### Java

**环境配置**

-   推荐使用JDK 1.8及以上版本。
-   请在Maven项目的`pom.xml`文件中导入以下依赖。

<a id="code-block-4"></a>

```xml
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
-   modelName：指定文件将要用于哪个模型，如`qwen3-vl-plus`。
-   filePath：待上传的本地文件路径（图片、视频等）。

<a id="code-block-5"></a>

```java
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

    // 北京与新加坡地域的 API Key 不同，请使用对应地域的 API Key
    // 以下为北京地域 url，若使用新加坡地域，需将 url 替换为：https://dashscope-intl.aliyuncs.com/api/v1/uploads
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
        String modelName = "qwen3-vl-plus";
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

<a id="code-block-6"></a>

```text
文件上传成功，有效期为48小时，过期时间: 2024-07-18 17:36:15
临时URL: oss://dashscope-instant/xxx/2024-07-18/xxx/cat.png
注意：使用oss://形式的临时URL时，必须在HTTP请求头（Header）中显式添加参数：X-DashScope-OssResourceResolve: enable，具体请参考：https://help.aliyun.com/zh/model-studio/get-temporary-file-url#http-call
```

> **重要**
>
> 获取临时 URL 后，调用时**必须**在 HTTP 请求头（Header）中显式添加参数：`X-DashScope-OssResourceResolve: enable`，具体请参见[通过HTTP调用](get-temporary-file-url.md#d6a1cb0f01h5k)。

<a id="dashscope-sdk-python"></a>

<a id="dashscope-sdk-python-h4"></a>

#### DashScope SDK (Python)

**前提条件**

请[安装DashScope Python SDK](../preparations/install-sdk.md)，且DashScope Python SDK版本号 >= `2.0.1`。

DashScope SDK 提供了 `client.files` 资源，封装了文件上传、查询、删除等操作，免去手工拼接上传凭证与 OSS 表单。

> **说明**
>
> `client.files.upload` 签名为 `upload(file_path, purpose)`，其中 `purpose` 取值 `fine_tune`（微调训练文件）或 `inference`（推理临时文件，对应本文场景），**无 `model` 参数**。

<a id="code-block-7"></a>

```python
import os
import dashscope

# 北京与新加坡地域的 API Key 不同，请使用对应地域的 API Key
# 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
client = dashscope.Client(api_key=os.getenv('DASHSCOPE_API_KEY'))

# 上传文件（purpose=fine_tune 用于微调训练文件，purpose=inference 用于推理临时文件）
result = client.files.upload(
    file_path='train_data.jsonl',
    purpose='fine_tune',
)

print(result)
```

**输出示例（HTTP 接口返回）**

<a id="code-block-8"></a>

```text
{"request_id": "xxx", "code": "", "message": "", "output": {"uploaded_files": [{"name": "train_data.jsonl", "file_id": "file-xxx"}], "failed_uploads": []}}
```

<a id="dashscope-cli"></a>

<a id="dashscope-cli-h4"></a>

#### dashscope CLI

<a id="code-block-9"></a>

```bash
export DASHSCOPE_API_KEY="your-api-key"
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
# 列出已上传的文件
dashscope files list

# 上传本地文件
dashscope oss upload -f train_data.jsonl -m qwen-plus
```

> **重要**
>
> SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见
>
> [DashScope SDK Expert](../preparations/dashscope-sdk-expert.md)。

完整地域表见 [Base URL 总览](../preparations/base-url.md)。

<a id="方式二-通过命令行工具上传文件"></a>

<a id="方式二-通过命令行工具上传文件-h4"></a>

#### 方式二：通过命令行工具上传文件

对于熟悉命令行的开发者，可使用DashScope提供的命令行工具来上传文件。**执行命令后，即可获取临时URL**。

<a id="64bddcdb76ef1"></a>

#### 前提条件

1.  环境准备：推荐使用 Python 3.9 及以上版本。
2.  获取API-KEY：在调用前，您需要[获取与配置 API Key](../preparations/get-api-key.md)。
3.  安装SDK：请确保[DashScope Python SDK](../preparations/install-sdk.md) 版本不低于 2.0.1。执行以下命令进行安装或升级：

<a id="code-block-10"></a>

```bash
pip install -U dashscope
```

<a id="sec-tabs-3"></a>

<a id="方法1-使用环境变量-推荐"></a>

<a id="方法1-使用环境变量-推荐-h4"></a>

#### 方法1：使用环境变量（推荐）

此方法更安全，可以避免API-KEY在命令历史或脚本中明文暴露。

前提条件：请确保已[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

执行上传命令：

<a id="code-block-11"></a>

```bash
# 默认使用北京地域，若使用新加坡地域，请先执行：export DASHSCOPE_HTTP_BASE_URL="https://dashscope-intl.aliyuncs.com/api/v1"（新加坡地域 API Key 不同）
dashscope oss.upload --model qwen3-vl-plus --file cat.png
```

输出示例：

<a id="code-block-12"></a>

```text
Start oss.upload: model=qwen3-vl-plus, file=cat.png, api_key=None
Uploaded oss url: oss://dashscope-instant/xxxx/2025-08-01/xxxx/cat.png
```

> **重要**
>
> 获取临时 URL 后，调用时**必须**在 HTTP 请求头（Header）中显式添加参数：`X-DashScope-OssResourceResolve: enable`，具体请参见[通过HTTP调用](get-temporary-file-url.md#d6a1cb0f01h5k)。

<a id="方法2-通过命令行参数指定api-key-临时使用"></a>

<a id="方法2-通过命令行参数指定api-key-临时使用-h4"></a>

#### 方法2：通过命令行参数指定API-KEY（临时使用）

执行上传命令：

<a id="code-block-13"></a>

```bash
# 默认使用北京地域，若使用新加坡地域，请先执行：export DASHSCOPE_HTTP_BASE_URL="https://dashscope-intl.aliyuncs.com/api/v1"（新加坡地域 API Key 不同）
dashscope oss.upload --model qwen3-vl-plus --file cat.png --api_key sk-xxxxxxx
```

输出示例：

<a id="code-block-14"></a>

```text
Start oss.upload: model=qwen3-vl-plus, file=cat.png, api_key=sk-xxxxxxx
Uploaded oss url: oss://dashscope-instant/xxx/2025-08-01/xxx/cat.png
```

> **重要**
>
> 获取临时 URL 后，调用时**必须**在 HTTP 请求头（Header）中显式添加参数：`X-DashScope-OssResourceResolve: enable`，具体请参见[通过HTTP调用](get-temporary-file-url.md#d6a1cb0f01h5k)。

<a id="a33377c69bwdq"></a>

#### 命令行参数说明

| 参数 | 是否必须 | 说明 | 示例 |
| --- | --- | --- | --- |
| oss.upload | 是 | dashscope的子命令，用于执行文件上传操作。 | oss.upload |
| \--model | 是 | 指定文件将要用于哪个模型。 | qwen3-vl-plus |
| \--file | 是 | 本地文件的路径。可以是相对路径或绝对路径。 | cat.png，/data/img.jpg |
| \--api\_key | 否 | 阿里云百炼API-KEY。如已配置环境变量，无需填写此参数。 | sk-xxxx |

<a id="步骤二-使用临时url调用模型"></a>

<a id="1c60469225ufa"></a>

## 步骤二：使用临时URL调用模型

<a id="使用限制-2"></a>

<a id="788832c151s25"></a>

#### 使用限制

-   **文件格式**：临时URL须通过上述方式生成，且以 `oss://`为前缀的URL字符串。
-   **文件未过期**：文件URL仍在上传后的48小时有效期内。
-   **模型一致**：模型调用所使用的模型必须与文件上传时指定的模型完全一致。
-   **账号一致**：模型调用的API KEY必须与文件上传时使用的API KEY同属一个阿里云主账号。

<a id="方式一-通过http调用"></a>

<a id="d6a1cb0f01h5k"></a>

#### 方式一：通过HTTP调用

通过curl、Postman或任何其他HTTP客户端直接调用API，则**必须遵循以下规则**：

> **重要**
>
> -   使用临时URL，**必须**在请求的**Header**中添加参数：`X-DashScope-OssResourceResolve: enable`。
> -   若缺失此Header，系统将无法解析`oss://`链接，请求将失败，报错信息请参考[错误码](get-temporary-file-url.md#3b9b15a6a8qkl)。

<a id="sec-tabs-4"></a>

<a id="请求示例"></a>

<a id="请求示例-h4"></a>

#### 请求示例

本示例为调用 qwen3-vl-plus 模型识别图片内容。

> **说明**
>
> 请将 `oss://...`替换为真实的临时 URL，否则请求将失败。

<a id="code-block-15"></a>

```bash
# 以下为北京地域 url，若使用新加坡地域，需将 url 替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-OssResourceResolve: enable' \
-d '{
  "model": "qwen3-vl-plus",
  "messages": [{
      "role": "user",
      "content":
      [{"type": "text","text": "这是什么"},
       {"type": "image_url","image_url": {"url": "oss://dashscope-instant/xxx/2024-07-18/xxxx/cat.png"}}]
    }]
}'
```

<a id="响应示例"></a>

<a id="响应示例-h4"></a>

#### 响应示例

<a id="code-block-16"></a>

```json
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
  "model": "qwen3-vl-plus",
  "id": "chatcmpl-cfc4f2aa-22a8-9a94-8243-44c5bd9899bc"
}
```

<a id="上传的本地图片示例"></a>

<a id="上传的本地图片示例-h4"></a>

#### 上传的本地图片示例

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5231249371/p915804.png)

<a id="方式二-通过dashscope-sdk调用"></a>

<a id="f0ce0f5987cpa"></a>

#### 方式二：通过DashScope SDK调用

您也可以使用阿里云百炼提供的 Python 或 Java SDK。

-   **直接传入 URL**：调用模型 SDK 时，直接将以`oss://`为前缀的URL字符串作为文件参数传入。
-   **无需关心 Header**：SDK 会自动添加必需的请求头，无需额外操作。

**注意**：并非所有模型都支持 SDK 调用，请以模型 API 文档为准。

> 不支持 OpenAI SDK。

<a id="sec-tabs-5"></a>

<a id="python-2"></a>

<a id="python-2-h4"></a>

#### Python

**前提条件**

请[安装DashScope Python SDK](../preparations/install-sdk.md)，且DashScope Python SDK版本号 >=`2.0.1`。

**示例代码**

本示例为调用 qwen3-vl-plus 模型识别图片内容。此代码示例仅适用于 qwen-vl 和 omni 系列模型。

<a id="sec-tabs-6"></a>

<a id="请求示例-2"></a>

<a id="请求示例-2-h4"></a>

#### 请求示例

> **说明**
>
> 请将 image 参数中的 `oss://...`替换为真实的临时 URL，否则请求将失败。

<a id="code-block-17"></a>

```python
import os
import dashscope

# 北京与新加坡地域的 API Key 不同，请使用对应地域的 API Key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
client = dashscope.Client(api_key=os.getenv('DASHSCOPE_API_KEY'))

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

response = client.multimodal.chat.create(
    model='qwen3-vl-plus',
    messages=messages
)

print(response.output_text)
```

<a id="响应示例-2"></a>

<a id="响应示例-2-h4"></a>

#### 响应示例

<a id="code-block-18"></a>

```json
{
    "request_id": "ccd9dcfb-98f0-92bc-xxxxxx",
    "choices": [
        {
            "index": 0,
            "finish_reason": "stop",
            "message": {
                "role": "assistant",
                "content": "这是一张一只猫在草地上奔跑的照片。猫的毛色主要是白色，带有浅棕色的斑点，眼睛是蓝色的，显得非常可爱。背景是一个模糊的绿色草地和一些树木，阳光照射下来，给整个画面增添了一种温暖的感觉。猫的姿态显示出它正在快速移动，可能是在追逐什么或只是在享受户外活动的乐趣。整体来看，这是一幅充满活力和生机的图片。"
            }
        }
    ],
    "usage": {
        "input_tokens": 1112,
        "output_tokens": 91,
        "total_tokens": 1203,
        "input_tokens_details": {
            "text_tokens": 21,
            "image_tokens": 1091
        },
        "output_tokens_details": {
            "text_tokens": 91
        }
    }
}
```

<a id="java-2"></a>

<a id="java-2-h4"></a>

#### Java

**前提条件**

请[安装DashScope Java SDK](../preparations/install-sdk.md)，且DashScope Java SDK版本号 >= `2.21.0`。

**示例代码**

本示例为调用 qwen3-vl-plus 模型识别图片内容。此代码示例仅适用于 qwen-vl 和 omni 系列模型。

<a id="sec-tabs-7"></a>

<a id="请求示例-3"></a>

<a id="请求示例-3-h4"></a>

#### 请求示例

> **说明**
>
> 请将 `oss://...`替换为真实的临时 URL，否则请求将失败。

<a id="code-block-19"></a>

```java
import com.alibaba.dashscope.aigc.multimodalconversation.*;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.Arrays;

public class MultiModalConversationUsage {

    private static final String modelName = "qwen3-vl-plus";

    // 北京与新加坡地域的 API Key 不同，请使用对应地域的 API Key
    // 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void simpleMultiModalConversationCall() throws ApiException, NoApiKeyException, UploadFileException {
        // 以下为北京地域 url，若使用新加坡地域，需将 url 替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
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

<a id="响应示例-3"></a>

<a id="响应示例-3-h4"></a>

#### 响应示例

<a id="code-block-20"></a>

```json
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

<a id="附接口说明"></a>

<a id="26fd68eaf04kx"></a>

## 附接口说明

在上述[获取临时URL](get-temporary-file-url.md#a363e01e741gu)的两种方式中，代码调用和命令行工具已集成以下三个步骤，简化文件上传操作。以下是各步骤的接口说明。

<a id="步骤1-获取文件上传凭证"></a>

<a id="32db94982cllx"></a>

#### 步骤1：获取文件上传凭证

<a id="daa30479cemad"></a>

##### 前提条件

您需要已[获取与配置 API Key](../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="cd5c7c20fb74b"></a>

##### 请求接口

<a id="code-block-21"></a>

```http
北京地域：GET https://dashscope.aliyuncs.com/api/v1/uploads
新加坡地域：GET https://dashscope-intl.aliyuncs.com/api/v1/uploads
```

> **重要**
>
> 文件上传凭证接口限流为 100 QPS（按“阿里云主账号+模型”维度），且临时存储不可扩容。生产环境或高并发场景请使用[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)等存储服务。

<a id="c606afaf252dg"></a>

##### 入参描述

<table><thead><tr><th><p><strong>传参方式</strong></p></th><th><p><strong>字段</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必选</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>Header</p></td><td><p>Content-Type</p></td><td><p><em>string</em></p></td><td><p>是</p></td><td><p>请求类型：application/json 。</p></td><td><p>application/json</p></td></tr><tr><td><p>Authorization</p></td><td><p><em>string</em></p></td><td><p>是</p></td><td><p>阿里云百炼API Key，例如：Bearer sk-xxx。</p></td><td><p>Bearer sk-xxx</p></td></tr><tr><td rowspan="2"><p>Params</p></td><td><p>action</p></td><td><p><em>string</em></p></td><td><p>是</p></td><td><p>操作类型，当前场景为<code>getPolicy</code>。</p></td><td><p>getPolicy</p></td></tr><tr><td><p>model</p></td><td><p><em>string</em></p></td><td><p>是</p></td><td><p>需要调用的模型名称。</p></td><td><p>qwen3-vl-plus</p></td></tr></tbody></table>

<a id="58595f510c3zl"></a>

##### 出参描述

| 字段 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| request\_id | _string_ | 本次请求的系统唯一码。 | 7574ee8f-...-11c33ab46e51 |
| data | _object_ | \- | \- |
| data.policy | _string_ | 上传凭证。 | eyJl...1ZSJ9XX0= |
| data.signature | _string_ | 上传凭证的签名。 | g5K...d40= |
| data.upload\_dir | _string_ | 上传文件的目录。 | dashscope-instant/xxx/2024-07-18/xxxx |
| data.upload\_host | _string_ | 上传的host地址。 | [https://dashscope-file-xxx.oss-cn-beijing.aliyuncs.com](https://dashscope-file-xxx.oss-cn-beijing.aliyuncs.com) |
| data.expire\_in\_seconds | _string_ | 凭证有效期（单位：秒）。<br><br>过期后，重新调用本接口获取新的凭证。 | 300 |
| data.max\_file\_size\_mb | _string_ | 本次允许上传的最大文件的大小（单位：MB）。<br><br>该值与需要访问的模型相关。 | 100 |
| data.capacity\_limit\_mb | _string_ | 同一个主账号每天上传容量限制（单位：MB）。 | 999999999 |
| data.oss\_access\_key\_id | _string_ | 用于上传的access key。 | LTAxxx |
| data.x\_oss\_object\_acl | _string_ | 上传文件的访问权限，`private`表示私有。 | private |
| data.x\_oss\_forbid\_overwrite | _string_ | 文件同名时是否可以覆盖，`true`表示不可覆盖。 | true |

<a id="2fcbfbaf30a0f"></a>

##### 请求示例

<a id="code-block-22"></a>

```bash
# 以下为北京地域 url，若使用新加坡地域，需将 url 替换为：https://dashscope-intl.aliyuncs.com/api/v1/uploads
curl --location 'https://dashscope.aliyuncs.com/api/v1/uploads?action=getPolicy&model=qwen3-vl-plus' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

> **说明**
>
> 若未配置阿里云百炼API Key到环境变量，请将`$DASHSCOPE_API_KEY`替换为实际API Key，例如：`--header "Authorization: Bearer sk-xxx"`。

<a id="响应示例-4"></a>

<a id="615ec0a5ed3lr"></a>

#### 响应示例

<a id="code-block-23"></a>

```json
{
    "request_id": "52f4383a-c67d-9f8c-xxxxxx",
    "data": {
        "policy": "eyJl...1ZSJ=",
        "signature": "YOUR_SIGNATURE",
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

<a id="步骤2-上传文件至临时存储空间"></a>

<a id="9bfba9d00bb8k"></a>

#### 步骤2：上传文件至临时存储空间

<a id="前提条件"></a>

<a id="0d33d16fe2jue"></a>

#### 前提条件

-   已获取文件上传凭证。
    
-   确保文件上传凭证在有效期内，若凭证过期，请重新调用步骤1的接口获取新的凭证。
    
    > 查看文件上传凭证有效期：步骤1的输出参数`data.expire_in_seconds`为凭证有效期，单位为秒。
    

<a id="请求接口"></a>

<a id="6215233bf0bl2"></a>

#### 请求接口

<a id="code-block-24"></a>

```http
POST {data.upload_host}
```

> **说明**
>
> 请将{data.upload\_host}替换为步骤1的输出参数`data.upload_host`对应的值。

<a id="入参描述"></a>

<a id="22dc4afc8cadg"></a>

#### 入参描述

<table><thead><tr><th><strong>传参方式</strong></th><th><strong>字段</strong></th><th><strong>类型</strong></th><th><strong>必选</strong></th><th><strong>描述</strong></th><th><strong>示例值</strong></th></tr></thead><tbody><tr><td><p>Header</p></td><td><p>Content-Type</p></td><td><p><em>string</em></p></td><td><p>否</p></td><td><p>提交表单必须为<code>multipart/form-data</code>。</p><p>在提交表单时，Content-Type会以<code>multipart/form-data;boundary=xxxxxx</code>的形式展示。</p><blockquote><p>boundary 是自动生成的随机字符串，无需手动指定。若使用 SDK 拼接表单，SDK 也会自动生成该随机值。</p></blockquote></td><td><p>multipart/form-data; boundary=9431149156168</p></td></tr><tr><td rowspan="8"><p>form-data</p></td><td><p>OSSAccessKeyId</p></td><td><p><em>text</em></p></td><td><p>是</p></td><td><p>文件上传凭证接口的输出参数 <code>data.oss_access_key_id</code> 的值。</p></td><td><p>LTAm5xxx</p></td></tr><tr><td><p>policy</p></td><td><p><em>text</em></p></td><td><p>是</p></td><td><p>文件上传凭证接口的输出参数 <code>data.policy</code> 的值。</p></td><td><p>g5K...d40=</p></td></tr><tr><td><p>Signature</p></td><td><p><em>text</em></p></td><td><p>是</p></td><td><p>文件上传凭证接口的输出参数 <code>data.signature</code> 的值。</p></td><td><p>YOUR_SIGNATURE</p></td></tr><tr><td><p>key</p></td><td><p><em>text</em></p></td><td><p>是</p></td><td><p>文件上传凭证接口的输出参数 <code>data.upload_dir</code> 的值拼接上<code>/ 文件名</code>。</p></td><td><p>例如，<code>upload_dir</code> 为 <code>dashscope-instant/xxx/2024-07-18/xxx</code>，需要上传的文件名为 <code>cat.png</code>，拼接后的完整路径为：</p><p><code>dashscope-instant/xxx/2024-07-18/xxx/cat.png</code></p></td></tr><tr><td><p>x-oss-object-acl</p></td><td><p><em>text</em></p></td><td><p>是</p></td><td><p>文件上传凭证接口的输出参数 <code>data.x_oss_object_acl</code> 的值。</p></td><td><p>private</p></td></tr><tr><td><p>x-oss-forbid-overwrite</p></td><td><p><em>text</em></p></td><td><p>是</p></td><td><p>文件上传凭证接口的输出参数中<code>data.x_oss_forbid_overwrite</code> 的值。</p></td><td><p>true</p></td></tr><tr><td><p>success_action_status</p></td><td><p><em>text</em></p></td><td><p>否</p></td><td><p>通常取值为 200，上传完成后接口返回 HTTP code 200，表示操作成功。</p></td><td><p>200</p></td></tr><tr><td><p>file</p></td><td><p><em>text</em></p></td><td><p>是</p></td><td><p>文件或文本内容。</p><div><div><p><strong>说明</strong></p><ul><li>一次只支持上传一个文件。</li><li>file必须为最后一个表单域，除file以外的其他表单域并无顺序要求。</li></ul></div></div></td><td><p>例如，待上传文件<code>cat.png</code>在Linux系统中的存储路径为<code>/tmp</code>，则此处应为<code>file=@&quot;/tmp/cat.png&quot;</code>。</p></td></tr></tbody></table>

<a id="出参描述"></a>

<a id="ec61f03079vzk"></a>

#### 出参描述

调用成功时，本接口无任何参数输出。

<a id="请求示例-4"></a>

<a id="daa0012d98vst"></a>

#### 请求示例

<a id="code-block-25"></a>

```bash
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

<a id="步骤3-生成文件url"></a>

<a id="7c1b018ab4hwv"></a>

#### 步骤3：生成文件URL

文件URL拼接逻辑：`oss://` + `key` （步骤2的入参`key`）。该URL有效期为 48 小时。

<a id="code-block-26"></a>

```text
oss://dashscope-instant/xxx/2024-07-18/xxxx/cat.png
```

<a id="错误码"></a>

<a id="3b9b15a6a8qkl"></a>

## 错误码

如果接口调用失败并返回报错信息，请参见[错误码](../preparations/error-code.md)进行解决。

本文的API还有特定状态码，具体如下所示。

<table><thead><tr><th><strong>HTTP状态码</strong></th><th><strong>接口错误码（code）</strong></th><th><strong>接口错误信息（message）</strong></th><th><strong>含义说明</strong></th></tr></thead><tbody><tr><td><p>400</p></td><td><p>invalid_parameter_error</p></td><td><p>InternalError.Algo.InvalidParameter: The provided URL does not appear to be valid. Ensure it is correctly formatted.</p></td><td><p>无效URL，请检查URL是否填写正确。</p><blockquote><p>若使用临时文件URL，需确保请求的 Header 中添加了参数 <code>X-DashScope-OssResourceResolve: enable</code>。</p></blockquote></td></tr><tr><td><p>400</p></td><td><p>InvalidParameter.DataInspection</p></td><td><p>The media format is not supported or incorrect for the data inspection.</p></td><td><p>可能的原因有：</p><ul><li>请求Header 缺少必要参数，请设置 <code>X-DashScope-OssResourceResolve: enable</code><strong>。</strong></li><li>上传的图片格式不符合模型要求，更多信息请参见<a href="../preparations/error-code.md">错误码</a>。</li></ul></td></tr><tr><td><p>403</p></td><td><p>AccessDenied</p></td><td><p>Invalid according to Policy: Policy expired.</p></td><td><p>文件上传凭证已经过期。</p><p>请重新调用<a href="get-temporary-file-url.md#32db94982cllx">文件上传凭证接口</a>生成新凭证。</p></td></tr><tr><td><p>429</p></td><td><p>Throttling.RateQuota</p></td><td><p>Requests rate limit exceeded, please try again later.</p></td><td><p>调用频次触发限流。</p><p><a href="get-temporary-file-url.md#32db94982cllx">文件上传凭证接口</a>限流为 100 QPS（按阿里云主账号 + 模型维度）。触发限流后，建议降低请求频率，或迁移至 OSS 等自有存储服务以规避限制。</p></td></tr></tbody></table>

<a id="常见问题"></a>

<a id="b5dbd90a80t4l"></a>

## 常见问题

<a id="q-使用oss-前缀的-url-调用时报错-该如何处理"></a>

<a id="8eb407980dybc"></a>

#### Q：使用`oss://`前缀的 URL 调用时报错，该如何处理？

A：请按以下步骤排查：

1.  **检查请求头（Header）**：  
    若您通过 HTTP（如 Postman、curl）直接调用，**必须在**`Header`**中添加参数**`X-DashScope-OssResourceResolve: enable`。未添加该参数会导致服务端无法识别 OSS 内部协议。关于请求头配置，请参见[通过HTTP调用](get-temporary-file-url.md#d6a1cb0f01h5k)。
2.  **检查 URL 有效性**：  
    `oss://` 链接为临时 URL，请确保该链接是48小时内生成的。如果链接已过期，请重新上传文件获取新的 URL。

<a id="q-文件上传与模型调用使用的api-key可以不一样吗"></a>

<a id="72fd224ef9nv0"></a>

#### Q：文件上传与模型调用使用的API KEY可以不一样吗？

A：文件存储和访问权限基于阿里云主账号管理，API Key 仅为主账号的访问凭证。

因此，同一阿里云主账号下的不同 API Key 可正常使用，不同主账号的 API Key因账号隔离，模型调用无法跨账号读取文件。

请确保文件上传与模型调用使用的 API Key 属于同一阿里云主账号。
