# 向量化（Embedding）

向量化模型可将文本、图像、视频等数据转换为数值向量，用于语义搜索、推荐、聚类、分类、异常检测等下游任务。

<a id="准备工作"></a>

<a id="5a258c65c3ixb"></a>

## 准备工作

您需要已[获取与配置 API Key](../../../model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过OpenAI SDK或DashScope SDK进行调用，还需要[安装SDK](../../../model-api-reference/preparations/install-sdk.md)。

<a id="获取embedding"></a>

<a id="eb8eea2b1cr5n"></a>

## 获取Embedding

<a id="sec-tabs"></a>

<a id="文本信息向量"></a>

<a id="文本信息向量-h4"></a>

#### 文本信息向量

调用API时，需在请求中同时指定要向量化的文本内容和所使用的模型名称。

<a id="sec-tabs-2"></a>

<a id="openai兼容接口"></a>

<a id="openai兼容接口-h4"></a>

#### OpenAI兼容接口

<a id="fig-code-group"></a>

<a id="fig-code-group-python-tab"></a>

python

<a id="code-code-group-python"></a>

```python
import os
from openai import OpenAI

input_text = "衣服的质量杠杠的"

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

completion = client.embeddings.create(
    model="qwen3.7-text-embedding",
    input=input_text
)

print(completion.model_dump_json())
```

<a id="fig-code-group-javascript-tab"></a>

javascript

<a id="code-code-group-javascript"></a>

```javascript
const OpenAI = require("openai");

const openai = new OpenAI({
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey:'sk-xxx',
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下是北京地域base-url，如果使用新加坡地域的模型，需要将baseURL替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

async function getEmbedding() {
    try {
        const inputTexts = "衣服的质量杠杠的";
        const completion = await openai.embeddings.create({
            model: "qwen3.7-text-embedding",
            input: inputTexts
        });

        console.log(JSON.stringify(completion, null, 2));
    } catch (error) {
        console.error('Error:', error);
    }
}

getEmbedding();
```

<a id="fig-code-group-bash-tab"></a>

bash

<a id="code-code-group-bash"></a>

```bash
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3.7-text-embedding",
    "input": "衣服的质量杠杠的"
}'
```

<a id="dashscope"></a>

<a id="dashscope-h4"></a>

#### DashScope

<a id="fig-code-group-2"></a>

<a id="fig-code-group-2-python-tab"></a>

python

<a id="code-code-group-2-python"></a>

```python
import os
import dashscope
# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
input_text = "衣服的质量杠杠的"
resp = client.embeddings.create(
    model="qwen3.7-text-embedding",
    input=input_text,
)

print(resp)
```

<a id="fig-code-group-2-java-tab"></a>

java

<a id="code-code-group-2-java"></a>

```java
import com.alibaba.dashscope.embeddings.TextEmbedding;
import com.alibaba.dashscope.embeddings.TextEmbeddingParam;
import com.alibaba.dashscope.embeddings.TextEmbeddingResult;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

import java.util.Collections;

public class Main {
    // 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的配置不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static void main(String[] args) {
        String inputTexts = "衣服的质量杠杠的";
        try {
            // 构建请求参数
            TextEmbeddingParam param = TextEmbeddingParam
                    .builder()
                    .model("qwen3.7-text-embedding")
                    // 输入文本
                    .texts(Collections.singleton(inputTexts))
                    .build();

            // 创建模型实例并调用
            TextEmbedding textEmbedding = new TextEmbedding();
            TextEmbeddingResult result = textEmbedding.call(param);

            // 输出结果
            System.out.println(result);

        } catch (NoApiKeyException e) {
            // 捕获并处理API Key未设置的异常
            System.err.println("调用 API 时发生异常: " + e.getMessage());
            System.err.println("请检查您的 API Key 是否已正确配置。");
            e.printStackTrace();
        }
    }
}
```

<a id="fig-code-group-2-bash-tab"></a>

bash

<a id="code-code-group-2-bash"></a>

```bash
# ======= 重要提示 =======
# 各地域API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，各地域的URL不同。
# === 执行时请删除该注释 ===
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3.7-text-embedding",
    "input": {
        "texts": [
        "衣服的质量杠杠的"
        ]
    }
}'
```

<a id="多模态独立向量"></a>

<a id="多模态独立向量-h4"></a>

#### 多模态独立向量

可为文本、图片、视频等不同模态的内容分别生成独立的向量，适用于需要单独处理每种内容类型的场景。

> 多模态独立向量化功能需要通过 DashScope SDK 或 API 来调用，不支持 OpenAI 兼容接口调用或在控制台直接使用。

<a id="fig-code-group-3"></a>

<a id="fig-code-group-3-python-tab"></a>

Python

<a id="code-code-group-3-python"></a>

```python
import dashscope
import json
import os
# 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 输入可以是视频
# video = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"
# input = [{'video': video}]
# 或图片
image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"
input = [{'image': image}]
resp = client.multimodal.embeddings.create(
    model="tongyi-embedding-vision-plus",
    input=input
)

print(json.dumps(resp.model_dump(), indent=4))
```

<a id="fig-code-group-3-java-tab"></a>

Java

<a id="code-code-group-3-java"></a>

```java
import com.alibaba.dashscope.embeddings.MultiModalEmbedding;
import com.alibaba.dashscope.embeddings.MultiModalEmbeddingItemImage;
import com.alibaba.dashscope.embeddings.MultiModalEmbeddingItemVideo;
import com.alibaba.dashscope.embeddings.MultiModalEmbeddingParam;
import com.alibaba.dashscope.embeddings.MultiModalEmbeddingResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

import java.util.Collections;

public class Main {
    // 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的配置不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static void main(String[] args) {
        try {
            MultiModalEmbedding embedding = new MultiModalEmbedding();
            // 输入可以是视频
            // MultiModalEmbeddingItemVideo video = new MultiModalEmbeddingItemVideo(
            //     "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4");
            // 或图片
            MultiModalEmbeddingItemImage image = new MultiModalEmbeddingItemImage(
                "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png");

            MultiModalEmbeddingParam param = MultiModalEmbeddingParam.builder()
                .model("tongyi-embedding-vision-plus")
                .contents(Collections.singletonList(image))
                .build();

            MultiModalEmbeddingResult result = embedding.call(param);
            System.out.println(result);

        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.err.println("调用 API 时发生异常: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

<a id="多模态融合向量"></a>

<a id="多模态融合向量-h4"></a>

#### 多模态融合向量

可将文本、图片、视频等不同模态的内容融合成一个融合向量，适用于文搜图、图搜图、文搜视频、跨模态检索等场景。

> 多模态融合向量功能需要通过 Python DashScope SDK 或 API 来调用，暂不支持 OpenAI 兼容接口、Java DashScope SDK 调用或在控制台直接使用。

-   `qwen3-vl-embedding`：同时支持融合向量和独立向量生成。在多模态独立向量的基础上增加 bool 类型字段 `enable_fusion`，当 `enable_fusion=true` 时返回融合向量。
-   `qwen2.5-vl-embedding`：仅支持融合向量，不支持独立向量。
-   `tongyi-embedding-vision-plus-2026-03-06` 和 `tongyi-embedding-vision-flash-2026-03-06`：同时支持融合向量和独立向量。融合向量通过将 text、image、video 放在同一个 content 对象中实现，无需 enable\_fusion 参数。

<a id="sec-tabs-3"></a>

<a id="python"></a>

<a id="python-h4"></a>

#### Python

<a id="code-block"></a>

```python
import dashscope
import json
import os
# 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 多模态融合向量：将文本、图片、视频融合成一个融合向量
# 适用于跨模态检索、图搜等场景
text = "这是一段测试文本，用于生成多模态融合向量"
image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"
video = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"

# 输入包含文本、图片、视频，通过 enable_fusion 参数生成融合向量
input_data = [
    {"text": text},
    {"image": image},
    {"video": video}
]

# 使用 qwen3-vl-embedding 生成融合向量
resp = client.multimodal.embeddings.create(
    model="qwen3-vl-embedding",
    input=input_data,
    enable_fusion=True,
    # 可选参数：指定向量维度（支持 2560, 2048, 1536, 1024, 768, 512, 256，默认 2560）
    # dimension = 1024
)

print(json.dumps(resp.model_dump(), indent=4))
```

以下示例使用 `tongyi-embedding-vision-plus-2026-03-06` 生成融合向量。与 `qwen3-vl-embedding` 不同，该模型通过将 text、image、video 放在同一个 content 对象中实现融合，无需 `enable_fusion` 参数。

<a id="code-block-2"></a>

```python
import dashscope
import json
import os
# 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# tongyi-embedding-vision-plus-2026-03-06 融合向量示例
# 将 text、image 放在同一个 content 对象中，无需 enable_fusion 参数
text = "白色运动鞋，轻量透气，适合跑步和日常穿着"
image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"

# 同一对象中的多模态内容会被融合为 1 个向量（type 为 "fused"）
input_data = [
    {"text": text, "image": image}
]

resp = client.multimodal.embeddings.create(
    model="tongyi-embedding-vision-plus-2026-03-06",
    input=input_data,
    # 可选参数：指定向量维度（支持 1152, 1024, 512, 256, 128, 64，默认 1152）
    dimension=1152
)

print(json.dumps(resp.model_dump(), indent=4))
```

<a id="java-http"></a>

<a id="java-http-h4"></a>

#### Java（HTTP）

<a id="code-block-3"></a>

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Main {
    public static void main(String[] args) throws Exception {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx";
        String apiKey = System.getenv("DASHSCOPE_API_KEY");

        // 多模态融合向量：通过 enable_fusion 将文本、图片、视频融合成一个融合向量
        String requestBody = "{"
                + "\"model\": \"qwen3-vl-embedding\","
                + "\"input\": {"
                + "  \"contents\": ["
                + "    {\"text\": \"这是一段测试文本，用于生成多模态融合向量\"},"
                + "    {\"image\": \"https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png\"},"
                + "    {\"video\": \"https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4\"}"
                + "  ]"
                + "},"
                + "\"parameters\": {"
                + "  \"enable_fusion\": true"
                + "}"
                + "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding"))
                .header("Authorization", "Bearer " + apiKey)
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());
    }
}
```

以下示例使用 `tongyi-embedding-vision-plus-2026-03-06` 生成融合向量。与 `qwen3-vl-embedding` 不同，该模型通过将 text、image 放在同一个 content 对象中实现融合，无需 `enable_fusion` 参数。

<a id="code-block-4"></a>

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class Main {
    public static void main(String[] args) throws Exception {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx";
        String apiKey = System.getenv("DASHSCOPE_API_KEY");

        // tongyi-embedding-vision-plus-2026-03-06 融合向量
        // 将 text、image 放在同一个 content 对象中，无需 enable_fusion 参数
        String requestBody = "{"
                + "\"model\": \"tongyi-embedding-vision-plus-2026-03-06\","
                + "\"input\": {"
                + "  \"contents\": ["
                + "    {"
                + "      \"text\": \"白色运动鞋，轻量透气，适合跑步和日常穿着\","
                + "      \"image\": \"https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png\""
                + "    }"
                + "  ]"
                + "},"
                + "\"parameters\": {"
                + "  \"dimension\": 1152"
                + "}"
                + "}";

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding"))
                .header("Authorization", "Bearer " + apiKey)
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());
    }
}
```

<a id="模型选择"></a>

<a id="a74af50386cer"></a>

## 模型选择

选择合适的模型取决于您的输入数据类型和应用场景。

-   **处理纯文本或代码**：推荐使用`qwen3.7-text-embedding` 。它是当前性能最强的模型，支持任务指令（instruct）、稀疏向量等高级功能，能覆盖绝大多数文本处理场景。若更关注成本与吞吐，可使用轻量版 `qwen3.7-text-embedding-flash`，它同样支持任务指令（instruct）与三种向量输出类型，并保持 201 种语言和 128K 上下文，向量维度可在 256~1024 范围内选择。
    
-   **处理多模态内容**：
    
    -   **融合向量：**若要将单模态或混合模态输入表征为融合向量，适用于跨模态检索、图搜等场景，可使用 `qwen2.5-vl-embedding`、`qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 或 `tongyi-embedding-vision-flash-2026-03-06`。例如，输入一张衬衫图片并附加文本”找相似风格但更显年轻的款式”，模型能将图像和文本指令融合成一个向量进行理解。
    -   **独立向量：**若要为每个输入（如图片和其对应的文字标题）生成独立的向量，可选择 `tongyi-embedding-vision-plus`、`tongyi-embedding-vision-flash`、`tongyi-embedding-vision-plus-2026-03-06`、`tongyi-embedding-vision-flash-2026-03-06` 或通用多模态模型`multimodal-embedding-v1`为每个输入部分（图片、文字）生成一个独立的向量。
