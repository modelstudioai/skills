# 同步接口API详情

通用文本向量模型可将文本数据转换为数值向量，用于语义搜索、推荐、聚类、分类等下游任务。

## **模型概览**

**模型名称**

**向量维度**

**最大行数**

**单行最大**[Token](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#f300d75bd5rb2)**数**

**单价（每千输入Token）**

**支持语种**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

text-embedding-v4

> 属于[Qwen3-Embedding](https://qwenlm.github.io/zh/blog/qwen3-embedding/)系列

2,048、1,536、1,024（默认）、768、512、256、128、64

10

8,192

0.0005元

[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)：0.00025元

中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等100+主流语种及多种编程语言

各100万Token

有效期：百炼开通后90天内

text-embedding-v3

1,024（默认）、768、512、256、128或64

中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等50+主流语种

text-embedding-v2

1,536

25

2,048

0.0007元

[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)：0.00035元

中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语

各50万Token

有效期：百炼开通后90天内

text-embedding-v1

中文、英语、西班牙语、法语、葡萄牙语、印尼语

关于模型限流，请参考[限流](https://help.aliyun.com/zh/model-studio/rate-limit#953ddcd76495l)。

## **前提条件**

若熟悉OpenAI生态，可使用兼容API快速迁移；DashScope API则提供更丰富的独有特性。请根据您的需求选择。

您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，还需要[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

## **OpenAI兼容**

## 公共云

**使用SDK调用时需配置的base\_url：**`https://dashscope.aliyuncs.com/compatible-mode/v1`

**使用HTTP方式调用时需配置的endpoint：**`POST https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings`

### **请求体**

## 输入字符串

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 百炼服务的base_url
)

completion = client.embeddings.create(
    model="text-embedding-v4",
    input='衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买',
    dimensions=1024, # 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
    encoding_format="float"
)

print(completion.model_dump_json())
```

## Java

```
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.embeddings.CreateEmbeddingResponse;
import com.openai.models.embeddings.EmbeddingCreateParams;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();

        // 创建向量化请求参数
        EmbeddingCreateParams params = EmbeddingCreateParams.builder()
                .model("text-embedding-v4")
                .input(EmbeddingCreateParams.Input.ofString("衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买"))
                // 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
                .dimensions(1024)
                .build();

        try {
            // 发送请求并获取响应
            CreateEmbeddingResponse response = client.embeddings().create(params);
            System.out.println(response);
        } catch (Exception e) {
            System.err.println("请求出错，请查看错误码对照网页：");
            System.err.println("https://help.aliyun.com/zh/model-studio/faq-about-alibaba-cloud-model-studio?spm=a2c4g.11186623.help-menu-2400256.d_0_17_0.18733a66lTrcHv#1c38f58abfcml");
            System.err.println("错误详情：" + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

## curl

```
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "text-embedding-v4",
    "input": "风急天高猿啸哀，渚清沙白鸟飞回，无边落木萧萧下，不尽长江滚滚来",  
    "dimensions": 1024,  
    "encoding_format": "float"
}'
```

## 输入字符串列表

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 百炼服务的base_url
)

completion = client.embeddings.create(
    model="text-embedding-v4",
    input=['风急天高猿啸哀', '渚清沙白鸟飞回', '无边落木萧萧下', '不尽长江滚滚来'],
    dimensions=1024,# 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
    encoding_format="float"
)

print(completion.model_dump_json())
```

## Java

```
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.embeddings.CreateEmbeddingResponse;
import com.openai.models.embeddings.EmbeddingCreateParams;

import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();

        // 创建输入字符串列表
        List<String> inputList = Arrays.asList(
            "风急天高猿啸哀",
            "渚清沙白鸟飞回",
            "无边落木萧萧下",
            "不尽长江滚滚来"
        );

        // 存储所有响应的列表
        List<CreateEmbeddingResponse> responses = new ArrayList<>();

        // 循环处理每个字符串
        for (String text : inputList) {
            try {
                // 创建向量化请求参数
                EmbeddingCreateParams params = EmbeddingCreateParams.builder()
                        .model("text-embedding-v4")
                        .input(EmbeddingCreateParams.Input.ofString(text))
                        // 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
                        .dimensions(1024)
                        .build();

                // 发送请求并获取响应
                CreateEmbeddingResponse response = client.embeddings().create(params);
                responses.add(response);
                System.out.println("处理文本: " + text);
                System.out.println("向量化结果: " + response);
                System.out.println("------------------------");
            } catch (Exception e) {
                System.err.println("处理文本时出错: " + text);
                System.err.println("错误详情：" + e.getMessage());
                e.printStackTrace();
            }
        }

        // 打印总结信息
        System.out.println("\n总共处理了 " + responses.size() + " 个文本");
    }
}
```

## curl

```
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "text-embedding-v4",
    "input": [
        "风急天高猿啸哀",
        "渚清沙白鸟飞回", 
        "无边落木萧萧下", 
        "不尽长江滚滚来"
        ],
    "dimensions": 1024,
    "encoding_format": "float"
}'
```

## 输入文件

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"  # 百炼服务的base_url
)
# 确保将 'texts_to_embedding.txt' 替换为您自己的文件名或路径
with open('texts_to_embedding.txt', 'r', encoding='utf-8') as f:
    completion = client.embeddings.create(
        model="text-embedding-v4",
        input=f,
        dimensions=1024,# 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
        encoding_format="float"
    )
print(completion.model_dump_json())
```

## Java

```
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.embeddings.CreateEmbeddingResponse;
import com.openai.models.embeddings.EmbeddingCreateParams;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();

        // 确保将 'texts_to_embedding.txt' 替换为您自己的文件名或绝对路径
        String filePath = "/src/main/java/org/example/text_to_embedding.txt";

        try {
            // 读取文件内容
            StringBuilder fileContent = new StringBuilder();
            try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    fileContent.append(line).append("\n");
                }
            }

            // 创建向量化请求参数
            EmbeddingCreateParams params = EmbeddingCreateParams.builder()
                    .model("text-embedding-v4")
                    .input(EmbeddingCreateParams.Input.ofString(fileContent.toString()))
                    // 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
                    .dimensions(1024)
                    .build();

            // 发送请求并获取响应
            CreateEmbeddingResponse response = client.embeddings().create(params);
            System.out.println(response);

        } catch (IOException e) {
            System.err.println("读取文件时出错：" + e.getMessage());
            e.printStackTrace();
        } catch (Exception e) {
            System.err.println("请求出错，请查看错误码对照网页：");
            System.err.println("https://help.aliyun.com/zh/model-studio/faq-about-alibaba-cloud-model-studio?spm=a2c4g.11186623.help-menu-2400256.d_0_17_0.18733a66lTrcHv#1c38f58abfcml");
            System.err.println("错误详情：" + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

## curl

> 确保将 'texts\_to\_embedding.txt' 替换为您自己的文件名或路径

```
FILE_CONTENT=$(cat texts_to_embedding.txt | jq -Rs .)
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "text-embedding-v4",
    "input": ['"$FILE_CONTENT"'],
    "dimensions": 1024,
    "encoding_format": "float"
}'
```

**model** `_string_`**必选**

调用的模型名称，参考[模型概览](#6b8938034edvk)表格中的模型名称进行选择。

**input** `_array<string> 或 string 或 file_` **必选**

输入待处理的文本。可以是字符串（string）、字符串列表（array）或文件（file）。不同模型版本支持的文本长度和批量大小不同，具体如下：

-   **text-embedding-v3 / v4 模型：**
    
    -   **输入为字符串**：最长支持 **8,192** Token。
        
    -   **输入为字符串列表或文件**：最多支持 **10** 条（行），每条（行）最长支持 **8,192** Token。
        
-   **text-embedding-v1 / v2 模型：**
    
    -   **输入为字符串**：最长支持 **2,048** Token。
        
    -   **输入为字符串列表或文件**：最多支持 **25** 条（行），每条（行）最长支持 **2,048** Token。
        

**dimensions** `_integer_` **可选**

指定的向量维度，必须为以下值之一：2048（仅适用于`text-embedding-v4`）、1536（仅适用于`text-embedding-v4`）1024、768、512、256、128 或 64，默认值为1024。

**encoding\_format** `_string_` **可选**

用于控制返回的Embedding格式，当前仅支持`float`格式。

### **响应对象**

## 成功响应

```
{
  "data": [
    {
      "embedding": [
        -0.0695386752486229, 0.030681096017360687, ...
      ],
      "index": 0,
      "object": "embedding"
    },
    ...
    {
      "embedding": [
        -0.06348952651023865, 0.060446035116910934, ...
      ],
      "index": 5,
      "object": "embedding"
    }
  ],
  "model": "text-embedding-v4",
  "object": "list",
  "usage": {
    "prompt_tokens": 184,
    "total_tokens": 184
  },
  "id": "73591b79-d194-9bca-8bb5-xxxxxxxxxxxx"
}
```

## 异常响应

```
{
    "error": {
        "message": "Incorrect API key provided. ",
        "type": "invalid_request_error",
        "param": null,
        "code": "invalid_api_key"
    }
}
```

**data** `_array_`

任务输出信息。

**属性**

**embedding** `_list_`

本次调用返回object对象的value，类型是元素为float数据的数组，包含具体Embedding向量。

**index** `_integer_`

本结构中的算法结果对应的输入文字在输入数组中的索引值。

**object** _string_

本次调用返回的object对象类型，默认为embedding。

**model** `_string_`

本次调用的模型名。

**object** _string_

本次调用返回的data类型，默认为list。

**usage** `_object_`

**属性**

**prompt\_tokens** _integer_

用户输入文本转换成Token后的长度。

**total\_tokens** _integer_

本次请求输入内容的 Token 数目，算法的计量是根据用户输入字符串被模型Tokenizer解析之后对应的Token数目来进行。

**id** _string_

请求唯一标识。可用于请求明细溯源和问题排查。

## DashScope

## 公共云

**使用SDK调用时需配置的base\_url：**https://dashscope.aliyuncs.com/api/v1

**使用HTTP方式调用时需配置的endpoint：**POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding

### **请求体**

## 输入字符串

## Python

```
import dashscope
from http import HTTPStatus

