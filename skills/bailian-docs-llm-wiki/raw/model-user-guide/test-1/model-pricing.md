# 模型调用价格

模型调用默认**按量计费**，涵盖各类模型的计费规则与价格。

## **阶梯计费规则**

百炼部分模型实行阶梯计费。单价取决于单次请求的输入 Token 总量。该请求的所有 Token 均按对应阶梯的单价结算。

例如，某模型设有两档计费区间：0 < Token ≤ 32K 和 32K < Token ≤ 128K。若输入 100K Token，因数值落在第二区间（32K < 100K ≤ 128K），所有 Token 均按第二档单价结算。

## **文本生成-千问**

### **千问Max**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费；若模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，仅输入Token享有折扣。两者不能同时生效。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3.7-max

> 当前能力等同于qwen3.7-max-2026-05-20

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

非思考和思考模式

0<Token≤1M

12元

36元

100万Token

qwen3.7-max-2026-06-08

中国内地

非思考和思考模式

0<Token≤1M

12元

36元

100万Token

qwen3.7-max-2026-05-20

中国内地

非思考和思考模式

0<Token≤1M

12元

36元

100万Token

qwen3.7-max-preview

> 当前能力等同于qwen3.7-max-2026-05-17

中国内地

仅思考模式

0<Token≤1M

12元

36元

100万Token

qwen3.7-max-2026-05-17

中国内地

仅思考模式

0<Token≤1M

12元

36元

100万Token

qwen3.6-max-preview

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

非思考和思考模式

0<Token≤128K

9元

54元

100万Token

128K<Token≤256K

15元

90元

qwen3-max

> 当前能力等同于qwen3-max-2026-01-23

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

非思考和思考模式

0<Token≤32K

2.5元

10元

100万Token

32K<Token≤128K

4元

16元

128K<Token≤256K

7元

28元

qwen3-max-2026-01-23

中国内地

非思考和思考模式

0<Token≤32K

2.5元

10元

100万Token

32K<Token≤128K

4元

16元

128K<Token≤256K

7元

28元

qwen3-max-2025-09-23

中国内地

仅非思考模式

0<Token≤32K

6元

24元

100万Token

32K<Token≤128K

10元

40元

128K<Token≤256K

15元

60元

qwen3-max-preview

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

非思考和思考模式

0<Token≤32K

6元

24元

100万Token

32K<Token≤128K

10元

40元

128K<Token≤256K

15元

60元

##### **更多模型**

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-max

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

中国内地

仅非思考模式

无阶梯计价

2.4元

9.6元

100万Token

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3.7-max

> 当前能力等同于qwen3.7-max-2026-05-20

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤1M

12元

36元

qwen3.7-max-2026-06-08

全球

非思考和思考模式

0<Token≤1M

12元

36元

qwen3.7-max-2026-05-20

全球

非思考和思考模式

0<Token≤1M

12元

36元

qwen3-max

> 当前能力等同于qwen3-max-2026-01-23

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

仅非思考模式

0<Token≤32K

2.5元

10元

32K<Token≤128K

4元

16元

128K<Token≤256K

7元

28元

qwen3-max-2025-09-23

全球

仅非思考模式

0<Token≤32K

6元

24元

32K<Token≤128K

10元

40元

128K<Token≤256K

15元

60元

qwen3-max-preview

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤32K

6元

24元

32K<Token≤128K

10元

40元

128K<Token≤256K

15元

60元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3.7-max

> 当前能力等同于qwen3.7-max-2026-05-20

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

非思考和思考模式

0<Token≤1M

18.736元

56.207元

qwen3.7-max-2026-06-08

国际

非思考和思考模式

0<Token≤1M

18.736元

56.207元

qwen3.7-max-2026-05-20

国际

非思考和思考模式

0<Token≤1M

18.736元

56.207元

qwen3.6-max-preview

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

非思考和思考模式

0<Token≤128K

9.742元

58.455元

128K<Token≤256K

14.988元

89.93元

qwen3-max

> 当前能力等同于qwen3-max-2026-01-23

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

非思考和思考模式

0<Token≤32K

8.807元

44.035元

32K<Token≤128K

17.614元

88.071元

128K<Token≤256K

22.018元

110.089元

qwen3-max-2026-01-23

国际

非思考和思考模式

0<Token≤32K

8.807元

44.035元

32K<Token≤128K

17.614元

88.071元

128K<Token≤256K

22.018元

110.089元

qwen3-max-2025-09-23

国际

仅非思考模式

0<Token≤32K

8.807元

44.035元

32K<Token≤128K

17.614元

88.071元

128K<Token≤256K

22.018元

110.089元

qwen3-max-preview

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

非思考和思考模式

0<Token≤32K

8.807元

44.035元

32K<Token≤128K

17.614元

88.071元

128K<Token≤256K

22.018元

110.089元

##### **更多模型**

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen-max

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

国际

仅非思考模式

无阶梯计价

11.743元

46.971元

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3.7-max

> 当前能力等同于qwen3.7-max-2026-05-20

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤1M

12元

36元

qwen3.7-max-2026-06-08

全球

非思考和思考模式

0<Token≤1M

12元

36元

qwen3.7-max-2026-05-20

全球

非思考和思考模式

0<Token≤1M

12元

36元

qwen3-max

> 当前能力等同于qwen3-max-2026-01-23

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

仅非思考模式

0<Token≤32K

2.5元

10元

32K<Token≤128K

4元

16元

128K<Token≤256K

7元

28元

qwen3-max

> 当前能力等同于qwen3-max-2026-01-23

欧盟

非思考和思考模式

0<Token≤32K

8.993元

44.965元

32K<Token≤128K

17.986元

89.93元

128K<Token≤256K

22.483元

112.413元

qwen3-max-2026-01-23

欧盟

非思考和思考模式

0<Token≤32K

8.993元

44.965元

32K<Token≤128K

17.986元

89.93元

128K<Token≤256K

22.483元

112.413元

qwen3-max-2025-09-23

全球

仅非思考模式

0<Token≤32K

6元

24元

32K<Token≤128K

10元

40元

128K<Token≤256K

15元

60元

qwen3-max-preview

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤32K

6元

24元

32K<Token≤128K

10元

40元

128K<Token≤256K

15元

60元

#### 日本（东京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3.7-max

> 当前能力等同于qwen3.7-max-2026-05-20

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤1M

12元

36元

qwen3.7-max-2026-05-20

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤1M

12元

36元

### **千问Plus**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

**非思考模式**

**思考模式（思维链+回答）**

qwen3.7-plus

> 当前能力等同于qwen3.7-plus-2026-05-26

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

0<Token≤256K

2元

8元

8元

100万Token

256K<Token≤1M

6元

24元

24元

qwen3.7-plus-2026-05-26

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

0<Token≤256K

2元

8元

8元

100万Token

256K<Token≤1M

6元

24元

24元

qwen3.6-plus

> 当前能力等同于qwen3.6-plus-2026-04-02

中国内地

0<Token≤256K

2元

12元

12元

100万Token

256K<Token≤1M

8元

48元

48元

qwen3.6-plus-2026-04-02

中国内地

0<Token≤256K

2元

12元

12元

100万Token

256K<Token≤1M

8元

48元

48元

qwen3.5-plus

> 当前能力等同于qwen3.5-plus-2026-02-15

中国内地

0<Token≤128K

0.8元

4.8元

4.8元

100万Token

128K<Token≤256K

2元

12元

12元

256K<Token≤1M

4元

24元

24元

qwen3.5-plus-2026-04-20

中国内地

0<Token≤128K

0.8元

4.8元

4.8元

100万Token

128K<Token≤256K

2元

12元

12元

256K<Token≤1M

4元

24元

24元

qwen3.5-plus-2026-02-15

中国内地

0<Token≤128K

0.8元

4.8元

4.8元

100万Token

128K<Token≤256K

2元

12元

12元

256K<Token≤1M

4元

24元

24元

qwen-plus

> 当前能力等同于qwen-plus-2025-12-01

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

中国内地

0<Token≤128K

0.8元

2元

8元

100万Token

128K<Token≤256K

2.4元

20元

24元

256K<Token≤1M

4.8元

48元

64元

qwen-plus-latest

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

中国内地

0<Token≤128K

0.8元

2元

8元

100万Token

128K<Token≤256K

2.4元

20元

24元

256K<Token≤1M

4.8元

48元

64元

qwen-plus-2025-12-01

中国内地

0<Token≤128K

0.8元

2元

8元

100万Token

128K<Token≤256K

2.4元

20元

24元

256K<Token≤1M

4.8元

48元

64元

qwen-plus-2025-09-11

中国内地

0<Token≤128K

0.8元

2元

8元

100万Token

128K<Token≤256K

2.4元

20元

24元

256K<Token≤1M

4.8元

48元

64元

qwen-plus-2025-07-28

中国内地

0<Token≤128K

0.8元

2元

8元

100万Token

128K<Token≤256K

2.4元

20元

24元

256K<Token≤1M

4.8元

48元

64元

qwen-plus-2025-07-14

中国内地

无阶梯计价

0.8元

2元

8元

100万Token

qwen-plus-2025-04-28

中国内地

无阶梯计价

0.8元

2元

8元

100万Token

##### **更多模型**

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-plus-2025-01-25

中国内地

无阶梯计价

0.8元

2元

100万Token

qwen-plus-2025-01-12

中国内地

无阶梯计价

0.8元

2元

100万Token

qwen-plus-2024-12-20

中国内地

无阶梯计价

0.8元

2元

100万Token

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.7-plus

> 当前能力等同于qwen3.7-plus-2026-05-26

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

0<Token≤256K

2元

8元

8元

256K<Token≤1M

6元

24元

24元

qwen3.7-plus-2026-05-26

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

0<Token≤256K

2元

8元

8元

256K<Token≤1M

6元

24元

24元

qwen3.6-plus

> 当前能力等同于qwen3.6-plus-2026-04-02

全球

0<Token≤256K

2元

12元

12元

256K<Token≤1M

8元

48元

48元

qwen3.6-plus-2026-04-02

全球

0<Token≤256K

2元

12元

12元

256K<Token≤1M

8元

48元

48元

qwen3.5-plus

> 当前能力等同于qwen3.5-plus-2026-02-15

全球

0<Token≤128K

0.8元

4.8元

4.8元

128K<Token≤256K

2元

12元

12元

256K<Token≤1M

4元

24元

24元

qwen3.5-plus-2026-02-15

全球

0<Token≤128K

0.8元

4.8元

4.8元

128K<Token≤256K

2元

12元

12元

256K<Token≤1M

4元

24元

24元

qwen-plus

> 当前能力等同于qwen-plus-2025-12-01

全球

0<Token≤128K

0.8元

2元

8元

128K<Token≤256K

2.4元

20元

24元

256K<Token≤1M

4.8元

48元

64元

qwen-plus-us

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

美国

0<Token≤256K

2.936元

8.807元

29.357元

256K<Token≤1M

8.807元

26.421元

88.071元

qwen-plus-2025-12-01

全球

0<Token≤128K

0.8元

2元

8元

128K<Token≤256K

2.4元

20元

24元

256K<Token≤1M

4.8元

48元

64元

qwen-plus-2025-12-01-us

美国

0<Token≤256K

2.936元

8.807元

29.357元

256K<Token≤1M

8.807元

26.421元

88.071元

qwen-plus-2025-09-11

全球

0<Token≤128K

0.8元

2元

8元

128K<Token≤256K

2.4元

20元

24元

256K<Token≤1M

4.8元

48元

64元

qwen-plus-2025-07-28

全球

0<Token≤128K

0.8元

2元

8元

128K<Token≤256K

2.4元

20元

24元

256K<Token≤1M

4.8元

48元

64元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.7-plus

> 当前能力等同于qwen3.7-plus-2026-05-26

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

0<Token≤256K

2.998元

11.991元

11.991元

256K<Token≤1M

8.993元

35.972元

35.972元

qwen3.7-plus-2026-05-26

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

0<Token≤256K

2.998元

11.991元

11.991元

256K<Token≤1M

8.993元

35.972元

35.972元

qwen3.6-plus

> 当前能力等同于qwen3.6-plus-2026-04-02

国际

0<Token≤256K

3.7471元

22.4826元

22.4826元

256K<Token≤1M

14.9884元

44.965元

44.965元

qwen3.6-plus-2026-04-02

国际

0<Token≤256K

3.7471元

22.4826元

22.4826元

256K<Token≤1M

14.9884元

44.965元

44.965元

qwen3.5-plus

> 当前能力等同于qwen3.5-plus-2026-02-15

国际

0<Token≤256K

2.936元

17.614元

17.614元

256K<Token≤1M

3.67元

22.018元

22.018元

qwen3.5-plus-2026-04-20

国际

0<Token≤256K

2.936元

17.614元

17.614元

256K<Token≤1M

3.67元

22.018元

22.018元

qwen3.5-plus-2026-02-15

国际

0<Token≤256K

2.936元

17.614元

17.614元

256K<Token≤1M

3.67元

22.018元

22.018元

qwen-plus

> 当前能力等同于qwen-plus-2025-12-01

国际

0<Token≤256K

2.936元

8.807元

29.357元

256K<Token≤1M

8.807元

26.421元

88.071元

qwen-plus-latest

国际

0<Token≤256K

2.936元

8.807元

29.357元

256K<Token≤1M

8.807元

26.421元

88.071元

qwen-plus-2025-12-01

国际

0<Token≤256K

2.936元

8.807元

29.357元

256K<Token≤1M

8.807元

26.421元

88.071元

qwen-plus-2025-09-11

国际

0<Token≤256K

2.936元

8.807元

29.357元

256K<Token≤1M

8.807元

26.421元

88.071元

qwen-plus-2025-07-28

国际

0<Token≤256K

2.936元

8.807元

29.357元

256K<Token≤1M

8.807元

26.421元

88.071元

qwen-plus-2025-07-14

国际

无阶梯计价

2.936元

8.807元

29.357元

qwen-plus-2025-04-28

国际

无阶梯计价

2.936元

8.807元

29.357元

##### **更多模型**

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen-plus-2025-01-25

国际

无阶梯计价

2.936元

8.807元

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.7-plus

> 当前能力等同于qwen3.7-plus-2026-05-26

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

0<Token≤256K

2元

8元

8元

256K<Token≤1M

6元

24元

24元

qwen3.7-plus-2026-05-26

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

0<Token≤256K

2元

8元

8元