-   **处理大规模数据**：若您需要处理大规模、非实时的文本数据，建议使用 `qwen3.7-text-embedding`、`qwen3.7-text-embedding-flash` 或 `text-embedding-v4` 并结合 [OpenAI兼容-Batch调用](../../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，以显著降低成本。
    

下表包含所有可用向量化模型的详细规格。

<a id="文本向量"></a>

<a id="ee47f9d186aa2"></a>

### 文本向量

<a id="sec-tabs-4"></a>

<a id="北京"></a>

<a id="北京-h4"></a>

#### 北京

<table><thead><tr><th><strong>模型名称</strong></th><th><strong>向量维度</strong></th><th><strong>批次大小</strong></th><th><p><strong>单批次最大处理Token数（</strong><a href="https://help.aliyun.com/zh/model-studio/billing-for-model-studio">注</a><strong>）</strong></p></th><th><strong>单价（每千输入Token）</strong></th><th><p><strong>免费额度</strong><a href="../../test-1/new-free-quota.md#977b13081ab56">（注）</a></p></th><th><strong>支持语种</strong></th></tr></thead><tbody><tr><td><p>qwen3.7-text-embedding</p></td><td><p>2560、2,048、1,536、1,024（默认）、768、512、256</p></td><td><p>20</p></td><td><p>128,000</p></td><td><p>0.0005元</p><p><a href="../../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch接口调用</a>：0.00025元</p></td><td><p>100万Token</p><p>有效期：自开通百炼/模型发布/申请通过之日起90天（以较晚者为准）</p></td><td rowspan="2"><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等201种主流语种与方言</p><a id="accordion-所有支持语言"></a><section><p>所有支持语言</p><div><p><strong>汉藏语系</strong>：中文（简体中文、繁体中文、粤语）、缅甸语、藏语、梅泰语</p><p><strong>印欧语系</strong>：英语、法语、葡萄牙语、德语、罗马尼亚语、瑞典语、丹麦语、保加利亚语、俄语、捷克语、希腊语、乌克兰语、西班牙语、荷兰语、斯洛伐克语、克罗地亚语、波兰语、立陶宛语、挪威语（博克马尔语）、挪威尼诺斯克语、波斯语、斯洛文尼亚语、古吉拉特语、拉脱维亚语、意大利语、奥克语、尼泊尔语、马拉地语、白俄罗斯语、塞尔维亚语、卢森堡语、威尼斯语、阿萨姆语、威尔士语、西里西亚语、阿斯图里亚语、恰蒂斯加尔语、阿瓦德语、迈蒂利语、博杰普尔语、信德语、爱尔兰语、法罗语、印地语、旁遮普语、孟加拉语、奥里雅语、塔吉克语、东意第绪语、伦巴第语、利古里亚语、西西里语、弗留利语、撒丁岛语、加利西亚语、加泰罗尼亚语、冰岛语、托斯克语、阿尔巴尼亚语、林堡语、罗马尼亚语、达里语、南非荷兰语、马其顿语僧伽罗语、乌尔都语、马加希语、波斯尼亚语、亚美尼亚语、拉特加利亚语、苏格兰盖尔语、中库尔德语、北库尔德语、南普什图语、梵语、敦达里语、马尔瓦里语、阿希拉尼语、巴盖利语、巴格里语、本德利语、布拉吉语、库马翁语、克什米尔语</p><p><strong>亚非语系</strong>：阿拉伯语（标准语、内志语、黎凡特语、埃及语、摩洛哥语、美索不达米亚语、塔伊兹-阿德尼语、突尼斯语、海湾语、阿尔及利亚语、苏丹语、利比亚语）、希伯来语、马耳他语、阿姆哈拉语、提格里尼亚语、卡比尔语、索马里语、西中奥罗莫语、豪萨语</p><p><strong>南岛语系</strong>：印度尼西亚语、马来语、他加禄语、宿务语、爪哇语、巽他语、米南加保语、巴厘岛语、班加语、邦阿西楠语、伊洛科语、瓦雷语（菲律宾）、高原马达加斯加语、马达加斯加语、布吉语、毛利语、萨摩亚语、夏威夷语、斐济语</p><p>德拉威语：泰米尔语、泰卢固语、卡纳达语、马拉雅拉姆语</p><p>突厥语系：土耳其语、北阿塞拜疆语、北乌兹别克语、哈萨克语、巴什基尔语、鞑靼语、克里米亚鞑靼语、吉尔吉斯语、土库曼语、维吾尔语</p><p><strong>壮侗语系</strong>：泰语、老挝语、掸语</p><p><strong>乌拉尔语系</strong>：芬兰语、爱沙尼亚语、匈牙利语、草原马里语</p><p><strong>南亚语系</strong>：越南语、高棉语</p><p><strong>尼日尔-刚果语系</strong>：约鲁巴语、埃维语、卢旺达语、林加拉语、北索托语、尼扬贾语、绍纳语、南索托语、茨瓦纳语、科萨语、祖鲁语、卢干达语、斯瓦蒂语、聪加语、通布卡语、文达语、乔奎语、卢巴-卡赛语、隆迪语、姆本杜语、基库尤语、刚果语、尼日利亚富拉语、沃洛夫语、丰语、卡比耶语、莫西语、阿坎语、特维语、班巴拉语、伊博语</p><p><strong>其他</strong>：日语、韩语、格鲁吉亚语、巴斯克语、海地语、帕皮阿门托语、卡布维尔迪亚努语、托克皮辛语、斯瓦希里语、中部艾马拉语、图卢语、那加语、尼日利亚皮钦语、毛里求斯克里奥尔语、桑戈语、阿亚库乔克丘亚语、喀尔喀蒙古语、西南丁卡语、努埃尔语、瓜拉尼语</p></div></section></td></tr><tr><td><p>qwen3.7-text-embedding-flash</p></td><td><p>1,024（默认）、768、512、256</p></td><td><p>20</p></td><td><p>128,000</p></td><td><p>0.000125元</p><p><a href="../../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch接口调用</a>：0.000063元</p></td><td><p>100万Token</p><p>有效期：自开通百炼/模型发布/申请通过之日起90天（以较晚者为准）</p></td></tr><tr><td><p>text-embedding-v4</p><blockquote><p>属于<a href="https://qwenlm.github.io/zh/blog/qwen3-embedding/">Qwen3-Embedding</a>系列</p></blockquote></td><td><p>2,048、1,536、1,024（默认）、768、512、256、128、64</p></td><td rowspan="2"><p>10</p></td><td><p>33,000</p></td><td><p>0.0005元</p><p><a href="../../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch接口调用</a>：0.00025元</p></td><td><p>100万Token</p><p>有效期：自开通百炼/模型发布/申请通过之日起90天（以较晚者为准）</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等100+主流语种</p></td></tr><tr><td><p>text-embedding-v3</p></td><td><p>1,024（默认）、768、512、256、128或64</p></td><td><p>8,192</p></td><td><p>0.0005元</p><p><a href="../../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch接口调用</a>：0.00025元</p></td><td rowspan="3"><p>无免费额度</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等50+主流语种</p></td></tr><tr><td><p>text-embedding-v2</p></td><td rowspan="4"><p>1,536</p></td><td rowspan="2"><p>25</p></td><td rowspan="4"><p>2,048</p></td><td rowspan="2"><p>0.0007元</p><p><a href="../../../model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">Batch接口调用</a>：0.00035元</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语</p></td></tr><tr><td><p>text-embedding-v1</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语</p></td></tr><tr><td><p>text-embedding-async-v2</p></td><td rowspan="2"><p>100,000</p></td><td rowspan="2"><p>0.0007元</p></td><td><p>2000万Token</p><p>有效期：自开通百炼/模型发布/申请通过之日起90天（以较晚者为准）</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语</p></td></tr><tr><td><p>text-embedding-async-v1</p></td><td><p>无免费额度</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语</p></td></tr></tbody></table>

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

<table><thead><tr><th><strong>模型名称</strong></th><th><strong>向量维度</strong></th><th><strong>批次大小</strong></th><th><p><strong>单批次最大处理Token数（</strong><a href="https://help.aliyun.com/zh/model-studio/billing-for-model-studio">注</a><strong>）</strong></p></th><th><strong>单价（每千输入Token）</strong></th><th><p><strong>免费额度</strong><a href="../../test-1/new-free-quota.md#977b13081ab56">（注）</a></p></th><th><strong>支持语种</strong></th></tr></thead><tbody><tr><td><p>qwen3.7-text-embedding</p></td><td><p>2560、2,048、1,536、1,024（默认）、768、512、256</p></td><td><p>20</p></td><td><p>128,000</p></td><td><p>0.000525元</p></td><td rowspan="3"><p>无免费额度</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等201种主流语种与方言</p><a id="accordion-所有支持语言-2"></a><section><p>所有支持语言</p><div><p><strong>汉藏语系</strong>：中文（简体中文、繁体中文、粤语）、缅甸语、藏语、梅泰语</p><p><strong>印欧语系</strong>：英语、法语、葡萄牙语、德语、罗马尼亚语、瑞典语、丹麦语、保加利亚语、俄语、捷克语、希腊语、乌克兰语、西班牙语、荷兰语、斯洛伐克语、克罗地亚语、波兰语、立陶宛语、挪威语（博克马尔语）、挪威尼诺斯克语、波斯语、斯洛文尼亚语、古吉拉特语、拉脱维亚语、意大利语、奥克语、尼泊尔语、马拉地语、白俄罗斯语、塞尔维亚语、卢森堡语、威尼斯语、阿萨姆语、威尔士语、西里西亚语、阿斯图里亚语、恰蒂斯加尔语、阿瓦德语、迈蒂利语、博杰普尔语、信德语、爱尔兰语、法罗语、印地语、旁遮普语、孟加拉语、奥里雅语、塔吉克语、东意第绪语、伦巴第语、利古里亚语、西西里语、弗留利语、撒丁岛语、加利西亚语、加泰罗尼亚语、冰岛语、托斯克语、阿尔巴尼亚语、林堡语、罗马尼亚语、达里语、南非荷兰语、马其顿语僧伽罗语、乌尔都语、马加希语、波斯尼亚语、亚美尼亚语、拉特加利亚语、苏格兰盖尔语、中库尔德语、北库尔德语、南普什图语、梵语、敦达里语、马尔瓦里语、阿希拉尼语、巴盖利语、巴格里语、本德利语、布拉吉语、库马翁语、克什米尔语</p><p><strong>亚非语系</strong>：阿拉伯语（标准语、内志语、黎凡特语、埃及语、摩洛哥语、美索不达米亚语、塔伊兹-阿德尼语、突尼斯语、海湾语、阿尔及利亚语、苏丹语、利比亚语）、希伯来语、马耳他语、阿姆哈拉语、提格里尼亚语、卡比尔语、索马里语、西中奥罗莫语、豪萨语</p><p><strong>南岛语系</strong>：印度尼西亚语、马来语、他加禄语、宿务语、爪哇语、巽他语、米南加保语、巴厘岛语、班加语、邦阿西楠语、伊洛科语、瓦雷语（菲律宾）、高原马达加斯加语、马达加斯加语、布吉语、毛利语、萨摩亚语、夏威夷语、斐济语</p><p>德拉威语：泰米尔语、泰卢固语、卡纳达语、马拉雅拉姆语</p><p>突厥语系：土耳其语、北阿塞拜疆语、北乌兹别克语、哈萨克语、巴什基尔语、鞑靼语、克里米亚鞑靼语、吉尔吉斯语、土库曼语、维吾尔语</p><p><strong>壮侗语系</strong>：泰语、老挝语、掸语</p><p><strong>乌拉尔语系</strong>：芬兰语、爱沙尼亚语、匈牙利语、草原马里语</p><p><strong>南亚语系</strong>：越南语、高棉语</p><p><strong>尼日尔-刚果语系</strong>：约鲁巴语、埃维语、卢旺达语、林加拉语、北索托语、尼扬贾语、绍纳语、南索托语、茨瓦纳语、科萨语、祖鲁语、卢干达语、斯瓦蒂语、聪加语、通布卡语、文达语、乔奎语、卢巴-卡赛语、隆迪语、姆本杜语、基库尤语、刚果语、尼日利亚富拉语、沃洛夫语、丰语、卡比耶语、莫西语、阿坎语、特维语、班巴拉语、伊博语</p><p><strong>其他</strong>：日语、韩语、格鲁吉亚语、巴斯克语、海地语、帕皮阿门托语、卡布维尔迪亚努语、托克皮辛语、斯瓦希里语、中部艾马拉语、图卢语、那加语、尼日利亚皮钦语、毛里求斯克里奥尔语、桑戈语、阿亚库乔克丘亚语、喀尔喀蒙古语、西南丁卡语、努埃尔语、瓜拉尼语</p></div></section></td></tr><tr><td><p>text-embedding-v4</p><blockquote><p>属于<a href="https://qwenlm.github.io/zh/blog/qwen3-embedding/">Qwen3-Embedding</a>系列</p></blockquote></td><td><p>2,048、1,536、1,024（默认）、768、512、256、128、64</p></td><td rowspan="2"><p>10</p></td><td rowspan="2"><p>8,192</p></td><td rowspan="2"><p>0.000514元</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等100+主流语种</p></td></tr><tr><td><p>text-embedding-v3</p></td><td><p>1,024（默认）、768、512、256、128或64</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等50+主流语种</p></td></tr></tbody></table>

> **说明**
>
> 批次大小指单次API调用中能处理的文本数量上限。例如，text-embedding-v4的批次大小为10，意味着一次请求最多可传入10个文本进行向量化，且每个文本不得超过 8192 个Token。这个限制适用于：
>
> -   字符串数组输入：数组最多包含10个元素。
> -   文件输入：文本文件最多包含10行文本。

<a id="多模态向量"></a>

<a id="a05d738632511"></a>

### 多模态向量

模型根据用户的输入生成连续向量，这些输入可以是文本、图片或视频。适用于视频分类、图像分类、图文检索，以文/图搜图，以文/图搜视频等任务场景。

> 接口支持单段文本、单张图片或单个视频文件的上传，也允许不同类型组合（如文本+图片），部分模型支持同类型内容的多个输入（如多张图片），请参考具体模型的限制说明。

<a id="sec-tabs-5"></a>

<a id="北京-2"></a>

<a id="北京-2-h4"></a>

#### 北京

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>向量维度</strong></p></th><th><p><strong>文本长度限制</strong></p></th><th><p><strong>图片大小限制</strong></p></th><th><p><strong>视频大小限制</strong></p></th><th><p><strong>单价（每千输入Token）</strong></p></th><th><p><strong>免费额度</strong><a href="../../test-1/new-free-quota.md#977b13081ab56">（注）</a></p></th></tr></thead><tbody><tr><td><p>qwen3-vl-embedding</p></td><td><p>2560（默认）, 2048, 1536, 1024, 768, 512, 256</p></td><td rowspan="2"><p>32,000 Token</p></td><td><p>单张大小不超过<strong>10 MB</strong></p></td><td rowspan="2"><p>视频文件大小不超过 <strong>50 MB</strong></p></td><td rowspan="2"><p>图片/视频：0.0018元</p><p>文本：0.0007元</p></td><td><p>100万Token</p><p>有效期：自开通百炼/模型发布/申请通过之日起90天（以较晚者为准）</p></td></tr><tr><td><p>qwen2.5-vl-embedding</p></td><td><p>2048, 1024（默认）, 768, 512</p></td><td><p>单张大小不超过<strong>5 MB</strong></p></td><td><p>无免费额度</p></td></tr><tr><td><p>tongyi-embedding-vision-plus-2026-03-06</p></td><td><p>1152（默认）, 1024, 512, 256, 128, 64</p></td><td rowspan="4"><p>1,024 Token</p></td><td rowspan="2"><p>建议单张大小不超过<strong>5 MB</strong>，最大<strong>10 MB。</strong>支持多图，最多支持输入<strong>64张</strong></p></td><td rowspan="2"><p>视频文件大小不超过 <strong>50 MB</strong></p><p>且编码类型为H.264/H.265</p></td><td><p>0.0005元</p></td><td><p>无免费额度</p></td></tr><tr><td><p>tongyi-embedding-vision-flash-2026-03-06</p></td><td><p>768（默认）, 512, 256, 128, 64</p></td><td><p>0.00015元</p></td><td><p>无免费额度</p></td></tr><tr><td><p>tongyi-embedding-vision-plus</p></td><td><p>1152（默认）, 1024, 512, 256, 128, 64</p></td><td rowspan="2"><p>单张大小不超过<strong>3 MB</strong>。支持多图，最多支持输入<strong>8张</strong></p></td><td rowspan="2"><p>视频文件大小不超过 <strong>10 MB</strong></p></td><td><p>0.0005元</p></td><td><p>100万Token</p><p>有效期：自开通百炼/模型发布/申请通过之日起90天（以较晚者为准）</p></td></tr><tr><td><p>tongyi-embedding-vision-flash</p></td><td><p>768（默认）, 512, 256, 128, 64</p></td><td><p>0.00015元</p></td><td><p>100万Token</p><p>有效期：自开通百炼/模型发布/申请通过之日起90天（以较晚者为准）</p></td></tr><tr><td><p>multimodal-embedding-v1</p></td><td><p>1,024</p></td><td><p>512 Token</p></td><td><p>单张大小不超过<strong>3 MB</strong></p></td><td><p>视频文件大小不超过 <strong>10 MB</strong></p></td><td><p>图片/视频：0.0009 元</p><p>文本：0.0007 元</p></td><td><p>无免费额度</p></td></tr></tbody></table>

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>向量维度</strong></p></th><th><p><strong>文本长度限制</strong></p></th><th><p><strong>图片大小限制</strong></p></th><th><p><strong>视频大小限制</strong></p></th><th><p><strong>单价（每千输入Token）</strong></p></th></tr></thead><tbody><tr><td><p>tongyi-embedding-vision-plus</p></td><td><p>1152（默认）, 1024, 512, 256, 128, 64</p></td><td><p>1,024 Token</p></td><td rowspan="2"><p>最多 <strong>8 张</strong>且单张大小不超过<strong>3 MB</strong></p></td><td rowspan="2"><p>视频文件大小不超过 <strong>10 MB</strong></p></td><td><p>0.0005元</p></td></tr><tr><td><p>tongyi-embedding-vision-flash</p></td><td><p>768（默认）, 512, 256, 128, 64</p></td><td><p>1,024 Token</p></td><td><p>0.00015元</p></td></tr></tbody></table>

<a id="输入与语种限制"></a>

<a id="993adb781aelw"></a>

#### 输入与语种限制

<table><thead><tr><th colspan="5"><strong>多模态融合向量模型</strong></th></tr><tr><th><strong>模型</strong></th><th><strong>文本</strong></th><th><strong>图片</strong></th><th><strong>视频</strong></th><th><strong>单次请求条数</strong></th></tr></thead><tbody><tr><td><p>qwen3-vl-embedding</p></td><td><p>支持中、英、日、韩、法、德等33种主流语言</p><a id="accordion-所有支持语言-3"></a><section><p>所有支持语言</p><div><p>中文、日语、韩语、印尼语、越南语、泰语、英语、法语、德语、俄语、葡萄牙语、西班牙语、意大利语、瑞典语、丹麦语、捷克语、挪威语、荷兰语、芬兰语、土耳其语、波兰语、斯瓦希里语、罗马尼亚语、塞尔维亚语、希腊语、哈萨克语、乌兹别克语、宿务语、阿拉伯语、乌尔都语、波斯语、印地语 / 天城语、希伯来语。</p></div></section></td><td rowspan="2"><p>JPEG, PNG, WEBP, BMP, TIFF, ICO, DIB, ICNS, SGI（支持URL或Base64）</p></td><td rowspan="2"><p>MP4, AVI, MOV（仅支持URL）</p></td><td><p>一次请求中传入内容元素总数不超过 20。图片数量不超过10，视频数量不超过1。</p></td></tr><tr><td><p>qwen2.5-vl-embedding</p></td><td><p>支持中、英、日、韩、法、德等11种主流语言</p><a id="accordion-所有支持语言-4"></a><section><p>所有支持语言</p><div><p>中文、英语、日语、韩语、法语、德语、俄语、葡萄牙语、西班牙语、意大利语、印尼语</p></div></section></td><td><p>一次请求内，图片、文本、视频、融合对象每种类型最多出现 1 次。</p></td></tr><tr><td colspan="5"><strong>多模态向量模型</strong></td></tr><tr><td><strong>模型</strong></td><td><strong>文本</strong></td><td><strong>图片</strong></td><td><strong>视频</strong></td><td><strong>单次请求条数</strong></td></tr><tr><td><p>tongyi-embedding-vision-plus-2026-03-06</p></td><td rowspan="2"><p>支持中、英、日、韩等超30种主流语言</p><a id="accordion-所有支持语言-5"></a><section><p>所有支持语言</p><div><p>中文、日语、韩语、印尼语、越南语、泰语、英语、法语、德语、俄语、葡萄牙语、西班牙语、意大利语、瑞典语、丹麦语、捷克语、挪威语、荷兰语、芬兰语、土耳其语、波兰语、斯瓦希里语、罗马尼亚语、塞尔维亚语、希腊语、哈萨克语、乌兹别克语、宿务语、阿拉伯语、乌尔都语、波斯语、印地语 / 天城语、希伯来语。</p></div></section></td><td rowspan="2"><p>JPEG, PNG, WEBP, BMP, TIFF, ICO, DIB, ICNS, SGI（支持URL或Base64）</p></td><td rowspan="2"><p>MP4, MPEG, MOV, MPG, WEBM, AVI, FLV, MKV（仅支持URL）</p></td><td rowspan="2"><p>一次请求中传入内容元素总数不超过 20，单次图片总数不超过64，视频数量不超过8。</p></td></tr><tr><td><p>tongyi-embedding-vision-flash-2026-03-06</p></td></tr><tr><td><p>tongyi-embedding-vision-plus</p></td><td rowspan="2"><p>中文与英文</p></td><td rowspan="2"><p>JPG, PNG, BMP (支持URL或Base64)</p></td><td rowspan="3"><p>MP4, MPEG, MOV, MPG, WEBM, AVI, FLV, MKV（仅支持URL）</p></td><td rowspan="2"><p>暂无传入内容元素数量限制，输入内容Token数不超过单批次处理Token数量上限即可。</p></td></tr><tr><td><p>tongyi-embedding-vision-flash</p></td></tr><tr><td><p>multimodal-embedding-v1</p></td><td><p>中文与英文</p></td><td><p>JPG, PNG, BMP (支持URL或Base64)</p></td><td><p>一次请求中传入内容元素总数不超过 20；图片、视频各最多 1 条，文本最多 20 条，共享总条数上限。</p></td></tr></tbody></table>

<a id="核心功能"></a>

<a id="50a0f41076ngn"></a>

## 核心功能

<a id="切换向量维度"></a>

<a id="c2f07398beub8"></a>

### 切换向量维度

`qwen3.7-text-embedding`、`qwen3.7-text-embedding-flash`、`text-embedding-v4` 、 `text-embedding-v3`、`tongyi-embedding-vision-plus`、`tongyi-embedding-vision-flash`、`tongyi-embedding-vision-plus-2026-03-06`、`tongyi-embedding-vision-flash-2026-03-06`、`qwen3-vl-embedding`和`qwen2.5-vl-embedding`支持自定义向量维度。更高的维度能保留更丰富的语义信息，但也会相应增加存储和计算成本。

-   **通用场景（推荐）**：1024 维度是性能与成本的最佳平衡点，适用于绝大多数语义检索任务。
-   **追求精度**：对于高精度要求领域，可选择 1536 或 2048 维度。这会带来一定的精度提升，但存储和计算开销会显著增加。
-   **资源受限**：在对成本极其敏感的场景下，可选择 768 及以下维度。这能显著降低资源消耗，但会损失部分语义信息。

<a id="fig-code-group-4"></a>

<a id="fig-code-group-4-openai兼容接口-tab"></a>

OpenAI兼容接口

<a id="code-code-group-4-openai兼容接口"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

resp = client.embeddings.create(
    model="qwen3.7-text-embedding",
    input=["喜欢，以后还来这里买"],
    # 将向量维度设置为 256
    dimensions=256
)
print(f"向量维度: {len(resp.data[0].embedding)}")
```

<a id="fig-code-group-4-dashscope-tab"></a>

DashScope

<a id="code-code-group-4-dashscope"></a>

```python
import os
import dashscope
# 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
resp = client.embeddings.create(
    model="qwen3.7-text-embedding",
    input=["喜欢，以后还来这里买"],
    # 将向量维度设置为 256
    dimension=256
)

print(f"向量维度: {len(resp.embeddings[0].embedding)}")
```

<a id="区分查询与文档文本-text-type"></a>

<a id="92608abc9dcxe"></a>

### 区分查询与文档文本 (text\_type)

> 该参数目前仅支持通过DashScope SDK及API启用。

为了在搜索类任务中取得最佳效果，应根据任务目标对不同的内容进行有针对性的向量化处理，以充分发挥各自的作用。`text_type` 参数正是为此设计：

-   `text_type: 'query'`：用于用户输入的**查询文本**。模型将生成一个类似“标题”的向量，更具方向性，专为“提问”和“查找”进行优化。
-   `text_type: 'document'` (默认值)：用于存入底库的**文档文本**。模型将生成一个类似“正文”的向量，包含更全面的信息，专为“被匹配”进行优化。

当使用短文本去匹配长文本时，应区分 `query` 和 `document`。而在聚类、分类等所有文本处于相同角色的任务中，则无需设置此参数。

<a id="使用任务指令提升效果-instruct"></a>

<a id="eb35b65eben45"></a>

### 使用任务指令提升效果 (instruct)

> 该参数目前仅支持通过DashScope SDK及API启用。

通过提供明确的英文任务指令（instruct），可以引导 `qwen3.7-text-embedding`、`qwen3.7-text-embedding-flash` 和 `text-embedding-v4` 模型针对特定检索场景优化向量质量，有效提升精度。其中 `qwen3.7-text-embedding` 在指令遵循能力上对比 text-embedding-v4 提升了 **16.4%**，建议优先使用。使用此功能时，必须将 `text_type` 参数设置为 `query`。

<a id="code-block-5"></a>

```python
# 场景：为搜索引擎构建文档向量时，可以添加指令以优化用于检索的向量质量。
resp = client.embeddings.create(
    model="qwen3.7-text-embedding",
    input="机器学习的相关论文",
    text_type="query",
    instruct="Given a research paper query, retrieve relevant research paper"
)
```

<a id="稠密与稀疏向量"></a>

<a id="58a9ececa45lw"></a>

### 稠密与稀疏向量

> 该参数目前仅支持通过DashScope SDK及API启用。

`qwen3.7-text-embedding`、`qwen3.7-text-embedding-flash`、`text-embedding-v4`和`text-embedding-v3`支持输出三种类型的向量，以适应不同检索策略的需求。其中 `qwen3.7-text-embedding` 的 Sparse Embedding 采用全新类 SPLADE 训练策略，效果提升 **8.4%**，并新增跨语言检索支持。

| 向量类型 (output\_type) | 核心优势 | 主要不足 | 典型应用场景 |
| --- | --- | --- | --- |
| dense | **深度语义理解**，能识别同义词和上下文，与召回结果更相关。 | **计算和存储成本较高**；无法保证关键词的精确匹配。 | 语义搜索、智能问答、内容推荐。 |
| sparse | **高计算效率**，专注于关键词的**精确匹配**和快速过滤。 | **牺牲了语义理解能力**，无法处理同义词或上下文。 | 日志检索、商品SKU搜索、精确信息过滤。 |
| dense&sparse | 结合语义与关键词，搜索效果最好。**生成成本不变**，API调用开销与单向量模式相同。 | **存储需求大**，系统架构和检索逻辑更复杂。 | 高质量、生产级的混合搜索引擎。 |

<a id="应用示例"></a>

<a id="a356aa16bdi40"></a>

## 应用示例

> 以下为功能演示代码。在生产环境中，请预先计算向量并持久化存储在向量数据库中，检索时仅需计算查询向量。

<a id="语义搜索"></a>

<a id="5141fd5463kr0"></a>

### 语义搜索

通过计算查询与文档之间的向量相似度，实现精准的语义匹配。

<a id="code-block-6"></a>

```python
import os
import dashscope
import numpy as np
# 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def cosine_similarity(a, b):
    """计算余弦相似度"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def semantic_search(query, documents, top_k=5):
    """语义搜索"""
    # 生成查询向量
    query_resp = client.embeddings.create(
        model="qwen3.7-text-embedding",
        input=query,
        dimension=1024
    )
    query_embedding = query_resp.embeddings[0].embedding

    # 生成文档向量
    doc_resp = client.embeddings.create(
        model="qwen3.7-text-embedding",
        input=documents,
        dimension=1024
    )

    # 计算相似度
    similarities = []
    for i, doc_emb in enumerate(doc_resp.embeddings):
        similarity = cosine_similarity(query_embedding, doc_emb.embedding)
        similarities.append((i, similarity))

    # 排序并返回top_k结果
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [(documents[i], sim) for i, sim in similarities[:top_k]]

# 使用示例
documents = [
    "人工智能是计算机科学的一个分支",
    "机器学习是实现人工智能的重要方法",
    "深度学习是机器学习的一个子领域"
]
query = "什么是AI？"
results = semantic_search(query, documents, top_k=2)
for doc, sim in results:
    print(f"相似度: {sim:.3f}, 文档: {doc}")

```

<a id="推荐系统"></a>

<a id="e42c4bf795jh8"></a>

### 推荐系统

通过分析用户历史行为向量，发现用户的兴趣偏好并推荐相似物品。

<a id="code-block-7"></a>

```python
import os
import dashscope
import numpy as np
# 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def cosine_similarity(a, b):
    """计算余弦相似度"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
def build_recommendation_system(user_history, all_items, top_k=10):
    """构建推荐系统"""
    # 生成用户历史向量
    history_resp = client.embeddings.create(
        model="qwen3.7-text-embedding",
        input=user_history,
        dimension=1024
    )

    # 计算用户偏好向量（取平均）
    user_embedding = np.mean([
        emb.embedding for emb in history_resp.embeddings
    ], axis=0)

    # 生成所有物品向量
    items_resp = client.embeddings.create(
        model="qwen3.7-text-embedding",
        input=all_items,
        dimension=1024
    )

    # 计算推荐分数
    recommendations = []
    for i, item_emb in enumerate(items_resp.embeddings):
        score = cosine_similarity(user_embedding, item_emb.embedding)
        recommendations.append((all_items[i], score))

    # 排序并返回推荐结果
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:top_k]

