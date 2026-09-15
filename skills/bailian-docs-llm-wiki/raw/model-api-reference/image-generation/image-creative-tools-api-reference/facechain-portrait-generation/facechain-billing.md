# FaceChain人物写真生成模型计量计费

**重要**

-   本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
-   FaceChain人物写真生成需“[申请体验](https://bailian.console.aliyun.com/model/market/detail/facechain-generation)”并通过后才可使用，否则API调用将返回错误状态码。

### 计费单元

**模型服务**

**计费单元**

FaceChain人物图像检测

限时免费

FaceChain人物形象训练

训练形象次数

FaceChain人物写真生成

生成图片张数

### 计费单价

**模型服务**

**模型名称**

**计费单价**

FaceChain人物图像检测

facechain-facedetect

限时免费

FaceChain人物形象训练

facechain-finetune

2.5元/次

FaceChain人物写真生成

facechain-generation

0.18元/张

### 免费额度

**模型名称**

**免费额度**

facechain-facedetect

申请体验通过后，单个阿里云账号（含RAM用户）对模型提供首次使用500张图像生成免费额度，有效期90天。

facechain-finetune

50次

有效期：申请通过后90天内

facechain-generation

500张

有效期：申请通过后90天内

**重要**免费额度将在申请体验审批通过后下一个整点生效。例如，您的审批在15:30分通过，您的免费额度将在16:00后生效，将抵扣您16:00后产生的账单费用。

**说明**您可以参阅[新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)确认您是否具备享有免费额度的资格，并查询免费总额度、剩余额度及到期时间。

### 接口限制

万相系列模型，均对调用QPS与并发进行限制，以账号（含子账户）为单位，模型间互相独立，限制信息如下。

**模型服务**

**模型名称**

**任务下发接口QPS限制**

**同时处理中任务数量**

FaceChain人物图像检测

facechain-facedetect

5

同步接口无限制

FaceChain人物形象训练

facechain-finetune

2

1

FaceChain人物写真生成

facechain-generation

2

1

## 查看账单

有关账单详情请前往[费用与成本](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)查询。
