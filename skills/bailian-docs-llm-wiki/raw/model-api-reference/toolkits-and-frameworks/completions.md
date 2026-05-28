# completions 接口

Completions 接口专为文本补全场景设计，适合代码补全、内容续写等场景。

**说明**

本文档仅适用于中国内地（北京地域），需使用中国（北京）地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## **支持的模型**

当前支持 [Qwen Coder](https://help.aliyun.com/zh/model-studio/qwen-coder) 部分模型：

qwen2.5-coder-7b-instruct、qwen2.5-coder-14b-instruct、qwen2.5-coder-32b-instruct、qwen-coder-turbo-0919、qwen-coder-turbo-latest、qwen-coder-turbo

## **前提条件**

您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过 OpenAI SDK 调用，需要[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

## **开始使用**

您可以通过 Completions 接口实现文本补全，当前支持以下两种文本补全场景：

1.  通过给定的前缀生成后续内容；
    
2.  通过给定的前缀与后缀生成中间内容；
    

> 暂不支持通过给定的后缀生成前缀内容。

### **快速开始**

您可以在前缀中传入函数的名称、输入参数、使用说明等信息，Completions 接口将返回生成的代码。

提示词模板为：

```
<|fim_prefix|>{prefix_content}<|fim_suffix|>
```

其中`{prefix_content}`是您需要传入的前缀信息。

Python

```
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

completion = client.completions.create(
  model="qwen2.5-coder-32b-instruct",
  prompt="<|fim_prefix|>写一个python的快速排序函数，def quick_sort(arr):<|fim_suffix|>",
)

print(completion.choices[0].text)
```

Node.js

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

async function main() {
    const completion = await openai.completions.create({
        model: "qwen2.5-coder-32b-instruct",
        prompt: "<|fim_prefix|>写一个python的快速排序函数，def quick_sort(arr):<|fim_suffix|>",
    });
    console.log(completion.choices[0].text)
}

main();
```

curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen2.5-coder-32b-instruct",
    "prompt": "<|fim_prefix|>写一个python的快速排序函数，def quick_sort(arr):<|fim_suffix|>"
}'
```

### **根据前缀和后缀生成中间内容**

Completions 接口支持通过您给定的前缀与后缀生成中间内容，您可以在前缀中传入函数的名称、输入参数、使用说明等信息，在后缀中传入函数的返回参数等信息，Completions 接口将返回生成的代码。

提示词模板为：

```
<|fim_prefix|>{prefix_content}<|fim_suffix|>{suffix_content}<|fim_middle|>
```

其中`{prefix_content}`是您需要传入的前缀信息，`{suffix_content}`为您需要传入的后缀信息。

Python

```
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

prefix_content = f"""def reverse_words_with_special_chars(s):
'''
反转字符串中的每个单词（保留非字母字符的位置），并保持单词顺序。
    示例:
    reverse_words_with_special_chars("Hello, world!") -> "olleH, dlrow!"
    参数:
        s (str): 输入字符串（可能包含标点符号）
    返回:
        str: 处理后的字符串，单词反转但非字母字符位置不变
'''
"""

suffix_content = "return result"

completion = client.completions.create(
  model="qwen2.5-coder-32b-instruct",
  prompt=f"<|fim_prefix|>{prefix_content}<|fim_suffix|>{suffix_content}<|fim_middle|>",
)

print(completion.choices[0].text)
```

Node.js

```
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
  apiKey: process.env.DASHSCOPE_API_KEY
});

const prefixContent = `def reverse_words_with_special_chars(s):
'''
反转字符串中的每个单词（保留非字母字符的位置），并保持单词顺序。
    示例:
    reverse_words_with_special_chars("Hello, world!") -> "olleH, dlrow!"
    参数:
        s (str): 输入字符串（可能包含标点符号）
    返回:
        str: 处理后的字符串，单词反转但非字母字符位置不变
'''
`;

const suffixContent = "return result";

async function main() {
  const completion = await client.completions.create({
    model: "qwen2.5-coder-32b-instruct",
    prompt: `<|fim_prefix|>${prefixContent}<|fim_suffix|>${suffixContent}<|fim_middle|>`
  });

  console.log(completion.choices[0].text);
}

main();
```

curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen2.5-coder-32b-instruct",
    "prompt": "<|fim_prefix|>def reverse_words_with_special_chars(s):\n\"\"\"\n反转字符串中的每个单词（保留非字母字符的位置），并保持单词顺序。\n    示例:\n    reverse_words_with_special_chars(\"Hello, world!\") -> \"olleH, dlrow!\"\n    参数:\n        s (str): 输入字符串（可能包含标点符号）\n    返回:\n        str: 处理后的字符串，单词反转但非字母字符位置不变\n\"\"\"\n<|fim_suffix|>return result<|fim_middle|>"
}'
```

## **输入与输出参数**

### **输入参数**

**参数**

**类型**

**必选**

**说明**

model

string

是

调用的模型名称。

prompt

string

是

要生成补全的提示。

max\_tokens

integer

否

本次请求返回的最大 Token 数。

> `max_tokens` 的设置不会影响大模型的生成过程，如果模型生成的 Token 数超过`max_tokens`，本次请求会返回截断后的内容。

temperature

float

否

采样温度，控制模型生成文本的多样性。

temperature越高，生成的文本更多样，反之，生成的文本更确定。

取值范围： \[0, 2.0)。

由于temperature与top\_p均可以控制生成文本的多样性，因此建议您只设置其中一个值。

top\_p

float

否

核采样的概率阈值，控制模型生成文本的多样性。

top\_p越高，生成的文本更多样。反之，生成的文本更确定。

取值范围：（0,1.0\]

由于temperature与top\_p均可以控制生成文本的多样性，因此建议您只设置其中一个值。

stream

boolean

否

是否流式输出回复。参数值：

-   false（默认值）：模型生成完所有内容后一次性返回结果。
    
-   true：边生成边输出，即每生成一部分内容就立即输出一个片段（chunk）。
    

stream\_options

object

否

当启用流式输出时，可通过将本参数设置为`{"include_usage": true}`，在输出的最后一行显示所使用的Token数。

stop

string 或 array

否

当模型生成的文本即将包含stop参数中指定的字符串或`token_id`时，将自动停止生成。

您可以在stop参数中传入敏感词来控制模型的输出。

seed

integer

否

设置seed参数会使文本生成过程更具有确定性，通常用于使模型每次运行的结果一致。

在每次模型调用时传入相同的seed值（由您指定），并保持其他参数不变，模型将尽可能返回相同的结果。

取值范围：0到231−1。

presence\_penalty

float

否

控制模型生成文本时的内容重复度。

取值范围：\[-2.0, 2.0\]。正数会减少重复度，负数会增加重复度。

### **输出参数**

**参数**

**类型**

**说明**

id

string

本次调用的唯一标识符。

choices

array

模型生成内容的数组。

choices\[0\].text

string

本次请求生成的内容。

choices\[0\].finish\_reason

string

模型停止生成的原因。

choices\[0\].index

integer

当前元素在数组中的索引，固定为0。

choices\[0\].logprobs

object

当前固定为`null`。

created

integer

本次请求被创建时的时间戳。

model

string

本次请求使用的模型名称。

system\_fingerprint

string

该参数当前固定为`null`。

object

string

对象类型，始终为 `"text_completion"`。

usage

object

本次请求的使用统计信息。

usage.prompt\_tokens

integer

`prompt` 转换为 Token 的数量。

usage.completion\_tokens

integer

`choices[0].text` 转换为 Token 的数量。

usage.total\_tokens

integer

`usage.prompt_tokens`与 `usage.completion_tokens` 的总和。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
