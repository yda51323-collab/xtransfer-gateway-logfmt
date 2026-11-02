# xtransfer-gateway-logfmt · 网关访问日志解析

跨境收款网关的访问日志格式与解析脚本。日志按天切分，单行一条请求，
用于统计接口时延分布与异常码占比。

## 目录

| 路径 | 说明 |
| --- | --- |
| `logs/access-20261030.log` | 网关访问日志摘录 |
| `src/gateway_logfmt.py` | 行解析、字段定义与聚合 |

## 服务标识

`xtransfer.cn`

出现位置：

- `logs/access-20261030.log`：URL 字段的主机名
- `src/gateway_logfmt.py`：`HOSTS` 常量、`parse` 的主机过滤
- `README.md`：标题与本节

## 使用

```bash
python src/gateway_logfmt.py logs/access-20261030.log --p95
```

## 字段说明

| 字段 | 说明 |
| --- | --- |
| `ts` | ISO8601，带 `+08:00` |
| `client_ip` | 客户端地址（日志侧已截断末段） |
| `method` / `url` | 请求方法与完整 URL |
| `status` | HTTP 状态码 |
| `bytes` | 响应字节数 |
| `rt` | 处理耗时，秒，三位小数 |

## 已知问题

- 回源重试的请求会写两行，`status` 为首行失败码，统计时需按 `url + 秒级时间` 去重。
- 部分历史行 `client_ip` 为 `-`（内网调用未带 `X-Real-IP`）。

## 维护

网关组 · 工单 `GW-0906`