# 使用示例
user_history = ["科幻类", "动作类", "悬疑类"]
all_movies = ["未来世界", "太空探险", "古代战争", "浪漫之旅", "超级英雄"]
recommendations = build_recommendation_system(user_history, all_movies)
for movie, score in recommendations:
    print(f"推荐分数: {score:.3f}, 电影: {movie}")
```

<a id="文本聚类"></a>

<a id="d5c766dd40q98"></a>

### 文本聚类

通过分析向量间的距离，将相似的文本自动分组。

<a id="code-block-8"></a>

```python
# 需要安装 scikit-learn: pip install scikit-learn
import os
import dashscope
import numpy as np
from sklearn.cluster import KMeans
# 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def cluster_texts(texts, n_clusters=2):
    """将一组文本进行聚类"""
    # 1. 获取所有文本的向量
    resp = client.embeddings.create(
        model="qwen3.7-text-embedding",
        input=texts,
        dimension=1024
    )
    embeddings = np.array([item.embedding for item in resp.embeddings])

    # 2. 使用KMeans算法进行聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto').fit(embeddings)

    # 3. 整理并返回结果
    clusters = {i: [] for i in range(n_clusters)}
    for i, label in enumerate(kmeans.labels_):
        clusters[label].append(texts[i])
    return clusters

