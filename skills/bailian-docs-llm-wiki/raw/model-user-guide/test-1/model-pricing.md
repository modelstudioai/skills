# 模型调用价格

## **阶梯计费规则**

百炼部分模型实行阶梯计费。单价取决于单次请求的输入 Token 总量。该请求的所有 Token 均按对应阶梯的单价结算。

例如，某模型设有两档计费区间：0 < Token ≤ 32K 和 32K < Token ≤ 128K。若输入 100K Token，因数值落在第二区间（32K < 100K ≤ 128K），所有 Token 均按第二档单价结算。

## **文本生成-千问**

### **千问Max**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费；若模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，仅输入Token享有折扣。两者不能同时生效。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3.7-max

> 当前能力等同于qwen3.7-max-2026-05-20

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

非思考和思考模式

0<Token≤1M

12元

36元

各100万Token

有效期：阿里云百炼开通后90天内

qwen3.7-max-2026-05-20

非思考和思考模式

0<Token≤1M

12元

36元

qwen3.7-max-preview

> 当前能力等同于qwen3.7-2026-05-17

仅思考模式

0<Token≤1M

12元

36元

qwen3.7-2026-05-17

仅思考模式

0<Token≤1M

12元

36元

qwen3.6-max-preview

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

非思考和思考模式

0<Token≤128K

9元

54元

128K<Token≤256K

15元

90元

qwen3-max

> 当前能力等同于qwen3-max-2026-01-23

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

非思考和思考模式

0<Token≤32K

2.5元

10元

32K<Token≤128K

4元

16元

128K<Token≤256K

7元

28元

qwen3-max-2026-01-23

非思考和思考模式

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

##### **更多模型**

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-max

> 当前能力等同于qwen-max-2024-09-19

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

仅非思考模式

无阶梯计价

2.4元

9.6元

各100万Token

有效期：阿里云百炼开通后90天内

qwen-max-latest

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

仅非思考模式

无阶梯计价

2.4元

9.6元

qwen-max-2025-01-25

仅非思考模式

无阶梯计价

2.4元

9.6元

qwen-max-2024-09-19

仅非思考模式

无阶梯计价

20元

60元

qwen-max-2024-04-28

仅非思考模式

无阶梯计价

40元

120元

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3.7-max

> 当前能力等同于qwen3.7-max-2026-05-20

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

非思考和思考模式

0<Token≤1M

12元

36元

qwen3.7-max-2026-05-20

非思考和思考模式

0<Token≤1M

12元

36元

qwen3-max

> 当前能力等同于qwen3-max-2026-01-23

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

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

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3.7-max

> 当前能力等同于qwen3.7-max-2026-05-20

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

非思考和思考模式

0<Token≤1M

18.736元

56.207元

qwen3.7-max-2026-05-20

非思考和思考模式

0<Token≤1M

18.736元

56.207元

qwen3.6-max-preview

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

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

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen-max

> 当前能力等同于qwen-max-2025-01-25

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

仅非思考模式

无阶梯计价

11.743元

46.971元

qwen-max-latest

仅非思考模式

无阶梯计价

11.743元

46.971元

qwen-max-2025-01-25

仅非思考模式

无阶梯计价

11.743元

46.971元

## 欧盟

