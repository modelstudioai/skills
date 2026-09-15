# 数学能力（Qwen-Math）

阿里云百炼提供的 Qwen-Math 系列模型具备强大的数学推理和计算能力，模型提供详细的解题步骤，便于理解和验证。

**说明**

-   推荐参考[选择模型](raw/model-user-guide/get-started-with-models/models.md)，使用**最新的**通用模型替代 Qwen-Math 模型，后者仍基于 Qwen2.5 模型。
-   本文档仅适用于华北2（北京）地域，需使用华北2（北京）地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 模型与价格

**商业版**

**模型名称**

**输入价格**

**输出价格**

**上下文长度**

**最大输入**

**最大输出**

**免费额度**

[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#977b13081ab56)

**（每百万Token）**

**（Token数）**

**qwen-math-plus**

4元

12元

4,096

3,072

3,072

各100万Token

有效期：百炼开通后90天内

**qwen-math-turbo**

2元

6元

> **各模型的免费额度均不共用。**

关于模型的限流条件，请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 快速开始

您需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过OpenAI SDK或DashScope SDK进行调用，还需要[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。请将示例代码中的 `DASHSCOPE_API_HOST` 替换为获取的 API Host。

#### OpenAI兼容

Python

```
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"), # 请勿在代码中硬编码凭证，应始终使用环境变量或密钥管理服务
    # 以下为华北2（北京）地域的URL，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-math-plus",
    messages=[{'role': 'user', 'content': 'Derive a universal solution for the quadratic equation $ Ax^2+Bx+C=0 $'}])
print(completion.choices[0].message.content)
```

curl

```
curl --location "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
    "model": "qwen-math-plus",
    "messages": [
        {
            "role": "user",
            "content": "Derive a universal solution for the quadratic equation $ Ax^2+Bx+C=0 $"
        }
    ]
}'
```

#### DashScope

Python

```
from http import HTTPStatus
import dashscope

# 以下为华北2（北京）地域的URL，各地域的URL不同。
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

def call_with_messages():
    messages = [
        {'role': 'user', 'content': 'Derive a universal solution for the quadratic equation $ Ax^2+Bx+C=0 $'}]
    response = dashscope.Generation.call(
        model='qwen-math-plus',
        messages=messages,
        # 设置result_format为message格式
        result_format='message',
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

if __name__ == '__main__':
    call_with_messages()
```

Java

```
import java.util.Arrays;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    public static void callWithMessage()
            throws NoApiKeyException, ApiException, InputRequiredException {
        // 以下为华北2（北京）地域的URL，各地域的URL不同。
        Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
        Generation gen = new Generation();
        Message userMsg = Message.builder().role(Role.USER.getValue()).content("Derive a universal solution for the quadratic equation $ Ax^2+Bx+C=0 $").build();
        GenerationParam param =GenerationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-math-plus")
                .messages(Arrays.asList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();
        GenerationResult result = gen.call(param);
        System.out.println(result);
    }

    public static void main(String[] args){
        try {
            callWithMessage();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

curl

```
curl --location "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
    "model": "qwen-math-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": "Derive a universal solution for the quadratic equation $ Ax^2+Bx+C=0 $"
            }
        ]
    },
    "parameters": {
        "result_format": "message"
    }
}'
```

> 也可以前往[百炼控制台](https://bailian.console.aliyun.com/model/experience/text?modelId=qwen-math-plus)体验模型。

## 使用建议

1.  **使用英文+ LaTeX：**Qwen-Math 模型专精于英文数学问题，输入时建议使用 LaTeX 表示数学符号或公式。
2.  **规范内容输出：**[前缀续写模式（Partial Mode）](raw/model-user-guide/model-experience/text-generation-model/partial-mode.md)可提供精确控制能力，确保模型输出的内容紧密衔接提供的前缀，提升生成结果的准确性与可控性。
3.  模型默认设置`temperature=0`，无须调节。
4.  **便捷提取结果：**Qwen-Math 模型默认将把最终结果输出在`\boxed{}`区块中。

```
### Final Answer:
The universal solution for the quadratic equation $ Ax^2 + Bx + C = 0 $ is:
$$
\boxed{x = \frac{-B \pm \sqrt{B^2 - 4AC}}{2A}}
$$
```

## 常见问题

**如何利用通义千问数学模型解答图片中的数学问题？**

通义千问数学模型暂不支持图片识别功能。

-   如果图片中是简单的数学问题，可以使用[通义千问VL](raw/model-user-guide/model-experience/vision-model/vision.md)、[QVQ](raw/model-user-guide/model-experience/vision-model/visual-reasoning.md) 模型进行解答。
    
-   如果图片中包含复杂的数学问题，可以先使用[通义千问VL](raw/model-user-guide/model-experience/vision-model/vision.md)、[QVQ](raw/model-user-guide/model-experience/vision-model/visual-reasoning.md) 模型提取图片中的文字，再使用通义千问数学模型解答问题。
    

关于通义千问数学模型的输入与输出参数，请参考[通义千问 API 参考](raw/model-api-reference/qwen-api-reference.md)。

**在哪里可以查到错误码的详细信息？**

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
