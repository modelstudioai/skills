# 模型下线机制说明

为优化资源利用和确保用户使用最新、最优模型，阿里云百炼平台将根据模型迭代升级情况不定期下线历史模型。本文将为您介绍模型下线机制。

## 模型类型

百炼提供的模型版本分为正式版和预览版两类，建议优先使用正式版模型。

-   **正式版模型**：面向生产环境的稳定商用版本。同一模型系列提供三种形态：系列模型名（如 qwen-max、qwen-plus、qwen-turbo）、带「年-月-日」日期后缀的版本名（如 qwen-max-2025-01-25）、-latest 别名（如 qwen-max-latest）。以上形态均属于正式版模型。
-   **预览版模型**：公测模型，模型 ID 中包含 preview、beta、experimental 等标识，或在文档、控制台中明确标注为「预览版」。预览版模型用于新能力验证和体验收集，版本更新较快，后续可能下线。

## 下线节点

模型下线指旧版本模型停止提供服务，您需要切换至其他模型才能继续使用。下线过程包含以下节点：

节点

说明

时间安排

启动下线

发布下线公告，正式告知客户模型下线计划。自即日起停止新用户接入，并可能逐步下调该模型的默认限流（QPM 和 TPM）

正式版、预览版一致

停止新购（EoM）

End of Marketing，停止该模型的所有新购订单。对于按量付费模型，指停止新客户开通该模型的按量计费服务

正式版：启动下线后 7 天；预览版：不涉及

停止服务（EoS）

End of Service，停止该模型的所有服务。已创建的模型推理服务无法继续调用，控制台和文档同步下线，相关数据清理并撤销访问权限

正式版：启动下线后 3 个月；预览版：启动下线后 14 天

## 通知机制

### 通知时间

-   **正式版模型**：不晚于停止服务（EoS）前 **3 个月**发布下线通知。
-   **预览版模型**：不晚于停止服务（EoS）前 **14 天**发布下线通知。

### 通知方式

通过官网公告、邮件、短信、站内信等方式。

> 如您近 3 个月内调用过待下线模型，我们还会通过邮件、短信或站内信通知您。

## 下线影响

-   **自启动下线之日起**：停止新用户接入，并逐步缩减待下线模型的 QPM（每分钟调用次数）和 TPM（每分钟消耗 Token 数）。对于申请过扩容的模型，会先恢复至[默认限流](raw/model-user-guide/get-started-with-models/rate-limit.md)值，再进行缩减。在此过程中，模型 API 接口、控制台上的相关功能均保持正常使用。
    
-   **自停止新购之日起（仅正式版模型）**：停止该模型的新购订单，按量付费模式下新客户无法开通该模型的计费服务。
    
-   **自停止服务之日起**：
    
    -   **模型推理**：停止支持模型推理服务，已创建的调用该模型的应用和服务将无法返回结果。
    -   **控制台功能及官方文档**：模型相关的控制台功能（模型广场、体验中心等）、官方文档将同步下线，相关数据清理、访问权限撤销。

## 下线计划的调整

-   如遇特殊情况，下线可能暂停、延期或中止。中止下线的模型恢复为正常售卖状态，并可能在后续下线计划中重新纳入。
-   已发布的公告可能更新内容，例如调整替代模型、部分模型中止下线。公告更新时会附加「变更说明」，标注变更内容、变更原因及变更前后对比。

## 操作建议

1.  前往[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)页面，检查您的账号是否正在使用待下线的模型。
2.  如果正在使用，建议您先测试替代模型的业务效果，再切换至替代模型。

## 下线模型列表

### 2027年1月19日将下线

详细说明，请参见以下官网公告：

-   [https://www.aliyun.com/notice/118728](https://www.aliyun.com/notice/118728)

### 2026年10月10日已下线

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