256K<Token≤1M

6元

24元

24元

qwen3.6-plus

> 当前能力等同于qwen3.6-plus-2026-04-02

全球

0<Token≤256K

2元

12元

12元

256K<Token≤1M

8元

48元

48元

qwen3.6-plus-2026-04-02

全球

0<Token≤256K

2元

12元

12元

256K<Token≤1M

8元

48元

48元

qwen3.5-plus

> 当前能力等同于qwen3.5-plus-2026-02-15

全球

0<Token≤128K

0.8元

4.8元

4.8元

128K<Token≤256K

2元

12元

12元

256K<Token≤1M

4元

24元

24元

qwen3.5-plus-2026-02-15

全球

0<Token≤128K

0.8元

4.8元

4.8元

128K<Token≤256K

2元

12元

12元

256K<Token≤1M

4元

24元

24元

qwen-plus

> 当前能力等同于qwen-plus-2025-12-01

全球

0<Token≤128K

0.8元

2元

8元

128K<Token≤256K

2.4元

20元

24元

256K<Token≤1M

4.8元

48元

64元

qwen-plus

> 当前能力等同于qwen-plus-2025-12-01

欧盟

0<Token≤256K

2.998元

8.993元

29.977元

256K<Token≤1M

8.993元

26.979元

89.93元

qwen-plus-2025-12-01

全球

0<Token≤128K

0.8元

2元

8元

128K<Token≤256K

2.4元

20元

24元

256K<Token≤1M

4.8元

48元

64元

qwen-plus-2025-12-01

欧盟

0<Token≤256K

2.998元

8.993元

29.977元

256K<Token≤1M

8.993元

26.979元

89.93元

qwen-plus-2025-09-11

全球

0<Token≤128K

0.8元

2元

8元

128K<Token≤256K

2.4元

20元

24元

256K<Token≤1M

4.8元

48元

64元

qwen-plus-2025-07-28

全球

0<Token≤128K

0.8元

2元

8元

128K<Token≤256K

2.4元

20元

24元

256K<Token≤1M

4.8元

48元

64元

#### 日本（东京）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.7-plus

> 当前能力等同于qwen3.7-plus-2026-05-26

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

日本

0<Token≤256K

2.998元

11.991元

11.991元

256K<Token≤1M

8.993元

35.972元

35.972元

qwen3.7-plus-2026-05-26

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

日本

0<Token≤256K

2.998元

11.991元

11.991元

256K<Token≤1M

8.993元

35.972元

35.972元

qwen3.7-plus

> 当前能力等同于qwen3.7-plus-2026-05-26

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

0<Token≤256K

2元

8元

8元

256K<Token≤1M

6元

24元

24元

qwen3.7-plus-2026-05-26

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

0<Token≤256K

2元

8元

8元

256K<Token≤1M

6元

24元

24元

qwen3.6-plus

> 当前能力等同于qwen3.6-plus-2026-04-02

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

0<Token≤256K

2元

12元

12元

256K<Token≤1M

8元

48元

48元

qwen3.6-plus-2026-04-02

全球

0<Token≤256K

2元

12元

12元

256K<Token≤1M

8元

48元

48元

### **千问Flash**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费；若模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，仅输入Token享有折扣。两者不能同时生效。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3.6-flash

> 当前能力等同于qwen3.6-flash-2026-04-16

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

非思考和思考模式

0<Token≤256K

1.2元

7.2元

100万Token

256K<Token≤1M

4.8元

28.8元

qwen3.6-flash-2026-04-16

中国内地

非思考和思考模式

0<Token≤256K

1.2元

7.2元

100万Token

256K<Token≤1M

4.8元

28.8元

qwen3.5-flash

> 当前能力等同于qwen3.5-flash-2026-02-23

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

非思考和思考模式

0<Token≤128K

0.2元

2元

100万Token

128K<Token≤256K

0.8元

8元

256K<Token≤1M

1.2元

12元

qwen3.5-flash-2026-02-23

中国内地

非思考和思考模式

0<Token≤128K

0.2元

2元

100万Token

128K<Token≤256K

0.8元

8元

256K<Token≤1M

1.2元

12元

qwen-flash

> 当前能力等同于qwen-flash-2025-07-28

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

非思考和思考模式

0<Token≤128K

0.15元

1.5元

100万Token

128K<Token≤256K

0.6元

6元

256K<Token≤1M

1.2元

12元

qwen-flash-2025-07-28

中国内地

非思考和思考模式

0<Token≤128K

0.15元

1.5元

100万Token

128K<Token≤256K

0.6元

6元

256K<Token≤1M

1.2元

12元

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3.6-flash

> 当前能力等同于qwen3.6-flash-2026-04-16

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤256K

1.2元

7.2元

256K<Token≤1M

4.8元

28.8元

qwen3.6-flash-2026-04-16

全球

非思考和思考模式

0<Token≤256K

1.2元

7.2元

256K<Token≤1M

4.8元

28.8元

qwen3.5-flash

> 当前能力等同于qwen3.5-flash-2026-02-23

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤128K

0.2元

2元

128K<Token≤256K

0.8元

8元

256K<Token≤1M

1.2元

12元

qwen3.5-flash-2026-02-23

全球

非思考和思考模式

0<Token≤128K

0.2元

2元

128K<Token≤256K

0.8元

8元

256K<Token≤1M

1.2元

12元

qwen-flash

> 当前能力等同于qwen-flash-2025-07-28

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤128K

0.15元

1.5元

128K<Token≤256K

0.6元

6元

256K<Token≤1M

1.2元

12元

qwen-flash-us

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

美国

0<Token≤256K

0.367元

2.936元

256K<Token≤1M

1.835元

14.678元

qwen-flash-2025-07-28

全球

非思考和思考模式

0<Token≤128K

0.15元

1.5元

128K<Token≤256K

0.6元

6元

256K<Token≤1M

1.2元

12元

qwen-flash-2025-07-28-us

美国

0<Token≤256K

0.367元

2.936元

256K<Token≤1M

1.835元

14.678元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3.6-flash

> 当前能力等同于qwen3.6-flash-2026-04-16

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

非思考和思考模式

0<Token≤256K

1.87355元

11.2413元

256K<Token≤1M

7.4942元

29.9758元

qwen3.6-flash-2026-04-16

国际

非思考和思考模式

0<Token≤256K

1.87355元

11.2413元

256K<Token≤1M

7.4942元

29.9758元

qwen3.5-flash

> 当前能力等同于qwen3.5-flash-2026-02-23

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

非思考和思考模式

0<Token≤1M

0.734元

2.936元

qwen3.5-flash-2026-02-23

国际

非思考和思考模式

0<Token≤1M

0.734元

2.936元

qwen-flash

> 当前能力等同于qwen-flash-2025-07-28

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

非思考和思考模式

0<Token≤256K

0.367元

2.936元

256K<Token≤1M

1.835元

14.678元

qwen-flash-2025-07-28

国际

非思考和思考模式

0<Token≤256K

0.367元

2.936元

256K<Token≤1M

1.835元

14.678元

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3.6-flash

> 当前能力等同于qwen3.6-flash-2026-04-16

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤256K

1.2元

7.2元

256K<Token≤1M

4.8元

28.8元

qwen3.6-flash-2026-04-16

全球

非思考和思考模式

0<Token≤256K

1.2元

7.2元

256K<Token≤1M

4.8元

28.8元

qwen3.5-flash

> 当前能力等同于qwen3.5-flash-2026-02-23

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤128K

0.2元

2元

128K<Token≤256K

0.8元

8元

256K<Token≤1M

1.2元

12元

qwen3.5-flash

> 当前能力等同于qwen3.5-flash-2026-02-23

欧盟

非思考和思考模式

0.749元

2.998元

qwen3.5-flash-2026-02-23

全球

非思考和思考模式

0<Token≤128K

0.2元

2元

128K<Token≤256K

0.8元

8元

256K<Token≤1M

1.2元

12元

qwen3.5-flash-2026-02-23

欧盟

非思考和思考模式

0.749元

2.998元

qwen-flash

> 当前能力等同于qwen-flash-2025-07-28

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤128K

0.15元

1.5元

128K<Token≤256K

0.6元

6元

256K<Token≤1M

1.2元

12元

qwen-flash-2025-07-28

全球

非思考和思考模式

0<Token≤128K

0.15元

1.5元

128K<Token≤256K

0.6元

6元

256K<Token≤1M

1.2元

12元

#### 日本（东京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3.6-flash

> 当前能力等同于qwen3.6-flash-2026-04-16

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤256K

1.2元

7.2元

256K<Token≤1M

4.8元

28.8元

qwen3.6-flash-2026-04-16

全球

非思考和思考模式

0<Token≤256K

1.2元

7.2元

256K<Token≤1M

4.8元

28.8元

### **千问Turbo**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

**非思考模式**

**思考模式（思维链+回答）**

qwen-turbo

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

中国内地

非思考和思考模式

0.3元

0.6元

3元

100万Token

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen-turbo

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

国际

非思考和思考

0.367元

1.468元

3.67元

### **QwQ**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwq-plus

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

中国内地

仅思考模式

1.6元

4元

100万Token

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwq-plus

国际

仅思考模式

5.871元

17.614元

### 千问Long

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-long

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

中国内地

0.5元

2元

100万Token

qwen-long-latest

中国内地

0.5元

2元

100万Token

qwen-long-2025-01-25

中国内地

0.5元

2元

100万Token

