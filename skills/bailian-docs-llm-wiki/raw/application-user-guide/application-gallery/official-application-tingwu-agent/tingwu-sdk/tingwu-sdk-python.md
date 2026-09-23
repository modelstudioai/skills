# 服务端Python SDK

本文介绍通义听悟 Python SDK，帮助开发者快速调用服务。

## 前提条件

已开通服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

**说明**当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。

使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

-   [安装最新版DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)（DashScope版本号须>=1.24.1，Python须3.9及以上版本）。

## 接口说明

### TingWu.py

通过`TingWu.py`的`call`方法调用服务：

```
def call(
          model: str,
          user_defined_input: Dict[str, Any],
          parameters: Dict[str, Any] = None,
          api_key: str = None,
          **kwargs
  ) -> DashScopeAPIResponse:
"""Call generation model service.

    Args:
          model (str): The requested model, such as qwen-turbo
          api_key (str, optional): The api api_key, can be None,
              if None, will get by default rule(TODO: api key doc).
          user_defined_input: custom input
          parameters: custom parameters
          **kwargs:
              base_address: base address
              additional parameters for request

    Raises:
          InvalidInput: The history and auto_history are mutually exclusive.

    Returns:
          Union[GenerationResponse,
                Generator[GenerationResponse, None, None]]: If
          stream is True, return Generator, otherwise GenerationResponse.
"""
```

以[汽车销售服务洞察](raw/application-user-guide/application-gallery/official-application-tingwu-agent/tingwu-automotive-service-insights.md)为例，关键参数说明如下，更多参数请参见[汽车销售服务洞察API参考](raw/_short/tingwu-automotive-service-insights-api-bd40f6442abd84b5.md)或[购车客户画像API参考](raw/_short/tingwu-automotive-customer-profile-api-cf3538cc3525d65a.md)：

-   model
    
    **名称**
    
    **类型**
    
    **必填**
    
    **描述**
    
    **示例值**
    
    model
    
    string
    
    是
    
    定义业务类型
    
    具体参数请参见API参考
    
    tingwu-automotive-service-insights
    
-   user\_defined\_input
    
    **名称**
    
    **类型**
    
    **必填**
    
    **描述**
    
    **示例值**
    
    fileUrl
    
    string
    
    3选1
    
    待分析文件oss URL地址
    
    https://_**.oss-cn-hangzhou.aliyuncs.com/%E8%AF%95%E9%A9%BE%E6%A1%88%E4%BE%8Bsmall.wav?OSSAccessKeyId=YOUR\_ACCESS\_KEY\_ID&Expires=**_&Signature=YOUR\_SIGNATURE
    
    text
    
    string
    
    待分析文本
    
    每行必须按照如下格式：
    
    ${发言人名称}: ${发言人内容}
    
    例子比如：
    
    ```
    张3: 我想买一个SUV汽车
    李4: 想要什么价位的？
    ```
    
    dataId
    
    string
    
    已上传并解析完成的任务id
    
    appId
    
    string
    
    是
    
    应用id
    
    task
    
    string
    
    是
    
    任务类型：
    
    -   createTask：创建任务
    -   getTask：获取任务结果
    
    createTask
    
-   parameters（具体参数请参见API参考）
    

#### 示例代码

```
from dashscope.multimodal.tingwu.tingwu import TingWu
import os

# 创建TingWu实例
tingwu = TingWu()
resp = TingWu.call(
    model='tingwu-automotive-service-insights',
    user_defined_input={"task": "createTask", "text": "张*:我想买一个SUV\n李*:想要什么价位的？", "appId": "123456"},
    api_key="your_api_key",
    base_address="https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
    parameters={"serviceInsights": {"insightsContents": [
        {"title": "到店迎接-欢迎语", "content": "销售在开场白的时候主动向客户打招呼进行欢迎", "score": "20"},
        {"title": "离店送别-客户留资", "content": "销售邀请客户留下微信、电话号码、名片等联系方式", "score": "30"},
        {"title": "到店迎接-饮品提供",
         "content": "销售在接待客户的时候主动询问是否需要饮料（如咖啡、橙汁、水、茶等）、点心、零食、水果等", "score": "50"}]}}
)
print(resp)
```

## 响应结果

以[汽车销售服务洞察](raw/application-user-guide/application-gallery/official-application-tingwu-agent/tingwu-automotive-service-insights.md)为例，主要返回参数如下，更多说明请参见[汽车销售服务洞察API参考](raw/_short/tingwu-automotive-service-insights-api-bd40f6442abd84b5.md)或[购车客户画像API参考](raw/_short/tingwu-automotive-customer-profile-api-cf3538cc3525d65a.md)：

**名称**

**类型**

**描述**

**示例值**

output

object

output.dataId

string

任务id

output.status

string

-   0：成功
    
-   1：进行中
    
-   2：失败
    

0

usage

object

code

string

错误码

InvalidParameter

message

string

错误信息

Agent Input text format error.

request\_id

string

请求id

f97ee37d-0f9c-9b93-b6bf-bd263a232bf9

响应结果示例：

```
{
    "output": {
        "dataId": "dj***"
    },
    "usage": {},
    "request_id": "8313c0bc-ff3f-98e8-b87a-0118f6fe3049"
}
```
