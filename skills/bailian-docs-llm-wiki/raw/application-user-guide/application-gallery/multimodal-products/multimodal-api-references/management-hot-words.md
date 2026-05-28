# 管理热词

本文介绍如何使用热词OpenAPI程序化管理热词。

### **授权信息**

在使用热词OpenAPI前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具访问API。细节请参见[创建AccessKey](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)。注意：调用热词OpenAPI的账号与创建百炼多模态交互应用的账号需要属于同一个阿里云主账号。

RAM用户调用热词OpenAPI需要访问多模态对话产品的权限，授权方式如下：

在[RAM控制台](https://ram.console.aliyun.com/users)的身份管理 > 用户中，找到AccessKey所属的RAM账户，单击操作列的添加权限，选择系统策略中的“AliyunMultimodalDialogFullAccess”管理多模态对话（MultimodalDialog）的权限，授予RAM账户。

### **示例代码**

为方便您快速接入热词OpenAPI，建议使用阿里云SDK调用OpenAPI，可在[OpenAPI调试页面](https://api.aliyun.com/api/MultimodalDialog/2025-09-03/Vocabulary?RegionId=cn-beijing&tab=DEMO&lang=JAVA&useCommon=true)查看示例代码，并下载完整示例工程。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8629232671/p1018133.png)

### **请求参数**

请求参数在[热词OpenAPI门户](https://next.api.aliyun.com/document/MultimodalDialog/2025-09-03/Vocabulary)中有完整说明，本文档对创建热词、删除热词、更新热词、查询热词等操作的参数给出详细示例（代码调用方式可参考示例代码小节的说明，本文档仅以json格式给出各种操作需要填写的参数）。

#### **创建热词**

```
{
  "action": "createVocabulary",
  "vocabularyName": "热词表",
  "vocabulary":[
          {"text": "张三", "lang": "zh", "type": "contact_name"}, 
          {"text": "Bale", "lang": "en", "type": "contact_name"}
      ]
}
```
```
{
  "code": 200,
  "message": "Success", 
  "requestId": "a2a2987e2f8a********4ed7464d9593",
  "vocabularyId": "44f683d4cfd********c367f7f156587"
}
```

#### **删除热词**

```
{
  "action": "deleteVocabulary",
  "vocabularyId": "44f683d4cfd********c367f7f156587"
}
```
```
{
  "code": 200,
  "message": "Success", 
  "requestId": "b2a2987e2f8a********4ed7464d9593"
}
```

#### **更新热词**

```
{
  "action": "updateVocabulary",
  "vocabularyId": "44f683d4cfd********c367f7f156587",
  "vocabulary":[
          {"text": "张三", "lang": "zh", "type": "contact_name"},
          {"text": "Bale", "lang": "en", "type": "contact_name"}
      ]
}
```
```
{
  "code": 200,
  "message": "Success", 
  "requestId": "c2a2987e2f8a********4ed7464d9593"
}
```

#### **查询热词**

```
{
  "action": "queryVocabulary",
  "vocabularyIds": [
    "44f683d4cfd********c367f7f156587",
    "44f683d4cfd********c367f7f156587"
  ]
}
```
```
{
  "code": 200,
  "message": "Success", 
  "requestId": "d2a2987e2f8a********4ed7464d9593",
  "vocabularys":[
      {
        "vocabularyId": "44f683d4cfd********c367f7f156587",
        "vocabularyName": "***",
        "vocabulary":[
            {"text": "张三", "lang": "zh", "type": "contact_name"},
            {"text": "Bale", "lang": "en", "type": "contact_name"}
        ],
        "modifiedTime": 1749565022301
      },
      {
        "vocabularyId": "44f683d4cfd********c367f7f156587",
        "vocabularyName": "***",
        "vocabulary":[
            {"text": "张三", "lang": "zh", "type": "contact_name"},
            {"text": "Bale", "lang": "en", "type": "contact_name"}
        ],
        "modifiedTime": 1749565022301
      } 
    ]
}
```

### **常见问题**

1.  使用热词OpenAPI创建的热词，如何在对话链路中使用？
    

参考[实时多模态交互协议（WebSocket）](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol)，在Start指令中通过parameters.upstream.vocabulary\_id参数指定热词id，设置该参数后会覆盖管控台热词配置。
