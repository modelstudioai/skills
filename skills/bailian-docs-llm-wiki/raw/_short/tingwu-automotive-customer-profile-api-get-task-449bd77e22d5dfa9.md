# GetTask - 查询购车客户画像任务状态和结果

查询购车客户画像任务状态和结果的API参考。

<a id="前提条件"></a>

<a id="8a24f2ed09vr0"></a>

## 前提条件

已开通服务并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

> **说明**
>
> 当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](../model-api-reference/more-about-models/generate-temporary-api-key.md)。
>
> 与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。
>
> 使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

<a id="接入地址"></a>

<a id="52a5ef4ab7tfg"></a>

## 接入地址

<a id="code-block"></a>

```http
https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

<a id="请求方式"></a>

<a id="606a6390d6xdn"></a>

## 请求方式

post方法

<a id="请求头"></a>

<a id="24323e44bdlg5"></a>

## 请求头

<a id="code-block-2"></a>

```http
Authorization: Bearer {api-key} // 需将{api-key}替换为实际的API Key
Content-Type: application/json
```

<a id="获取任务结果"></a>

<a id="81e1c5277c5v0"></a>

## 获取任务结果

获取购车客户画像分析任务结果。

<a id="请求参数"></a>

<a id="aeb640d676sod"></a>

### 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| model | string | 是 | 定义业务类型，固定为`tingwu-automotive-customer-profile` | tingwu-automotive-customer-profile |
| input | object | 是 | 传入相关业务参数 |  |
| input.task | string | 是 | 定义任务类型，固定为`getTask`，表示获取任务结果 |  |
| input.dataId | string | 是 | 需要查询的音频任务id | wkb\*\*\* |

<a id="返回参数"></a>

<a id="e3ad7402edjab"></a>

### 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值/解析协议</strong></p></th></tr></thead><tbody><tr><td><p>code</p></td><td><p>string</p></td><td><p>错误码</p></td><td></td></tr><tr><td><p>message</p></td><td><p>string</p></td><td><p>错误信息</p></td><td></td></tr><tr><td><p>request_id</p></td><td><p>string</p></td><td><p>请求id</p></td><td><p>f97ee37d-0f9c-9b93-b6bf-bd263a232bf9</p></td></tr><tr><td><p>usage</p></td><td><p>object</p></td><td><p>用量</p></td><td><p>{}</p></td></tr><tr><td><p>output</p></td><td><p>object</p></td><td><p>业务返回体</p></td><td></td></tr><tr><td><p>output.status</p></td><td><p>string</p></td><td><p>任务状态：</p><ul><li><p>0：成功</p></li><li><p>1：进行中</p></li><li><p>2：失败</p></li></ul></td><td><p>0</p></td></tr><tr><td><p>output.errorCode</p></td><td><p>string</p></td><td><p>任务成功提交，但是执行失败（<code>status</code>为2时）的错误码</p></td><td><p>&quot;TSC.FileError&quot;</p></td></tr><tr><td><p>output.errorMessage</p></td><td><p>string</p></td><td><p>任务成功提交，但是任务执行失败（<code>status</code>为2时）的错误信息</p></td><td><p>&quot;File cannot be read.&quot;</p></td></tr><tr><td><p>output.customerProfilePath</p></td><td><p>string</p></td><td><p>分析结果的ossUrl，参见<a href="tingwu-automotive-customer-profile-api-get-task-449bd77e22d5dfa9.md#613d249381m8l">output.customerProfilePath 的解析协议</a></p></td><td rowspan="4"><p>ossUrl对应的文件内容解析协议参见：</p><ul><li><p><a href="tingwu-automotive-customer-profile-api-get-task-449bd77e22d5dfa9.md#613d249381m8l">output.customerProfilePath 的解析协议</a></p></li><li><p><a href="tingwu-automotive-customer-profile-api-get-task-449bd77e22d5dfa9.md#760913439awmi">output.transcriptionPath 的解析协议</a></p></li><li><p><a href="tingwu-automotive-customer-profile-api-get-task-449bd77e22d5dfa9.md#ad71dfc56eizu">output.identityRecognitionPath 的解析协议</a></p></li><li><p><a href="tingwu-automotive-customer-profile-api-get-task-449bd77e22d5dfa9.md#33e8cdf060pf3">output.contentExtractionsPath 的解析协议</a></p></li></ul></td></tr><tr><td><p>output.transcriptionPath</p></td><td><p>string</p></td><td><p>语音转文字结果的ossUrl，参见<a href="tingwu-automotive-customer-profile-api-get-task-449bd77e22d5dfa9.md#760913439awmi">output.transcriptionPath 的解析协议</a></p></td></tr><tr><td><p>output.identityRecognitionPath</p></td><td><p>string</p></td><td><p>角色识别结果ossUrl，参见<a href="tingwu-automotive-customer-profile-api-get-task-449bd77e22d5dfa9.md#ad71dfc56eizu">output.identityRecognitionPath 的解析协议</a></p></td></tr><tr><td><p>output.contentExtractionsPath</p></td><td><p>string</p></td><td><p>客户关注点内容提取结果ossUrl的集合（0个或多个），参见<a href="tingwu-automotive-customer-profile-api-get-task-449bd77e22d5dfa9.md#33e8cdf060pf3">output.contentExtractionsPath 的解析协议</a></p></td></tr></tbody></table>

<a id="output-transcriptionpath-的解析协议"></a>

<a id="760913439awmi"></a>

#### output.transcriptionPath 的解析协议

最外层是一个Object，具体字段如下：

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| paragraphs | Array | 段落列表 |  |
| paragraphs\[0\].paragraphId | String | 段落ID | 16987422100275\*\*\*\*\* |
| paragraphs\[0\].speakerId | String | 说话者ID | 1 |
| paragraphs\[0\].words | Array | 字词列表 |  |
| paragraphs\[0\].words\[0\].id | Integer | 字词编号 | 10 |
| paragraphs\[0\].words\[0\].sentenceId | Integer | 句子ID | 1 |
| paragraphs\[0\].words\[0\].start | Integer | 开始时间（毫秒） | 4970 |
| paragraphs\[0\].words\[0\].end | Integer | 结束时间（毫秒） | 5560 |
| paragraphs\[0\].words\[0\].text | String | 字词文本 | 您好， |

示例json如下：

<a id="code-block-3"></a>

```json
{
  "paragraphs": [
    {
      "paragraphId": "16987422100275*******",
      "speakerId": "1",
      "words": [
        {
          "id": 10,
          "sentenceId": 1,
          "start": 4970,
          "end": 5560,
          "text": "您好，"
        },
        {
          "id": 20,
          "sentenceId": 1,
          "start": 5730,
          "end": 6176,
          "text": "我是"
        }
      ]
    }
  ]
}
```

<a id="output-customerprofilepath-的解析协议"></a>

<a id="613d249381m8l"></a>

#### output.customerProfilePath 的解析协议

最外层是一个Object，具体字段如下：

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| saleClueClassify | Object | 销售线索分类 |  |
| saleClueClassify.classify | String | 线索类别 | B |
| saleClueClassify.evidence | String | 分类依据 | 客户仅表达想了解SUV，无明确购车意愿 |
| customerNotMentioned | Integer | 客户未提及个数 | 46 |
| tryDriveIntentionEvaluation | Object | 试驾意向评估 |  |
| tryDriveIntentionEvaluation.score | Integer | 评分 | 0 |
| tryDriveIntentionEvaluation.evidence | String | 评估依据 | 客户未提及试驾意愿，仅询问价位 |
| customerConcerned | Integer | 客户关注点个数 | 4 |
| oneSentenceSumUp | String | 客户关注点总结 | 客户关注点：SUV车型、外观设计、内饰质量、具体配置、续航能力、预计到店时间。顾虑点：购车过程中的价格透明度、售后服务、车辆实际性能与宣传是否一致。 |

示例json如下：

<a id="code-block-4"></a>

```json
{
  "saleClueClassify": {
    "classify": "B",
    "evidence": "客户仅表达想了解SUV，无明确购车意愿"
  },
  "customerNotMentioned": 46,
  "tryDriveIntentionEvaluation": {
    "score": 0,
    "evidence": "客户未提及试驾意愿，仅询问价位"
  },
  "customerConcerned": 4,
  "oneSentenceSumUp": "客户关注点：SUV车型、外观设计、内饰质量、具体配置、续航能力、预计到店时间。\n顾虑点：购车过程中的价格透明度、售后服务、车辆实际性能与宣传是否一致。"
}
```

<a id="output-identityrecognitionpath-的解析协议"></a>

<a id="ad71dfc56eizu"></a>

#### output.identityRecognitionPath 的解析协议

最外层是一个Object，具体字段如下：

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| identityResults | Array | 身份识别结果列表 |  |
| identityResults\[0\].identity | String | 识别的身份 | 客户 |
| identityResults\[0\].speakerId | String | 说话者ID | 1 |

示例json如下：

<a id="code-block-5"></a>

```json
{
  "identityResults": [
      {
          "identity": "客户",
          "speakerId": "1"
      },
      {
          "identity": "销售",
          "speakerId": "2"
      }
  ]
}
```

<a id="output-contentextractionspath-的解析协议"></a>

<a id="33e8cdf060pf3"></a>

#### output.contentExtractionsPath 的解析协议

最外层是一个JSONArray，内部的每一个元素如下：

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
| result | String | 结果描述 | 购车费用 |
| matchedSentenceIds | Array<Integer> | 匹配的句子ID列表 | \[1, 2\] |
| title | String | 标题 | 用车成本 |
| remarks | String | 备注 | 客户在对话中表达了对购车费用的关注，询问了关于价位的信息 |

示例json如下：

<a id="code-block-6"></a>

```json
[
  {
    "result": "未提及",
    "matchedSentenceIds": [],
    "title": "产品配置",
    "remarks": "对话中客户与销售的交流未涉及任何具体的产品配置细节，如AR-HUD、电动脚托或脚垫、全景天幕等。"
  },
  {
    "result": "购车费用",
    "matchedSentenceIds": [
      1,
      2
    ],
    "title": "用车成本",
    "remarks": "客户在对话中表达了对购车费用的关注，询问了关于价位的信息。"
  }
]
```

<a id="请求示例"></a>

<a id="a5536fd76fv4q"></a>

### 请求示例

请求头Authorization中的"sk-\*\*\*"需要替换为真实的阿里云百炼[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

<a id="code-block-7"></a>

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Authorization: Bearer sk-***' \
--header 'Content-Type: application/json' \
--data '{
  "model": "tingwu-automotive-customer-profile",
  "input": {
    "dataId": "***",
    "task": "getTask"
  }
}'
```

<a id="返回示例"></a>

<a id="7cbef05d68ydm"></a>

### 返回示例

<a id="code-block-8"></a>

```json
{
    "output": {
        "identityRecognitionPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/idRecog/1627865205776705/llm-3cx2a3o4n8y45iee/2025/07/09/2deb5d827f1548a88440b6a40836f239?Expires=***&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "customerProfilePath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/customerProfile/1627865205776705/llm-3cx2a3o4n8y45iee/2025/07/09/3880ad6e4b4e4f99a536ac472f083a04?Expires=***&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "contentExtractionsPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/conExtract/1627865205776705/llm-3cx2a3o4n8y45iee/2025/07/09/e669817cb93c4a90869d1b733aec8267?Expires=***&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "status": 0,
        "transcriptionPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/transcription/1627865205776705/llm-3cx2a3o4n8y45iee/2025/07/09/e565ebbb891e4943a482bda4619081aa?Expires=***&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE"
    },
    "usage": {},
    "request_id": "fb9f5972-0dc0-9d7f-afe6-3120b46419f4"
}
```
