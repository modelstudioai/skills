# AnalyzeAudioSync - 语音文件实时分析

对进行语音文件进行实时对话分析。应用调用支持 HTTPS 调用来完成客户的响应。

## 接口说明

请确保在使用该接口前，已充分了解通义晓蜜 CCAI-对话分析 AIO 产品的收费方式和价格。

## [](#前提条件)前提条件

-   1.已开通通义晓蜜 CCAI-对话分析 AIO 服务。
-   2.已创建应用：应用中心完成通义晓蜜 CCAI-对话分析 AIO 应用创建，并获取到 APP-ID 和 WORKSPACE-ID：[获取 APP-ID 和 WORKSPACE-ID](https://help.aliyun.com/zh/model-studio/developer-reference/obtain-api-key-app-id-and-workspace-id?spm=openapi-amp.newDocPublishment.0.0.3491281fOQZK5f)。

## [](#注意事项)注意事项

-   1.超过 3 分钟的音频请使用离线任务分析。
-   2.目前支持双轨录音文件，并且需要指定声轨对应的角色。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/AnalyzeAudioSync)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/AnalyzeAudioSync)

## 授权信息

当前API暂无授权信息透出。

## 请求语法

```
POST /{workspaceId}/ccai/app/{appId}/analyzeAudioSync HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

业务空间 Id

llm-ik\*\*\*\*\*\*RVYCKzt

appId

string

是

应用 id

a070a49c681f4a95a0f0\*\*\*\*\*\*\*\*\*35c

body

object

否

请求体

modelCode

string

否

模型 code

tyxmTurbo

fields

array<object>

否

字段结构信息

object

否

字段结构信息

code

string

否

字段编码

phoneNumber

name

string

否

字段名称

来电原因类型

desc

string

否

字段描述

用户来电咨询的原因分类，主要有投诉、咨询、政策建议等。

enumValues

array<object>

否

枚举值列表

object

否

枚举值列表

desc

string

否

枚举描述

客户有新的需求/新的场景，客服跟进沟通需求细节

enumValue

string

否

枚举值

新业务拓展

resultTypes

array

否

任务类型

string

是

summary-对话摘要，title-标题生成、fields-字段信息抽取、keywords -关键字抽取，service\_inspection-服务质检、question\_solution-问题和解决方案、questions\_and\_answer-QA 抽取、custom\_prompt-自定义指令

summary

serviceInspection

object

否

服务质检结构信息

inspectionContents

array<object>

否

质检项列表

object

否

质检项结构

content

string

否

质检项描述

客服在服务客户过程中，基于已有的服务标准是否存在过度承诺的行为，如：最快到货时间是12小时，无法给客户承诺更快的到货时间。

title

string

否

质检名称

客服是否过度承诺

inspectionIntroduction

string

否

服务质检场景详细介绍及描述

请检测客服是否存在服务不当的行为，包括：过度承诺、故意套取客户隐私信息等

sceneIntroduction

string

否

服务质检场景

保险销售场景

templateIds

array

否

模版 id

string

否

模版 id，模版 id 和指令任务类型同时存在时，优先使用模版 id

34

categoryTags

array<object>

否

标签分类列表

object

否

标签分类列表

tagName

string

否

标签名称

客服过度承诺

tagDesc

string

否

标签描述

客服在服务客户过程中，基于已有的服务标准是否存在过度承诺的行为

customPrompt

string

否

自定义指令

对通话内容进行总结

transcription

object

否

语音类型执行参数

autoSplit

integer

否

多数情况下适用于单轨录音，取值：0、1，是否自动分轨，1 为自动分轨，0 为不分轨；默认：1；若指定为 1，则表示上传的音频为单轨；自动分轨会额外占用处理时间。若录音为双轨录音，该参数必须传 0。

1

clientChannel

integer

否

适用于双轨录音，指定客户角色的轨道编号，取值：0、1，默认 1，即第 1 轨为客户；通常音轨都是从 0 开始编号，2 个轨就是 0，1；具体 0 是客服还是客户，需要您自行确认。\*\*若使用此参数，请务必传入 autoSplit 参数，值为 0。\*\*单轨文件忽略此参数。

1

serviceChannel

integer

否

适用于双轨录音，指定客服角色的轨道编号，取值：0、1，默认 0，即第 0 轨为客服；通常音轨都是从 0 开始编号，2 个轨就是 0，1；具体 0 是客服还是客户，需要您自行确认。\*\*若使用此参数，请务必传入 autoSplit 参数，值为 0。\*\*若单轨文件忽略此参数。

1

fileName

string

是

文件名。

sss.mp3

voiceFileUrl

string

是

文件地址

http://1111.com/sss.mp3

serviceChannelKeywords

array

否

客服通话关键字列表

string

否

多数情况下适用于单轨录音，设置一组客服可能说的关键词列表（请确保选择那些区别性比较高的关键词），通过对转写文本从上到下逐句分析，当一句话命中某一个关键词时，则判定该句的角色为客服，则另一个角色就是客户。

你好

asrModelCode

string

否

语音转写模型，取值 nls （小模型），paraformer（大模型）

nls

vocabularyId

string

否

语音热词 id

esnvknv\*\*\*\*\*skdnvjksd

level

string

否

语音转写优先级

low

variables

array<object>

否

变量列表

object

否

变量列表

variableCode

string

否

变量 code

name

variableValue

string

否

变量值

张三

responseFormatType

string

否

输出结果格式化类型，jsonObject-json 结构，text-原始字符串

jsonObject

stream

boolean

是

是否流式返回结果，流式返回-true，全量返回-false

false

## [](#接口请求示例)接口请求示例

```java
import com.alibaba.fastjson.JSONObject;
import com.aliyun.contactcenterai20240603.Client;
import com.aliyun.contactcenterai20240603.models.AnalyzeAudioSyncRequest;
import com.aliyun.contactcenterai20240603.models.AnalyzeAudioSyncResponse;

