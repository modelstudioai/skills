# 服务端Java SDK

本文介绍通义听悟 Java SDK，帮助开发者快速调用服务。

## 前提条件

已开通服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

**说明**当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。

使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

-   [安装最新版DashScope SDK](raw/model-api-reference/preparations/install-sdk.md)（DashScope版本号须>=2.21.1）

## 接口说明

### TingWuParam.java

参数配置类。以[汽车销售服务洞察](raw/application-user-guide/application-gallery/official-application-tingwu-agent/tingwu-automotive-service-insights.md)为例，创建任务主要参数如下，更多参数说明请参见[汽车销售服务洞察API参考](raw/application-user-guide/application-gallery/official-application-tingwu-agent/tingwu-automotive-service-insights/tingwu-automotive-service-insights-api.md)或[购车客户画像API参考](raw/application-user-guide/application-gallery/official-application-tingwu-agent/tingwu-automotive-customer-profile/tingwu-automotive-customer-profile-api.md)：

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

input

object

是

传入相关业务参数

input.fileUrl

string

3选1

待分析文件oss URL地址，sdk调用

https://_**.oss-cn-hangzhou.aliyuncs.com/%E8%AF%95%E9%A9%BE%E6%A1%88%E4%BE%8Bsmall.wav?OSSAccessKeyId=YOUR\_ACCESS\_KEY\_ID&Expires=**_&Signature=YOUR\_SIGNATURE

input.text

string

待分析文本

每行必须按照如下格式：

${发言人名称}: ${发言人内容}

例子比如：

```
张3: 我想买一个SUV汽车
李4: 想要什么价位的？
```

input.dataId

string

关联已上传并解析完成的任务

input.appId

string

是

应用id

input.task

string

是

定义任务类型：

-   createTask：表示创建任务
-   getTask：表示获取任务结果

createTask

parameters

object

否

请求参数（若传入空对象则复用已发布上线的配置项）

具体参数请参见API参考

#### 示例代码

```
import java.util.Map;
import java.util.HashMap;
import com.alibaba.dashscope.multimodal.tingwu.TingWuParam;

//构建自定义 Input
public static Map<String, Object> buildCustomInput(String appId) {
        Map<String, Object> params = new HashMap<>();
        params.put("fileUrl", "http://demo.com/test.mp3");
        params.put("appId", appId);
        params.put("task", "createTask");
        //设置其他参数
        return params;
}
//构建 TingWuParam
TingWuParam param = TingWuParam.builder().
    model("tingwu-automotive-service-insights")
    .input(buildCustomInput("your_app_id"))
    .parameters(new HashMap<>())  //设置parameters参数
    .apiKey("your_api_key")
    .build();
```

### TingWu.java

-   听悟 Http服务接口类。

```
/**
 * the tingwu client with baseUrl
 * param protocol : http or websocket, default should http
 * param baseUrl : custom server host
 */
public TingWu(String protocol, String baseUrl)
```

-   发送请求，返回[响应结果](https://help.aliyun.com/zh/model-studio/tingwu-sdk-java#16ca9e9081zuf)。

```
/**
 * Call the server to get the whole result, only http protocol
 * param param: the TingWuParam
 * return DashScopeResult
 */
public DashScopeResult call(TingWuParam param)
```

## 响应结果

以[汽车销售服务洞察](raw/application-user-guide/application-gallery/official-application-tingwu-agent/tingwu-automotive-service-insights.md)为例，主要返回参数如下，更多说明请参见[汽车销售服务洞察API参考](raw/application-user-guide/application-gallery/official-application-tingwu-agent/tingwu-automotive-service-insights/tingwu-automotive-service-insights-api.md)或[购车客户画像API参考](raw/application-user-guide/application-gallery/official-application-tingwu-agent/tingwu-automotive-customer-profile/tingwu-automotive-customer-profile-api.md)：

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
