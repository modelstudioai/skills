# CreateVocab - 创建热词

将一组语音热词上传到服务端，并获取返回热词ID。

## 接口说明

请确保在使用该接口前，已充分了解通义晓蜜 CCAI-对话分析 AIO 产品的收费方式和价格。

前提条件

-   已开通通义晓蜜 CCAI-对话分析 AIO 服务。
-   已创建应用：应用中心完成通义晓蜜 CCAI-对话分析 AIO 应用创建，并获取到 APP-ID 和 WORKSPACE-ID：[获取 APP-ID 和 WORKSPACE-ID](https://help.aliyun.com/zh/model-studio/developer-reference/obtain-api-key-app-id-and-workspace-id?spm=openapi-amp.newDocPublishment.0.0.39e3281fMO5qOX)。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/CreateVocab)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/CreateVocab)

## 授权信息

当前API暂无授权信息透出。

## 请求语法

```
POST /vocab/createVocab HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

body

object

否

请求 Body

workspaceId

string

是

业务空间 ID

llm-9\*\*\*\*me1

name

string

是

名称

词表1

description

string

否

版本描述

销售词表

audioModelCode

string

否

语音转写模型

nls

wordWeightList

array<object>

是

热词组

object

是

weight

integer

是

权重值

2

word

string

是

单词

大树

## [](#请求入参限制)请求入参限制

-   默认最多创建 10 个词表。
    
-   每个词表最多添加 500 个词，每个词语最长 10 个字。
    
-   业务专属热词必须为 UTF-8 编码，不能包含标点、特殊字符。
    
-   业务专属词对应的权重取值范围为\[-6,5\]之间的整数。
    
-   取值大于 0 增大该词语被识别的概率，小于 0 减小该词语被识别的概率。
    
-   取值为-6：表示尽量不要识别出该词语。
    
-   取值为 2：常用值。
    
-   如果效果不明显可以适当增加权重，但是当权重较大时可能会引起负面效果，导致其他词语识别不准确。
    

## [](#接口请求示例)接口请求示例

```java
import com.alibaba.fastjson.JSONObject;
import com.aliyun.contactcenterai20240603.Client;
import com.aliyun.contactcenterai20240603.models.CreateVocabRequest;
import com.aliyun.contactcenterai20240603.models.CreateVocabResponse;
import com.aliyun.teaopenapi.models.Config;

import java.util.ArrayList;
import java.util.List;

public class Vocab {

    private static String accessKeyId = "YOUR_ACCESS_KEY_ID";

    private static String accessKeySecret = "YOUR_ACCESS_KEY_SECRET";

    private static String workspaceId = "YOUR_WORKSPACE_ID";

    private static Config config = new Config();

    static {
        config.setAccessKeyId(accessKeyId).setAccessKeySecret(accessKeySecret).setEndpoint("contactcenterai.cn-shanghai.aliyuncs.com")
                .setReadTimeout(30000).setConnectTimeout(300000).setRegionId("cn-shanghai").setProtocol("HTTPS");
    }

    public static void main(String[] args) throws Exception {
        Client client = new Client(config);

        CreateVocabRequest request = new CreateVocabRequest();
        request.setName("销售词表");
        request.setDescription("东北一区销售业务专用");
        request.setWorkspaceId(workspaceId);

        List<CreateVocabRequest.CreateVocabRequestWordWeightList> wordWeightList = new ArrayList<>();
        CreateVocabRequest.CreateVocabRequestWordWeightList word1 = new CreateVocabRequest.CreateVocabRequestWordWeightList();
        word1.setWord("儿童");
        word1.setWeight(3);
        wordWeightList.add(word1);

        CreateVocabRequest.CreateVocabRequestWordWeightList word2 = new CreateVocabRequest.CreateVocabRequestWordWeightList();
        word2.setWord("金属");
        word2.setWeight(3);
        wordWeightList.add(word2);

        request.setWordWeightList(wordWeightList);

        CreateVocabResponse response = client.createVocab(request);
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

success

string

调用是否成功

True

data

object

返回数据。

vocabularyId

string

热词 id

f3d82\*\*\*\*\*\*\*7

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "968A8634-FA2C-5381-9B3E-*******F",
  "success": "True",
  "data": {
    "vocabularyId": "f3d82*******7"
  }
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
