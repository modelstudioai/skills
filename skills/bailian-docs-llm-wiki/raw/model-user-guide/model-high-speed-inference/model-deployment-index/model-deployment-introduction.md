# 专属部署概述

通过部署获得独立的、资源专享的推理服务，以满足高并发、低延迟等性能需求；本文介绍各计费方式选型、部署方法与通用运维。

<a id="计费方式"></a>

<a id="7e244afe7f49k"></a>

## 计费方式

> 部署前可以在[专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)查看不同模型的预估每小时费用。

> **说明**
>
> 计费方式在服务创建后无法更改。如需切换，必须下线已经部署的模型后再重新部署。

<table><thead><tr><th></th><th colspan="2"><p><strong>模型单元</strong></p><p><strong>（自定义性能指标；资源隔离）</strong></p></th><th><p><strong>Token 用量</strong></p><p><strong>（调优后按量计费/效果验证）</strong></p></th></tr></thead><tbody><tr><td><p><strong>定义</strong></p></td><td colspan="2"><p>按使用时长与模型单元数量配置算力，资源独占的模型部署方式。</p></td><td><p>以每次调用产生的输入 Token 与输出 Token 作为用量计量依据的模型部署方式。</p></td></tr><tr><td><p><strong>优势</strong></p></td><td colspan="2"><ol><li><p>延迟/吞吐等<strong>性能指标可自定义</strong>。</p></li><li><p>支持设置自动续费。</p></li><li><p>支持 <a href="model-deployment-modes/dtu-model-deployment.md">PD 分离计算模式</a>。</p></li></ol></td><td><p><strong>不使用不计费</strong>。</p></td></tr><tr><td><p><strong>支持模型</strong></p></td><td colspan="2"><p>部分预置模型与所有调优后模型</p></td><td><p>部分经过 LoRA 调优后的模型</p></td></tr><tr><td><p><strong>使用场景</strong></p></td><td colspan="2"><ol><li><p>电商专属微调大模型（部署私有模型，大促时手动扩容）。</p></li><li><p>医药公司的分子筛选模型（需独占资源跑长时任务）。</p></li><li><p>自动驾驶仿真（需要进行长时间持续计算）。</p></li></ol></td><td><p>调优后模型效果验证</p></td></tr><tr><td><p><strong>计费图示</strong></p></td><td colspan="2"><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6346770771/p1052921.png" alt="image"></p></td><td><p><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6346770771/p1052922.png" alt="image"></p></td></tr><tr><td><p><strong>计费方式</strong></p></td><td colspan="2"><p>按使用时长和模型单元数量</p><p>随用随付、包月</p></td><td><p>按模型 Token 使用量</p><p>随用随付</p></td></tr><tr><td><p><strong>扩缩容方式</strong></p></td><td colspan="2"><p>自助增减模型单元数量</p></td><td><p>在控制台提交申请，等待人工审核。</p></td></tr><tr><td><p><strong>产品约束</strong></p></td><td colspan="2"><p>预付费购买后，若在首月内提前退订，日单价（≈ 月单价 / 30）将按 <strong>1.2</strong> 倍计费</p></td><td><ol><li><p>只支持部分高效微调（LoRA）后的模型。</p></li><li><p>一个月内不使用将自动释放。</p></li></ol></td></tr></tbody></table>

如需查看单次调用的 Token 使用量及调用次数历史统计，请前往：[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)。

DTU 是模型单元(MU)的继任方案（计量粒度由单元数改为输入/输出TPM），新购独占部署优先选 DTU，详见[独占算力部署](model-deployment-modes/dtu-model-deployment.md)。

<a id="部署模式"></a>

<a id="model-support-matrix"></a>

## 部署模式

各部署模式支持的模型与价格详见对应模式页：

> **说明**
>
> 预置吞吐单元（PTU）的创建与管理现已支持在“吞吐预留”页面进行，支持叠加容量包等更完整的容量管理功能。详见[吞吐预留](../tpm-reservation.md)。