### **千问Omni**

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费与限流](https://help.aliyun.com/zh/model-studio/qwen-omni#12db7427b94qt)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

**文本/图片/视频**

**音频**

**文本**

> 多模态输入

**文本+音频**

> 仅音频计费

qwen3.5-omni-plus

> 当前能力等同于qwen3.5-omni-plus-2026-03-15

中国内地

7元

53元

40元

213元

100万Token

qwen3.5-omni-plus-2026-03-15

中国内地

7元

53元

40元

213元

100万Token

qwen3.5-omni-flash

> 当前能力等同于qwen3.5-omni-flash-2026-03-15

中国内地

2.2元

18元

13.3元

72元

100万Token

qwen3.5-omni-flash-2026-03-15

中国内地

2.2元

18元

13.3元

72元

100万Token

##### 更多模型

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

**文本**

**音频**

**图片/视频**

**文本**

> 仅纯文本输入

**文本**

> 多模态输入

**文本+音频**

> 仅音频计费

qwen3-omni-flash

> 当前能力等同于qwen3-omni-flash-2025-12-01

中国内地

非思考和思考模式

1.8元

15.8元

3.3元

6.9元

12.7元

62.6元

100万Token

qwen3-omni-flash-2025-12-01

中国内地

非思考和思考模式

1.8元

15.8元

3.3元

6.9元

12.7元

62.6元

100万Token

qwen3-omni-flash-2025-09-15

中国内地

非思考和思考模式

1.8元

15.8元

3.3元

6.9元

12.7元

62.6元

100万Token

qwen-omni-turbo

> 当前能力等同于qwen-omni-turbo-2025-03-26

中国内地

非思考模式

0.4元

25元

1.5元

1.6元

4.5元

50元

100万Token

qwen-omni-turbo-latest

中国内地

非思考模式

0.4元

25元

1.5元

1.6元

4.5元

50元

100万Token

qwen-omni-turbo-2025-03-26

中国内地

非思考模式

0.4元

25元

1.5元

1.6元

4.5元

50元

100万Token

qwen-omni-turbo-2025-01-19

中国内地

非思考模式

0.4元

25元

1.5元

1.6元

4.5元

50元

100万Token

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**文本/图片/视频**

**音频**

**文本**

> 多模态输入

**文本+音频**

> 仅音频计费

qwen3.5-omni-plus

> 当前能力等同于qwen3.5-omni-plus-2026-03-15

国际

10.49元

82.44元

62.2元

329.74元

qwen3.5-omni-plus-2026-03-15

国际

10.49元

82.44元

62.2元

329.74元

qwen3.5-omni-flash

> 当前能力等同于qwen3.5-omni-flash-2026-03-15

国际

3元

22.48元

16.49元

89.18元

qwen3.5-omni-flash-2026-03-15

国际

3元

22.48元

16.49元

89.18元

##### 更多模型

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**文本**

**音频**

**图片/视频**

**文本**

> 仅纯文本输入

**文本**

> 多模态输入

**文本+音频**

> 仅音频计费

qwen3-omni-flash

> 当前能力等同于qwen3-omni-flash-2025-12-01

国际

非思考和思考模式

3.156元

27.962元

5.725元

12.183元

22.458元

110.896元

qwen3-omni-flash-2025-12-01

国际

非思考和思考模式

3.156元

27.962元

5.725元

12.183元

22.458元

110.896元

qwen3-omni-flash-2025-09-15

国际

非思考和思考模式

3.156元

27.962元

5.725元

12.183元

22.458元

110.896元

qwen-omni-turbo

> 当前能力等同于qwen-omni-turbo-2025-03-26

国际

非思考模式

0.514元

32.586元

1.541元

1.982元

4.624元

65.246元

qwen-omni-turbo-latest

国际

非思考模式

0.514元

32.586元

1.541元

1.982元

4.624元

65.246元

qwen-omni-turbo-2025-03-26

国际

非思考模式

0.514元

32.586元

1.541元

1.982元

4.624元

65.246元

### **千问Omni-Realtime**

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费与限流](https://help.aliyun.com/zh/model-studio/realtime#dc0370c95d3ja)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

**文本/图片**

**音频**

**文本**

> 多模态输入

**文本+音频**

> 仅音频计费

qwen3.5-omni-plus-realtime

中国内地

10元

80元

60元

300元

100万Token

qwen3.5-omni-plus-realtime-2026-03-15

中国内地

10元

80元

60元

300元

100万Token

qwen3.5-omni-flash-realtime

中国内地

3.3元

27元

20元

107元

100万Token

qwen3.5-omni-flash-realtime-2026-03-15

中国内地

3.3元

27元

20元

107元

100万Token

##### 更多模型

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

**文本**

**音频**

**图片**

**文本**

> 仅纯文本输入

**文本**

> 多模态输入

**文本+音频**

> 仅音频计费

qwen3-omni-flash-realtime

中国内地

2.2元

18.9元

3.9元

8.3元

15.2元

75.1元

100万Token

qwen3-omni-flash-realtime-2025-12-01

中国内地

2.2元

18.9元

3.9元

8.3元

15.2元

75.1元

100万Token

qwen3-omni-flash-realtime-2025-09-15

中国内地

2.2元

18.9元

3.9元

8.3元

15.2元

75.1元

100万Token

qwen-omni-turbo-realtime

中国内地

1.6元

25元

6元

6.4元

18元

50元

100万Token

qwen-omni-turbo-realtime-latest

中国内地

1.6元

25元

6元

6.4元

18元

50元

100万Token

qwen-omni-turbo-realtime-2025-05-08

中国内地

1.6元

25元

6元

6.4元

18元

50元

100万Token

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**文本/图片**

**音频**

**文本**

> 多模态输入

**文本+音频**

> 仅音频计费

qwen3.5-omni-plus-realtime

国际

15.74元

123.65元

92.93元

464.64元

qwen3.5-omni-plus-realtime-2026-03-15

国际

15.74元

123.65元

92.93元

464.64元

qwen3.5-omni-flash-realtime

国际

4.12元

33.72元

24.73元

132.65元

qwen3.5-omni-flash-realtime-2026-03-15

国际

4.12元

33.72元

24.73元

132.65元

##### 更多模型

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**文本**

**音频**

**图片**

**文本**

> 仅纯文本输入

**文本**

> 多模态输入

**文本+音频**

> 仅音频计费

qwen3-omni-flash-realtime

国际

3.816元

33.54元

6.899元

14.605元

26.935元

133.06元

qwen3-omni-flash-realtime-2025-12-01

国际

3.816元

33.54元

6.899元

14.605元

26.935元

133.06元

qwen3-omni-flash-realtime-2025-09-15

国际

3.816元

33.54元

6.899元

14.605元

26.935元

133.06元

qwen-omni-turbo-realtime

国际

1.982元

32.586元

6.165元

7.853元

18.495元

65.246元

qwen-omni-turbo-realtime-latest

国际

1.982元

32.586元

6.165元

7.853元

18.495元

65.246元

qwen-omni-turbo-realtime-2025-05-08

国际

1.982元

32.586元

6.165元

7.853元

18.495元

65.246元

### **QVQ**

计费规则：按输入Token和输出Token计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qvq-max

中国内地

8元

32元

100万Token

qvq-plus

中国内地

2元

5元

100万Token

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qvq-max

国际

8.807元

35.228元

### 千问VL

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-vl-plus

> 当前能力等同于qwen3-vl-plus-2025-12-19

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

非思考和思考模式

0<Token≤32K

1元

10元

100万Token

32K<Token≤128K

1.5元

15元

128K<Token≤256K

3元

30元

qwen3-vl-plus-2025-12-19

中国内地

非思考和思考模式

0<Token≤32K

1元

10元

100万Token

32K<Token≤128K

1.5元

15元

128K<Token≤256K

3元

30元

qwen3-vl-plus-2025-09-23

中国内地

非思考和思考模式

0<Token≤32K

1元

10元

100万Token

32K<Token≤128K

1.5元

15元

128K<Token≤256K

3元

30元

qwen3-vl-flash

> 当前能力等同于qwen3-vl-flash-2026-01-22

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

非思考和思考模式

0<Token≤32K

0.15元

1.5元

100万Token

32K<Token≤128K

0.3元

3元

128K<Token≤256K

0.6元

6元

qwen3-vl-flash-2026-01-22

中国内地

非思考和思考模式

0<Token≤32K

0.15元

1.5元

100万Token

32K<Token≤128K

0.3元

3元

128K<Token≤256K

0.6元

6元

qwen3-vl-flash-2025-10-15

中国内地

非思考和思考模式

0<Token≤32K

0.15元

1.5元

100万Token

32K<Token≤128K

0.3元

3元

128K<Token≤256K

0.6元

6元

##### **更多模型**

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-vl-max

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

无阶梯计价

1.6元

4元

100万Token

qwen-vl-plus

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

无阶梯计价

0.8元

2元

100万Token

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3-vl-flash

> 当前能力等同于qwen3-vl-flash-2025-10-15

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤32K

0.15元

1.5元

32K<Token≤128K

0.3元

3元

128K<Token≤256K

0.6元

6元

qwen3-vl-flash-us

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

美国

非思考和思考模式

0<Token≤32K

0.367元

2.936元

32K<Token≤128K

0.55元

4.404元

128K<Token≤256K

0.881元

7.046元

qwen3-vl-flash-2026-01-22-us

美国

非思考和思考模式

0<Token≤32K

0.367元

2.936元

32K<Token≤128K

0.55元

4.404元

128K<Token≤256K

0.881元

7.046元

qwen3-vl-flash-2025-10-15

全球

非思考和思考模式

0<Token≤32K

0.15元

1.5元

32K<Token≤128K

0.3元

3元

128K<Token≤256K

0.6元

6元

qwen3-vl-flash-2025-10-15-us

美国

非思考和思考模式

0<Token≤32K

0.367元

2.936元

32K<Token≤128K

0.55元

4.404元

128K<Token≤256K

0.881元

7.046元

qwen3-vl-plus

> 当前能力等同于qwen3-vl-plus-2025-12-19

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤32K

1元

10元

32K<Token≤128K

1.5元

15元

128K<Token≤256K

3元

30元

qwen3-vl-plus-2025-09-23

全球

非思考和思考模式

0<Token≤32K

1元

10元

32K<Token≤128K

1.5元

15元

128K<Token≤256K

3元

30元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen3-vl-plus

> 当前能力等同于qwen3-vl-plus-2025-12-19

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

非思考和思考模式

0<Token≤32K

1.468元

11.743元

32K<Token≤128K

2.202元

17.614元

128K<Token≤256K

4.404元

35.228元

qwen3-vl-plus-2025-12-19

国际

非思考和思考模式

0<Token≤32K

1.468元

11.743元

32K<Token≤128K

2.202元

17.614元

128K<Token≤256K

4.404元

35.228元

qwen3-vl-plus-2025-09-23

国际

非思考和思考模式

0<Token≤32K

1.468元

11.743元

32K<Token≤128K

2.202元

17.614元

128K<Token≤256K

4.404元

35.228元

qwen3-vl-flash

> 当前能力等同于qwen3-vl-flash-2026-01-22

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

非思考和思考模式

0<Token≤32K

0.367元

2.936元

32K<Token≤128K

0.55元

4.404元

128K<Token≤256K

0.881元

7.046元

qwen3-vl-flash-2026-01-22

国际

非思考和思考模式

0<Token≤32K

0.367元

2.936元

32K<Token≤128K

0.55元

4.404元

128K<Token≤256K

0.881元

7.046元

qwen3-vl-flash-2025-10-15

国际

非思考和思考模式

0<Token≤32K

0.367元

2.936元

32K<Token≤128K

0.55元

4.404元

128K<Token≤256K

0.881元

7.046元

##### **更多模型**

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token数**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen-vl-max

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

无阶梯计价

5.871元

23.486元

qwen-vl-plus

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

无阶梯计价

1.541元

4.624元

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3-vl-flash

> 当前能力等同于qwen3-vl-flash-2025-10-15

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤32K

0.15元

1.5元

32K<Token≤128K

0.3元

3元

128K<Token≤256K

0.6元

6元

qwen3-vl-flash

> 当前能力等同于qwen3-vl-flash-2026-01-22

欧盟

非思考和思考模式

0<Token≤32K

0.375元

2.998元

32K<Token≤128K

0.562元

4.497元

128K<Token≤256K

0.899元

7.194元

qwen3-vl-flash-2026-01-22

欧盟

非思考和思考模式

0<Token≤32K

0.375元

2.998元

32K<Token≤128K

0.562元

4.497元

128K<Token≤256K

0.899元

7.194元

qwen3-vl-flash-2025-10-15

全球

非思考和思考模式

0<Token≤32K

0.15元

1.5元

32K<Token≤128K

0.3元

3元

128K<Token≤256K

0.6元

6元

qwen3-vl-flash-2025-10-15

欧盟

非思考和思考模式

0<Token≤32K

0.375元

2.998元

32K<Token≤128K

0.562元

4.497元

128K<Token≤256K

0.899元

7.194元

qwen3-vl-plus

> 当前能力等同于qwen3-vl-plus-2025-12-19

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤32K

1元

10元

32K<Token≤128K

1.5元

15元

128K<Token≤256K

3元

30元

qwen3-vl-plus

欧盟

非思考和思考模式

0<Token≤32K

1.499元

11.991元

32K<Token≤128K

2.248元

17.986元

128K<Token≤256K

4.497元

35.972元

qwen3-vl-plus-2025-09-23

全球

非思考和思考模式

0<Token≤32K

1元

10元

32K<Token≤128K

1.5元

15元

128K<Token≤256K

3元

30元

qwen3-vl-plus-2025-09-23

欧盟

非思考和思考模式

0<Token≤32K

1.499元

11.991元

32K<Token≤128K

2.248元

17.986元

128K<Token≤256K

4.497元

35.972元

### 千问OCR

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3.5-ocr

中国内地

0.5元

2元

100万Token

qwen-vl-ocr

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

中国内地

0.3元

0.5元

100万Token

qwen-vl-ocr-latest

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

中国内地

0.3元

0.5元

100万Token

qwen-vl-ocr-2025-11-20

中国内地

0.3元

0.5元

100万Token

qwen-vl-ocr-2025-08-28

中国内地

5元

5元

100万Token

qwen-vl-ocr-2025-04-13

中国内地

5元

5元

100万Token

qwen-vl-ocr-2024-10-28

中国内地

5元

5元

100万Token

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen-vl-ocr

全球

0.3元

0.5元

qwen-vl-ocr-2025-11-20

全球

0.3元

0.5元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen-vl-ocr

国际

0.514元

1.174元

qwen-vl-ocr-2025-11-20

国际

0.514元

1.174元

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen-vl-ocr

全球

0.3元

0.5元

qwen-vl-ocr-2025-11-20

全球

0.3元

0.5元

### 千问Audio

计费规则：按输入Token和输出Token计费。

音频Token计算规则：每一秒钟的音频对应25个Token。若音频时长不足1秒，则按25个Token计算。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-audio-turbo

中国内地

目前仅供免费体验。

> 免费额度用完后不可调用，推荐使用[全模态（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)作为替代模型

10万Token

qwen-audio-turbo-latest

中国内地

### 千问数学模型

计费规则：按输入Token和输出Token计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-math-plus

中国内地

4元

12元

100万Token

qwen-math-turbo

中国内地

2元

6元

### 千问Coder

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，仅输入Token享有折扣。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-coder-plus

> 当前能力等同于qwen3-coder-plus-2025-09-23

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

0<Token≤32K

4元

16元

100万Token

32K<Token≤128K

6元

24元

128K<Token≤256K

10元

40元

256K<Token≤1M

20元

200元

qwen3-coder-plus-2025-09-23

中国内地

0<Token≤32K

4元

16元

100万Token

32K<Token≤128K

6元

24元

128K<Token≤256K

10元

40元

256K<Token≤1M

20元

200元

qwen3-coder-plus-2025-07-22

中国内地

0<Token≤32K

4元

16元

100万Token

32K<Token≤128K

6元

24元

128K<Token≤256K

10元

40元

256K<Token≤1M

20元

200元

qwen3-coder-flash

> 当前能力等同于qwen3-coder-flash-2025-07-28

中国内地

0<Token≤32K

1元

4元

100万Token

32K<Token≤128K

1.5元

6元

128K<Token≤256K

2.5元

10元

256K<Token≤1M

5元

25元

qwen3-coder-flash-2025-07-28

中国内地

0<Token≤32K

1元

4元

100万Token

32K<Token≤128K

1.5元

6元

128K<Token≤256K

2.5元

10元

256K<Token≤1M

5元

25元

##### **更多模型**

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-coder-plus

中国内地

无阶梯计价

3.5元

7元

100万Token

qwen-coder-turbo

中国内地

无阶梯计价

2元

6元

100万Token

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token数**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen3-coder-plus

> 当前能力等同于qwen3-coder-plus-2025-09-23

全球

0<Token≤32K

4元

16元

32K<Token≤128K

6元

24元

128K<Token≤256K

10元

40元

256K<Token≤1M

20元

200元

qwen3-coder-plus-2025-09-23

全球

0<Token≤32K

4元

16元

32K<Token≤128K

6元

24元

128K<Token≤256K

10元

40元

256K<Token≤1M

20元

200元

qwen3-coder-plus-2025-07-22

全球

0<Token≤32K

4元

16元

32K<Token≤128K

6元

24元

128K<Token≤256K

10元

40元

256K<Token≤1M

20元

200元

qwen3-coder-flash

> 当前能力等同于qwen3-coder-flash-2025-07-28

全球

0<Token≤32K

1元

4元

32K<Token≤128K

1.5元

6元

128K<Token≤256K

2.5元

10元

256K<Token≤1M

5元

25元

qwen3-coder-flash-2025-07-28

全球

0<Token≤32K

1元

4元

32K<Token≤128K

1.5元

6元

128K<Token≤256K

2.5元

10元

256K<Token≤1M

5元

25元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token数**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen3-coder-plus

> 当前能力等同于qwen3-coder-plus-2025-09-23

国际

0<Token≤32K

7.339元

36.696元

32K<Token≤128K

13.211元

66.053元

128K<Token≤256K

22.018元

110.089元

256K<Token≤1M

44.035元

440.354元

qwen3-coder-plus-2025-09-23

国际

0<Token≤32K

7.339元

36.696元

32K<Token≤128K

13.211元

66.053元

128K<Token≤256K

22.018元

110.089元

256K<Token≤1M

44.035元

440.354元

qwen3-coder-plus-2025-07-22

国际

0<Token≤32K

7.339元

36.696元

32K<Token≤128K

13.211元

66.053元

128K<Token≤256K

22.018元

110.089元

256K<Token≤1M

44.035元

440.354元

qwen3-coder-flash

> 当前能力等同于qwen3-coder-flash-2025-07-28

国际

0<Token≤32K

2.202元

11.009元

32K<Token≤128K

3.67元

18.348元

128K<Token≤256K

5.871元

29.357元

256K<Token≤1M

11.743元

70.457元

qwen3-coder-flash-2025-07-28

国际

0<Token≤32K

2.202元

11.009元

32K<Token≤128K

3.67元

18.348元

128K<Token≤256K

5.871元

29.357元

256K<Token≤1M

11.743元

70.457元

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token数**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen3-coder-plus

> 当前能力等同于qwen3-coder-plus-2025-09-23

全球

0<Token≤32K

4元

16元

32K<Token≤128K

6元

24元

128K<Token≤256K

10元

40元

256K<Token≤1M

20元

200元

qwen3-coder-plus-2025-09-23

全球

0<Token≤32K

4元

16元

32K<Token≤128K

6元

24元

128K<Token≤256K

10元

40元

256K<Token≤1M

20元

200元

qwen3-coder-plus-2025-07-22

全球

0<Token≤32K

4元

16元

32K<Token≤128K

6元

24元

128K<Token≤256K

10元

40元

256K<Token≤1M

20元

200元

qwen3-coder-flash

> 当前能力等同于qwen3-coder-flash-2025-07-28

全球

0<Token≤32K

1元

4元

32K<Token≤128K

1.5元

6元

128K<Token≤256K

2.5元

10元

256K<Token≤1M

5元

25元

qwen3-coder-flash-2025-07-28

全球

0<Token≤32K

1元

4元

32K<Token≤128K

1.5元

6元

128K<Token≤256K

2.5元

10元

256K<Token≤1M

5元

25元

### **千问翻译模型**

计费规则：按输入Token和输出Token计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-mt-plus

中国内地

1.8元

5.4元

100万Token

qwen-mt-flash

中国内地

0.7元

1.95元

100万Token

qwen-mt-lite

中国内地

0.6元

1.6元

100万Token

qwen-mt-turbo

中国内地

0.7元

1.95元

100万Token

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen-mt-flash

全球

0.7元

1.95元

qwen-mt-lite

全球

0.6元

1.6元

qwen-mt-lite-us

美国

0.881元

2.642元

qwen-mt-plus

全球

1.8元

5.4元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen-mt-plus

国际

18.055元

54.09元

qwen-mt-flash

国际

1.174元

3.596元

qwen-mt-lite

国际

0.881元

2.642元

qwen-mt-turbo

国际

1.174元

3.596元

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen-mt-plus

全球

1.8元

5.4元

qwen-mt-flash

全球

0.7元

1.95元

qwen-mt-lite

全球

0.6元

1.6元

### 千问数据挖掘模型

计费规则：按输入Token和输出Token计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-doc-turbo

中国内地

0.6元

1元

无免费额度

### **千问深入研究模型**

计费规则：按输入Token和输出Token计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-deep-research

中国内地

54元

163元

无免费额度

qwen-deep-research-2025-12-15

中国内地

79元

236元

无免费额度

### **通义晓蜜对话分析模型**

计费规则：按输入Token和输出Token计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

tongyi-xiaomi-analysis-flash

中国内地

0.2元

0.4元

100万Token

tongyi-xiaomi-analysis-pro

中国内地

1.0元

2.7元

100万Token

## **文本生成-千问-开源版**

### **Qwen3.6**

计费规则：按输入Token和输出Token计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

**非思考模式**

**思考模式（思维链+回答）**

qwen3.6-35b-a3b

中国内地

0<Token≤256K

1.8元

10.8元

10.8元

100万Token

qwen3.6-27b

中国内地

0<Token≤256K

3元

18元

18元

100万Token

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.6-35b-a3b

全球

0<Token≤256K

1.8元

10.8元

10.8元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.6-35b-a3b

国际

0<Token≤256K

2.810325元

16.86195元

16.86195元

qwen3.6-27b

国际

0<Token≤256K

4.49652元

26.97912元

26.97912元

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.6-35b-a3b

全球

0<Token≤256K

1.8元

10.8元

10.8元

### **Qwen3.5**

计费规则：按输入Token和输出Token计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

**非思考模式**

**思考模式（思维链+回答）**

qwen3.5-397b-a17b

中国内地

0<Token≤128K

1.2元

7.2元

7.2元

100万Token

128K<Token≤256K

3元

18元

18元

qwen3.5-122b-a10b

中国内地

0<Token≤128K

0.8元

6.4元

6.4元

100万Token

128K<Token≤256K

2元

16元

16元

qwen3.5-27b

中国内地

0<Token≤128K

0.6元

4.8元

4.8元

100万Token

128K<Token≤256K

1.8元

14.4元

14.4元

qwen3.5-35b-a3b

中国内地

0<Token≤128K

0.4元

3.2元

3.2元

100万Token

128K<Token≤256K

1.6元

12.8元

12.8元

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.5-397b-a17b

全球

0<Token≤128K

1.2元

7.2元

7.2元

128K<Token≤256K

3元

18元

18元

qwen3.5-122b-a10b

全球

0<Token≤128K

0.8元

6.4元

6.4元

128K<Token≤256K

2元

16元

16元

qwen3.5-27b

全球

0<Token≤128K

0.6元

4.8元

4.8元

128K<Token≤256K

1.8元

14.4元

14.4元

qwen3.5-35b-a3b

全球

0<Token≤128K

0.4元

3.2元

3.2元

128K<Token≤256K

1.6元

12.8元

12.8元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.5-397b-a17b

国际

0<Token≤256K

4.404元

26.421元

26.421元

qwen3.5-122b-a10b

国际

0<Token≤256K

2.936元

23.486元

23.486元

qwen3.5-27b

国际

0<Token≤256K

2.202元

17.614元

17.614元

qwen3.5-35b-a3b

国际

0<Token≤256K

1.835元

14.678元

14.678元

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.5-397b-a17b

全球

0<Token≤128K

1.2元

7.2元

7.2元

128K<Token≤256K

3元

18元

18元

qwen3.5-122b-a10b

全球

0<Token≤128K

0.8元

6.4元

6.4元

128K<Token≤256K

2元

16元

16元

qwen3.5-27b

全球

0<Token≤128K

0.6元

4.8元

4.8元

128K<Token≤256K

1.8元

14.4元

14.4元

qwen3.5-35b-a3b

全球

0<Token≤128K

0.4元

3.2元

3.2元

128K<Token≤256K

1.6元

12.8元

12.8元

### **Qwen3**

计费规则：按输入Token和输出Token计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

**非思考模式**

**思考模式（思维链+回答）**

qwen3-next-80b-a3b-thinking

中国内地

仅思考模式

1元

\-

10元

100万Token

qwen3-next-80b-a3b-instruct

中国内地

仅非思考模式

1元

4元

\-

100万Token

qwen3-235b-a22b-thinking-2507

中国内地

仅思考模式

2元

\-

20元

100万Token

qwen3-235b-a22b-instruct-2507

中国内地

仅非思考模式

2元

8元

\-

100万Token

qwen3-30b-a3b-thinking-2507

中国内地

仅思考模式

0.75元

\-

7.5元

100万Token

qwen3-30b-a3b-instruct-2507

中国内地

仅非思考模式

0.75元

3元

\-

100万Token

qwen3-235b-a22b

中国内地

非思考和思考模式

2元

8元

20元

100万Token

qwen3-32b

中国内地

非思考和思考模式

2元

8元

20元

100万Token

qwen3-30b-a3b

中国内地

非思考和思考模式

0.75元

3元

7.5元

100万Token

qwen3-14b

中国内地

非思考和思考模式

1元

4元

10元

100万Token

qwen3-8b

中国内地

非思考和思考模式

0.5元

2元

5元

100万Token

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3-next-80b-a3b-thinking

全球

仅思考模式

1元

\-

10元

qwen3-next-80b-a3b-instruct

全球

仅非思考模式

1元

4元

\-

qwen3-235b-a22b-thinking-2507

全球

仅思考模式

1.688元

\-

16.88元

qwen3-235b-a22b-instruct-2507

全球

仅非思考模式

1.688元

6.752元

\-

qwen3-30b-a3b-thinking-2507

全球

仅思考模式

0.75元

\-

7.5元

qwen3-30b-a3b-instruct-2507

全球

仅非思考模式

0.75元

3元

\-

qwen3-235b-a22b

全球

非思考和思考模式

2元

8元

20元

qwen3-32b

全球

非思考和思考模式

1.174元

4.697元

4.697元

qwen3-30b-a3b

全球

非思考和思考模式

0.75元

3元

7.5元

qwen3-14b

全球

非思考和思考模式

1元

4元

10元

qwen3-8b

全球

非思考和思考模式

0.5元

2元

5元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

**非思考模式**

**思考模式（思维链+回答）**

qwen3-next-80b-a3b-thinking

国际

仅思考模式

1.101元

\-

8.807元

无免费额度

qwen3-next-80b-a3b-instruct

国际

仅非思考模式

1.101元

8.807元

\-

无免费额度

qwen3-235b-a22b-thinking-2507

国际

仅思考模式

1.688元

\-

16.88元

无免费额度

qwen3-235b-a22b-instruct-2507

国际

仅非思考模式

1.688元

6.752元

\-

无免费额度

qwen3-30b-a3b-thinking-2507

国际

仅思考模式

1.468元

\-

17.614元

无免费额度

qwen3-30b-a3b-instruct-2507

国际

仅非思考模式

1.468元

5.871元

\-

无免费额度

qwen3-235b-a22b

国际

非思考和思考模式

5.137元

20.55元

61.65元

无免费额度

qwen3-32b

国际

非思考和思考模式

1.174元

4.697元

4.697元

无免费额度

qwen3-30b-a3b

国际

非思考和思考模式

1.468元

5.871元

17.614元

无免费额度

qwen3-14b

国际

非思考和思考模式

2.569元

10.275元

30.825元

无免费额度

qwen3-8b

国际

非思考和思考模式

1.321元

5.137元

15.412元

无免费额度

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3-next-80b-a3b-thinking

全球

仅思考模式

1元

\-

10元

qwen3-next-80b-a3b-instruct

全球

仅非思考模式

1元

4元

\-

qwen3-235b-a22b-thinking-2507

全球

仅思考模式

1.688元

\-

16.88元

qwen3-235b-a22b-instruct-2507

全球

仅非思考模式

1.688元

6.752元

\-

qwen3-30b-a3b-thinking-2507

全球

仅思考模式

0.75元

\-

7.5元

qwen3-30b-a3b-instruct-2507

全球

仅非思考模式

0.75元

3元

\-

qwen3-235b-a22b

全球

非思考和思考模式

2元

8元

20元

qwen3-32b

全球

非思考和思考模式

1.174元

4.697元

4.697元

qwen3-30b-a3b

全球

非思考和思考模式

0.75元

3元

7.5元

qwen3-14b

全球

非思考和思考模式

1元

4元

10元

qwen3-8b

全球

非思考和思考模式

0.5元

2元

5元

### **Qwen-Omni**

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费与限流](https://help.aliyun.com/zh/model-studio/qwen-omni#12db7427b94qt)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

**文本**

**音频**

**图片/视频**

**文本**

> 仅纯文本输入

**文本**

> 多模态输入

**文本+音频**

> 仅音频计费

qwen2.5-omni-7b

中国内地

0.6元

38元

2元

2.4元

6元

76元

100万Token（不区分模态）

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**文本**

**音频**

**图片/视频**

**文本**

> 仅纯文本输入

**文本**

> 多模态输入

**文本+音频**

> 仅音频计费

qwen2.5-omni-7b

国际

0.734元

49.613元

2.055元

2.936元

6.165元

99.153元

### **Qwen3-Omni-Captioner**

计费规则：按输入Token和输出Token计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-omni-30b-a3b-captioner

中国内地

15.8元

12.7元

100万Token

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen3-omni-30b-a3b-captioner

国际

27.962元

22.458元

### **Qwen-VL**

计费规则：按输入Token和输出Token计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-vl-235b-a22b-thinking

中国内地

仅思考模式

2元

20元

100万 Token

qwen3-vl-235b-a22b-instruct

中国内地

仅非思考模式

2元

8元

100万 Token

qwen3-vl-32b-thinking

中国内地

仅思考模式

2元

20元

100万 Token

qwen3-vl-32b-instruct

中国内地

仅非思考模式

2元

8元

100万 Token

qwen3-vl-30b-a3b-thinking

中国内地

仅思考模式

0.75元

7.5元

100万 Token

qwen3-vl-30b-a3b-instruct

中国内地

仅非思考模式

0.75元

3元

100万 Token

qwen3-vl-8b-thinking

中国内地

仅思考模式

0.5元

5元

100万 Token

qwen3-vl-8b-instruct

中国内地

仅非思考模式

0.5元

2元

100万 Token

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3-vl-235b-a22b-thinking

全球

仅思考模式

2元

20元

qwen3-vl-235b-a22b-instruct

全球

仅非思考模式

2元

8元

qwen3-vl-32b-thinking

全球

仅思考模式

1.174元

4.697元

qwen3-vl-32b-instruct

全球

仅非思考模式

1.174元

4.697元

qwen3-vl-30b-a3b-thinking

全球

仅思考模式

0.75元

7.5元

qwen3-vl-30b-a3b-instruct

全球

仅非思考模式

0.75元

3元

qwen3-vl-8b-thinking

全球

仅思考模式

0.5元

5元

qwen3-vl-8b-instruct

全球

仅非思考模式

0.5元

2元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3-vl-235b-a22b-thinking

国际

仅思考模式

2.936元

29.357元

qwen3-vl-235b-a22b-instruct

国际

仅非思考模式

2.936元

11.743元

qwen3-vl-32b-thinking

国际

仅思考模式

1.174元

4.697元

qwen3-vl-32b-instruct

国际

仅非思考模式

1.174元

4.697元

qwen3-vl-30b-a3b-thinking

国际

仅思考模式

1.468元

17.614元

qwen3-vl-30b-a3b-instruct

国际

仅非思考模式

1.468元

5.871元

qwen3-vl-8b-thinking

国际

仅思考模式

1.321元

15.412元

qwen3-vl-8b-instruct

国际

仅非思考模式

1.321元

5.137元

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3-vl-235b-a22b-thinking

全球

仅思考模式

2元

20元

qwen3-vl-235b-a22b-instruct

全球

仅非思考模式

2元

8元

qwen3-vl-32b-thinking

全球

仅思考模式

1.174元

4.697元

qwen3-vl-32b-instruct

全球

仅非思考模式

1.174元

4.697元

qwen3-vl-30b-a3b-thinking

全球

仅思考模式

0.75元

7.5元

qwen3-vl-30b-a3b-instruct

全球

仅非思考模式

0.75元

3元

qwen3-vl-8b-thinking

全球

仅思考模式

0.5元

5元

qwen3-vl-8b-instruct

全球

仅非思考模式

0.5元

2元

### **Qwen-Audio**

计费规则：按输入Token和输出Token计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen2-audio-instruct

中国内地

目前仅供免费体验。

> 免费额度用完后不可调用，推荐使用[全模态（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)作为替代模型。

10万Token

qwen-audio-chat

中国内地

### **Qwen-Coder**

计费规则：按输入Token和输出Token计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-coder-next

中国内地

0<Token≤32K

1元

4元

100万Token

32K<Token≤128K

1.5元

6元

128K<Token≤256K

2.5元

10元

qwen3-coder-480b-a35b-instruct

中国内地

0<Token≤32K

6元

24元

100万Token

32K<Token≤128K

9元

36元

128K<Token≤200K

15元

60元

qwen3-coder-30b-a3b-instruct

中国内地

0<Token≤32K

1.5元

6元

100万Token

32K<Token≤128K

2.25元

9元

128K<Token≤200K

3.75元

15元

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen3-coder-480b-a35b-instruct

全球

0<Token≤32K

6元

24元

32K<Token≤128K

9元

36元

128K<Token≤200K

15元

60元

qwen3-coder-30b-a3b-instruct

全球

0<Token≤32K

1.5元

6元

32K<Token≤128K

2.25元

9元

128K<Token≤200K

3.75元

15元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen3-coder-next

国际

0<Token≤32K

2.202元

11.009元

32K<Token≤128K

3.67元

18.348元

128K<Token≤256K

5.871元

29.357元

qwen3-coder-480b-a35b-instruct

国际

0<Token≤32K

11.009元

55.044元

32K<Token≤128K

19.816元

99.08元

128K<Token≤200K

33.027元

165.133元

qwen3-coder-30b-a3b-instruct

国际

0<Token≤32K

3.303元

16.513元

32K<Token≤128K

5.504元

27.522元

128K<Token≤200K

8.807元

44.035元

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen3-coder-30b-a3b-instruct

全球

0<Token≤32K

1.5元

6元

32K<Token≤128K

2.25元

9元

128K<Token≤200K

3.75元

15元

qwen3-coder-480b-a35b-instruct

全球

0<Token≤32K

6元

24元

32K<Token≤128K

9元

36元

128K<Token≤200K

15元

60元

qwen3-coder-next

欧盟

0<Token≤32K

2.248元

11.241元

32K<Token≤128K

3.747元

18.736元

128K<Token≤256K

5.995元

29.977元

## **文本生成-第三方模型**

### **DeepSeek**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

deepseek-v4-pro

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

12元

24元

100万Token

deepseek-v4-flash

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

1元

2元

100万Token

deepseek-v3.2

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

2元

3元

100万Token

deepseek-v3.2-exp

中国内地

2元

3元

100万Token

deepseek-v3.1

中国内地

4元

12元

100万Token

deepseek-r1

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

中国内地

4元

16元

100万Token

deepseek-r1-0528

中国内地

4元

16元

100万Token

deepseek-v3

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

中国内地

2元

8元

100万Token

deepseek-r1-distill-qwen-1.5b

中国内地

限时免费

deepseek-r1-distill-qwen-7b

中国内地

0.5元

1元

100万Token

deepseek-r1-distill-qwen-14b

中国内地

1元

3元

100万Token

deepseek-r1-distill-qwen-32b

中国内地

2元

6元

100万Token

deepseek-r1-distill-llama-8b

中国内地

限时免费

deepseek-r1-distill-llama-70b

中国内地

目前仅供免费体验

> 免费额度用完后不可调用，推荐使用[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)、[DeepSeek -阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)、[Kimi-阿里云](https://help.aliyun.com/zh/model-studio/kimi-api)作为替代模型

100万Token

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

deepseek-v4-pro

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

12元

24元

deepseek-v4-pro-us

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

17.986元

35.972元

deepseek-v4-flash

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

1元

2元

deepseek-v4-flash-us

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

1.499元

2.998元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

deepseek-v4-pro

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

17.986元

35.972元

deepseek-v4-flash

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

1.499元

2.998元

deepseek-v3.2

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

国际

4.272元

12.815元

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

deepseek-v4-pro

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

12元

24元

deepseek-v4-flash

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

1元

2元

#### 日本（东京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

deepseek-v4-pro

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

12元

24元

deepseek-v4-flash

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

1元

2元

deepseek-v4-pro

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

日本

17.986元

35.972元

deepseek-v4-flash

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

日本

1.499元

2.998元

### **DeepSeek-硅基流动**

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**

siliconflow/deepseek-v3.2

中国内地

2元

3元

无

siliconflow/deepseek-v3.1-terminus

中国内地

4元

12元

siliconflow/deepseek-r1-0528

中国内地

4元

16元

siliconflow/deepseek-v3-0324

中国内地

2元

8元

### **DeepSeek-快手万擎**

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**

vanchin/deepseek-v3.2-think

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

2元

3元

无

vanchin/deepseek-v3.1-terminus

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

4元

12元

vanchin/deepseek-r1

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

4元

16元

vanchin/deepseek-v3

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

2元

8元

vanchin/deepseek-ocr

中国内地

0.216元

0.216元

### **Kimi**

计费规则：按输入Token和输出Token计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

kimi-k2.7-code

中国内地

仅思考模式

6.5元

27元

100万Token

kimi-k2.6

中国内地

非思考和思考模式

6.5元

27元

100万Token

kimi-k2.5

中国内地

非思考和思考模式

4元

21元

100万Token

kimi-k2-thinking

中国内地

仅思考模式

4元

16元

100万Token

Moonshot-Kimi-K2-Instruct

中国内地

非思考模式

4元

16元

100万Token

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

kimi-k2.7-code

全球

仅思考模式

6.5元

27元

kimi-k2.5

全球

非思考和思考模式

4元

21元

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

kimi-k2.7-code

全球

仅思考模式

6.5元

27元

kimi-k2.5

全球

非思考和思考模式

4元

21元

#### 日本（东京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

kimi-k2.5

全球

非思考和思考模式

4元

21元

### **Kimi-月之暗面**

计费规则：按输入Token和输出Token计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

kimi/kimi-k2.7-code-highspeed

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

13元

54元

无

kimi/kimi-k2.7-code

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

6.5元

27元

kimi/kimi-k2.6

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

6.5元

27元

kimi/kimi-k2.5

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

4元

21元

### **GLM**

计费规则：按输入Token和输出Token计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

glm-5.2

中国内地

非思考和思考模式

不区分阶梯

8元

28元

100万Token

glm-5.1

中国内地

非思考和思考模式

0<Token≤32K

6元

24元

100万Token

32K<Token≤200K

8元

28元

glm-5

中国内地

非思考和思考模式

0<Token≤32K

4元

18元

100万Token

32K<Token≤198K

6元

22元

glm-4.7

中国内地

非思考和思考模式

0<Token≤32K

3元

14元

100万Token

32K<Token≤166K

4元

16元

glm-4.6

中国内地

非思考和思考模式

0<Token≤32K

3元

14元

100万Token

32K<Token≤166K

4元

16元

glm-4.5

中国内地

非思考和思考模式

0<Token≤32K

3元

14元

100万Token

32K<Token≤96K

4元

16元

glm-4.5-air

中国内地

非思考和思考模式

0<Token≤32K

0.8元

6元

100万Token

32K<Token≤96K

1.2元

8元

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

glm-5.2

全球

非思考和思考模式

不区分阶梯

8元

28元

glm-5.1

全球

非思考和思考模式

0<Token≤32K

6元

24元

32K<Token≤200K

8元

28元

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

glm-5.1

国际

非思考和思考模式

0<Token≤200K

10.492元

32.974元

100万Token

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

glm-5.2

全球

非思考和思考模式

不区分阶梯

8元

28元

glm-5.1

全球

非思考和思考模式

0<Token≤32K

6元

24元

32K<Token≤200K

8元

28元

#### 日本（东京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

glm-5.1

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

全球

非思考和思考模式

0<Token≤32K

6元

24元

32K<Token≤200K

8元

28元

### **GLM-智谱**

计费规则：按输入Token和输出Token计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

ZHIPU/GLM-5.2

中国内地

非思考和思考模式

8元

28元

无

ZHIPU/GLM-5.1

中国内地

非思考和思考模式

8元

28元

无

ZHIPU/GLM-5

中国内地

非思考和思考模式

6元

22元

无

### MiniMax

计费规则：按输入Token和输出Token计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

MiniMax-M2.5

中国内地

仅思考模式

2.1元

8.4元

100万Token

MiniMax-M2.1

中国内地

仅思考模式

2.1元

8.4元

### **MiniMax-稀宇科技**

计费规则：按输入Token和输出Token计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

MiniMax/MiniMax-M3

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

非思考和思考模式

4.2元

16.8元

无

MiniMax/MiniMax-M2.7

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

仅思考模式

2.1元

8.4元

MiniMax/MiniMax-M2.5

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

仅思考模式

2.1元

8.4元

MiniMax/MiniMax-M2.1

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

中国内地

仅思考模式

2.1元

8.4元

### **MiMo-小米**

计费规则：按输入Token和输出Token计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入Token数量**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

xiaomi/mimo-v2.5-pro

中国内地

0<Token≤256K

7元

21元

无

256K<Token≤1M

14元

42元

### **Stepfun-阶跃星辰**

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

stepfun/step-3.7-flash

中国内地

1.35元

8.1元

无

## **图像生成**

计费规则：输入不计费，输出计费。输出按成功生成的 **图像张数** 计费。

计费公式：`费用 = 图像单价 × 输出的图像张数`。

计费说明：

-   费用与输出图像的分辨率、宽高比无关。
    
-   请求失败不产生任何费用，也不消耗免费额度。
    

计费示例：部分图像生成失败

假设图像单价为 0.10元/张。若您调用接口请求生成 4 张图像，但实际仅成功返回 3 张图像的 URL，另 1 张生成失败，系统将仅对成功生成的图像进行计费。

-   计费数量：3 张。
    
-   费用计算：0.1 × 3 = 0.3元。
    

### **千问文生图**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-image-2.0-pro

中国内地

0.5元/张

100张

qwen-image-2.0-pro-2026-04-22

中国内地

0.5元/张

100张

qwen-image-2.0-pro-2026-03-03

中国内地

0.5元/张

100张

qwen-image-2.0

中国内地

0.2元/张

100张

qwen-image-2.0-2026-03-03

中国内地

0.2元/张

100张

qwen-image-max

> 当前能力等同于qwen-image-max-2025-12-30

中国内地

0.5元/张

100张

qwen-image-max-2025-12-30

中国内地

0.5元/张

100张

qwen-image-plus

> 当前能力等同于qwen-image

中国内地

0.2元/张

100张

qwen-image-plus-2026-01-09

中国内地

0.2元/张

100张

qwen-image

中国内地

0.25元/张

100张

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

qwen-image-2.0-pro

国际

0.550443元/张

qwen-image-2.0-pro-2026-04-22

国际

0.550443元/张

qwen-image-2.0-pro-2026-03-03

国际

0.550443元/张

qwen-image-2.0

国际

0.256873元/张

qwen-image-2.0-2026-03-03

国际

0.256873元/张

qwen-image-max

> 当前能力等同于qwen-image-max-2025-12-30

国际

0.550443元/张

qwen-image-max-2025-12-30

国际

0.550443元/张

qwen-image-plus

> 当前能力等同于qwen-image

国际

0.220177元/张

qwen-image-plus-2026-01-09

国际

0.220177元/张

qwen-image

国际

0.256873元/张

### **千问图像编辑**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-image-2.0-pro

中国内地

0.5元/张

100张

qwen-image-2.0-pro-2026-04-22

中国内地

0.5元/张

100张

qwen-image-2.0-pro-2026-03-03

中国内地

0.5元/张

100张

qwen-image-2.0

中国内地

0.2元/张

100张

qwen-image-2.0-2026-03-03

中国内地

0.2元/张

100张

qwen-image-edit-max

> 当前能力等同于qwen-image-edit-max-2026-01-16

中国内地

0.5元/张

100张

qwen-image-edit-max-2026-01-16

中国内地

0.5元/张

100张

qwen-image-edit-plus

> 当前能力等同于qwen-image-edit-plus-2025-10-30

中国内地

0.2元/张

100张

qwen-image-edit-plus-2025-12-15

中国内地

0.2元/张

100张

qwen-image-edit-plus-2025-10-30

中国内地

0.2元/张

100张

qwen-image-edit

中国内地

0.3元/张

100张

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

qwen-image-2.0-pro

国际

0.550443元/张

qwen-image-2.0-pro-2026-04-22

国际

0.550443元/张

qwen-image-2.0-pro-2026-03-03

国际

0.550443元/张

qwen-image-2.0

国际

0.256873元/张

qwen-image-2.0-2026-03-03

国际

0.256873元/张

qwen-image-edit-max

> 当前能力等同于qwen-image-edit-max-2026-01-16

国际

0.550443元/张

qwen-image-edit-max-2026-01-16

国际

0.550443元/张

qwen-image-edit-plus

> 当前能力等同于qwen-image-edit-plus-2025-10-30

国际

0.220177元/张

qwen-image-edit-plus-2025-12-15

国际

0.220177元/张

qwen-image-edit-plus-2025-10-30

国际

0.220177元/张

qwen-image-edit

国际

0.330266元/张

### **千问图像翻译**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-mt-image

中国内地

0.003元/张

100张

### **Z-Image**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

z-image-turbo

中国内地

关闭提示词改写（`prompt_extend=false`）：0.1元/张

开启提示词改写（`prompt_extend=true`）：0.2元/张

100张

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

z-image-turbo

国际

关闭提示词改写（`prompt_extend=false`）：0.110089元/张

开启提示词改写（`prompt_extend=true`）：0.220177元/张

### **万相文生图**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.6-t2i

中国内地

0.20元/张

50张

wan2.5-t2i-preview

中国内地

0.20元/张

50张

wan2.2-t2i-plus

中国内地

0.20元/张

100张

wan2.2-t2i-flash

中国内地

0.14元/张

100张

wanx2.1-t2i-plus

中国内地

0.20元/张

500张

wanx2.1-t2i-turbo

中国内地

0.14元/张

500张

wanx2.0-t2i-turbo

中国内地

0.04元/张

500张

wanx-v1

中国内地

0.16元/张

500张

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

wan2.6-t2i

全球

0.20元/张

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

wan2.6-t2i

国际

0.220177元/张

wan2.5-t2i-preview

国际

0.220177元/张

wan2.2-t2i-plus

国际

0.366962元/张

wan2.2-t2i-flash

国际

0.183481元/张

wan2.1-t2i-plus

国际

0.366962元/张

wan2.1-t2i-turbo

国际

0.183481元/张

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

wan2.6-t2i

全球

0.20元/张

### **万相图像生成与编辑**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.7-image-pro

中国内地

0.50元/张

50张

wan2.7-image

中国内地

0.20元/张

50张

wan2.6-image

中国内地

0.20元/张

50张

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

wan2.6-image

全球

0.20元/张

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

wan2.7-image-pro

国际

0.562065元/张

wan2.7-image

国际

0.220177元/张

wan2.6-image

国际

0.220177元/张

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

wan2.6-image

全球

0.20元/张

### **万相通用图像编辑**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.5-i2i-preview

中国内地

0.20元/张

50张

wanx2.1-imageedit

中国内地

0.14元/张

500张

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

wan2.5-i2i-preview

国际

0.220177元/张

### **万相涂鸦作画**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wanx-sketch-to-image-lite

中国内地

0.06元/张

500张

### **万相图像局部重绘**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wanx-x-painting

中国内地

目前仅供免费体验。

> 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)获取替代方案。

500张

### 人像风格重绘

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wanx-style-repaint-v1

中国内地

0.12元/张

500张

### **图像背景生成**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wanx-background-generation-v2

中国内地

0.08元/张

500张

### **图像画面扩展**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

image-out-painting

中国内地

0.18元/张

500张

### **人物实例分割**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

image-instance-segmentation

中国内地

目前仅供免费体验。

> 免费额度用完后不可调用。

500张

### **图像擦除补全**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

image-erase-completion

中国内地

目前仅供免费体验。

> 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)获取替代方案。

