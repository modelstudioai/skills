# OpenAI Embedding接口兼容

阿里云百炼的Embedding模型兼容OpenAI接口规范。将原有 OpenAI 应用迁移至阿里云百炼只需调整三个参数：

-   base\_url：替换为`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
-   api\_key：替换为[阿里云百炼 API Key](../preparations/get-api-key.md)
-   model：替换为以下模型列表中的模型名称

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡、中国香港地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<a id="支持的模型"></a>

<a id="04b110d5870wm"></a>

## 支持的模型

<table><thead><tr><th><strong>模型名称</strong></th><th><strong>向量维度</strong></th><th><strong>最大行数</strong></th><th><p><strong>单行最大</strong><a href="https://help.aliyun.com/zh/model-studio/billing-for-model-studio">Token</a><strong>数</strong></p></th><th><strong>单价（每千输入Token）</strong></th><th><strong>支持语种</strong></th><th><p><strong>免费额度</strong><a href="../../model-user-guide/test-1/new-free-quota.md#977b13081ab56">（注）</a></p></th></tr></thead><tbody><tr><td><p>qwen3.7-text-embedding</p></td><td><p>2560、2,048、1,536、1,024（默认）、768、512、256</p></td><td><p>20</p></td><td><p>128,000</p></td><td><p>0.0005元</p><p><a href="batch-interfaces-compatible-with-openai.md">Batch调用</a>：0.00025元</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等201种主流语种与方言</p></td><td rowspan="4"><p>各100万Token</p><p>有效期：百炼开通后90天内</p></td></tr><tr><td><p>qwen3.7-text-embedding-flash</p></td><td><p>1,024（默认）、768、512、256</p></td><td><p>20</p></td><td><p>128,000</p></td><td><p>0.000125元</p><p><a href="batch-interfaces-compatible-with-openai.md">Batch调用</a>：0.000063元</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等201种主流语种与方言</p></td></tr><tr><td><p>text-embedding-v4</p><blockquote><p>属于<a href="https://qwenlm.github.io/zh/blog/qwen3-embedding/">Qwen3-Embedding</a>系列</p></blockquote></td><td><p>2,048、1,536、1,024（默认）、768、512、256、128、64</p></td><td rowspan="2"><p>10</p></td><td rowspan="2"><p>8,192</p></td><td rowspan="2"><p>0.0005元</p><p><a href="batch-interfaces-compatible-with-openai.md">Batch调用</a>：0.00025元</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等100+主流语种及多种编程语言</p></td></tr><tr><td><p>text-embedding-v3</p></td><td><p>1,024（默认）、768、512、256、128或64</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等50+主流语种</p></td></tr><tr><td><p>text-embedding-v2</p></td><td rowspan="2"><p>1,536</p></td><td rowspan="2"><p>25</p></td><td rowspan="2"><p>2,048</p></td><td rowspan="2"><p>0.0007元</p><p><a href="batch-interfaces-compatible-with-openai.md">Batch调用</a>：0.00035元</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语</p></td><td rowspan="2"><p>各50万Token</p><p>有效期：百炼开通后90天内</p></td></tr><tr><td><p>text-embedding-v1</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语</p></td></tr></tbody></table>

> 多模态Embedding模型（例如qwen3-vl-embedding、tongyi-embedding-vision系列）不支持OpenAI兼容接口。请参见[多模态向量](../vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

> **说明**
>
> OpenAI兼容接口不支持稀疏向量输出。使用 `text-embedding-v4` 时，如需设置 `output_type=sparse`，请调用 DashScope 接口。通过 OpenAI 兼容接口传入 `output_type=sparse` 会返回 HTTP 200，但 embedding 结果为空。

<a id="模型调用"></a>

<a id="aad9ffd00arml"></a>

## 模型调用

<a id="调用示例"></a>

<a id="t4GMg"></a>

### 调用示例

本章节提供Python（OpenAI SDK）和cURL（HTTP接口）的字符串输入调用示例，更多编程语言或输入方式示例请参考：[文本与多模态向量化](../../model-user-guide/model-experience/embedding-rerank-model/embedding.md)。

<a id="sec-tabs"></a>

<a id="使用openai-sdk调用"></a>

<a id="使用openai-sdk调用-h4"></a>

#### 使用OpenAI SDK调用

使用OpenAI SDK调用服务，您还需安装[OpenAI SDK](../preparations/install-sdk.md)。

<a id="code-block"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 百炼服务的base_url
)

completion = client.embeddings.create(
    model="text-embedding-v4",
    input='衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买',
    dimensions=1024, # 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
    encoding_format="float"
)

print(completion.model_dump_json())
```

<a id="使用http接口调用"></a>

<a id="使用http接口调用-h4"></a>

#### 使用HTTP接口调用

<a id="712f34105ala9"></a>

### 提交接口调用

<a id="code-block-2"></a>

```http
POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/embeddings
```

<a id="7d406f850epst"></a>

### 命令行调用

<a id="code-block-3"></a>

```bash
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "text-embedding-v4",
    "input": "衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买",
    "encoding_format": "float"
}'
```

运行代码可以获得以下结果：

<a id="accordion-运行结果"></a>

运行结果

<a id="code-block-4"></a>

```json
{
  "data": [
    {
      "embedding": [
        0.0023064255,
        -0.009327292,
        ....
        -0.0028842222
      ],
      "index": 0,
      "object": "embedding"
    }
  ],
  "model":"text-embedding-v4",
  "object":"list",
  "usage":{"total_tokens":23},
  "id":"f62c2ae7-0906-9758-ab34-47c5764f07e2"
}
```

<a id="异常响应示例"></a>

<a id="0ea417000ckjs"></a>

### 异常响应示例

在访问请求出错的情况下，输出的结果中会通过`code`和`message`指明出错原因。

<a id="code-block-5"></a>

```json
{
    "error": {
        "message": "Incorrect API key provided. ",
        "type": "invalid_request_error",
        "param": null,
        "code": "invalid_api_key"
    }
}
```

<a id="api参考"></a>

<a id="3cd262793blik"></a>

## API参考

[通用文本向量接口API详情](../vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)

<a id="错误码"></a>

<a id="efc117f59a2gm"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../preparations/error-code.md)进行解决。