# 使用示例
documents_to_cluster = [
    "手机公司A发售新款手机",
    "搜索引擎公司B推出新款系统",
    "世界杯决赛阿根廷对阵法国",
    "奥运会中国队再添一金",
    "某公司发布最新AI芯片",
    "欧洲杯赛事报道"
]
clusters = cluster_texts(documents_to_cluster, n_clusters=2)
for cluster_id, docs in clusters.items():
    print(f"--- 类别 {cluster_id} ---")
    for doc in docs:
        print(f"- {doc}")
```

<a id="文本分类"></a>

<a id="122d8699273b2"></a>

### 文本分类

通过计算输入文本与预定义标签的向量相似度，实现在没有预先标记的示例的情况下，对新类别进行识别和分类。

<a id="code-block-9"></a>

```python
import os
import dashscope
import numpy as np
# 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def cosine_similarity(a, b):
    """计算余弦相似度"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def classify_text_zero_shot(text, labels):
    """零样本文本分类"""
    # 1. 获取输入文本和所有标签的向量
    resp = client.embeddings.create(
        model="qwen3.7-text-embedding",
        input=[text] + labels,
        dimension=1024
    )
    embeddings = resp.embeddings
    text_embedding = embeddings[0].embedding
    label_embeddings = [emb.embedding for emb in embeddings[1:]]

    # 2. 计算与每个标签的相似度
    scores = [cosine_similarity(text_embedding, label_emb) for label_emb in label_embeddings]

    # 3. 返回相似度最高的标签
    best_match_index = np.argmax(scores)
    return labels[best_match_index], scores[best_match_index]

# 使用示例
text_to_classify = "这件衣服的料子很舒服，款式也好看"
possible_labels = ["数码产品", "服装配饰", "食品饮料", "家居生活"]

label, score = classify_text_zero_shot(text_to_classify, possible_labels)
print(f"输入文本: '{text_to_classify}'")
print(f"最匹配的分类是: '{label}' (相似度: {score:.3f})")
```

<a id="异常检测"></a>

<a id="b12ec1e5ebdp5"></a>

### 异常检测

通过计算文本向量与正常样本中心的向量相似度，识别出与常规模式显著不同的异常数据。

> 示例代码中的阈值（threshold）仅为演示目的。在真实业务场景中，相似度的具体数值会因数据内容和分布的不同而变化，没有一个固定的阈值。建议基于自己的数据集来校准此值。

<a id="code-block-10"></a>

```python
import os
import dashscope
import numpy as np
# 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def cosine_similarity(a, b):
    """计算余弦相似度"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def detect_anomaly(new_comment, normal_comments, threshold=0.6):
    # 1. 向量化所有正常评论和新评论
    all_texts = normal_comments + [new_comment]
    resp = client.embeddings.create(
        model="qwen3.7-text-embedding",
        input=all_texts,
        dimension=1024
    )
    embeddings = [item.embedding for item in resp.embeddings]

    # 2. 计算正常评论的中心向量（平均值）
    normal_embeddings = np.array(embeddings[:-1])
    normal_center_vector = np.mean(normal_embeddings, axis=0)

    # 3. 计算新评论与中心向量的相似度
    new_comment_embedding = np.array(embeddings[-1])
    similarity = cosine_similarity(new_comment_embedding, normal_center_vector)

    # 4. 判断是否为异常
    is_anomaly = similarity < threshold
    return is_anomaly, similarity