resp = dashscope.TextEmbedding.call(
    model="text-embedding-v4",
    input='衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买',
    dimension=1024,  # 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
    output_type="dense&sparse"
)

print(resp) if resp.status_code == HTTPStatus.OK else print(resp)
```

## Java

```
import java.util.Arrays;
import com.alibaba.dashscope.embeddings.TextEmbedding;
import com.alibaba.dashscope.embeddings.TextEmbeddingParam;
import com.alibaba.dashscope.embeddings.TextEmbeddingResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;

/**
 * 千问文本向量模型调用示例
 */
public final class Main {
    public static void main(String[] args) {
        try {
            // 构建请求参数
            TextEmbeddingParam param = TextEmbeddingParam
                    .builder()
                    .model("text-embedding-v4")  // 使用text-embedding-v4模型
                    .texts(Arrays.asList("衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买"))  // 输入文本
                    .parameter("dimension", 1024)  // 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
                    .build();

            // 创建模型实例并调用
            TextEmbedding textEmbedding = new TextEmbedding();
            TextEmbeddingResult result = textEmbedding.call(param);
            
            // 输出结果
            System.out.println(result);
            
        } catch (ApiException | NoApiKeyException e) {
            System.out.println("调用失败：" + e.getMessage());
        }
    }
}
```

## curl

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "text-embedding-v4",
    "input": {
        "texts": [
        "风急天高猿啸哀，渚清沙白鸟飞回，无边落木萧萧下，不尽长江滚滚来"
        ]
    },
    "parameters": {
    	"dimension": 1024,
    	"output_type": "dense"
    }
}'
```

