# 妙笔写作信源对接

本文档主要介绍妙笔对接写作信源的操作步骤，有两种写作信源的对接方式，分别是API对接和本地上传，它们均可以作为写作信源提供相应素材能力。

## **通过API引入数据源**

-   客户已经有自己的搜索引擎或者是RAG链路，此时可以通过配置接口来实现信源配置，可直接通过API 进行配置，具体操作如下：
    

1\. 第一步调用[数据源-创建](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-createdataset)接口：http://${host}/api/privateDataset/createDataset

请求入参示例：

```
{
 "datasetName": "f1869e067f104c2897906e1f9cd268",
 "datasetType": "ThirdSearch",
 "datasetDescription": "test_11"
}
```

2\. 第二步调用[数据源-修改](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-updatedataset)接口：http://${host}/api/privateDataset/updateDataset

请求入参示例：

```
{
  "agentId": "3",
  "tenantId": "3",
  "datasetId": 463,
  "createUser": "227",
  "createTime": "2025-12-08 10:39:21",
  "datasetType": "ThirdSearch",
  "datasetName": "d18f9d02087c4e309470bf73df3329",
  "datasetConfig": {
    "searchSourceConfigs": [
      {
        "searchSourceRequestConfig": {
          "url": "http://xxxx/api/search",
          "method": "GET",
          "connectTimeout": 3000,
          "socketTimeout": 3000,
          "headers": [
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ],
          "params": [
            {
              "name": "querySelf",
              "value": "${query}"
            },
            {
              "name": "current",
              "value": "${current}"
            },
            {
              "name": "size",
              "value": "${size}"
            },
            {
              "name": "includeContent",
              "valueType": "boolean",
              "value": "${includeContent}"
            },
            {
              "name": "startTime",
              "valueType": "time",
              "valueFormat": "yyyy-MM-dd HH:mm:ss",
              "value": "${startTime}"
            },
            {
              "name": "endTime",
              "valueType": "time",
              "valueFormat": "yyyy-MM-dd HH:mm:ss",
              "value": "${endTime}"
            }
          ],
          "pathParamsEnable": false,
          "body": "{\"query\":\"${querySelf}\",\"size\":\"${size}\",\"current\":\"${current}\"}"
        },
        "searchSourceResponseConfig": {
          "jqNodes": [
            {
              "key": "total",
              "type": "number",
              "path": "totalSelf"
            },
            {
              "key": "data",
              "type": "list",
              "path": "dataSelf",
              "jqNodes": [
                {
                  "key": "summary",
                  "type": "string",
                  "path": "summary"
                },
                {
                  "key": "score",
                  "type": "string",
                  "path": "score"
                },
                {
                  "key": "docUuid",
                  "type": "string",
                  "path": "docUuid"
                },
                {
                  "key": "pubTime",
                  "type": "string",
                  "path": "pubTime"
                },
                {
                  "key": "source",
                  "type": "string",
                  "path": "source"
                },
                {
                  "key": "tag",
                  "type": "string",
                  "path": "tag"
                },
                {
                  "key": "title",
                  "type": "string",
                  "path": "title"
                },
                {
                  "key": "extendInfo",
                  "type": "object",
                  "path": ".",
                  "jqNodes": [
                    {
                      "key": "docUuid",
                      "type": "string",
                      "path": "docUuid"
                    }
                  ]
                },
                {
                  "key": "url",
                  "type": "string",
                  "path": "url"
                },
                {
                  "key": "content",
                  "type": "string",
                  "path": "content"
                }
              ]
            }
          ]
        }
      }
    ]
  },
  "datasetDescription": "11211",
  "searchDatasetEnable": 3,
  "documentHandleConfig": {}
}
```

-   具体参数含义请参考如下文档：[妙搜-通过API引入数据源](https://help.aliyun.com/zh/model-studio/miaosou-introduce-data-source-through-api)。
    

## **上传文件用作数据源**

此种场景为客户仅有原始数据，没有现成的搜索引擎或者RAG链路，需要通过全妙-妙搜的能力构建向量索引。所以需要将用户的原始数据上传到妙搜中构建为数据源，此场景下需要客户开通妙搜服务，可以点击[计费说明（妙搜和妙读）](https://help.aliyun.com/zh/model-studio/miaosou-miaodu-api-billing)文档查看开通和计费的详情。

具体对接的接口文档：[数据源-创建](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-createdataset)、[妙搜-智能搜索](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runsearchgeneration)。