服务部署范围为[欧盟](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于欧盟境内；静态数据存储于您所选的地域。该部署范围支持的地域：德国（法兰克福）。

**说明**

欧盟部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3-max

> 当前能力等同于qwen3-max-2026-01-23

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

### **千问Plus**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

**非思考模式**

**思考模式（思维链+回答）**

qwen3.6-plus

> 当前能力等同于qwen3.6-plus-2026-04-02

0<Token≤256K

2元

12元

12元

各100万Token

有效期：阿里云百炼开通后90天内

256K<Token≤1M

8元

48元

48元

qwen3.6-plus-2026-04-02

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

qwen3.5-plus-2026-04-20

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

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

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

qwen-plus-latest

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

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

qwen-plus-2025-09-11

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

qwen-plus-2025-07-14

无阶梯计价

0.8元

2元

8元

qwen-plus-2025-04-28

无阶梯计价

0.8元

2元

8元

##### **更多模型**

**模型 ID（Model ID）**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-plus-2025-01-25

无阶梯计价

0.8元

2元

各100万Token

有效期：阿里云百炼开通后90天内

qwen-plus-2025-01-12

无阶梯计价

0.8元

2元

qwen-plus-2024-12-20

无阶梯计价

0.8元

2元

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**单次请求的输入Token范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.6-plus

> 当前能力等同于qwen3.6-plus-2026-04-02

0<Token≤256K

2元

12元

12元

256K<Token≤1M

8元

48元

48元

qwen3.6-plus-2026-04-02

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

qwen-plus-2025-09-11

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

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**单次请求的输入Token范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.6-plus

> 当前能力等同于qwen3.6-plus-2026-04-02

0<Token≤256K

3.7471元

22.4826元

22.4826元

256K<Token≤1M

14.9884元

44.965元

44.965元

qwen3.6-plus-2026-04-02

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

0<Token≤256K

2.936元

17.614元

17.614元

256K<Token≤1M

3.67元

22.018元

22.018元

qwen3.5-plus-2026-04-20

0<Token≤256K

2.936元

17.614元

17.614元

256K<Token≤1M

3.67元

22.018元

22.018元

qwen3.5-plus-2026-02-15

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

0<Token≤256K

2.936元

8.807元

29.357元

256K<Token≤1M

8.807元

26.421元

88.071元

qwen-plus-latest

0<Token≤256K

2.936元

8.807元

29.357元

256K<Token≤1M

8.807元

26.421元

88.071元

qwen-plus-2025-12-01

0<Token≤256K

2.936元

8.807元

29.357元

256K<Token≤1M

8.807元

26.421元

88.071元

qwen-plus-2025-09-11

0<Token≤256K

2.936元

8.807元

29.357元

256K<Token≤1M

8.807元

26.421元

88.071元

qwen-plus-2025-07-28

0<Token≤256K

2.936元

8.807元

29.357元

256K<Token≤1M

8.807元

26.421元

88.071元

qwen-plus-2025-07-14

无阶梯计价

2.936元

8.807元

29.357元

qwen-plus-2025-04-28

无阶梯计价

2.936元

8.807元

29.357元

##### **更多模型**

**模型 ID（Model ID）**

**单次请求的输入Token范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen-plus-2025-01-25

无阶梯计价

2.936元

8.807元

## 美国

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于美国境内；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）。

**说明**

美国部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**单次请求的输入Token范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen-plus-us

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

0<Token≤256K

2.936元

8.807元

29.357元

256K<Token≤1M

8.807元

26.421元

88.071元

qwen-plus-2025-12-01-us

0<Token≤256K

2.936元

8.807元

29.357元

256K<Token≤1M

8.807元

26.421元

88.071元

## 欧盟

服务部署范围为[欧盟](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于欧盟境内；静态数据存储于您所选的地域。该部署范围支持的地域：德国（法兰克福）。

**说明**

欧盟部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**单次请求的输入Token范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen-plus

> 当前能力等同于qwen-plus-2025-12-01

0<Token≤256K

2.998元

8.993元

29.977元

256K<Token≤1M

8.993元

26.979元

89.93元

qwen-plus-2025-12-01

0<Token≤256K

2.998元

8.993元

29.977元

256K<Token≤1M

8.993元

26.979元

89.93元

### **千问Flash**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费；若模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，仅输入Token享有折扣。两者不能同时生效。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3.6-flash

> 当前能力等同于qwen3.6-flash-2026-04-16

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

非思考和思考模式

0<Token≤256K

1.2元

7.2元

各100万Token

有效期：阿里云百炼开通后90天内

256K<Token≤1M

4.8元

28.8元

qwen3.6-flash-2026-04-16

非思考和思考模式

0<Token≤256K

1.2元

7.2元

256K<Token≤1M

4.8元

28.8元

qwen3.5-flash

> 当前能力等同于qwen3.5-flash-2026-02-23

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

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

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3.6-flash

> 当前能力等同于qwen3.6-flash-2026-04-16

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

非思考和思考模式

0<Token≤256K

1.2元

7.2元

256K<Token≤1M

4.8元

28.8元

qwen3.6-flash-2026-04-16

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

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3.6-flash

> 当前能力等同于qwen3.6-flash-2026-04-16

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

非思考和思考模式

0<Token≤256K

1.87355元

11.2413元

256K<Token≤1M

7.4942元

29.9758元

qwen3.6-flash-2026-04-16

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

非思考和思考模式

0<Token≤1M

0.734元

2.936元

qwen3.5-flash-2026-02-23

非思考和思考模式

0<Token≤1M

0.734元

2.936元

qwen-flash

> 当前能力等同于qwen-flash-2025-07-28

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

非思考和思考模式

0<Token≤256K

0.367元

2.936元

256K<Token≤1M

1.835元

14.678元

qwen-flash-2025-07-28

非思考和思考模式

0<Token≤256K

0.367元

2.936元

256K<Token≤1M

1.835元

14.678元

## 美国

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于美国境内；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）。

**说明**

美国部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**单次请求的输入Token范围**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen-flash-us

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

0<Token≤256K

0.367元

2.936元

256K<Token≤1M

1.835元

14.678元

qwen-flash-2025-07-28-us

0<Token≤256K

0.367元

2.936元

256K<Token≤1M

1.835元

14.678元

## 欧盟

服务部署范围为[欧盟](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于欧盟境内；静态数据存储于您所选的地域。该部署范围支持的地域：德国（法兰克福）。

**说明**

欧盟部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3.5-flash

> 当前能力等同于qwen3.5-flash-2026-02-23

非思考和思考模式

0.749元

2.998元

qwen3.5-flash-2026-02-23

非思考和思考模式

0.749元

2.998元

### **千问Turbo**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

**非思考模式**

**思考模式（思维链+回答）**

qwen-turbo

> 当前能力等同于qwen-turbo-2025-04-28

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

非思考和思考模式

0.3元

0.6元

3元

各100万Token

有效期：阿里云百炼开通后90天内

qwen-turbo-latest

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

非思考和思考模式

0.3元

0.6元

3元

qwen-turbo-2025-07-15

非思考和思考模式

0.3元

0.6元

3元

qwen-turbo-2025-04-28

非思考和思考模式

0.3元

0.6元

3元

##### **更多模型**

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：百炼开通后90天内

qwen-turbo-2025-02-11

0.3元

0.6元

100万Token

qwen-turbo-2024-11-01

0.3元

0.6元

1000万Token

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**模式**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen-turbo

> 当前能力等同于qwen-turbo-2025-04-28

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

非思考和思考

0.367元

1.468元

3.67元

qwen-turbo-latest

非思考和思考

0.367元

1.468元

3.67元

qwen-turbo-2025-04-28

非思考和思考

0.367元

1.468元

3.67元

##### 更多模型

**模型 ID（Model ID）**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen-turbo-2024-11-01

0.367元

1.468元

### **QwQ**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwq-plus

> 当前能力等同于qwq-plus-2025-03-05

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

仅思考模式

1.6元

4元

各100万Token

有效期：阿里云百炼开通后90天内

qwq-plus-latest

仅思考模式

1.6元

4元

qwq-plus-2025-03-05

仅思考模式

1.6元

4元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**模式**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwq-plus

> 当前能力等同于qwq-plus-2025-03-05

仅思考模式

5.871元

17.614元

### 千问Long

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-long

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

0.5元

2元

各100万Token

有效期：阿里云百炼开通后90天内

qwen-long-latest

0.5元

2元

qwen-long-2025-01-25

0.5元

2元

### **千问Omni**

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费与限流](https://help.aliyun.com/zh/model-studio/qwen-omni#12db7427b94qt)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

**文本/图片/视频**

**音频**

**文本**

> 多模态输入

**文本+音频**

> 仅音频计费

qwen3.5-omni-plus

> 当前能力等同于qwen3.5-omni-plus-2026-03-15

7元

53元

40元

213元

各100万Token

有效期：阿里云百炼开通后90天内

qwen3.5-omni-plus-2026-03-15

7元

53元

40元

213元

qwen3.5-omni-flash

> 当前能力等同于qwen3.5-omni-flash-2026-03-15

2.2元

18元

13.3元

72元

qwen3.5-omni-flash-2026-03-15

2.2元

18元

13.3元

72元

##### 更多模型

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

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

非思考和思考模式

1.8元

15.8元

3.3元

6.9元

12.7元

62.6元

各100万Token

有效期：阿里云百炼开通后90天内

qwen3-omni-flash-2025-12-01

非思考和思考模式

1.8元

15.8元

3.3元

6.9元

12.7元

62.6元

qwen3-omni-flash-2025-09-15

非思考和思考模式

1.8元

15.8元

3.3元

6.9元

12.7元

62.6元

qwen-omni-turbo

> 当前能力等同于qwen-omni-turbo-2025-03-26

非思考模式

0.4元

25元

1.5元

1.6元

4.5元

50元

qwen-omni-turbo-latest

非思考模式

0.4元

25元

1.5元

1.6元

4.5元

50元

qwen-omni-turbo-2025-03-26

非思考模式

0.4元

25元

1.5元

1.6元

4.5元

50元

qwen-omni-turbo-2025-01-19

非思考模式

0.4元

25元

1.5元

1.6元

4.5元

50元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

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

10.49元

82.44元

62.2元

329.74元

qwen3.5-omni-plus-2026-03-15

10.49元

82.44元

62.2元

329.74元

qwen3.5-omni-flash

> 当前能力等同于qwen3.5-omni-flash-2026-03-15

3元

22.48元

16.49元

89.18元

qwen3.5-omni-flash-2026-03-15

3元

22.48元

16.49元

89.18元

##### 更多模型

**模型 ID（Model ID）**

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

非思考和思考模式

3.156元

27.962元

5.725元

12.183元

22.458元

110.896元

qwen3-omni-flash-2025-12-01

非思考和思考模式

3.156元

27.962元

5.725元

12.183元

22.458元

110.896元

qwen3-omni-flash-2025-09-15

非思考和思考模式

3.156元

27.962元

5.725元

12.183元

22.458元

110.896元

qwen-omni-turbo

> 当前能力等同于qwen-omni-turbo-2025-03-26

非思考模式

0.514元

32.586元

1.541元

1.982元

4.624元

65.246元

qwen-omni-turbo-latest

非思考模式

0.514元

32.586元

1.541元

1.982元

4.624元

65.246元

qwen-omni-turbo-2025-03-26

非思考模式

0.514元

32.586元

1.541元

1.982元

4.624元

65.246元

### **千问Omni-Realtime**

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费与限流](https://help.aliyun.com/zh/model-studio/realtime#dc0370c95d3ja)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

**文本/图片**

**音频**

**文本**

> 多模态输入

**文本+音频**

> 仅音频计费

qwen3.5-omni-plus-realtime

10元

80元

60元

300元

各100万Token

有效期：阿里云百炼开通后90天内

qwen3.5-omni-plus-realtime-2026-03-15

10元

80元

60元

300元

qwen3.5-omni-flash-realtime

3.3元

27元

20元

107元

qwen3.5-omni-flash-realtime-2026-03-15

3.3元

27元

20元

107元

##### 更多模型

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

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

2.2元

18.9元

3.9元

8.3元

15.2元

75.1元

各100万Token

有效期：阿里云百炼开通后90天内

qwen3-omni-flash-realtime-2025-12-01

2.2元

18.9元

3.9元

8.3元

15.2元

75.1元

qwen3-omni-flash-realtime-2025-09-15

2.2元

18.9元

3.9元

8.3元

15.2元

75.1元

qwen-omni-turbo-realtime

1.6元

25元

6元

6.4元

18元

50元

qwen-omni-turbo-realtime-latest

1.6元

25元

6元

6.4元

18元

50元

qwen-omni-turbo-realtime-2025-05-08

1.6元

25元

6元

6.4元

18元

50元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**文本/图片**

**音频**

**文本**

> 多模态输入

**文本+音频**

> 仅音频计费

qwen3.5-omni-plus-realtime

15.74元

123.65元

92.93元

464.64元

qwen3.5-omni-plus-realtime-2026-03-15

15.74元

123.65元

92.93元

464.64元

qwen3.5-omni-flash-realtime

4.12元

33.72元

24.73元

132.65元

qwen3.5-omni-flash-realtime-2026-03-15

4.12元

33.72元

24.73元

132.65元

##### 更多模型

**模型 ID（Model ID）**

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

3.816元

33.54元

6.899元

14.605元

26.935元

133.06元

qwen3-omni-flash-realtime-2025-12-01

3.816元

33.54元

6.899元

14.605元

26.935元

133.06元

qwen3-omni-flash-realtime-2025-09-15

3.816元

33.54元

6.899元

14.605元

26.935元

133.06元

qwen-omni-turbo-realtime

1.982元

32.586元

6.165元

7.853元

18.495元

65.246元

qwen-omni-turbo-realtime-latest

1.982元

32.586元

6.165元

7.853元

18.495元

65.246元

qwen-omni-turbo-realtime-2025-05-08

1.982元

32.586元

6.165元

7.853元

18.495元

65.246元

### **QVQ**

计费规则：按输入Token和输出Token计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qvq-max

> 当前能力等同于qvq-max-2025-03-25

8元

32元

各100万Token

有效期：阿里云百炼开通后90天内

qvq-max-latest

8元

32元

qvq-max-2025-05-15

8元

32元

qvq-max-2025-03-25

8元

32元

qvq-plus

> 当前能力等同于qvq-plus-2025-05-15

2元

5元

qvq-plus-latest

2元

5元

qvq-plus-2025-05-15

2元

5元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qvq-max

> 当前能力等同于qvq-max-2025-03-25

8.807元

35.228元

qvq-max-latest

8.807元

35.228元

qvq-max-2025-03-25

8.807元

35.228元

### 千问VL

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-vl-plus

> 当前能力等同于qwen3-vl-plus-2025-12-19

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

非思考和思考模式

0<Token≤32K

1元

10元

各100万Token

有效期：阿里云百炼开通后90天内

32K<Token≤128K

1.5元

15元

128K<Token≤256K

3元

30元

qwen3-vl-plus-2025-12-19

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

qwen3-vl-flash

> 当前能力等同于qwen3-vl-flash-2026-01-22

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

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

qwen3-vl-flash-2026-01-22

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

##### **更多模型**

**模型 ID（Model ID）**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-vl-max

> 当前能力等同于qwen-vl-max-2025-08-13

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

无阶梯计价

1.6元

4元

各100万Token

有效期：阿里云百炼开通后90天内

qwen-vl-max-latest

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

无阶梯计价

1.6元

4元

qwen-vl-max-2025-08-13

无阶梯计价

1.6元

4元

qwen-vl-max-2025-04-08

无阶梯计价

3元

9元

qwen-vl-max-2025-04-02

无阶梯计价

3元

9元

qwen-vl-max-2025-01-25

无阶梯计价

3元

9元

qwen-vl-max-2024-12-30

无阶梯计价

3元

9元

qwen-vl-max-2024-11-19

无阶梯计价

3元

9元

qwen-vl-plus

> 当前能力等同于qwen-vl-plus-2025-08-15

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

无阶梯计价

0.8元

2元

qwen-vl-plus-latest

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

无阶梯计价

0.8元

2元

qwen-vl-plus-2025-08-15

无阶梯计价

0.8元

2元

qwen-vl-plus-2025-07-10

无阶梯计价

0.15元

1.5元

qwen-vl-plus-2025-05-07

无阶梯计价

1.5元

4.5元

qwen-vl-plus-2025-01-25

无阶梯计价

1.5元

4.5元

qwen-vl-plus-2025-01-02

无阶梯计价

1.5元

4.5元

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3-vl-plus

> 当前能力等同于qwen3-vl-plus-2025-12-19

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

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

qwen3-vl-flash

> 当前能力等同于qwen3-vl-flash-2025-10-15

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

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

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen3-vl-plus

> 当前能力等同于qwen3-vl-plus-2025-12-19

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

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

**单次请求的输入Token数**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen-vl-max

> 当前能力等同于qwen-vl-max-2025-08-13

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

无阶梯计价

5.871元

23.486元

qwen-vl-max-latest

无阶梯计价

5.871元

23.486元

qwen-vl-max-2025-08-13

无阶梯计价

5.871元

23.486元

qwen-vl-max-2025-04-08

无阶梯计价

5.871元

23.486元

qwen-vl-plus

> 当前能力等同于qwen-vl-plus-2025-08-15

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

无阶梯计价

1.541元

4.624元

qwen-vl-plus-latest

无阶梯计价

1.541元

4.624元

qwen-vl-plus-2025-08-15

无阶梯计价

1.541元

4.624元

qwen-vl-plus-2025-05-07

无阶梯计价

1.541元

4.624元

qwen-vl-plus-2025-01-25

无阶梯计价

1.541元

4.624元

## 美国

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于美国境内；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）。

**说明**

美国部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3-vl-flash-us

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

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

qwen3-vl-flash-2025-10-15-us

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

## 欧盟

服务部署范围为[欧盟](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于欧盟境内；静态数据存储于您所选的地域。该部署范围支持的地域：德国（法兰克福）。

**说明**

欧盟部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3-vl-plus

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

qwen3-vl-flash

> 当前能力等同于qwen3-vl-flash-2026-01-22

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

### 千问OCR

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-vl-ocr

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

0.3元

0.5元

各100万Token

有效期：阿里云百炼开通后90天内

qwen-vl-ocr-latest

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

0.3元

0.5元

qwen-vl-ocr-2025-11-20

0.3元

0.5元

qwen-vl-ocr-2025-08-28

5元

5元

qwen-vl-ocr-2025-04-13

5元

5元

qwen-vl-ocr-2024-10-28

5元

5元

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen-vl-ocr

0.3元

0.5元

qwen-vl-ocr-2025-11-20

0.3元

0.5元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen-vl-ocr

0.514元

1.174元

qwen-vl-ocr-2025-11-20

0.514元

1.174元

### 千问Audio

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

音频Token计算规则：每一秒钟的音频对应25个Token。若音频时长不足1秒，则按25个Token计算。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-audio-turbo

目前仅供免费体验。

> 免费额度用完后不可调用，推荐使用[全模态（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)作为替代模型

各10万Token

有效期：阿里云百炼开通后90天内

qwen-audio-turbo-latest

### 千问数学模型

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-math-plus

4元

12元

各100万Token

有效期：阿里云百炼开通后90天内

qwen-math-turbo

2元

6元

### 千问Coder

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，仅输入Token享有折扣。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-coder-plus

> 当前能力等同于qwen3-coder-plus-2025-09-23

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

0<Token≤32K

4元

16元

各100万Token

有效期：阿里云百炼开通后90天内

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

##### **更多模型**

**模型 ID（Model ID）**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-coder-plus

> 当前能力等同于qwen-coder-plus-2024-11-06

无阶梯计价

3.5元

7元

各100万Token

有效期：阿里云百炼开通后90天内

qwen-coder-plus-latest

无阶梯计价

3.5元

7元

qwen-coder-plus-2024-11-06

无阶梯计价

3.5元

7元

qwen-coder-turbo

> 当前能力等同于qwen-coder-turbo-2024-09-19

无阶梯计价

2元

6元

qwen-coder-turbo-latest

无阶梯计价

2元

6元

qwen-coder-turbo-2024-09-19

无阶梯计价

2元

6元

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**单次请求的输入Token数**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen3-coder-plus

> 当前能力等同于qwen3-coder-plus-2025-09-23

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

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际（新加坡）模型无免费额度。

**模型 ID（Model ID）**

**单次请求的输入Token数**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen3-coder-plus

> 当前能力等同于qwen3-coder-plus-2025-09-23

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

### **千问翻译模型**

计费规则：按输入Token和输出Token计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-mt-plus

1.8元

5.4元

各100万Token

有效期：阿里云百炼开通后90天内

qwen-mt-flash

0.7元

1.95元

qwen-mt-lite

0.6元

1.6元

qwen-mt-turbo

0.7元

1.95元

## **全球**

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen-mt-plus

1.8元

5.4元

qwen-mt-flash

0.7元

1.95元

qwen-mt-lite

0.6元

1.6元

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际（新加坡）模型无免费额度。

**模型 ID（Model ID）**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen-mt-plus

18.055元

54.09元

qwen-mt-flash

1.174元

3.596元

qwen-mt-lite

0.881元

2.642元

qwen-mt-turbo

1.174元

3.596元

## 美国

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于美国境内；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）。

**说明**

美国部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen-mt-lite-us

0.881元

2.642元

### 千问数据挖掘模型

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-doc-turbo

0.6元

1元

无免费额度

### **千问深入研究模型**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-deep-research

54元

163元

无免费额度

### **通义晓蜜对话分析模型**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

tongyi-xiaomi-analysis-flash

0.2元

0.4元

各100万Token

有效期：百炼开通后90天内

tongyi-xiaomi-analysis-pro

1.0元

2.7元

## **文本生成-千问-开源版**

### **Qwen3.6**

计费规则：按输入Token和输出Token计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

**非思考模式**

**思考模式（思维链+回答）**

qwen3.6-35b-a3b

0<Token≤256K

1.8元

10.8元

10.8元

各100万Token

有效期：阿里云百炼开通后90天内

qwen3.6-27b

0<Token≤256K

3元

18元

18元

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型 ID（Model ID）**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.6-35b-a3b

0<Token≤256K

1.8元

10.8元

10.8元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型 ID（Model ID）**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.6-35b-a3b

0<Token≤256K

2.810325元

16.86195元

16.86195元

qwen3.6-27b

0<Token≤256K

4.49652元

26.97912元

26.97912元

### **Qwen3.5**

计费规则：按输入Token和输出Token计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

**非思考模式**

**思考模式（思维链+回答）**

qwen3.5-397b-a17b

0<Token≤128K

1.2元

7.2元

7.2元

各100万Token

有效期：阿里云百炼开通后90天内

128K<Token≤256K

3元

18元

18元

qwen3.5-122b-a10b

0<Token≤128K

0.8元

6.4元

6.4元

128K<Token≤256K

2元

16元

16元

qwen3.5-27b

0<Token≤128K

0.6元

4.8元

4.8元

128K<Token≤256K

1.8元

14.4元

14.4元

qwen3.5-35b-a3b

0<Token≤128K

0.4元

3.2元

3.2元

128K<Token≤256K

1.6元

12.8元

12.8元

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型 ID（Model ID）**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.5-397b-a17b

0<Token≤128K

1.2元

7.2元

7.2元

128K<Token≤256K

3元

18元

18元

qwen3.5-122b-a10b

0<Token≤128K

0.8元

6.4元

6.4元

128K<Token≤256K

2元

16元

16元

qwen3.5-27b

0<Token≤128K

0.6元

4.8元

4.8元

128K<Token≤256K

1.8元

14.4元

14.4元

qwen3.5-35b-a3b

0<Token≤128K

0.4元

3.2元

3.2元

128K<Token≤256K

1.6元

12.8元

12.8元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型 ID（Model ID）**

**单次请求的输入Token范围**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**非思考模式**

**思考模式（思维链+回答）**

qwen3.5-397b-a17b

0<Token≤256K

4.404元

26.421元

26.421元

qwen3.5-122b-a10b

0<Token≤256K

2.936元

23.486元

23.486元

qwen3.5-27b

0<Token≤256K

2.202元

17.614元

17.614元

qwen3.5-35b-a3b

0<Token≤256K

1.835元

14.678元

14.678元

### **Qwen3**

计费规则：按输入Token和输出Token计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

**非思考模式**

**思考模式（思维链+回答）**

qwen3-next-80b-a3b-thinking

仅思考模式

1元

\-

10元

各100万Token

有效期：阿里云百炼开通后90天内

qwen3-next-80b-a3b-instruct

仅非思考模式

1元

4元

\-

qwen3-235b-a22b-thinking-2507

仅思考模式

2元

\-

20元

qwen3-235b-a22b-instruct-2507

仅非思考模式

2元

8元

\-

qwen3-30b-a3b-thinking-2507

仅思考模式

0.75元

\-

7.5元

qwen3-30b-a3b-instruct-2507

仅非思考模式

0.75元

3元

\-

qwen3-235b-a22b

非思考和思考模式

2元

8元

20元

qwen3-32b

非思考和思考模式

2元

8元

20元

qwen3-30b-a3b

非思考和思考模式

0.75元

3元

7.5元

qwen3-14b

非思考和思考模式

1元

4元

10元

qwen3-8b

非思考和思考模式

0.5元

2元

5元

qwen3-4b

非思考和思考模式

0.3元

1.2元

3元

qwen3-1.7b

非思考和思考模式

0.3元

1.2元

3元

qwen3-0.6b

非思考和思考模式

0.3元

1.2元

3元

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

**非思考模式**

**思考模式（思维链+回答）**

qwen3-next-80b-a3b-thinking

仅思考模式

1元

\-

10元

无免费额度

qwen3-next-80b-a3b-instruct

仅非思考模式

1元

4元

\-

qwen3-235b-a22b-thinking-2507

仅思考模式

1.688元

\-

16.88元

qwen3-235b-a22b-instruct-2507

仅非思考模式

1.688元

6.752元

\-

qwen3-30b-a3b-thinking-2507

仅思考模式

0.75元

\-

7.5元

qwen3-30b-a3b-instruct-2507

仅非思考模式

0.75元

3元

\-

qwen3-235b-a22b

非思考和思考模式

2元

8元

20元

qwen3-32b

非思考和思考模式

1.174元

4.697元

4.697元

qwen3-30b-a3b

非思考和思考模式

0.75元

3元

7.5元

qwen3-14b

非思考和思考模式

1元

4元

10元

qwen3-8b

非思考和思考模式

0.5元

2元

5元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

**非思考模式**

**思考模式（思维链+回答）**

qwen3-next-80b-a3b-thinking

仅思考模式

1.101元

\-

8.807元

无免费额度

qwen3-next-80b-a3b-instruct

仅非思考模式

1.101元

8.807元

\-

qwen3-235b-a22b-thinking-2507

仅思考模式

1.688元

\-

16.88元

qwen3-235b-a22b-instruct-2507

仅非思考模式

1.688元

6.752元

\-

qwen3-30b-a3b-thinking-2507

仅思考模式

1.468元

\-

17.614元

qwen3-30b-a3b-instruct-2507

仅非思考模式

1.468元

5.871元

\-

qwen3-235b-a22b

非思考和思考模式

5.137元

20.55元

61.65元

qwen3-32b

非思考和思考模式

1.174元

4.697元

4.697元

qwen3-30b-a3b

非思考和思考模式

1.468元

5.871元

17.614元

qwen3-14b

非思考和思考模式

2.569元

10.275元

30.825元

qwen3-8b

非思考和思考模式

1.321元

5.137元

15.412元

qwen3-4b

非思考和思考模式

0.807元

3.082元

9.247元

qwen3-1.7b

非思考和思考模式

0.807元

3.082元

9.247元

qwen3-0.6b

非思考和思考模式

0.807元

3.082元

9.247元

### **QwQ-开源版**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwq-32b

2元

6元

100万Token

有效期：阿里云百炼开通后90天内

### **QwQ-Preview**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwq-32b-preview

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

2元

6元

各100万Token

有效期：阿里云百炼开通后90天内

### **Qwen2.5**

计费规则：按输入Token和输出Token计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen2.5-14b-instruct-1m

1元

3元

各100万Token

有效期：阿里云百炼开通后90天内

qwen2.5-7b-instruct-1m

0.5元

1元

qwen2.5-72b-instruct

4元

12元

qwen2.5-32b-instruct

2元

6元

qwen2.5-14b-instruct

1元

3元

qwen2.5-7b-instruct

0.5元

1元

qwen2.5-3b-instruct

0.3元

0.9元

qwen2.5-1.5b-instruct

目前仅供免费体验

> 免费额度用完后不可调用，推荐使用[Qwen3](https://help.aliyun.com/zh/model-studio/deep-thinking)、[DeepSeek -阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)、[Kimi-阿里云](https://help.aliyun.com/zh/model-studio/kimi-api)作为替代模型

qwen2.5-0.5b-instruct

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际（新加坡）模型无免费额度。

**模型 ID（Model ID）**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen2.5-14b-instruct-1m

5.908元

23.632元

qwen2.5-7b-instruct-1m

2.701元

10.789元

qwen2.5-72b-instruct

10.275元

41.1元

qwen2.5-32b-instruct

5.137元

20.55元

qwen2.5-14b-instruct

2.569元

10.275元

qwen2.5-7b-instruct

1.284元

5.137元

### **QVQ**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qvq-72b-preview

12元

36元

10万Token

有效期：阿里云百炼开通后90天内

### **Qwen-Omni**

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费与限流](https://help.aliyun.com/zh/model-studio/qwen-omni#12db7427b94qt)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

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

0.6元

38元

2元

2.4元

6元

76元

100万Token（不区分模态）

有效期：阿里云百炼开通后90天

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际（新加坡）模型无免费额度。

**模型 ID（Model ID）**

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

0.734元

49.613元

2.055元

2.936元

6.165元

99.153元

### **Qwen3-Omni-Captioner**

计费规则：按输入Token和输出Token计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-omni-30b-a3b-captioner

15.8元

12.7元

100万Token

有效期：阿里云百炼开通后90天内

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际（新加坡）模型无免费额度。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen3-omni-30b-a3b-captioner

27.962元

22.458元

### **Qwen-VL**

计费规则：按输入Token和输出Token计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-vl-235b-a22b-thinking

仅思考模式

2元

20元

各100万 Token

有效期：阿里云百炼开通后90天内

qwen3-vl-235b-a22b-instruct

仅非思考模式

2元

8元

qwen3-vl-32b-thinking

仅思考模式

2元

20元

qwen3-vl-32b-instruct

仅非思考模式

2元

8元

qwen3-vl-30b-a3b-thinking

仅思考模式

0.75元

7.5元

qwen3-vl-30b-a3b-instruct

仅非思考模式

0.75元

3元

qwen3-vl-8b-thinking

仅思考模式

0.5元

5元

qwen3-vl-8b-instruct

仅非思考模式

0.5元

2元

##### **更多模型**

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen2.5-vl-72b-instruct

16元

48元

各100万 Token

有效期：阿里云百炼开通后90天内

qwen2.5-vl-32b-instruct

8元

24元

qwen2.5-vl-7b-instruct

2元

5元

qwen2.5-vl-3b-instruct

1.2元

3.6元

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3-vl-235b-a22b-thinking

仅思考模式

2元

20元

qwen3-vl-235b-a22b-instruct

仅非思考模式

2元

8元

qwen3-vl-32b-thinking

仅思考模式

1.174元

4.697元

qwen3-vl-32b-instruct

仅非思考模式

1.174元

4.697元

qwen3-vl-30b-a3b-thinking

仅思考模式

0.75元

7.5元

qwen3-vl-30b-a3b-instruct

仅非思考模式

0.75元

3元

qwen3-vl-8b-thinking

仅思考模式

0.5元

5元

qwen3-vl-8b-instruct

仅非思考模式

0.5元

2元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

qwen3-vl-235b-a22b-thinking

仅思考模式

2.936元

29.357元

qwen3-vl-235b-a22b-instruct

仅非思考模式

2.936元

11.743元

qwen3-vl-32b-thinking

仅思考模式

1.174元

4.697元

qwen3-vl-32b-instruct

仅非思考模式

1.174元

4.697元

qwen3-vl-30b-a3b-thinking

仅思考模式

1.468元

17.614元

qwen3-vl-30b-a3b-instruct

仅非思考模式

1.468元

5.871元

qwen3-vl-8b-thinking

仅思考模式

1.321元

15.412元

qwen3-vl-8b-instruct

仅非思考模式

1.321元

5.137元

##### **更多模型**

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen2.5-vl-72b-instruct

20.55元

61.65元

各100万 Token

有效期：阿里云百炼开通后90天内

qwen2.5-vl-32b-instruct

10.275元

30.825元

qwen2.5-vl-7b-instruct

2.569元

7.706元

qwen2.5-vl-3b-instruct

1.541元

4.624元

### **Qwen-Audio**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen2-audio-instruct

目前仅供免费体验。

> 免费额度用完后不可调用，推荐使用[全模态（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)作为替代模型。

各10万Token

有效期：阿里云百炼开通后90天内

qwen-audio-chat

### **Qwen-Math**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen2.5-math-72b-instruct

4元

12元

各100万Token

有效期：阿里云百炼开通后90天内

qwen2.5-math-7b-instruct

1元

2元

### **Qwen-Coder**

计费规则：按输入Token和输出Token计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-coder-next

0<Token≤32K

1元

4元

各100万Token

有效期：阿里云百炼开通后90天内

32K<Token≤128K

1.5元

6元

128K<Token≤256K

2.5元

10元

qwen3-coder-480b-a35b-instruct

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

0<Token≤32K

1.5元

6元

32K<Token≤128K

2.25元

9元

128K<Token≤200K

3.75元

15元

qwen2.5-coder-32b-instruct

无阶梯计价

2元

6元

qwen2.5-coder-14b-instruct

无阶梯计价

2元

6元

qwen2.5-coder-7b-instruct

无阶梯计价

1元

2元

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen3-coder-480b-a35b-instruct

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

0<Token≤32K

1.5元

6元

32K<Token≤128K

2.25元

9元

128K<Token≤200K

3.75元

15元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际（新加坡）模型无免费额度。

**模型 ID（Model ID）**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen3-coder-next

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

0<Token≤32K

3.303元

16.513元

32K<Token≤128K

5.504元

27.522元

128K<Token≤200K

8.807元

44.035元

## 欧盟

服务部署范围为[欧盟](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于欧盟境内；静态数据存储于您所选的地域。该部署范围支持的地域：德国（法兰克福）。

**说明**

欧盟部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

qwen3-coder-next

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

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

deepseek-v4-pro

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

12元

24元

各100万Token

有效期：阿里云百炼开通后90天内

deepseek-v4-flash

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

1元

2元

deepseek-v3.2

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

2元

3元

deepseek-v3.2-exp

2元

3元

deepseek-v3.1

4元

12元

deepseek-r1

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

4元

16元

deepseek-r1-0528

4元

16元

deepseek-v3

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

2元

8元

deepseek-r1-distill-qwen-1.5b

限时免费

deepseek-r1-distill-qwen-7b

0.5元

1元

各100万Token

有效期：阿里云百炼开通后90天内

deepseek-r1-distill-qwen-14b

1元

3元

deepseek-r1-distill-qwen-32b

2元

6元

deepseek-r1-distill-llama-8b

限时免费

deepseek-r1-distill-llama-70b

目前仅供免费体验

> 免费额度用完后不可调用，推荐使用[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)、[DeepSeek -阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)、[Kimi-阿里云](https://help.aliyun.com/zh/model-studio/kimi-api)作为替代模型

各100万Token

有效期：阿里云百炼开通后90天内

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

deepseek-v4-pro

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

12元

24元

deepseek-v4-flash

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

1元

2元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际（新加坡）模型无免费额度。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

deepseek-v4-pro

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

17.986元

35.972元

deepseek-v4-flash

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

1.499元

2.998元

deepseek-v3.2

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

4.272元

12.815元

### **DeepSeek-硅基流动**

**说明**

服务部署范围仅支持中国内地。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**

siliconflow/deepseek-v3.2

2元

3元

无

siliconflow/deepseek-v3.1-terminus

4元

12元

siliconflow/deepseek-r1-0528

4元

16元

siliconflow/deepseek-v3-0324

2元

8元

### **DeepSeek-快手万擎**

**说明**

服务部署范围仅支持中国内地。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链+回答**

**免费额度**

vanchin/deepseek-v3.2-think

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

2元

3元

无

vanchin/deepseek-v3.1-terminus

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

4元

12元

vanchin/deepseek-r1

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

4元

16元

vanchin/deepseek-v3

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

2元

8元

vanchin/deepseek-ocr

0.216元

0.216元

### **Kimi**

计费规则：按输入Token和输出Token计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

kimi-k2.6

非思考和思考模式

6.5元

27元

各100万Token

有效期：阿里云百炼开通后90天内

kimi-k2.5

非思考和思考模式

4元

21元

kimi-k2-thinking

仅思考模式

4元

16元

Moonshot-Kimi-K2-Instruct

非思考模式

4元

16元

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

kimi-k2.5

非思考和思考模式

4元

21元

无

### **Kimi-月之暗面**

**说明**

服务部署范围仅支持中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

kimi/kimi-k2.6

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

6.5元

27元

无

kimi/kimi-k2.5

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

4元

21元

### **GLM**

计费规则：按输入Token和输出Token计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

glm-5.1

非思考和思考模式

0<Token≤32K

6元

24元

各100万Token

有效期：阿里云百炼开通后90天内

32K<Token≤200K

8元

28元

glm-5

非思考和思考模式

0<Token≤32K

4元

18元

32K<Token≤198K

6元

22元

glm-4.7

非思考和思考模式

0<Token≤32K

3元

14元

32K<Token≤166K

4元

16元

glm-4.6

非思考和思考模式

0<Token≤32K

3元

14元

32K<Token≤166K

4元

16元

glm-4.5

非思考和思考模式

0<Token≤32K

3元

14元

32K<Token≤96K

4元

16元

glm-4.5-air

非思考和思考模式

0<Token≤32K

0.8元

6元

32K<Token≤96K

1.2元

8元

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**模型 ID（Model ID）**

**模式**

**单次请求的输入Token数**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

glm-5.1

非思考和思考模式

0<Token≤32K

6元

24元

无

32K<Token≤200K

8元

28元

### **GLM-智谱**

**说明**

服务部署范围仅支持中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

ZHIPU/GLM-5.1

非思考和思考模式

8元

28元

无

ZHIPU/GLM-5

非思考和思考模式

6元

22元

无

### MiniMax

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

MiniMax-M2.5

仅思考模式

2.1元

8.4元

各100万Token

有效期：阿里云百炼开通后90天内

MiniMax-M2.1

仅思考模式

2.1元

8.4元

### **MiniMax-稀宇科技**

**说明**

服务部署范围仅支持中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**模式**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

MiniMax/MiniMax-M2.7

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

仅思考模式

2.1元

8.4元

无

MiniMax/MiniMax-M2.5

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

仅思考模式

2.1元

8.4元

MiniMax/MiniMax-M2.1

> [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣

仅思考模式

2.1元

8.4元

### **MiMo-小米**

**说明**

服务部署范围仅支持中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入Token数量**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

> **思维链和回答**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

xiaomi/mimo-v2.5-pro

0<Token≤256K

7元

21元

无

256K<Token≤1M

14元

42元

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

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-image-2.0-pro

0.5元/张

各100张

有效期：阿里云百炼开通后90天内

qwen-image-2.0-pro-2026-04-22

0.5元/张

qwen-image-2.0-pro-2026-03-03

0.5元/张

qwen-image-2.0

0.2元/张

qwen-image-2.0-2026-03-03

0.2元/张

qwen-image-max

> 当前能力等同于qwen-image-max-2025-12-30

0.5元/张

qwen-image-max-2025-12-30

0.5元/张

qwen-image-plus

> 当前能力等同于qwen-image

0.2元/张

qwen-image-plus-2026-01-09

0.2元/张

qwen-image

0.25元/张

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出单价**

qwen-image-2.0-pro

0.550443元/张

qwen-image-2.0-pro-2026-04-22

0.550443元/张

qwen-image-2.0-pro-2026-03-03

0.550443元/张

qwen-image-2.0

0.256873元/张

qwen-image-2.0-2026-03-03

0.256873元/张

qwen-image-max

> 当前能力等同于qwen-image-max-2025-12-30

0.550443元/张

qwen-image-max-2025-12-30

0.550443元/张

qwen-image-plus

> 当前能力等同于qwen-image

0.220177元/张

qwen-image-plus-2026-01-09

0.220177元/张

qwen-image

0.256873元/张

### **千问图像编辑**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-image-2.0-pro

0.5元/张

各100张

有效期：阿里云百炼开通后90天内

qwen-image-2.0-pro-2026-04-22

0.5元/张

qwen-image-2.0-pro-2026-03-03

0.5元/张

qwen-image-2.0

0.2元/张

qwen-image-2.0-2026-03-03

0.2元/张

qwen-image-edit-max

> 当前能力等同于qwen-image-edit-max-2026-01-16

0.5元/张

qwen-image-edit-max-2026-01-16

0.5元/张

qwen-image-edit-plus

> 当前能力等同于qwen-image-edit-plus-2025-10-30

0.2元/张

qwen-image-edit-plus-2025-12-15

0.2元/张

qwen-image-edit-plus-2025-10-30

0.2元/张

qwen-image-edit

0.3元/张

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出单价**

qwen-image-2.0-pro

0.550443元/张

qwen-image-2.0-pro-2026-04-22

0.550443元/张

qwen-image-2.0-pro-2026-03-03

0.550443元/张

qwen-image-2.0

0.256873元/张

qwen-image-2.0-2026-03-03

0.256873元/张

qwen-image-edit-max

> 当前能力等同于qwen-image-edit-max-2026-01-16

0.550443元/张

qwen-image-edit-max-2026-01-16

0.550443元/张

qwen-image-edit-plus

> 当前能力等同于qwen-image-edit-plus-2025-10-30

0.220177元/张

qwen-image-edit-plus-2025-12-15

0.220177元/张

qwen-image-edit-plus-2025-10-30

0.220177元/张

qwen-image-edit

0.330266元/张

### **千问图像翻译**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-mt-image

0.003元/张

100张

有效期：阿里云百炼开通后90天内

### **Z-Image**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

z-image-turbo

关闭提示词改写（`prompt_extend=false`）：0.1元/张

开启提示词改写（`prompt_extend=true`）：0.2元/张

100张

有效期：阿里云百炼开通后90天内

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出单价**

z-image-turbo

关闭提示词改写（`prompt_extend=false`）：0.110089元/张

开启提示词改写（`prompt_extend=true`）：0.220177元/张

### **万相文生图**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

0

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.6-t2i

0.20元/张

50张

wan2.5-t2i-preview

0.20元/张

50张

wan2.2-t2i-plus

0.20元/张

100张

wan2.2-t2i-flash

0.14元/张

100张

wanx2.1-t2i-plus

0.20元/张

500张

wanx2.1-t2i-turbo

0.14元/张

500张

wanx2.0-t2i-turbo

0.04元/张

500张

wanx-v1

0.16元/张

500张

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出单价**

wan2.6-t2i

0.20元/张

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出单价**

wan2.6-t2i

0.220177元/张

wan2.5-t2i-preview

0.220177元/张

wan2.2-t2i-plus

0.366962元/张

wan2.2-t2i-flash

0.183481元/张

wan2.1-t2i-plus

0.366962元/张

wan2.1-t2i-turbo

0.183481元/张

### **万相图像生成与编辑**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.7-image-pro

0.50元/张

50张

wan2.7-image

0.20元/张

50张

wan2.6-image

0.20元/张

50张

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出单价**

wan2.6-image

0.20元/张

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出单价**

wan2.7-image-pro

0.562065元/张

wan2.7-image

0.220177元/张

wan2.6-image

0.220177元/张

### **万相通用图像编辑**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.5-i2i-preview

0.20元/张

50张

wanx2.1-imageedit

0.14元/张

500张

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出单价**

wan2.5-i2i-preview

0.220177元/张

### **万相涂鸦作画**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

wanx-sketch-to-image-lite

0.06元/张

500张

有效期：阿里云百炼开通后90天内

### **万相图像局部重绘**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

wanx-x-painting

目前仅供免费体验。

> 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)获取替代方案。

500张

有效期：阿里云百炼开通后90天内

### 人像风格重绘

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

wanx-style-repaint-v1

0.12元/张

500张

有效期：阿里云百炼开通后90天内

### **图像背景生成**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

wanx-background-generation-v2

0.08元/张

500张

有效期：阿里云百炼开通后90天内

### **图像画面扩展**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

image-out-painting

0.18元/张

500张

有效期：阿里云百炼开通后90天内

### **人物实例分割**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

image-instance-segmentation

目前仅供免费体验。

> 免费额度用完后不可调用。

500张

有效期：阿里云百炼开通后90天内

### **图像擦除补全**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

image-erase-completion

目前仅供免费体验。

> 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)获取替代方案。

500张

有效期：阿里云百炼开通后90天内

### **虚拟模特**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

wanx-virtualmodel

目前仅供免费体验。

> 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)获取替代方案。

各500张

有效期：阿里云百炼开通后90天内

virtualmodel-v2

### **鞋靴模特**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

shoemodel-v1

目前仅供免费体验。

> 免费额度用完后不可调用。

500张

有效期：阿里云百炼开通后90天内

### **创意海报生成**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

wanx-poster-generation-v1

目前仅供免费体验。

> 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)获取替代方案。

500张

有效期：阿里云百炼开通后90天内

### **人物写真生成-FaceChain**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

-   facechain-facedetect：限时免费。
    
-   facechain-finetune：按训练次数计费，请求失败不计费。
    
-   facechain-generation：输入不计费，输出计费。输出按成功生成的图片张数计费，计费规则请参见[图像生成](#26310bc5cf4do)。
    

**模型服务**

**模型 ID（Model ID）**

**单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

人物图像检测

facechain-facedetect

限时免费

限时免费

人物形象训练

facechain-finetune

2.5元/次

50次

有效期：申请通过后90天内

人物写真生成

facechain-generation

0.18元/张

500张

有效期：申请通过后90天内

### **创意文字生成-WordArt锦书**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**模型服务**

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

文字纹理生成

wordart-texture

0.08元/张

500张

有效期：阿里云百炼开通后90天内

文字变形

wordart-semantic

0.24元/张

### **AI试衣-OutfitAnyone**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

-   aitryon：输入不计费，输出计费。计费规则请参见[图像生成](#26310bc5cf4do)。
    
-   aitryon-plus：输入不计费，输出计费。计费规则请参见[图像生成](#26310bc5cf4do)。
    
-   aitryon-parsing-v1：输入计费，输出不计费。按输入的图像张数计费，请求失败不计费。
    
-   aitryon-refiner：输入不计费，输出计费。计费规则请参见[图像生成](#26310bc5cf4do)。
    

**模型服务**

**模型 ID（Model ID）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

AI试衣-基础版

aitryon

400张

AI试衣-Plus版

aitryon-plus

400张

AI试衣-图片分割

aitryon-parsing-v1

400张

AI试衣-图片精修

aitryon-refiner

100张

**模型服务**

**模型 ID（Model ID）**

**单价**

**折扣**

**阶梯层级**

AI试衣-基础版

aitryon

0.20元/张

无

无

AI试衣-Plus版

aitryon-plus

0.50元/张

无

无

AI试衣-图片分割

aitryon-parsing-v1

0.004元/张

无

无

AI试衣-图片精修

aitryon-refiner

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

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

**模型 ID（Model ID）**

**输出图像分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

kling/kling-v3-image-generation

1K

0.2元/张

无免费额度

2K

0.2元/张

kling/kling-v3-omni-image-generation

1K

0.2元/张

2K

0.2元/张

4K

0.4元/张

## **音乐生成**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输出音频的秒数计费，输入不计费。

**模型 ID（Model ID）**

**输出单价（每秒）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

fun-music-v1

0.002元

1,000秒

有效期：阿里云百炼开通后90天内

## **语音合成（文本转语音）**

### **Qwen-TTS**

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

## **千问3-TTS-Instruct-Flash**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-tts-instruct-flash

0.8元

不计费

1万字符

有效期：阿里云百炼开通后90天内

qwen3-tts-instruct-flash-2026-01-26

0.8元

不计费

## **千问3-TTS-VD**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-tts-vd-2026-01-26

0.8元

不计费

1万字符

有效期：阿里云百炼开通后90天内

## **千问3-TTS-VC**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-tts-vc-2026-01-22

0.8元

不计费

1万字符

有效期：阿里云百炼开通后90天内

## 千问3-TTS-Flash

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-tts-flash

> 当前能力等同于qwen3-tts-flash-2025-11-27

0.8元

不计费

1万字符

有效期：阿里云百炼开通后90天内

qwen3-tts-flash-2025-11-27

0.8元

不计费

qwen3-tts-flash-2025-09-18

0.8元

不计费

2025年11月13日0点前开通阿里云百炼：2000字符

2025年11月13日0点后开通阿里云百炼：1万字符

有效期：阿里云百炼开通后90天内

## 千问-TTS

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-tts-flash

1.6元

10元

各100万Token

有效期：阿里云百炼开通后90天内

qwen-tts-latest

1.6元

10元

qwen-tts-2025-05-22

1.6元

10元

qwen-tts-2025-04-10

1.6元

10元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

## **千问3-TTS-Instruct-Flash**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

qwen3-tts-instruct-flash

0.8元

qwen3-tts-instruct-flash-2026-01-26

0.8元

## **千问3-TTS-VD**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

qwen3-tts-vd-2026-01-26

0.8元

## **千问3-TTS-VC**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

qwen3-tts-vc-2026-01-22

0.8元

## 千问3-TTS-Flash

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

qwen3-tts-flash

> 当前能力等同于qwen3-tts-flash-2025-11-27

0.733924元

qwen3-tts-flash-2025-11-27

0.733924元

qwen3-tts-flash-2025-09-18

0.733924元

### **Qwen-TTS-Realtime**

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

## **千问3-TTS-Instruct-Flash-Realtime**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-tts-instruct-flash-realtime

1元

不计费

1万字符

有效期：阿里云百炼开通后90天内

qwen3-tts-instruct-flash-realtime-2026-01-22

1元

不计费

1万字符

有效期：阿里云百炼开通后90天内

## 千问3-TTS-VD-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-tts-vd-realtime-2026-01-15

1元

不计费

1万字符

有效期：阿里云百炼开通后90天内

qwen3-tts-vd-realtime-2025-12-16

1元

不计费

1万字符

有效期：阿里云百炼开通后90天内

## 千问3-TTS-VC-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-tts-vc-realtime-2026-01-15

1元

不计费

1万字符

有效期：阿里云百炼开通后90天内

qwen3-tts-vc-realtime-2025-11-27

## 千问3-TTS-Flash-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-tts-flash-realtime

1元

不计费

2025年11月13日0点前开通阿里云百炼：2000字符

2025年11月13日0点后开通阿里云百炼：1万字符

有效期：阿里云百炼开通后90天内

qwen3-tts-flash-realtime-2025-11-27

1元

不计费

1万字符

有效期：阿里云百炼开通后90天内

qwen3-tts-flash-realtime-2025-09-18

1元

不计费

2025年11月13日0点前开通阿里云百炼：2000字符

2025年11月13日0点后开通阿里云百炼：1万字符

有效期：阿里云百炼开通后90天内

## 千问-TTS-Realtime

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-tts-realtime

2.4元

12元

各100万Token

有效期：阿里云百炼开通后90天内

qwen-tts-realtime-latest

2.4元

12元

qwen-tts-realtime-2025-07-15

2.4元

12元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

## **千问3-TTS-Instruct-Flash-Realtime**

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

qwen3-tts-instruct-flash-realtime

1元

qwen3-tts-instruct-flash-realtime-2026-01-22

1元

## 千问3-TTS-VD-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

qwen3-tts-vd-realtime-2026-01-15

0.954101元

qwen3-tts-vd-realtime-2025-12-16

0.954101元

## 千问3-TTS-VC-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

qwen3-tts-vc-realtime-2026-01-15

0.954101元

qwen3-tts-vc-realtime-2025-11-27

## 千问3-TTS-Flash-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

qwen3-tts-flash-realtime

0.954101元

qwen3-tts-flash-realtime-2025-11-27

0.954101元

qwen3-tts-flash-realtime-2025-09-18

0.954101元

### **Qwen-TTS声音复刻**

计费规则：按新建音色个数计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**单价（每个音色）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-voice-enrollment

0.01元

1000个音色/账号

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**单价（每个音色）**

qwen-voice-enrollment

0.01元

### **Qwen-TTS声音设计**

计费规则：按新建音色个数计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**单价（每个音色）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-voice-design

0.2元

10个音色/账号

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**单价（每个音色）**

qwen-voice-design

0.2元

### **CosyVoice**

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

cosyvoice-v3.5-plus

1.5元

1万字符

有效期：阿里云百炼开通后90天内

cosyvoice-v3.5-flash

0.8元

cosyvoice-v3-plus

2元

cosyvoice-v3-flash

1元

cosyvoice-v2

2元

cosyvoice-v1

2元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

cosyvoice-v3-plus

1.9082元

无免费额度

cosyvoice-v3-flash

0.9541元

### **Sambert**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入文本的字符数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每万字符）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

参见[模型列表](https://help.aliyun.com/zh/model-studio/sambert-java-sdk#57d33631f7doi)

1元

每主账号每模型每月3万字符。

### MiniMax

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入文本的字符数计费，输出不计费。

复刻音色收取一次性费用，费用在首次使用该音色进行语音合成的时候，与语音合成的费用一同出账。

**模型名称**

**语音合成单价（每万字符）**

[复刻一个音色](https://help.aliyun.com/zh/model-studio/mini-clone-api)

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

MiniMax/speech-2.8-hd

3.5元

9.9元

（在首次使用复刻出来的音色进行语音合成的时候收取）

无

MiniMax/speech-02-hd

3.5元

MiniMax/speech-2.8-turbo

2元

MiniMax/speech-02-turbo

2元

## **语音识别（语音转文本）与翻译（语音转成指定语种的文本）**

### **千问-LiveTranslate-Flash-Realtime**

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费说明](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#6a95f2fc38za0)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

**输入：音频**

**输入：图片**

**输出：文本**

**输出：音频**

qwen3.5-livetranslate-flash-realtime

40元

3.3元

100元

160元

各100万Token

有效期：阿里云百炼开通后90天内

qwen3.5-livetranslate-flash-realtime-2026-05-19

40元

3.3元

100元

160元

qwen3-livetranslate-flash-realtime

64元

8元

64元

240元

qwen3-livetranslate-flash-realtime-2025-09-22

64元

8元

64元

240元

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输入单价 (每百万 Token)**

**输出单价 (每百万 Token)**

**输入：音频**

**输入：图片**

**输出：文本**

**输出：音频**

qwen3.5-livetranslate-flash-realtime

56.207元

4.122元

149.884元

224.826元

qwen3.5-livetranslate-flash-realtime-2026-05-19

56.207元

4.122元

149.884元

224.826元

qwen3-livetranslate-flash-realtime

73.392元

9.541元

73.392元

278.891元

qwen3-livetranslate-flash-realtime-2025-09-22

73.392元

9.541元

73.392元

278.891元

### **千问ASR**

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

计费规则：按输入音频的秒数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-asr-flash-filetrans

0.00022元/秒

不计费

36,000秒（10小时）

有效期：阿里云百炼开通后90天内

qwen3-asr-flash-filetrans-2025-11-17

qwen3-asr-flash

> 当前能力等同于qwen3-asr-flash-2025-09-08

qwen3-asr-flash-2026-02-10

qwen3-asr-flash-2025-09-08

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

计费规则：按输入音频的秒数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价**

**输出单价**

qwen3-asr-flash-filetrans

0.00026元/秒

不计费

qwen3-asr-flash-filetrans-2025-11-17

qwen3-asr-flash

> 当前能力等同于qwen3-asr-flash-2025-09-08

qwen3-asr-flash-2026-02-10

qwen3-asr-flash-2025-09-08

## 美国

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于美国境内；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）。

**说明**

美国部署范围下的模型无免费额度。

计费规则：按输入音频的秒数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价**

**输出单价**

qwen3-asr-flash-us

0.000035元/秒

不计费

qwen3-asr-flash-2025-09-08-us

### **千问ASR-Realtime**

计费规则：按输入音频的秒数计费，输出不计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-asr-flash-realtime

0.00033元/秒

36,000秒（10小时）

有效期：阿里云百炼开通后90天内

qwen3-asr-flash-realtime-2026-02-10

qwen3-asr-flash-realtime-2025-10-27

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输入单价**

qwen3-asr-flash-realtime

0.00066元/秒

qwen3-asr-flash-realtime-2026-02-10

qwen3-asr-flash-realtime-2025-10-27

### **Fun-ASR**

#### **录音文件识别**

计费规则：按输入音频的秒数计费，输出不计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

fun-asr

0.00022元/秒

36,000秒（10小时）

有效期：阿里云百炼开通后90天

fun-asr-2025-11-07

fun-asr-2025-08-25

fun-asr-mtl

fun-asr-mtl-2025-08-25

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输入单价**

fun-asr

0.00026元/秒

fun-asr-2025-11-07

fun-asr-2025-08-25

fun-asr-mtl

fun-asr-mtl-2025-08-25

#### **实时语音识别**

计费规则：按输入音频的秒数计费，输出不计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

fun-asr-realtime

0.00033元/秒

36,000秒（10小时）

有效期：阿里云百炼开通后90天

fun-asr-realtime-2026-02-28

fun-asr-realtime-2025-11-07

fun-asr-realtime-2025-09-15

fun-asr-mtl-realtime

fun-asr-mtl-realtime-2025-12-10

fun-asr-flash-8k-realtime

0.00022元/秒

fun-asr-flash-8k-realtime-2026-01-28

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输入单价**

fun-asr-realtime

0.00066元/秒

fun-asr-realtime-2025-11-07

### **Paraformer**

#### **录音文件识别**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入音频的秒数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

paraformer-v2

0.00008元/秒

36,000秒（10小时）

每月1日0点自动发放

有效期1个月

paraformer-8k-v2

paraformer-v1

paraformer-8k-v1

paraformer-mtl-v1

#### **实时语音识别**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入音频的秒数计费，输出不计费。

**模型 ID（Model ID）**

**输入单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

paraformer-realtime-v2

0.00024元/秒

36,000秒（10小时）

每月1日0点自动发放

有效期1个月

paraformer-realtime-v1

paraformer-realtime-8k-v2

paraformer-realtime-8k-v1

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

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

happyhorse-1.0-t2v

720P

0.9元/秒

10秒

1080P

1.6元/秒

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

happyhorse-1.0-t2v

720P

0.9元/秒

1080P

1.6元/秒

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

happyhorse-1.0-t2v

720P

1.049188元/秒

1080P

1.798608元/秒

### **HappyHorse-图生视频-基于首帧**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

happyhorse-1.0-i2v

720P

0.9元/秒

10秒

1080P

1.6元/秒

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

happyhorse-1.0-i2v

720P

0.9元/秒

1080P

1.6元/秒

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

happyhorse-1.0-i2v

720P

1.049188元/秒

1080P

1.798608元/秒

### **HappyHorse-参考生视频**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

happyhorse-1.0-r2v

720P

0.9元/秒

10秒

1080P

1.6元/秒

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

happyhorse-1.0-r2v

720P

0.9元/秒

1080P

1.6元/秒

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

happyhorse-1.0-r2v

720P

1.049188元/秒

1080P

1.798608元/秒

### **HappyHorse-视频编辑**

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输入和输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

happyhorse-1.0-video-edit

720P

0.9元/秒

10秒

1080P

1.6元/秒

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输入和输出单价**

happyhorse-1.0-video-edit

720P

0.9元/秒

1080P

1.6元/秒

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输入和输出单价**

happyhorse-1.0-video-edit

720P

1.049188元/秒

1080P

1.798608元/秒

### **万相-文生视频**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.7-t2v-2026-04-25

720P

0.6元/秒

50秒

1080P

1元/秒

wan2.7-t2v

720P

0.6元/秒

50秒

1080P

1元/秒

wan2.6-t2v

720P

0.6元/秒

50秒

1080P

1元/秒

wan2.5-t2v-preview

480P

0.3元/秒

50秒

720P

0.6元/秒

1080P

1元/秒

wan2.2-t2v-plus

480P

0.14元/秒

50秒

1080P

0.70元/秒

wanx2.1-t2v-turbo

480P

0.24元/秒

200秒

720P

0.24元/秒

wanx2.1-t2v-plus

720P

0.70元/秒

200秒

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

wan2.6-t2v

720P

0.6元/秒

1080P

1元/秒

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

wan2.7-t2v-2026-04-25

720P

0.733924元/秒

1080P

1.100886元/秒

wan2.7-t2v

720P

0.733924元/秒

1080P

1.100886元/秒

wan2.6-t2v

720P

0.733924元/秒

1080P

1.100886元/秒

wan2.5-t2v-preview

480P

0.366961元/秒

720P

0.733923元/秒

1080P

1.100885元/秒

wan2.2-t2v-plus

480P

0.146785元/秒

1080P

0.733924元/秒

wan2.1-t2v-turbo

480P

0.264213元/秒

720P

0.264213元/秒

wan2.1-t2v-plus

720P

0.733924元/秒

## 美国

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于美国境内；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）。

**说明**

美国部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

wan2.6-t2v-us

720P

0.733924元/秒

1080P

1.100886元/秒

### **万相-图生视频**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出视频类型**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.7-i2v-2026-04-25

有声视频

720P

0.6元/秒

50秒

1080P

1元/秒

wan2.7-i2v

有声视频

720P

0.6元/秒

50秒

1080P

1元/秒

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频类型**

**输出视频分辨率**

**输出单价**

wan2.7-i2v-2026-04-25

有声视频

720P

0.733924元/秒

1080P

1.100886元/秒

wan2.7-i2v

有声视频

720P

0.733924元/秒

1080P

1.100886元/秒

### **万相-图生视频-基于首帧**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出视频类型**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.6-i2v-flash

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

有声视频

720P

0.6元/秒

50秒

1080P

1元/秒

wan2.5-i2v-preview

有声视频

480P

0.3元/秒

50秒

720P

0.6元/秒

1080P

1元/秒

wan2.2-i2v-flash

无声视频

480P

0.10元/秒

50秒

720P

0.20元/秒

1080P

0.48元/秒

wan2.2-i2v-plus

无声视频

480P

0.14元/秒

50秒

1080P

0.70元/秒

wanx2.1-i2v-turbo

无声视频

480P

0.24元/秒

200秒

720P

0.24元/秒

wanx2.1-i2v-plus

无声视频

720P

0.70元/秒

200秒

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频类型**

**输出视频分辨率**

**输出单价**

wan2.6-i2v

有声视频

720P

0.6元/秒

1080P

1元/秒

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频类型**

**输出视频分辨率**

**输出单价**

wan2.6-i2v-flash

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

有声视频

720P

0.733924元/秒

1080P

1.100886元/秒

wan2.5-i2v-preview

有声视频

480P

0.366961元/秒

720P

0.733923元/秒

1080P

1.100885元/秒

wan2.2-i2v-flash

无声视频

480P

0.110089元/秒

720P

0.264213元/秒

wan2.2-i2v-plus

无声视频

480P

0.146785元/秒

1080P

0.733924元/秒

wan2.1-i2v-turbo

无声视频

480P

0.264213元/秒

720P

0.264213元/秒

wan2.1-i2v-plus

无声视频

720P

0.733924元/秒

## 美国

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于美国境内；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）。

**说明**

美国部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频类型**

**输出视频分辨率**

**输出单价**

wan2.6-i2v-us

有声视频

720P

0.733924元/秒

1080P

1.100886元/秒

### **万相-图生视频-基于首尾帧**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.2-kf2v-flash

480P

0.10元/秒

50秒

720P

0.20元/秒

1080P

0.48元/秒

wanx2.1-kf2v-plus

720P

0.70元/秒

200秒

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

wan2.1-kf2v-plus

720P

0.733924元/秒

### **万相-参考生视频**

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

计费公式：计费时长 = 输入视频时长（上限 5 秒）+ 输出视频时长。

-   输入视频的计费时长不超过 **5 秒**，计算规则参见[计费与限流](https://help.aliyun.com/zh/model-studio/video-to-video-guide#6f5774ce5fqie)。
    
-   输出视频的计费时长为**成功生成的视频秒数**。
    

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出视频类型**

**输出视频分辨率**

**输入和输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.7-r2v

有声视频

720P

0.6元/秒

50秒

1080P

1元/秒

wan2.6-r2v-flash

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

有声视频

720P

0.6元/秒

50秒

1080P

1元/秒

## 全球

服务部署范围为[全球](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度；静态数据存储于您所选的地域。该部署范围支持的地域：美国（弗吉尼亚）、德国（法兰克福）。

**说明**

全球部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频类型**

**输出视频分辨率**

**输入和输出单价**

wan2.6-r2v

有声视频

720P

0.6元/秒

1080P

1元/秒

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频类型**

**输出视频分辨率**

**输入和输出单价**

wan2.7-r2v

有声视频

720P

0.733924元/秒

1080P

1.100886元/秒

wan2.6-r2v-flash

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

有声视频

720P

0.733924元/秒

1080P

1.100886元/秒

### **万相-视频编辑**

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输入和输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wan2.7-videoedit

720P

0.6元/秒

50秒

1080P

1元/秒

计费规则：输入不计费，输出视频计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

wanx2.1-vace-plus

720P

0.70元/秒

50秒

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输入和输出单价**

wan2.7-videoedit

720P

0.733924元/秒

1080P

1.100886元/秒

计费规则：输入不计费，输出视频计费，按**视频秒数**计费，失败不计费也不占用免费额度。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

wan2.1-vace-plus

720P

0.733924元/秒

### **万相-数字人**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

-   wan2.2-s2v-detect：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   wan2.2-s2v：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

**模型服务**

**模型 ID（Model ID）**

**单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

图像检测

wan2.2-s2v-detect

输入图像：0.004元/张

200张

视频生成

wan2.2-s2v

输出视频：

-   480P：0.5元/秒
    
-   720P：0.9元/秒
    

100秒

### **万相-图生动作**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出视频模式**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

wan2.2-animate-move

标准模式`wan-std`

0.4元/秒

50秒

有效期：阿里云百炼开通后90天内

专业模式`wan-pro`

0.6元/秒

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频模式**

**输出单价**

wan2.2-animate-move

标准模式`wan-std`

0.880709元/秒

专业模式`wan-pro`

1.321063元/秒

### **万相-视频换人**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输出视频模式**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

wan2.2-animate-mix

标准模式`wan-std`

0.6元/秒

50秒

有效期：阿里云百炼开通后90天内

专业模式`wan-pro`

0.9元/秒

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输出视频模式**

**输出单价**

wan2.2-animate-mix

标准模式`wan-std`

1.321063元/秒

专业模式`wan-pro`

1.908202元/秒

### **舞动人像AnimateAnyone**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

-   animate-anyone-detect-gen2：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   animate-anyone-template-gen2：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    
-   animate-anyone-gen2：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

**模型服务**

**模型 ID（Model ID）**

**单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

图像检测

animate-anyone-detect-gen2

输入图像：0.004元/张

200张

动作模板生成

animate-anyone-template-gen2

输出视频：0.08元/秒

1800秒（30分钟）

视频生成

animate-anyone-gen2

输出视频：0.08元/秒

1800秒（30分钟）

### **悦动人像EMO**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

-   emo-detect-v1：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   emo-v1：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

**模型服务**

**模型 ID（Model ID）**

**单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

图像检测

emo-detect-v1

输入图像：0.004元/张

200张

视频生成

emo-v1

输出视频：

-   1:1画幅视频：0.08元/秒
    
-   3:4画幅视频：0.16元/秒
    

1800秒（30分钟）

### **灵动人像LivePortrait**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

-   liveportrait-detect：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   liveportrait：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

**模型服务**

**模型 ID（Model ID）**

**单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

图像检测

liveportrait-detect

输入图像：0.004元/张

200张

视频生成

liveportrait

输出视频：0.02元/秒

1800秒（30分钟）

### **表情包Emoji**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

-   emoji-detect-v1：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   emoji-v1：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

**模型服务**

**模型 ID（Model ID）**

**单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

图像检测

emoji-detect-v1

输入图像：0.004元/张

200张

视频生成

emoji-v1

输出视频：0.08元/秒

1800秒（30分钟）

### **声动人像VideoRetalk**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**模型 ID（Model ID）**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

videoretalk

0.08元/秒

1800秒（30分钟）

### **视频风格重绘**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

video-style-transform

540P

0.2元/秒

600秒

有效期：阿里云百炼开通后90天内

720P

0.5元/秒

## **视频生成-第三方模型**

**爱诗-文生视频**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**模型 ID（Model ID）**

**输出视频类型**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

pixverse/pixverse-c1-t2v

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

有声视频

`audio=true`

360P

0.21元/秒

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

有声视频

`audio=true`

360P

0.47元/秒

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

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**模型 ID（Model ID）**

**输出视频类型**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

pixverse/pixverse-c1-it2v

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

有声视频

`audio=true`

360P

0.21元/秒

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

有声视频

`audio=true`

360P

0.47元/秒

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

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**模型 ID（Model ID）**

**输出视频类型**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

pixverse/pixverse-c1-kf2v

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

有声视频

`audio=true`

360P

0.21元/秒

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

有声视频

`audio=true`

360P

0.47元/秒

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

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**模型 ID（Model ID）**

**输出视频类型**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

pixverse/pixverse-c1-r2v

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

有声视频

`audio=true`

360P

0.47元/秒

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

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**模型 ID（Model ID）**

**输出视频类型**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

kling/kling-v3-video-generation

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

无声视频（无参考视频）

720P

0.6元/秒

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

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

vidu/viduq3-pro\_text2video

540P

0.3125元/秒

无免费额度

720P

0.78125元/秒

1080P

0.9375元/秒

vidu/viduq3-turbo\_text2video

540P

0.25元/秒

720P

0.375元/秒

1080P

0.4375元/秒

vidu/viduq2\_text2video

540P

0.1125元/秒

720P

0.21875元/秒

1080P

0.375元/秒

**Vidu-图生视频-基于首帧**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

vidu/viduq3-pro\_img2video

540P

0.3125元/秒

无免费额度

720P

0.78125元/秒

1080P

0.9375元/秒

vidu/viduq3-turbo\_img2video

540P

0.25元/秒

720P

0.375元/秒

1080P

0.4375元/秒

vidu/viduq2-pro\_img2video

540P

0.15625元/秒

720P

0.34375元/秒

1080P

0.71875元/秒

vidu/viduq2-turbo\_img2video

540P

0.0875元/秒

720P

0.25元/秒

1080P

0.46875元/秒

vidu/viduq2-pro-fast\_img2video

720P

0.1元/秒

1080P

0.2元/秒

**Vidu-图生视频-基于首尾帧**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

vidu/viduq3-pro\_start-end2video

540P

0.3125元/秒

无免费额度

720P

0.78125元/秒

1080P

0.9375元/秒

vidu/viduq3-turbo\_start-end2video

540P

0.25元/秒

720P

0.375元/秒

1080P

0.4375元/秒

vidu/viduq2-pro\_start-end2video

540P

0.15625元/秒

720P

0.34375元/秒

1080P

0.71875元/秒

vidu/viduq2-turbo\_start-end2video

540P

0.0875元/秒

720P

0.25元/秒

1080P

0.46875元/秒

**Vidu-参考生视频**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

**模型 ID（Model ID）**

**输出视频分辨率**

**输出单价**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

vidu/viduq3-mix\_reference2video

720P

0.78125元/秒

无免费额度

1080P

0.9375元/秒

vidu/viduq3\_reference2video

540P

0.3125元/秒

720P

0.625元/秒

1080P

0.78125元/秒

vidu/viduq3-turbo\_reference2video

540P

0.15625元/秒

720P

0.3125元/秒

1080P

0.40625元/秒

vidu/viduq2-pro\_reference2video

540P

0.25元/秒

720P

0.3125元/秒

1080P

0.78125元/秒

vidu/viduq2\_reference2video

540P

0.21875元/秒

720P

0.28125元/秒

1080P

0.71875元/秒

## **3D模型生成-第三方模型**

**Tripo-3D模型生成**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：输入不计费，输出按次数计费。

**模型 ID（Model ID）**

**3D任务类型**

**输出规格**

**输出单价**

Tripo/Tripo-H3.1

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

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

有效期：阿里云百炼开通后90天内

text-embedding-v4

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

0.5元

100万Token

text-embedding-v3

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

0.5元

50万Token

text-embedding-v2

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

0.7元

50万Token

text-embedding-v1

> [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价

0.7元

50万Token

text-embedding-async-v2

0.7元

2000万Token

text-embedding-async-v1

0.7元

2000万Token

## **国际**

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

text-embedding-v4

0.514元

text-embedding-v3

0.514元

## **多模态向量**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token计费，输出不计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

**文本**

**图片/视频**

qwen3-vl-embedding

0.7元

1.8元

各100万Token

有效期：阿里云百炼开通后90天内

qwen2.5-vl-embedding

tongyi-embedding-vision-plus

0.5元

0.5元

tongyi-embedding-vision-flash

0.15元

0.15元

multimodal-embedding-v1

0.7元

0.9元

## **文本排序**

### **文本排序模型**

计费规则：按输入Token计费，输出不计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-rerank

0.5元

各100万Token

有效期：阿里云百炼开通后90天内

gte-rerank-v2

0.8元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen3-rerank

0.74942元

无免费额度

## **行业模型**

### **通义法睿**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

farui-plus

20元

20元

无免费额度

### **意图理解**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

tongyi-intent-detect-v3

0.4元

1元

100万Token

有效期：阿里云百炼开通后90天内

### **角色扮演**

计费规则：按输入Token和输出Token计费。

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

qwen-plus-character

> [Session Cache](https://help.aliyun.com/zh/model-studio/role-play#6034f997cde74)享有折扣

0.8元

2元

各100万Token

有效期：阿里云百炼开通后90天内

qwen-flash-character

> [Session Cache](https://help.aliyun.com/zh/model-studio/role-play#6034f997cde74)享有折扣

0.25元

1.5元

qwen-flash-character-2026-02-26

> [Session Cache](https://help.aliyun.com/zh/model-studio/role-play#6034f997cde74)享有折扣

0.18元

1.5元

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

**说明**

国际部署范围下的模型无免费额度。

**模型 ID（Model ID）**

**输入单价 （每百万Token）**

**输出单价 （每百万Token）**

qwen-plus-character

> [Session Cache](https://help.aliyun.com/zh/model-studio/role-play#6034f997cde74)享有折扣

3.747元

10.492元

qwen-flash-character

> [Session Cache](https://help.aliyun.com/zh/model-studio/role-play#6034f997cde74)享有折扣

0.375元

2.998元

qwen-plus-character-ja

3.67元

10.275元

### **界面交互**

**说明**

服务部署范围仅支持[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

**模型 ID（Model ID）**

**输入单价（每百万Token）**

**输出单价（每百万Token）**

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

gui-plus

1.5元

4.5元

100万Token

有效期：阿里云百炼开通后90天内

gui-plus-2026-02-26

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
