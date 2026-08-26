# 模型下线机制说明

为优化资源利用和确保用户使用最新、最优模型，阿里云百炼平台将根据模型迭代升级情况不定期下线历史模型。本文将为您介绍模型下线机制。

## 通知机制

### 通知时间

-   **快照**模型（模型名称带有具体的日期标识，例如qwen-max-2025-01-25，常见于千问系列模型）将在正式**下线前30天**发布下线通知。
-   **主线**模型（系列模型的核心版本）将在正式**下线前3个月**发布下线通知。

### 通知方式

通过短信、邮件、站内信、官网公告等方式。

> 短信、邮件、站内信仅面向近3个月有待下线模型调用记录的用户。

## 下线影响

-   **自下线通知发布之日起**，将逐步缩减待下线模型的QPM（每分钟调用次数）和TPM（每分钟消耗Token数）。对于申请过扩容的模型，会先恢复至[默认限流](raw/model-user-guide/get-started-with-models/rate-limit.md)数据后再进行缩减。在此过程中，模型API接口、控制台上的相关功能均保持正常使用。
    
-   **自模型正式下线之日起**：
    
    -   **模型推理**：停止支持模型推理服务，已创建的调用该模型的应用和服务将无法返回结果。
    -   **模型调优及模型部署**：不再支持基于下线模型进行新的调优和部署操作（部分模型的调优与部署功能可能在模型下线后仍可正常使用，具体请以下线通知为准）。已经训练和部署的模型不受影响。
    -   **控制台功能及官方文档**：模型相关的控制台功能（模型广场、模型体验等）、官方文档将同步下线。

## 操作建议

1.  前往[模型观测](https://bailian.console.aliyun.com/#/model-telemetry)页面，检查您的账号是否正在使用待下线的模型。
2.  如果再使用，建议您先测试替代模型的业务效果，再切换至替代模型。

## 下线模型列表

### 2026年10月10日将下线

详细说明，请参见以下官网公告：

-   [https://www.aliyun.com/notice/118177](https://www.aliyun.com/notice/118177)
-   [https://www.aliyun.com/notice/118434](https://www.aliyun.com/notice/118434)
-   [https://www.aliyun.com/notice/118344](https://www.aliyun.com/notice/118344)
-   [https://www.aliyun.com/notice/118345](https://www.aliyun.com/notice/118345)
-   [https://www.aliyun.com/notice/118331](https://www.aliyun.com/notice/118331)
-   [https://www.aliyun.com/notice/118332](https://www.aliyun.com/notice/118332)

### 2026年5月30日已下线

详细说明，请参见官网公告[https://www.aliyun.com/notice/118217](https://www.aliyun.com/notice/118217)。

### 2026年5月13日已下线

详细说明，请参见官网公告[https://www.aliyun.com/notice/118178](https://www.aliyun.com/notice/118178)。

### 2026年3月30日已下线

该批次未发布专项公告。

### 2026年1月30日已下线

详细说明，请参见官网公告[https://www.aliyun.com/notice/117814](https://www.aliyun.com/notice/117814)。

### 2025年7月30日已下线

详细说明，请参见官网公告[https://www.aliyun.com/notice/117351](https://www.aliyun.com/notice/117351)。

### 2025年7月2日已下线

详细说明，请参见官网公告[https://www.aliyun.com/notice/117140](https://www.aliyun.com/notice/117140)。

### 2025年5月8日已下线

详细说明，请参见官网公告[https://www.aliyun.com/notice/117139](https://www.aliyun.com/notice/117139)。

### 2024年4月22日已下线

该批次未发布专项公告。