## 输入字符串列表

## Python

```
import dashscope
from http import HTTPStatus

DASHSCOPE_MAX_BATCH_SIZE = 10

inputs = ['风急天高猿啸哀', '渚清沙白鸟飞回', '无边落木萧萧下', '不尽长江滚滚来']

result = None
batch_counter = 0
for i in range(0, len(inputs), DASHSCOPE_MAX_BATCH_SIZE):
    batch = inputs[i:i + DASHSCOPE_MAX_BATCH_SIZE]
    resp = dashscope.TextEmbedding.call(
        model="text-embedding-v4",
        input=batch,
        dimension=1024  # 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
    )
    if resp.status_code == HTTPStatus.OK:
        if result is None:
            result = resp
        else:
            for emb in resp.output['embeddings']:
                emb['text_index'] += batch_counter
                result.output['embeddings'].append(emb)
            result.usage['total_tokens'] += resp.usage['total_tokens']
    else:
        print(resp)
    batch_counter += len(batch)

print(result)
```

## Java

```
import java.util.Arrays;
import java.util.List;
import com.alibaba.dashscope.embeddings.TextEmbedding;
import com.alibaba.dashscope.embeddings.TextEmbeddingParam;
import com.alibaba.dashscope.embeddings.TextEmbeddingResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.embeddings.TextEmbeddingResultItem;

public final class Main {
    private static final int DASHSCOPE_MAX_BATCH_SIZE = 10;

    public static void main(String[] args) {
        List<String> inputs = Arrays.asList(
                "风急天高猿啸哀",
                "渚清沙白鸟飞回",
                "无边落木萧萧下",
                "不尽长江滚滚来"
        );

        TextEmbeddingResult result = null;
        int batchCounter = 0;

        for (int i = 0; i < inputs.size(); i += DASHSCOPE_MAX_BATCH_SIZE) {
            List<String> batch = inputs.subList(i, Math.min(i + DASHSCOPE_MAX_BATCH_SIZE, inputs.size()));
            TextEmbeddingParam param = TextEmbeddingParam.builder()
                    .model("text-embedding-v4")
                    .texts(batch)
                    .parameter("dimension", 1024)  // 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
                    .build();

            TextEmbedding textEmbedding = new TextEmbedding();
            try {
                TextEmbeddingResult resp = textEmbedding.call(param);
                if (resp != null) {
                    if (result == null) {
                        result = resp;
                    } else {
                        for (var emb : resp.getOutput().getEmbeddings()) {
                            emb.setTextIndex(emb.getTextIndex() + batchCounter);
                            result.getOutput().getEmbeddings().add(emb);
                        }
                        result.getUsage().setTotalTokens(result.getUsage().getTotalTokens() + resp.getUsage().getTotalTokens());
                    }
                } else {
                    System.out.println(resp);
                }
            } catch (ApiException | NoApiKeyException e) {
                e.printStackTrace();
            }
            batchCounter += batch.size();
        }

        System.out.println(result);
    }
}
```