500张

### **虚拟模特**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wanx-virtualmodel

中国内地

目前仅供免费体验。

> 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)获取替代方案。

各500张

virtualmodel-v2

中国内地

### **鞋靴模特**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

shoemodel-v1

中国内地

目前仅供免费体验。

> 免费额度用完后不可调用。

500张

### **创意海报生成**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wanx-poster-generation-v1

中国内地

目前仅供免费体验。

> 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)获取替代方案。

500张

### **人物写真生成-FaceChain**

-   facechain-facedetect：限时免费。
    
-   facechain-finetune：按训练次数计费，请求失败不计费。
    
-   facechain-generation：输入不计费，输出计费。输出按成功生成的图片张数计费，计费规则请参见[图像生成](#26310bc5cf4do)。
    

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

facechain-facedetect

中国内地

限时免费

限时免费

facechain-finetune

中国内地

2.5元/次

50次

有效期：申请通过后90天内

facechain-generation

中国内地

0.18元/张

500张

有效期：申请通过后90天内

### **创意文字生成-WordArt锦书**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wordart-texture

中国内地

0.08元/张

500张

wordart-semantic

中国内地

0.24元/张

### **AI试衣-OutfitAnyone**

-   aitryon：输入不计费，输出计费。计费规则请参见[图像生成](#26310bc5cf4do)。
    
-   aitryon-plus：输入不计费，输出计费。计费规则请参见[图像生成](#26310bc5cf4do)。
    
-   aitryon-parsing-v1：输入计费，输出不计费。按输入的图像张数计费，请求失败不计费。
    
-   aitryon-refiner：输入不计费，输出计费。计费规则请参见[图像生成](#26310bc5cf4do)。
    

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

aitryon

中国内地

400张

aitryon-plus

中国内地

400张

aitryon-parsing-v1

中国内地

400张

aitryon-refiner

中国内地

100张

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**单价**

**折扣**

**阶梯层级**

aitryon

中国内地

0.20元/张

无

无

aitryon-plus

中国内地

0.50元/张

无

无

aitryon-parsing-v1

中国内地

0.004元/张

无

无

aitryon-refiner

中国内地

0.30元/张

无

生成数量 ≤ 25张

0.275元/张

9.2折

25张 ＜ 生成数量 ≤ 125张

0.25元/张

8.4折

125张 ＜ 生成数量 ≤ 250张

0.225元/张

7.5折

250张 ＜ 生成数量 ≤ 1250张

0.20元/张

6.7折

1250张 ＜ 生成数量 ≤ 2500张

0.175元/张

5.8折

2500张 ＜ 生成数量 ≤ 2.5万张

0.15元/张

5折

生成数量 ＞ 2.5万张

## **图像生成-第三方模型**

### **可灵-图像生成**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出图像分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

kling/kling-v3-image-generation

中国内地

1K

0.2元/张

无免费额度

2K

0.2元/张

kling/kling-v3-omni-image-generation

中国内地

1K

0.2元/张

2K

0.2元/张

4K

0.4元/张

## **音乐生成**

计费规则：按输出音频的秒数计费，输入不计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价（每秒）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

fun-music-preview

中国内地

0.005元

1,000秒

fun-music-v1

中国内地

0.002元

## **语音合成（文本转语音）**

### **Qwen-TTS**

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

#### **千问3-TTS-Instruct-Flash**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-tts-instruct-flash

中国内地

0.8元

不计费

1万字符

qwen3-tts-instruct-flash-2026-01-26

中国内地

0.8元

不计费

1万字符

#### **千问3-TTS-VD**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-tts-vd-2026-01-26

中国内地

0.8元

不计费

1万字符

#### **千问3-TTS-VC**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-tts-vc-2026-01-22

中国内地

0.8元

不计费

1万字符

#### 千问3-TTS-Flash

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-tts-flash

> 当前能力等同于qwen3-tts-flash-2025-11-27

中国内地

0.8元

不计费

1万字符

qwen3-tts-flash-2025-11-27

中国内地

0.8元

不计费

1万字符

qwen3-tts-flash-2025-09-18

中国内地

0.8元

不计费

2025年11月13日0点后开通阿里云百炼：1万字符

#### 千问-TTS

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-tts-flash

中国内地

1.6元

10元

100万Token

qwen-tts-latest

中国内地

1.6元

10元

100万Token

qwen-tts-2025-05-22

中国内地

1.6元

10元

100万Token

qwen-tts-2025-04-10

中国内地

1.6元

10元

100万Token

#### 新加坡

#### **千问3-TTS-Instruct-Flash**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

qwen3-tts-instruct-flash

国际

0.8元

qwen3-tts-instruct-flash-2026-01-26

国际

0.8元

#### **千问3-TTS-VD**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

qwen3-tts-vd-2026-01-26

国际

0.8元

#### **千问3-TTS-VC**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

qwen3-tts-vc-2026-01-22

国际

0.8元

#### 千问3-TTS-Flash

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

qwen3-tts-flash

> 当前能力等同于qwen3-tts-flash-2025-11-27

国际

0.733924元

qwen3-tts-flash-2025-11-27

国际

0.733924元

qwen3-tts-flash-2025-09-18

国际

0.733924元

### **Qwen-TTS-Realtime**

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

#### **千问3-TTS-Instruct-Flash-Realtime**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-tts-instruct-flash-realtime

中国内地

1元

不计费

1万字符

qwen3-tts-instruct-flash-realtime-2026-01-22

中国内地

1元

不计费

1万字符

#### 千问3-TTS-VD-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-tts-vd-realtime-2026-01-15

中国内地

1元

不计费

1万字符

qwen3-tts-vd-realtime-2025-12-16

中国内地

1元

不计费

1万字符

#### 千问3-TTS-VC-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-tts-vc-realtime-2026-01-15

中国内地

1元

不计费

1万字符

qwen3-tts-vc-realtime-2025-11-27

中国内地

1万字符

#### 千问3-TTS-Flash-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-tts-flash-realtime

中国内地

1元

不计费

2025年11月13日0点后开通阿里云百炼：1万字符

qwen3-tts-flash-realtime-2025-11-27

中国内地

1元

不计费

1万字符

qwen3-tts-flash-realtime-2025-09-18

中国内地

1元

不计费

2025年11月13日0点后开通阿里云百炼：1万字符

#### 千问-TTS-Realtime

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-tts-realtime

中国内地

2.4元

12元

100万Token

qwen-tts-realtime-latest

中国内地

2.4元

12元

100万Token

qwen-tts-realtime-2025-07-15

中国内地

2.4元

12元

100万Token

#### 新加坡

#### **千问3-TTS-Instruct-Flash-Realtime**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

qwen3-tts-instruct-flash-realtime

国际

1元

qwen3-tts-instruct-flash-realtime-2026-01-22

国际

1元

#### 千问3-TTS-VD-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

qwen3-tts-vd-realtime-2026-01-15

国际

0.954101元

qwen3-tts-vd-realtime-2025-12-16

国际

0.954101元

#### 千问3-TTS-VC-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

qwen3-tts-vc-realtime-2026-01-15

国际

0.954101元

qwen3-tts-vc-realtime-2025-11-27

国际

#### 千问3-TTS-Flash-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

qwen3-tts-flash-realtime

国际

0.954101元

qwen3-tts-flash-realtime-2025-11-27

国际

0.954101元

qwen3-tts-flash-realtime-2025-09-18

国际

0.954101元

### **Qwen-TTS声音复刻**

计费规则：按新建音色个数计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**单价（每个音色）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-voice-enrollment

中国内地

0.01元

1000个音色/账号

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**单价（每个音色）**

qwen-voice-enrollment

国际

0.01元

### **Qwen-TTS声音设计**

计费规则：按新建音色个数计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**单价（每个音色）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-voice-design

中国内地

0.2元

10个音色/账号

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**单价（每个音色）**

qwen-voice-design

国际

0.2元

### **CosyVoice**

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

cosyvoice-v3.5-plus

中国内地

1.5元

1万字符

cosyvoice-v3.5-flash

中国内地

0.8元

1万字符

cosyvoice-v3-plus

中国内地

2元

1万字符

cosyvoice-v3-flash

中国内地

1元

1万字符

cosyvoice-v2

中国内地

2元

1万字符

cosyvoice-v1

中国内地

2元

1万字符

#### 新加坡

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

cosyvoice-v3-plus

国际

1.9082元

1万字符

cosyvoice-v3-flash

国际

0.9541元

100万Token

### **Sambert**

计费规则：按输入文本的字符数计费，输出不计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每万字符）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

参见[模型列表](https://help.aliyun.com/zh/model-studio/sambert-java-sdk#57d33631f7doi)

中国内地

1元

每主账号每模型每月3万字符。

### MiniMax

计费规则：按输入文本的字符数计费，输出不计费。

复刻音色收取一次性费用，费用在首次使用该音色进行语音合成的时候，与语音合成的费用一同出账。

**模型名称**

**服务部署范围**

**语音合成单价（每万字符）**

[复刻一个音色](https://help.aliyun.com/zh/model-studio/mini-clone-api)

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

MiniMax/speech-2.8-hd

中国内地

3.5元

9.9元

（在首次使用复刻出来的音色进行语音合成的时候收取）

无

MiniMax/speech-02-hd

中国内地

3.5元

MiniMax/speech-2.8-turbo

中国内地

2元

MiniMax/speech-02-turbo

中国内地

2元

## **语音识别（语音转文本）与翻译（语音转成指定语种的文本）**

### **千问-LiveTranslate-Flash-Realtime**

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费说明](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#6a95f2fc38za0)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

**输入：音频**

**输入：图片**

**输出：文本**

**输出：音频**

qwen3.5-livetranslate-flash-realtime

中国内地

40元

3.3元

100元

160元

100万Token

qwen3.5-livetranslate-flash-realtime-2026-05-19

中国内地

40元

3.3元

100元

160元

100万Token

qwen3-livetranslate-flash-realtime

中国内地

64元

8元

64元

240元

100万Token

qwen3-livetranslate-flash-realtime-2025-09-22

中国内地

64元

8元

64元

240元

100万Token

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价 (每百万 Token)**

**输出单价 (每百万 Token)**

**输入：音频**

**输入：图片**

**输出：文本**

**输出：音频**

qwen3.5-livetranslate-flash-realtime

国际

56.207元

4.122元

149.884元

224.826元

qwen3.5-livetranslate-flash-realtime-2026-05-19

国际

56.207元

4.122元

149.884元

224.826元

qwen3-livetranslate-flash-realtime

国际

73.392元

9.541元

73.392元

278.891元

qwen3-livetranslate-flash-realtime-2025-09-22

国际

73.392元

9.541元

73.392元

278.891元

### **千问-LiveTranslate-Flash**

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费说明](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash#e02a82e668y2c)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

**输入：音频**

**输入：图片**

**输出：文本**

**输出：音频**

qwen3-livetranslate-flash

中国内地

10元

4元

10元

40元

100万Token

qwen3-livetranslate-flash-2025-12-01

中国内地

10元

4元

10元

40元

100万Token

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价 (每百万 Token)**

**输出单价 (每百万 Token)**

**输入：音频**

**输入：图片**

**输出：文本**

**输出：音频**

qwen3-livetranslate-flash

国际

11.573元

4.629元

11.573元

46.292元

qwen3-livetranslate-flash-2025-12-01

国际

11.573元

4.629元

11.573元

46.292元

### **千问ASR**

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

计费规则：按输入音频的秒数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-asr-flash-filetrans

中国内地

0.00022元/秒

不计费

36,000秒（10小时）

qwen3-asr-flash-filetrans-2025-11-17

中国内地

36,000秒（10小时）

qwen3-asr-flash

> 当前能力等同于qwen3-asr-flash-2025-09-08

中国内地

36,000秒（10小时）

qwen3-asr-flash-2026-02-10

中国内地

36,000秒（10小时）

qwen3-asr-flash-2025-09-08

中国内地

36,000秒（10小时）

#### 美国（弗吉尼亚）

计费规则：按输入音频的秒数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价**

**输出单价**

qwen3-asr-flash-us

美国

0.000035元/秒

不计费

qwen3-asr-flash-2025-09-08-us

美国

0.000035元/秒

#### 新加坡

计费规则：按输入音频的秒数计费，输出不计费。

**模型 ID（Model ID）**

**服务部署范围**

**输入单价**

**输出单价**

qwen3-asr-flash-filetrans

国际

0.00026元/秒

不计费

qwen3-asr-flash-filetrans-2025-11-17

国际

0.00026元/秒

qwen3-asr-flash

> 当前能力等同于qwen3-asr-flash-2025-09-08

国际

0.00026元/秒

qwen3-asr-flash-2026-02-10

国际

0.00026元/秒

qwen3-asr-flash-2025-09-08

国际

0.00026元/秒

### **千问ASR-Realtime**

计费规则：按输入音频的秒数计费，输出不计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-asr-flash-realtime

中国内地

0.00033元/秒

36,000秒（10小时）

qwen3-asr-flash-realtime-2026-02-10

中国内地

36,000秒（10小时）

qwen3-asr-flash-realtime-2025-10-27

中国内地

36,000秒（10小时）

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价**

qwen3-asr-flash-realtime

国际

0.00066元/秒

qwen3-asr-flash-realtime-2026-02-10

国际

qwen3-asr-flash-realtime-2025-10-27

国际

### **Fun-ASR**

#### **录音文件识别**

计费规则：按输入音频的秒数计费，输出不计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

fun-asr

中国内地

0.00022元/秒

36,000秒（10小时）

fun-asr-2025-11-07

中国内地

36,000秒（10小时）

fun-asr-2025-08-25

中国内地

36,000秒（10小时）

fun-asr-mtl

中国内地

36,000秒（10小时）

fun-asr-mtl-2025-08-25

中国内地

36,000秒（10小时）

fun-asr-flash-2026-06-15

中国内地

0.00022元/秒

36,000秒（10小时）

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价**

fun-asr

国际

0.00026元/秒

fun-asr-2025-11-07

国际

fun-asr-2025-08-25

国际

fun-asr-mtl

国际

fun-asr-mtl-2025-08-25

国际

fun-asr-flash-2026-06-15

国际

0.00026元/秒

#### **实时语音识别**

计费规则：按输入音频的秒数计费，输出不计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

fun-asr-realtime

中国内地

0.00033元/秒

36,000秒（10小时）

fun-asr-realtime-2026-02-28

中国内地

36,000秒（10小时）

fun-asr-realtime-2025-11-07

中国内地

36,000秒（10小时）

fun-asr-realtime-2025-09-15

中国内地

36,000秒（10小时）

fun-asr-mtl-realtime

中国内地

36,000秒（10小时）

fun-asr-mtl-realtime-2025-12-10

中国内地

36,000秒（10小时）

fun-asr-flash-8k-realtime

中国内地

0.00022元/秒

36,000秒（10小时）

fun-asr-flash-8k-realtime-2026-01-28

中国内地

36,000秒（10小时）

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价**

fun-asr-realtime

国际

0.00066元/秒

fun-asr-realtime-2025-11-07

国际

### **Paraformer**

#### **录音文件识别**

计费规则：按输入音频的秒数计费，输出不计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

paraformer-v2

中国内地

0.00008元/秒

36,000秒（10小时）

每月1日0点自动发放

有效期1个月

paraformer-8k-v2

中国内地

paraformer-v1

中国内地

paraformer-8k-v1

中国内地

paraformer-mtl-v1

中国内地

#### **实时语音识别**

计费规则：按输入音频的秒数计费，输出不计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

paraformer-realtime-v2

中国内地

0.00024元/秒

36,000秒（10小时）

每月1日0点自动发放

有效期1个月

paraformer-realtime-v1

中国内地

paraformer-realtime-8k-v2

中国内地

paraformer-realtime-8k-v1

中国内地

## **视频生成**

计费规则：输入不计费，输出计费。输出按成功生成的 **视频秒数** 计费。

计费公式：`费用 = 视频单价 × 输出的视频时长（单位：秒）`。

计费说明：

-   部分模型按**输出视频分辨率定价**。不同分辨率（480P/720P/1080P）的计费价格有差异。
    
-   部分模型按**输出视频模式定价**。不同视频模式（标准版/专业版）的计费价格有差异。
    
-   部分模型按**输出视频画幅定价**。不同视频画幅（1:1/3:4）的计费价格有差异。
    
-   部分模型采用**统一定价**，与分辨率、模式或画幅无关。
    
-   请求失败不产生任何费用，也不会消耗免费额度。
    

### **HappyHorse-文生视频**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

happyhorse-1.1-t2v

中国内地

720P

0.9元/秒

10秒

1080P

1.2元/秒

happyhorse-1.0-t2v

中国内地

720P

0.9元/秒

10秒

1080P

1.6元/秒

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

happyhorse-1.1-t2v

全球

720P

0.9元/秒

1080P

1.2元/秒

happyhorse-1.0-t2v

全球

720P

0.9元/秒

1080P

1.6元/秒

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

happyhorse-1.1-t2v

国际

720P

1.049188元/秒

1080P

1.348956元/秒

happyhorse-1.0-t2v

国际

720P

1.049188元/秒

1080P

1.798608元/秒

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

happyhorse-1.1-t2v

全球

720P

0.9元/秒

1080P

1.2元/秒

happyhorse-1.0-t2v

全球

720P

0.9元/秒

1080P

1.6元/秒

### **HappyHorse-图生视频-基于首帧**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

happyhorse-1.1-i2v

中国内地

720P

0.9元/秒

10秒

1080P

1.2元/秒

happyhorse-1.0-i2v

中国内地

720P

0.9元/秒

10秒

1080P

1.6元/秒

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

happyhorse-1.1-i2v

全球

720P

0.9元/秒

1080P

1.2元/秒

happyhorse-1.0-i2v

全球

720P

0.9元/秒

1080P

1.6元/秒

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

happyhorse-1.1-i2v

国际

720P

1.049188元/秒

1080P

1.348956元/秒

happyhorse-1.0-i2v

国际

720P

1.049188元/秒

1080P

1.798608元/秒

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

happyhorse-1.1-i2v

全球

720P

0.9元/秒

1080P

1.2元/秒

happyhorse-1.0-i2v

全球

720P

0.9元/秒

1080P

1.6元/秒

### **HappyHorse-参考生视频**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

happyhorse-1.1-r2v

中国内地

720P

0.9元/秒

10秒

1080P

1.2元/秒

happyhorse-1.0-r2v

中国内地

720P

0.9元/秒

10秒

1080P

1.6元/秒

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

happyhorse-1.1-r2v

全球

720P

0.9元/秒

1080P

1.2元/秒

happyhorse-1.0-r2v

全球

720P

0.9元/秒

1080P

1.6元/秒

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

happyhorse-1.1-r2v

国际

720P

1.049188元/秒

1080P

1.348956元/秒

happyhorse-1.0-r2v

国际

720P

1.049188元/秒

1080P

1.798608元/秒

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

happyhorse-1.1-r2v

全球

720P

0.9元/秒

1080P

1.2元/秒

happyhorse-1.0-r2v

全球

720P

0.9元/秒

1080P

1.6元/秒

### **HappyHorse-视频编辑**

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输入和输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

happyhorse-1.0-video-edit

中国内地

720P

0.9元/秒

10秒

1080P

1.6元/秒

#### 美国（弗吉尼亚）

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输入和输出单价**

happyhorse-1.0-video-edit

全球

720P

0.9元/秒

1080P

1.6元/秒

#### 新加坡

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输入和输出单价**

happyhorse-1.0-video-edit

国际

720P

1.049188元/秒

1080P

1.798608元/秒

#### 德国（法兰克福）

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输入和输出单价**

happyhorse-1.0-video-edit

全球

720P

0.9元/秒

1080P

1.6元/秒

### **万相-文生视频**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.7-t2v-2026-04-25

中国内地

720P

0.6元/秒

50秒

1080P

1元/秒

wan2.7-t2v

中国内地

720P

0.6元/秒

50秒

1080P

1元/秒

wan2.6-t2v

中国内地

720P

0.6元/秒

50秒

1080P

1元/秒

wan2.5-t2v-preview

中国内地

480P

0.3元/秒

50秒

720P

0.6元/秒

1080P

1元/秒

wan2.2-t2v-plus

中国内地

480P

0.14元/秒

50秒

1080P

0.70元/秒

wanx2.1-t2v-turbo

中国内地

480P

0.24元/秒

200秒

720P

0.24元/秒

wanx2.1-t2v-plus

中国内地

720P

0.70元/秒

200秒

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

wan2.6-t2v

全球

720P

0.6元/秒

1080P

1元/秒

wan2.6-t2v-us

美国

720P

0.733924元/秒

1080P

1.100886元/秒

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

wan2.7-t2v-2026-04-25

国际

720P

0.733924元/秒

1080P

1.100886元/秒

wan2.7-t2v

国际

720P

0.733924元/秒

1080P

1.100886元/秒

wan2.6-t2v

国际

720P

0.733924元/秒

1080P

1.100886元/秒

wan2.5-t2v-preview

国际

480P

0.366961元/秒

720P

0.733923元/秒

1080P

1.100885元/秒

wan2.2-t2v-plus

国际

480P

0.146785元/秒

1080P

0.733924元/秒

wan2.1-t2v-turbo

国际

480P

0.264213元/秒

720P

0.264213元/秒

wan2.1-t2v-plus

国际

720P

0.733924元/秒

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

wan2.6-t2v

全球

720P

0.6元/秒

1080P

1元/秒

### **万相-图生视频**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.7-i2v-2026-04-25

中国内地

有声视频

720P

0.6元/秒

50秒

1080P

1元/秒

wan2.7-i2v

中国内地

有声视频

720P

0.6元/秒

50秒

1080P

1元/秒

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输出单价**

wan2.7-i2v-2026-04-25

国际

有声视频

720P

0.733924元/秒

1080P

1.100886元/秒

wan2.7-i2v

国际

有声视频

720P

0.733924元/秒

1080P

1.100886元/秒

### **万相-图生视频-基于首帧**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.6-i2v-flash

中国内地

有声视频

`audio=true`

720P

0.3元/秒

50秒

1080P

0.5元/秒

无声视频

`audio=false`

720P

0.15元/秒

1080P

0.25元/秒

wan2.6-i2v

中国内地

有声视频

720P

0.6元/秒

50秒

1080P

1元/秒

wan2.5-i2v-preview

中国内地

有声视频

480P

0.3元/秒

50秒

720P

0.6元/秒

1080P

1元/秒

wan2.2-i2v-flash

中国内地

无声视频

480P

0.10元/秒

50秒

720P

0.20元/秒

1080P

0.48元/秒

wan2.2-i2v-plus

中国内地

无声视频

480P

0.14元/秒

50秒

1080P

0.70元/秒

wanx2.1-i2v-turbo

中国内地

无声视频

480P

0.24元/秒

200秒

720P

0.24元/秒

wanx2.1-i2v-plus

中国内地

无声视频

720P

0.70元/秒

200秒

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输出单价**

wan2.6-i2v

全球

有声视频

720P

0.6元/秒

1080P

1元/秒

wan2.6-i2v-us

美国

有声视频

720P

0.733924元/秒

1080P

1.100886元/秒

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输出单价**

wan2.6-i2v-flash

国际

有声视频

`audio=true`

720P

0.366962元/秒

1080P

0.550443元/秒

无声视频

`audio=false`

720P

0.183481元/秒

1080P

0.275221元/秒

wan2.6-i2v

国际

有声视频

720P

0.733924元/秒

1080P

1.100886元/秒

wan2.5-i2v-preview

国际

有声视频

480P

0.366961元/秒

720P

0.733923元/秒

1080P

1.100885元/秒

wan2.2-i2v-flash

国际

无声视频

480P

0.110089元/秒

720P

0.264213元/秒

wan2.2-i2v-plus

国际

无声视频

480P

0.146785元/秒

1080P

0.733924元/秒

wan2.1-i2v-turbo

国际

无声视频

480P

0.264213元/秒

720P

0.264213元/秒

wan2.1-i2v-plus

国际

无声视频

720P

0.733924元/秒

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输出单价**

wan2.6-i2v

全球

有声视频

720P

0.6元/秒

1080P

1元/秒

### **万相-图生视频-基于首尾帧**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.2-kf2v-flash

中国内地

480P

0.10元/秒

50秒

720P

0.20元/秒

1080P

0.48元/秒

wanx2.1-kf2v-plus

中国内地

720P

0.70元/秒

200秒

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

wan2.1-kf2v-plus

国际

720P

0.733924元/秒

### **万相-参考生视频**

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

计费公式：计费时长 = 输入视频时长（上限 5 秒）+ 输出视频时长。

-   输入视频的计费时长不超过 **5 秒**，计算规则参见[计费与限流](https://help.aliyun.com/zh/model-studio/video-to-video-guide#6f5774ce5fqie)。
    
-   输出视频的计费时长为**成功生成的视频秒数**。
    

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输入和输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.7-r2v

中国内地

有声视频

720P

0.6元/秒

50秒

1080P

1元/秒

wan2.6-r2v-flash

中国内地

有声视频

`audio=true`

720P

0.3元/秒

50秒

1080P

0.5元/秒

无声视频

`audio=false`

720P

0.15元/秒

1080P

0.25元/秒

wan2.6-r2v

中国内地

有声视频

720P

0.6元/秒

50秒

1080P

1元/秒

#### 美国（弗吉尼亚）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输入和输出单价**

wan2.6-r2v

全球

有声视频

720P

0.6元/秒

1080P

1元/秒

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输入和输出单价**

wan2.7-r2v

国际

有声视频

720P

0.733924元/秒

1080P

1.100886元/秒

wan2.6-r2v-flash

国际

有声视频

`audio=true`

720P

0.366962元/秒

1080P

0.550443元/秒

无声视频

`audio=false`

720P

0.183481元/秒

1080P

0.275221元/秒

wan2.6-r2v

国际

有声视频

720P

0.733924元/秒

1080P

1.100886元/秒

#### 德国（法兰克福）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输入和输出单价**

wan2.6-r2v

全球

有声视频

720P

0.6元/秒

1080P

1元/秒

### **万相-视频编辑**

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输入和输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.7-videoedit

中国内地

720P

0.6元/秒

50秒

1080P

1元/秒

计费规则：输入不计费，输出视频计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wanx2.1-vace-plus

中国内地

720P

0.70元/秒

50秒

#### 新加坡

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输入和输出单价**

wan2.7-videoedit

国际

720P

0.733924元/秒

1080P

1.100886元/秒

计费规则：输入不计费，输出视频计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

wan2.1-vace-plus

国际

720P

0.733924元/秒

### **万相-数字人**

-   wan2.2-s2v-detect：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   wan2.2-s2v：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.2-s2v-detect

中国内地

输入图像：0.004元/张

200张

wan2.2-s2v

中国内地

输出视频：

-   480P：0.5元/秒
    
-   720P：0.9元/秒
    

100秒

### **万相-图生动作**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频模式**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.2-animate-move

中国内地

标准模式`wan-std`

0.4元/秒

50秒

有效期：阿里云百炼开通后90天内

专业模式`wan-pro`

0.6元/秒

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出视频模式**

**输出单价**

wan2.2-animate-move

国际

标准模式`wan-std`

0.880709元/秒

专业模式`wan-pro`

1.321063元/秒

### **万相-视频换人**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频模式**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.2-animate-mix

中国内地

标准模式`wan-std`

0.6元/秒

50秒

有效期：阿里云百炼开通后90天内

专业模式`wan-pro`

0.9元/秒

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输出视频模式**

**输出单价**

wan2.2-animate-mix

国际

标准模式`wan-std`

1.321063元/秒

专业模式`wan-pro`

1.908202元/秒

### **舞动人像AnimateAnyone**

-   animate-anyone-detect-gen2：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   animate-anyone-template-gen2：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    
-   animate-anyone-gen2：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

animate-anyone-detect-gen2

中国内地

输入图像：0.004元/张

200张

animate-anyone-template-gen2

中国内地

输出视频：0.08元/秒

1800秒（30分钟）

animate-anyone-gen2

中国内地

输出视频：0.08元/秒

1800秒（30分钟）

### **悦动人像EMO**

-   emo-detect-v1：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   emo-v1：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

emo-detect-v1

中国内地

输入图像：0.004元/张

200张

emo-v1

中国内地

输出视频：

-   1:1画幅视频：0.08元/秒
    
-   3:4画幅视频：0.16元/秒
    

1800秒（30分钟）

### **灵动人像LivePortrait**

-   liveportrait-detect：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   liveportrait：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

liveportrait-detect

中国内地

输入图像：0.004元/张

200张

liveportrait

中国内地

输出视频：0.02元/秒

1800秒（30分钟）

### **表情包Emoji**

-   emoji-detect-v1：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   emoji-v1：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

emoji-detect-v1

中国内地

输入图像：0.004元/张

200张

emoji-v1

中国内地

输出视频：0.08元/秒

1800秒（30分钟）

### **声动人像VideoRetalk**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

videoretalk

中国内地

0.08元/秒

1800秒（30分钟）

### **视频风格重绘**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

video-style-transform

中国内地

540P

0.2元/秒

600秒

720P

0.5元/秒

## **视频生成-第三方模型**

**爱诗-文生视频**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输出单价**

**免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

pixverse/pixverse-c1-t2v

中国内地

有声视频

`audio=true`

360P

0.24元/秒

无免费额度

540P

0.3元/秒

720P

0.39元/秒

1080P

0.71元/秒

无声视频

`audio=false`

360P

0.18元/秒

540P

0.24元/秒

720P

0.3元/秒

1080P

0.56元/秒

pixverse/pixverse-v6-t2v

中国内地

有声视频

`audio=true`

360P

0.21元/秒

无免费额度

540P

0.27元/秒

720P

0.36元/秒

1080P

0.68元/秒

无声视频

`audio=false`

360P

0.15元/秒

540P

0.21元/秒

720P

0.27元/秒

1080P

0.53元/秒

pixverse/pixverse-v5.6-t2v

中国内地

有声视频

`audio=true`

360P

0.47元/秒

无免费额度

540P

0.47元/秒

720P

0.53元/秒

1080P

0.7元/秒

无声视频

`audio=false`

360P

0.21元/秒

540P

0.21元/秒

720P

0.27元/秒

1080P

0.44元/秒

pixverse/pixverse-v5.6-it2v

中国内地

有声视频

`audio=true`

360P

0.47元/秒

无免费额度

540P

0.47元/秒

720P

0.53元/秒

1080P

0.7元/秒

无声视频

`audio=false`

360P

0.21元/秒

540P

0.21元/秒

720P

0.27元/秒

1080P

0.44元/秒

**爱诗-图生视频-基于首帧**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输出单价**

**免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

pixverse/pixverse-c1-it2v

中国内地

有声视频

`audio=true`

360P

0.24元/秒

无免费额度

540P

0.3元/秒

720P

0.39元/秒

1080P

0.71元/秒

无声视频

`audio=false`

360P

0.18元/秒

540P

0.24元/秒

720P

0.3元/秒

1080P

0.56元/秒

pixverse/pixverse-v6-it2v

中国内地

有声视频

`audio=true`

360P

0.21元/秒

无免费额度

540P

0.27元/秒

720P

0.36元/秒

1080P

0.68元/秒

无声视频

`audio=false`

360P

0.15元/秒

540P

0.21元/秒

720P

0.27元/秒

1080P

0.53元/秒

pixverse/pixverse-v5.6-it2v

中国内地

有声视频

`audio=true`

360P

0.47元/秒

无免费额度

540P

0.47元/秒

720P

0.53元/秒

1080P

0.7元/秒

无声视频

`audio=false`

360P

0.21元/秒

540P

0.21元/秒

720P

0.27元/秒

1080P

0.44元/秒

**爱诗-图生视频-基于首尾帧**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输出单价**

**免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

pixverse/pixverse-c1-kf2v

中国内地

有声视频

`audio=true`

360P

0.24元/秒

无免费额度

540P

0.3元/秒

720P

0.39元/秒

1080P

0.71元/秒

无声视频

`audio=false`

360P

0.18元/秒

540P

0.24元/秒

720P

0.3元/秒

1080P

0.56元/秒

pixverse/pixverse-v6-kf2v

中国内地

有声视频

`audio=true`

360P

0.21元/秒

无免费额度

540P

0.27元/秒

720P

0.36元/秒

1080P

0.68元/秒

无声视频

`audio=false`

360P

0.15元/秒

540P

0.21元/秒

720P

0.27元/秒

1080P

0.53元/秒

pixverse/pixverse-v5.6-kf2v

中国内地

有声视频

`audio=true`

360P

0.47元/秒

无免费额度

540P

0.47元/秒

720P

0.53元/秒

1080P

0.7元/秒

无声视频

`audio=false`

360P

0.21元/秒

540P

0.21元/秒

720P

0.27元/秒

1080P

0.44元/秒

**爱诗-参考生视频**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输出单价**

**免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

pixverse/pixverse-c1-r2v

中国内地

有声视频

`audio=true`

360P

0.24元/秒

无免费额度

540P

0.3元/秒

720P

0.39元/秒

1080P

0.71元/秒

无声视频

`audio=false`

360P

0.18元/秒

540P

0.24元/秒

720P

0.3元/秒

1080P

0.56元/秒

pixverse/pixverse-v5.6-r2v

中国内地

有声视频

`audio=true`

360P

0.47元/秒

无免费额度

540P

0.47元/秒

720P

0.53元/秒

1080P

0.7元/秒

无声视频

`audio=false`

360P

0.21元/秒

540P

0.21元/秒

720P

0.27元/秒

1080P

0.44元/秒

**可灵-视频生成**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频类型**

**输出视频分辨率**

**输出单价**

**免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

kling/kling-v3-video-generation

中国内地

无声视频

720P

0.6元/秒

无免费额度

1080P

0.8元/秒

有声视频

720P

0.9元/秒

1080P

1.2元/秒

kling/kling-v3-omni-video-generation

中国内地

无声视频（无参考视频）

720P

0.6元/秒

无免费额度

1080P

0.8元/秒

无声视频（有参考视频）

720P

0.9元/秒

1080P

1.2元/秒

有声视频（无参考视频）

720P

0.9元/秒

1080P

1.2元/秒

**Vidu-文生视频**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

**免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

vidu/viduq3-pro\_text2video

中国内地

540P

0.3125元/秒

无免费额度

720P

0.78125元/秒

1080P

0.9375元/秒

vidu/viduq3-turbo\_text2video

中国内地

540P

0.25元/秒

无免费额度

720P

0.375元/秒

1080P

0.4375元/秒

vidu/viduq2\_text2video

中国内地

540P

0.1125元/秒

无免费额度

720P

0.21875元/秒

1080P

0.375元/秒

**Vidu-图生视频-基于首帧**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

**免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

vidu/viduq3-pro\_img2video

中国内地

540P

0.3125元/秒

无免费额度

720P

0.78125元/秒

1080P

0.9375元/秒

vidu/viduq3-turbo\_img2video

中国内地

540P

0.25元/秒

无免费额度

720P

0.375元/秒

1080P

0.4375元/秒

vidu/viduq2-pro\_img2video

中国内地

540P

0.15625元/秒

无免费额度

720P

0.34375元/秒

1080P

0.71875元/秒

vidu/viduq2-turbo\_img2video

中国内地

540P

0.0875元/秒

无免费额度

720P

0.25元/秒

1080P

0.46875元/秒

vidu/viduq2-pro-fast\_img2video

中国内地

720P

0.1元/秒

无免费额度

1080P

0.2元/秒

**Vidu-图生视频-基于首尾帧**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

**免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

vidu/viduq3-pro\_start-end2video

中国内地

540P

0.3125元/秒

无免费额度

720P

0.78125元/秒

1080P

0.9375元/秒

vidu/viduq3-turbo\_start-end2video

中国内地

540P

0.25元/秒

无免费额度

720P

0.375元/秒

1080P

0.4375元/秒

vidu/viduq2-pro\_start-end2video

中国内地

540P

0.15625元/秒

无免费额度

720P

0.34375元/秒

1080P

0.71875元/秒

vidu/viduq2-turbo\_start-end2video

中国内地

540P

0.0875元/秒

无免费额度

720P

0.25元/秒

1080P

0.46875元/秒

**Vidu-参考生视频**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输出视频分辨率**

**输出单价**

**免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

vidu/viduq3-mix\_reference2video

中国内地

720P

0.78125元/秒

无免费额度

1080P

0.9375元/秒

vidu/viduq3\_reference2video

中国内地

540P

0.3125元/秒

无免费额度

720P

0.625元/秒

1080P

0.78125元/秒

vidu/viduq3-turbo\_reference2video

中国内地

540P

0.15625元/秒

无免费额度

720P

0.3125元/秒

1080P

0.40625元/秒

vidu/viduq2-pro\_reference2video

中国内地

540P

0.25元/秒

无免费额度

720P

0.3125元/秒

1080P

0.78125元/秒

vidu/viduq2\_reference2video

中国内地

540P

0.21875元/秒

无免费额度

720P

0.28125元/秒

1080P

0.71875元/秒

## **3D模型生成-第三方模型**

**Tripo-3D模型生成**

计费规则：输入不计费，输出按次数计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**3D任务类型**

**输出规格**

**输出单价**

Tripo/Tripo-H3.1

中国内地

文生3D

标准版+无贴图

0.7元/次

标准版+带标清贴图

1.4元/次

标准版+带高清贴图

2.1元/次

超清版+无贴图

2.1元/次

超清版+带标清贴图

2.8元/次

超清版+带高清贴图

3.5元/次

单图生3D/多图生3D

标准版+无贴图

1.4元/次

标准版+带标清贴图

2.1元/次

标准版+带高清贴图

2.8元/次

超清版+无贴图

2.8元/次

超清版+带标清贴图

3.5元/次

超清版+带高清贴图

4.2元/次

Tripo/Tripo-P1.0

中国内地

文生3D

无贴图

2.1元/次

带标清贴图

2.8元/次

带高清贴图

3.5元/次

单图生3D/多图生3D

无贴图

2.8元/次

带标清贴图

3.5元/次

带高清贴图

4.2元/次

## **文本向量**

计费规则：按输入Token计费，输出不计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

text-embedding-v4

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

中国内地

0.5元

100万Token

text-embedding-v3

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

中国内地

0.5元

50万Token

text-embedding-v2

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

中国内地

0.7元

50万Token

text-embedding-v1

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

中国内地

0.7元

50万Token

text-embedding-async-v2

中国内地

0.7元

2000万Token

text-embedding-async-v1

中国内地

0.7元

2000万Token

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

text-embedding-v4

国际

0.514元

text-embedding-v3

国际

0.514元

## **多模态向量**

计费规则：按输入Token计费，输出不计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

**文本**

**图片/视频**

qwen3-vl-embedding

中国内地

0.7元

1.8元

100万Token

qwen2.5-vl-embedding

中国内地

100万Token

tongyi-embedding-vision-plus

中国内地

0.5元

0.5元

100万Token

tongyi-embedding-vision-flash

中国内地

0.15元

0.15元

100万Token

multimodal-embedding-v1

中国内地

0.7元

0.9元

100万Token

## **文本排序**

### **文本排序模型**

计费规则：按输入Token计费，输出不计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen3-vl-rerank

中国内地

文本输入：0.7元

图片输入：1.8元

100万Token

qwen3-rerank

中国内地

文本输入：0.5元

100万Token

gte-rerank-v2

中国内地

文本输入：0.8元

100万Token

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

qwen3-rerank

国际

0.74942元

## **行业模型**

### **通义法睿**

计费规则：按输入Token和输出Token计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

farui-plus

中国内地

20元

20元

无免费额度

### **意图理解**

计费规则：按输入Token和输出Token计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

tongyi-intent-detect-v3

中国内地

0.4元

1元

100万Token

### **角色扮演**

计费规则：按输入Token和输出Token计费。

**说明**

以下模型仅在中国内地服务部署范围下有免费额度，其他服务部署范围下均无免费额度。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

qwen-plus-character

> [Session Cache](https://help.aliyun.com/zh/model-studio/role-play#6034f997cde74)享有折扣

中国内地

0.8元

2元

100万Token

qwen-flash-character

> [Session Cache](https://help.aliyun.com/zh/model-studio/role-play#6034f997cde74)享有折扣

中国内地

0.25元

1.5元

100万Token

qwen-flash-character-2026-02-26

> [Session Cache](https://help.aliyun.com/zh/model-studio/role-play#6034f997cde74)享有折扣

中国内地

0.18元

1.5元

100万Token

#### 新加坡

**模型 ID（Model ID）**

**服务部署范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen-plus-character

> [Session Cache](https://help.aliyun.com/zh/model-studio/role-play#6034f997cde74)享有折扣

国际

3.747元

10.492元

qwen-flash-character

> [Session Cache](https://help.aliyun.com/zh/model-studio/role-play#6034f997cde74)享有折扣

国际

0.375元

2.998元

qwen-plus-character-ja

国际

3.67元

10.275元

### **界面交互**

计费规则：按输入Token和输出Token计费。

#### 华北2（北京）

**模型 ID（Model ID）**

**服务部署范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

gui-plus

中国内地

1.5元

4.5元

100万Token

gui-plus-2026-02-26

中国内地

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
