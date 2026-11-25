# CreateTask - 创建汽车销售服务洞察任务

创建汽车销售洞察服务任务，包括创建离线转写任务和服务质检任务。

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

<a id="e8ae9f13941un"></a>

## 接入地址

<a id="code-block"></a>

```http
https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

<a id="请求方式"></a>

<a id="58355fb966c2u"></a>

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

<a id="请求参数"></a>

<a id="34b842a7838b1"></a>

## 请求参数

<table><thead><tr><th><strong>名称</strong></th><th><strong>类型</strong></th><th><strong>必填</strong></th><th><strong>描述</strong></th><th><strong>示例值</strong></th></tr></thead><tbody><tr><td><p>model</p></td><td><p>string</p></td><td><p>是</p></td><td><p>定义业务类型，固定为<code>tingwu-automotive-service-insights</code></p></td><td><p>tingwu-automotive-service-insights</p></td></tr><tr><td><p>input</p></td><td><p>object</p></td><td><p>是</p></td><td><p>传入相关业务参数</p></td><td></td></tr><tr><td><p>input.fileUrl</p></td><td><p>string</p></td><td rowspan="3"><p>以下三个参数互斥且必选其一：fileUrl（音频文件OSS地址）、text（待分析文本）、dataId（已解析任务ID）</p></td><td><p>待分析文件oss URL地址</p></td><td><p>https://<em><strong>.oss-cn-hangzhou.aliyuncs.com/%E8%AF%95%E9%A9%BE%E6%A1%88%E4%BE%8Bsmall.wav?OSSAccessKeyId=YOUR_ACCESS_KEY_ID&amp;Expires=</strong></em>&amp;Signature=YOUR_SIGNATURE</p></td></tr><tr><td><p>input.text</p></td><td><p>string</p></td><td><p>待分析文本</p></td><td><p>每行必须按照如下格式：</p><p>${发言人名称}: ${发言人内容}</p><p>例子比如：</p><a id="code-block-3"></a><pre class="language-text"><code>张3: 我想买一个SUV汽车
李4: 想要什么价位的？
</code></pre></td></tr><tr><td><p>input.dataId</p></td><td><p>string</p></td><td><p>关联已上传并解析完成的任务</p></td><td></td></tr><tr><td><p>input.appId</p></td><td><p>string</p></td><td><p>是</p></td><td><p>应用id，可在控制台的应用配置页面获取</p></td><td></td></tr><tr><td><p>input.task</p></td><td><p>string</p></td><td><p>是</p></td><td><p>定义任务类型，固定为<code>createTask</code>，表示创建任务</p></td><td><p>createTask</p></td></tr><tr><td><p>parameters</p></td><td><p>object</p></td><td><p>否</p></td><td><p>汽车销售服务洞察控制参数（若传入空对象则复用已发布上线的配置项）</p></td><td></td></tr><tr><td><p>parameters.serviceInsights</p></td><td><p>object</p></td><td><p>否</p></td><td><p>汽车销售洞察参数对象</p></td><td></td></tr><tr><td><p>parameters.serviceInsights.insightsContents</p></td><td><p>list[]</p></td><td><p>是</p></td><td><p>汽车销售洞察的维度列表，包含洞察维度名称和定义，即需要大模型以什么样的标准判断该维度是否命中</p><strong>个数不超过150个</strong></td><td></td></tr><tr><td><p>parameters.serviceInsights.insightsContents[i].title</p></td><td><p>string</p></td><td><p>是</p></td><td><p>汽车销售洞察项的标题</p></td><td><p>开场介绍-品牌介绍</p></td></tr><tr><td><p>parameters.serviceInsights.insightsContents[i].content</p></td><td><p>string</p></td><td><p>是</p></td><td><p>汽车销售洞察项的内容</p></td><td><p>包含对汽车品牌的背景介绍</p></td></tr><tr><td><p>serviceInsights.insightsContents[i].score</p></td><td><p>string</p></td><td><p>否</p></td><td><p>汽车销售洞察项分值，用来表示该洞察项命中后，增加或扣减的分值，若未命中则为0</p><strong>范围是[-100, 100]</strong></td><td><p>50</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="e75d785e9ftr3"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td><p>output</p></td><td><p>object</p></td><td></td><td></td></tr><tr><td><p>output.dataId</p></td><td><p>string</p></td><td><p>任务id</p></td><td></td></tr><tr><td><p>output.status</p></td><td><p>string</p></td><td><ul><li><p>0：成功</p></li><li><p>1：进行中</p></li><li><p>2：失败</p></li></ul></td><td><p>0</p></td></tr><tr><td><p>usage</p></td><td><p>object</p></td><td><p>用量，目前为空object</p></td><td><p>{}</p></td></tr><tr><td><p>code</p></td><td><p>string</p></td><td><p>错误码</p></td><td><p>InvalidParameter</p></td></tr><tr><td><p>message</p></td><td><p>string</p></td><td><p>错误信息</p></td><td><p>Agent Input text format error.</p></td></tr><tr><td><p>request_id</p></td><td><p>string</p></td><td><p>请求id</p></td><td><p>f97ee37d-0f9c-9b93-b6bf-bd263a232bf9</p></td></tr></tbody></table>

<a id="请求示例"></a>

<a id="b38dac29897ll"></a>

## 请求示例

请求头Authorization中的"sk-\*\*\*"需要替换为真实的阿里云百炼[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

<a id="code-block-4"></a>

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Authorization: Bearer sk-******e181c' \
--header 'Content-Type: application/json' \
--data '{
    "model": "tingwu-automotive-service-insights",
    "input": {
        "task": "createTask",
        "text": "张*:我想买一个SUV\n李*:想要什么价位的？",
        "appId": "tw_***"
    },
    "parameters": {
        "serviceInsights": {
            "insightsContents": [
                {
                    "title": "到店迎接-欢迎语",
                    "content": "销售在开场白的时候主动向客户打招呼进行欢迎",
                    "score": "20"
                },
                {
                    "title": "离店送别-客户留资",
                    "content": "销售邀请客户留下微信、电话号码、名片等联系方式",
                    "score": "30"
                },
                {
                    "title": "到店迎接-饮品提供",
                    "content": "销售在接待客户的时候主动询问是否需要饮料（如咖啡、橙汁、水、茶等）、点心、零食、水果等",
                    "score": "50"
                }
            ]
        }
    }
}'
```

<a id="返回示例"></a>

<a id="47c8bc4835pnk"></a>

## 返回示例

<a id="code-block-5"></a>

```json
{
    "output": {
        "dataId": "dj***"
    },
    "usage": {},
    "request_id": "8313c0bc-ff3f-98e8-b87a-0118f6fe3049"
}
```
