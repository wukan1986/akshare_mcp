# akshare_mcp

`AKShare`数据接口的`MCP Server`封装

## 项目背景

`AKShare`提供了上千个数据接口，但`Github`上提供的服务都只支持少量接口，所以本项目将所有接口都暴露出来，方便用户使用。

## 安装

在虚拟环境下执行`pip install akshare_mcp`，运行`python -m akshare_mcp -h`检查是否安装成功

## 配置

```json
{
  "mcpServers": {
    "akshare_mcp": {
      "command": "D:\\Users\\Kan\\miniconda3\\envs\\py312\\python.exe",
      "args": [
        "-m",
        "akshare_mcp",
        "--format",
        "markdown"
      ]
    }
  }
}
```

## 注意

1. 1000+接口，全部暴露成工具，将会消耗大量`Token`
2. 部分MCP客户端只支持少量的工具，例如`Trae`最多支持40个工具

所以，请一定在使用前配置需要使用的接口。

1. 先运行`python -m akshare_mcp -h`，查看配置文件的位置。
2. 编辑配置文件，添加需要使用的接口。接口名参考`https://akshare.akfamily.xyz/data/index.html`
3. 重启MCP客户端