-   [独占算力部署](model-deployment-modes/dtu-model-deployment.md)
-   [Token按量部署](model-deployment-modes/model-deployment-token.md)

<a id="部署方法"></a>

<a id="5d4ad61090kms"></a>

## 部署方法

您可以在控制台上部署模型，请参考以下操作步骤：

> 如果提示权限不足，请参考[API 部署指南](model-deployment-quick-start.md)中的权限排查部分。

1.  登录[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，在左侧导航栏选择**模型推理** > **专属部署**。
    
2.  单击**部署新模型**。
    
3.  填写**服务名称**，完成**选择模型**与**计费方式**，其他配置保持默认，单击**确认**。
    
    > 需先完成[模型调优](../../fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)，方可部署大部分模型。
    
4.  返回部署列表，部署状态变为**运行中**时，代表该模型已部署成功。
    

> **重要**
>
> 模型部署成功后将产生费用。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8117463771/p1059807.png) ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8117463771/p1059808.png)

部署服务的详细配置参数（服务名称、模型、模型单元类型、副本数、推理模式、最长上下文、限流等）详见[独占算力部署](model-deployment-modes/dtu-model-deployment.md)与[API 部署指南](model-deployment-quick-start.md)。

<a id="部署列表页"></a>

<a id="audit20260611h2listpage"></a>

## 部署列表页

部署成功后，您可以在部署列表页查看和管理所有部署服务。列表页包含以下信息：

-   **服务名称**：部署服务的名称，单击可查看部署详情。
-   **模型名称**：部署使用的模型。
-   **模型Code**：模型部署成功后生成的唯一标识，用于 API 调用时指定模型。
-   **部署状态/事件状态**：包括待部署、部署中、运行中、部署失败、下线中、服务暂停、已停止、删除中、退订停服/欠费停服、停服恢复中、运行中（变配中）、运行中（变配失败）等状态。
-   **计费方式**：当前部署服务的计费方式。
-   **部署详情**：模型单元类型、副本数等配置信息。
-   **限流详情**：展示当前部署服务的 RPM（每分钟请求数）、TPM（每分钟 Token 数）等限流配置。
-   **服务时间**：展示部署服务的创建时间与到期时间。
-   **操作**：根据部署状态和计费方式，可执行更新、监控、扩缩容、续费、下线、删除、体验等操作。

部署成功后的 API 调用方式（DashScope / OpenAI 兼容接口 / Assistant SDK）详见[API 部署指南](model-deployment-quick-start.md)。

各计费方式的扩缩容操作（手动增减吞吐量/模型单元、Token 扩容申请、自动伸缩策略）详见对应模式页：[独占算力部署](model-deployment-modes/dtu-model-deployment.md)、[Token按量部署](model-deployment-modes/model-deployment-token.md)。

<a id="部署服务下线"></a>

<a id="7f8bfb70f9lvx"></a>

## 部署服务下线

前往[专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，找到要停止的部署服务，根据计费类型点击对应操作：

-   模型单元预付费：点击**下线**并确认。
-   后付费：点击**删除**并确认。

操作完成后将不再产生计费。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0929900771/p1051902.png)

<a id="常见问题"></a>

<a id="ec62eec452e3z"></a>

## 常见问题

<a id="可以上传和部署自己的模型吗"></a>

<a id="b10dd7c86275v"></a>

### 可以上传和部署自己的模型吗？

支持在[我的模型控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/model/custom)导入部分开源模型，详细支持列表请参考：[模型导入](model-import.md)。

此外，阿里云人工智能平台 PAI 提供了部署自有模型的功能，您可以参考[PAI-LLM大语言模型部署](https://help.aliyun.com/zh/pai/deploy-an-llm/)了解部署方法。

<a id="该如何切换到其他的计费方式"></a>

<a id="a8e9e4e6ef024"></a>

### 该如何切换到其他的计费方式？

只能释放原有资源，再通过需要的计费方式创建新资源。

建议按照以下步骤进行切换：

1.  使用需要的计费方式部署新的资源。
2.  切换 API 并测试服务可用性。
3.  下线释放原有资源。