## curl

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "text-embedding-v4",
    "input": {
        "texts": [
          "风急天高猿啸哀",
          "渚清沙白鸟飞回", 
          "无边落木萧萧下", 
          "不尽长江滚滚来"
        ]
    },
    "parameters": {
    	  "dimension": 1024,
    	  "output_type": "dense"
    }
}'
```

## 输入文件

## Python

```
from http import HTTPStatus
from dashscope import TextEmbedding

with open('texts_to_embedding.txt', 'r', encoding='utf-8') as f:
    resp = TextEmbedding.call(
        model="text-embedding-v4",
        input=f,
        dimension=1024 # 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
    )

    if resp.status_code == HTTPStatus.OK:
        print(resp)
    else:
        print(resp)
```

## Java

```
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import com.alibaba.dashscope.embeddings.TextEmbedding;
import com.alibaba.dashscope.embeddings.TextEmbeddingParam;
import com.alibaba.dashscope.embeddings.TextEmbeddingResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;

public final class Main {
    public static void main(String[] args) {
        try (BufferedReader reader = new BufferedReader(new FileReader("<文件所来自的内容根的路径>"))) {
            StringBuilder content = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                content.append(line).append("\n");
            }

            TextEmbeddingParam param = TextEmbeddingParam.builder()
                    .model("text-embedding-v4")
                    .text(content.toString())
                    .parameter("dimension", 1024)  // 指定向量维度（仅 text-embedding-v3及 text-embedding-v4支持该参数）
                    .build();

            TextEmbedding textEmbedding = new TextEmbedding();
            TextEmbeddingResult result = textEmbedding.call(param);

            if (result != null) {
                System.out.println(result);
            } else {
                System.out.println("Failed to get embedding: " + result);
            }
        } catch (IOException | ApiException | NoApiKeyException e) {
            e.printStackTrace();
        }
    }
}
```

## curl

> 确保将 'texts\_to\_embedding.txt' 替换为您自己的文件名或路径

```
FILE_CONTENT=$(cat texts_to_embedding.txt | jq -Rs .)
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "text-embedding-v4",
    "input": {
        "texts": ['"$FILE_CONTENT"']
    },
    "parameters": {
        "dimension": 1024,
        "output_type": "dense"
    }
}'
```

**model** `_string_` **必选**

调用的模型，参考[模型概览](#6b8938034edvk)表格中的模型名称进行选择。

**input** `_string_`_或_`_array<string>_` **必选**

输入待处理的文本。可以是字符串（string）、字符串列表（array）或文件（file）。不同模型版本支持的文本长度和批量大小不同，具体如下：

-   **text-embedding-v3 / v4 模型：**
    
    -   **输入为字符串**：最长支持 **8,192** Token。
        
    -   **输入为字符串列表或文件**：最多支持 **10** 条（行），每条（行）最长支持 **8,192** Token。
        
-   **text-embedding-v1 / v2 模型：**
    
    -   **输入为字符串**：最长支持 **2,048** Token。
        
    -   **输入为字符串列表或文件**：最多支持 **25** 条（行），每条（行）最长支持 **2,048** Token。
        

**text\_type** `_string_` **可选**

> 通过 HTTP 调用时，请将 **text\_type** 放入parameters对象中。

文本转换为向量后可以应用于检索、聚类、分类等下游任务，对检索这类非对称任务为了达到更好的检索效果建议区分查询文本（query）和底库文本（document）类型，入库、聚类、分类等对称任务可以不用特殊指定，采用系统默认值`document`即可。

**dimension** `_integer_` **可选**

> 通过 HTTP 调用时，请将 **dimension** 放入parameters对象中。

指定的向量维度，必须为以下值之一：2048（仅适用于`text-embedding-v4`）、1536（仅适用于`text-embedding-v4`）1024、768、512、256、128 或 64，默认值为1024。

**output\_type** `_string_` **可选**

> 通过 HTTP 调用时，请将 **output\_type** 放入parameters对象中。

用户指定输出离散向量表示只适用于`text-embedding-v3`与`text-embedding-v4`模型，取值在dense、sparse、dense&sparse之间，默认取dense，只输出连续向量。

**instruct** `_string_` **可选**

添加自定义任务说明，可用于指导模型理解查询意图。建议使用英文撰写，通常可带来约 1%–5% 的效果提升。

### **响应对象**

## 成功响应

```
{   "status_code": 200, 
    "request_id": "1ba94ac8-e058-99bc-9cc1-7fdb37940a46", 
    "code": "", 
    "message": "",
    "output":{
        "embeddings": [
          {  
             "sparse_embedding":[
               {"index":7149,"value":0.829,"token":"风"},
               .....
               {"index":111290,"value":0.9004,"token":"哀"}],
             "embedding": [-0.006929283495992422,-0.005336422007530928, ...],
             "text_index": 0
          }, 
          {
             "sparse_embedding":[
               {"index":246351,"value":1.0483,"token":"渚"},
               .....
               {"index":2490,"value":0.8579,"token":"回"}],
             "embedding": [-0.006929283495992422,-0.005336422007530928, ...],
             "text_index": 1
          },
          {
             "sparse_embedding":[
               {"index":3759,"value":0.7065,"token":"无"},
               .....
               {"index":1130,"value":0.815,"token":"下"}],
             "embedding": [-0.006929283495992422,-0.005336422007530928, ...],
             "text_index": 2
          },
          {
             "sparse_embedding":[
               {"index":562,"value":0.6752,"token":"不"},
               .....
               {"index":1589,"value":0.7097,"token":"来"}],
             "embedding": [-0.001945948973298072,-0.005336422007530928, ...],
             "text_index": 3
          }
        ]
    },
    "usage":{
        "total_tokens":27
    }
}
```

## 异常响应

```
{
    "code":"InvalidApiKey",
    "message":"Invalid API-key provided.",
    "request_id":"xxxxxxxx"
}
```

**status\_code** `string`

状态码，表示请求的执行结果（如 200 表示成功）。

**request\_id** `string`

请求唯一标识。可用于请求明细溯源和问题排查。

**code** `string`

请求失败，表示错误码，成功时返回参数中该参数为空。

**message** `string`

请求失败，表示失败详细信息，成功时返回参数中该参数为空。

**output** `_object_`

任务输出信息。

**属性**

**embeddings** `_array_`

本次请求的算法输出内容，是一个由结构组成的数组，每一个数组中包含一个对应的输入 text 的算法输出内容。

**属性**

**sparse\_embedding** `_array_`

对应字符串的算法输出离散向量表示 （sparse embedding仅适用于`text-embedding-v3`与`text-embedding-v4`）。

**属性**

**index** `_integer_`

词汇或字符在词汇表中的位置索引。

**value** `_float_`

表示该 `Token` 的权重或重要性分数，值越高，表示该 `Token` 在当前文本上下文中的重要性或相关性越大。

**token** `_string_`

实际的文本单元或词汇表中的词。

**embedding** `_array_`

对应字符串的算法输出连续向量表示 （dense embedding)。

**text\_index** `_integer_`

本结构中的算法结果对应的输入文字在输入数组中的索引值。

**usage** `_object_`

**属性**

**total\_tokens** _integer_

本次请求输入内容的 token 数目，算法的计量是根据用户输入字符串被模型tokenizer解析之后对应的token 数目来进行。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
