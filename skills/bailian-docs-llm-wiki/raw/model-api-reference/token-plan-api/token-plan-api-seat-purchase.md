# 席位购买与变配

Token Plan 团队版席位的购买与变配接口。

本组接口用于 Token Plan 团队版席位的购买与变配，属于 BssOpenApi（版本 `2023-09-30`），Endpoint 为 `business.aliyuncs.com`。

下单前可通过 `QueryProductList` 获取商品参数，通过 `DescribePricingModule` 和 `GetSubscriptionPrice`（版本 `2017-12-14`）查询定价。如果 `QueryProductList` 未返回席位商品，可使用 Token Plan 团队版控制台或订单中显示的商品参数。调用成功后生成订单，可通过 `GetOrders` 查询订单状态。

-   [创建席位（新购）](raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/create-credit-seat.md)
-   [新增席位](raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/add-credit-seats.md)
-   [升级席位](raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/upgrade-credit-seat.md)
-   [退订席位](raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/reduce-credit-seats.md)
-   [续费席位](raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase/renew-credit-seat.md)
