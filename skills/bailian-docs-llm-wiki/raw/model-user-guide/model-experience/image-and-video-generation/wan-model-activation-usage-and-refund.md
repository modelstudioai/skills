# 万相系列模型开通与退订说明

万相系列视频与图像生成模型需要单独开通。本文说明受影响模型、开通与退订的方法、调用时的余额要求，以及开通期间的余额预留与提现限制。

<a id="适用范围"></a>

<a id="wan-activation-scope"></a>

## 适用范围

万相（Wan）系列模型采用独立的开通管理。开通阿里云百炼服务后，系统不会默认开通下表中的万相系列模型，您需要在模型广场的模型详情页单独开通，也可以随时关闭。

-   未开通时，无法通过 API 或百炼控制台的体验中心调用这些模型。
-   开通时按地域逐个开通，开通状态按账号和地域管理；关闭服务时，所有已开通地域会同时关闭。

> **说明**
>
> 如果控制台提示“当前服务开通不含Wan系列视频生成模型，如需使用请至模型广场详情页开通”，表示百炼服务已开通，但万相系列模型尚未单独开通。

<a id="受影响模型"></a>

<a id="wan-activation-models"></a>

## 受影响模型

以下模型受本说明中的开通、余额和关闭规则约束。

<table><thead><tr><th>模型类型</th><th>模型 ID</th></tr></thead><tbody><tr><td rowspan="10"><p>视频生成</p></td><td><p><code>wan3.0-video-prime</code></p></td></tr><tr><td><p><code>wan3.0-video</code></p></td></tr><tr><td><p><code>wan2.7-r2v-2026-06-12</code></p></td></tr><tr><td><p><code>wan2.7-t2v-2026-06-12</code></p></td></tr><tr><td><p><code>wan2.7-t2v-2026-04-25</code></p></td></tr><tr><td><p><code>wan2.7-i2v-2026-04-25</code></p></td></tr><tr><td><p><code>wan2.7-videoedit</code></p></td></tr><tr><td><p><code>wan2.7-r2v</code></p></td></tr><tr><td><p><code>wan2.7-i2v</code></p></td></tr><tr><td><p><code>wan2.7-t2v</code></p></td></tr><tr><td rowspan="3"><p>图像生成</p></td><td><p><code>wan2.7-image-pro</code></p></td></tr><tr><td><p><code>wan2.7-image</code></p></td></tr><tr><td><p><code>image-instance-segmentation</code></p></td></tr></tbody></table>

<a id="开通服务"></a>

<a id="wan-activation-open"></a>

## 开通服务

1.  登录百炼控制台，进入[模型广场](https://bailian.console.aliyun.com/cn-beijing/model/market)。
2.  搜索并打开目标万相系列模型的详情页。未登录时，页面的开通按钮不可用。
3.  在详情页单击**开通服务**。
4.  确认开通后，模型状态变为已开通。如需在其他地域使用，请切换到对应地域后重复上述步骤。

<a id="调用服务"></a>

<a id="wan-activation-call"></a>

## 调用服务

1.  确认目标地域的万相系列模型已开通。
2.  [获取并配置 API Key](../../../model-api-reference/preparations/get-api-key.md)。
3.  接口说明见[万相3.0-视频生成API参考](../../../model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)。
4.  调用时请保证账号余额充足，避免因欠费停机影响调用。

体验中心的调用同样需要先开通对应的万相系列模型。

<a id="关闭服务"></a>

<a id="wan-activation-close"></a>

## 关闭服务

1.  进入任一已开通地域的万相系列模型详情页。
2.  单击**关闭服务**并确认。

关闭后，**该账号下所有已开通地域的万相系列模型都会停止服务**，API 和体验中心均无法继续调用。如需继续使用，可重新开通。

<a id="余额与提现"></a>

<a id="wan-activation-balance"></a>

## 余额与提现

开通万相系列模型期间，系统会从账号余额中预留一部分金额作为运行保障。该部分余额在服务开通期间不可提现，超出预留额度的余额可正常提现。

如需提现被预留的余额，请先关闭所有地域的万相系列模型服务，再前往[费用与成本](https://billing-cost.console.aliyun.com/home)提交提现。关闭服务后，预留金额解除锁定，可按页面提示提现。