# 使用示例
normal_user_comments = [
    "今天的会议很有成效",
    "项目进展顺利",
    "下周发布新版本",
    "用户反馈良好"
]

test_comments = {
    "正常评论": "功能符合预期",
    "异常-无意义乱码": "asdfghjkl zxcvbnm"
}

print("--- 异常检测示例 ---")
for desc, comment in test_comments.items():
    is_anomaly, score = detect_anomaly(comment, normal_user_comments)
    result = "是" if is_anomaly else "否"
    print(f"评论: '{comment}'")
    print(f"是否为异常: {result} (与正常样本相似度: {score:.3f})\n")
```

<a id="api参考"></a>

<a id="13089dd842upm"></a>

## API参考

-   **通用文本向量**
    -   [同步处理模型接口API详情](../../../model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
    -   [批处理模型接口API详情](../../../model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
-   **多模态向量**
    
    [多模态向量模型接口API详情](../../../model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
    

<a id="错误码"></a>

<a id="efc117f59a2gm"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../../model-api-reference/preparations/error-code.md)进行解决。

<a id="限流"></a>

<a id="73848402f9nin"></a>

## 限流

关于模型的限流条件，请参见[限流](../../get-started-with-models/rate-limit.md)。

<a id="模型性能-mteb-cmteb"></a>

<a id="2bab6468f7h2h"></a>

## 模型性能(MTEB/CMTEB)

<a id="评测基准"></a>

### 评测基准

-   **MTEB**：大规模文本嵌入评测基准，综合评估分类、聚类、检索等任务的通用性。
-   **CMTEB**：中文大规模文本嵌入评测基准，专门针对中文文本的评测。
-   分数范围0-100，数值越高代表效果越优。

| 模型 | MTEB | MTEB（Retrieval task） | CMTEB | CMTEB (Retrieval task) |
| --- | --- | --- | --- | --- |
| text-embedding-v1 | 58.30 | 45.47 | 59.84 | 56.59 |
| text-embedding-v2 | 60.13 | 49.49 | 62.17 | 62.78 |
| text-embedding-v3（64维度） | 57.40 | 46.52 | 59.19 | 62.03 |
| text-embedding-v3（128维度） | 60.19 | 52.51 | 63.81 | 68.22 |
| text-embedding-v3（256维度） | 61.13 | 54.41 | 65.92 | 71.07 |
| text-embedding-v3（512维度） | 62.11 | 54.30 | 66.81 | 71.88 |
| text-embedding-v3（768维度） | 62.43 | 54.74 | 67.90 | 72.29 |
| text-embedding-v3（1024维度） | 63.39 | 55.41 | 68.92 | 73.23 |
| text-embedding-v4（512维度） | 64.73 | 56.34 | 68.79 | 73.33 |
| text-embedding-v4（1024维度） | 68.36 | 59.30 | 70.14 | 73.98 |
| text-embedding-v4（2048维度） | 71.58 | 61.97 | 71.99 | 75.01 |
