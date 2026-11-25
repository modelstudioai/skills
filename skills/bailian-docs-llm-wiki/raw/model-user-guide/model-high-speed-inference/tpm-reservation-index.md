# 吞吐预留

阿里云百炼吞吐预留文档目录，包括吞吐预留概述、创建、接入与管理、长输入与前缀缓存、8 小时时段与叠加容量包，以及计费与 API 参考。

吞吐预留为指定模型锁定专属推理容量，确保业务高峰期不受公共限流影响。相关文档如下：

-   [吞吐预留概述](tpm-reservation-index/tpm-reservation.md)：产品概念、标准/高速模式对比、支持模型与常见问题。
-   [创建、接入与管理](tpm-reservation-index/tpm-reservation-create.md)：控制台创建流程、参数、三协议接入调用、查看监控与扩缩容、续订、退订。
-   [长输入与前缀缓存](tpm-reservation-index/tpm-reservation-long-input.md)：缓存折算系数、长输入阶梯、TPM 容量计算器与容量消耗字段。
-   [8 小时时段与叠加容量包计费](../test-1/tpm-reservation-billing.md#tpm-billing-8h-h2)：8 小时时段预留规则与叠加容量包计费。
-   [吞吐预留计费](../test-1/tpm-reservation-billing.md)：价格、扩缩容、退订退费与到期规则。
-   [吞吐预留 API 参考](../../model-api-reference/model-production/throughput-reservation-api.md)：吞吐预留 OpenAPI 管理接口。

**快速上手**：

1.  [创建吞吐预留并复制专属模型 code](tpm-reservation-index/tpm-reservation-create.md#tpm-create-h2)。
2.  [替换 model 参数发起调用](tpm-reservation-index/tpm-reservation-create.md#tpm-create-call-h2)。
3.  [验证 service\_tier 命中预留容量](tpm-reservation-index/tpm-reservation-long-input.md#tpm-long-input-api-h2)。