import com.aliyun.teaopenapi.models.Config;

import java.util.ArrayList;
import java.util.List;

public class CCAiTask {

    public static void main(String[] args) throws Exception {
        String accessKeyId = "YOUR_ACCESS_KEY_ID";
        String accessKeySecret = "YOUR_ACCESS_KEY_SECRET";
        String workspaceId = "YOUR_WORKSPACEID";
        String appId = "YOUR_APPID";

        Config config = new Config();
        config.setAccessKeyId(accessKeyId).setAccessKeySecret(accessKeySecret).setEndpoint("contactcenterai.cn-shanghai.aliyuncs.com")
                .setRegionId("cn-shanghai").setProtocol("HTTPS");

        Client client = new Client(config);

        AnalyzeAudioSyncRequest request = new AnalyzeAudioSyncRequest();
        request.setStream(false);

        request.setModelCode("tyxmPlus");

        List<String> typeList = new ArrayList<>();
        typeList.add("summary");
        request.setResultTypes(typeList);

        AnalyzeAudioSyncRequest.AnalyzeAudioSyncRequestTranscription transcription = new AnalyzeAudioSyncRequest.AnalyzeAudioSyncRequestTranscription();
        transcription.setFileName("out**.wav");
        transcription.setVoiceFileUrl("https://age***.com/out**.wav");
        transcription.setServiceChannel(1);
        transcription.setClientChannel(0);

        request.setTranscription(transcription);

        AnalyzeAudioSyncResponse response = client.analyzeAudioSync(workspaceId, appId, request);
        System.out.println(JSONObject.toJSONString(response));
    }
    
}
```

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

requestId

string

请求 id

968A8634-FA2C-5381-9B3E-\*\*\*\*\*\*\*F

finishReason

string

如果是流式输出，正在生成时为 null，生成结束时如果由于停止 token 导致则为 stop。

stop

success

boolean

请求是否成功

True

text

string

应用返回的结果。

这段对话似乎是客服与客户之间关于一个服务或产品的讨论，但具体内容难以明确理解，因为对话中的言语比较零散和抽象。

inputTokens

string

输入 Token 数量

1000

outputTokens

string

输出 Token 数量

2000

totalTokens

string

Tokens 总量

3000

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "968A8634-FA2C-5381-9B3E-*******F",
  "finishReason": "stop",
  "success": true,
  "text": "这段对话似乎是客服与客户之间关于一个服务或产品的讨论，但具体内容难以明确理解，因为对话中的言语比较零散和抽象。",
  "inputTokens": 1000,
  "outputTokens": 2000,
  "totalTokens": 3000
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

400

CCAI.InvalidParam.NotExist

The specified parameter %s is not valid.

请求API的参数不存在

400

CCAI.ParamInvalid.IllegalParamValue

The parameter value of the request API is illegal %s.

请求API的参数不合法

400

CCAI.Throttling.Qpm

Trigger QPM flow restriction. Please purchase higher QPM for paid API. If free API has special requirements, please contact us through DingTalk group (62730018475).

触发QPM限流，付费API请购买更高QPM，免费API如有特殊需求，请通过钉钉群（62730018475）联系我们。

400

CCAI.Throttling.Qps

Trigger current QPS limit, pay API please buy higher QPS, the free API if you have special requirements, please contact us through the DingTalk group (62730018475).

触发限流，付费API请购买更高QPS，免费API如有特殊需求，请通过钉钉群（62730018475）联系我们。

403

CCAI.IllegalPermission.NoAuth

User not authorized to operate on the specified resource.

该用户未被授权可操作指定资源

403

CCAI.ParamNotfound.MissParam

Parameter verification failed, The specified parameter %s is missing.

参数校验失败，指定参数缺失。

403

CCAI.TenantPermission.NoAuth

The current account does not have the permission to specify the business space. Please authorize the business space permission.

当前账号没有指定业务空间的权限，请进行业务空间权限授权。

500

CCAI.InternalError

The request processing has failed due to some unknown error, exception or failure.

系统内部错误，请稍后重试

访问[错误中心](< https://api.aliyun.com/document/ContactCenterAI/2024-06-03/errorCode>)查看更多错误码。
