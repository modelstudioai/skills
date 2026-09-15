# 删除响应

根据 Response ID 删除一个已存储的模型响应。

#### 华北2（北京）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`DELETE https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses/{response_id}`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

## 路径参数

**response\_id**`string`（必选）

要删除的 Response ID，格式为 `resp_xxx`。仅当原创建请求中 `store=true` 时返回的 Response ID 可被删除。

Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

response = client.responses.delete("resp_xxx")
print(response)
```

Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.responses.del("resp_xxx");
    console.log(response);
}

main();
```

curl

```
curl -X DELETE https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses/resp_xxx \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 返回结果

**id** `string`

被删除的 Response ID。

**deleted** `boolean`

是否删除成功，成功为 `true`。

```
{
    "deleted": true,
    "id": "resp_4ca7fa5e-6ff5-9787-bc18-af6ca5eff36c"
}
```

## 错误响应

当指定的 Response ID 不存在时，返回以下错误：

```
{
    "error": {
        "message": "Response with id 'resp_xxx' not found.",
        "type": "InvalidParameter"
    }
}
```
