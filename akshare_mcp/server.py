import inspect
import pathlib
import sys
from functools import wraps
from typing import Literal

import akshare as ak
import fastmcp
import pandas as pd

mcp = fastmcp.FastMCP("AKShare MCP Server")


def output_format(func, format: Literal["markdown", "csv", "json"]):
    @wraps(func)
    def decorated(*args, **kwargs):
        df: pd.DataFrame = func(*args, **kwargs)
        if format == 'markdown':
            return df.to_markdown()
        if format == 'csv':
            return df.to_csv()
        if format == 'json':
            return df.to_json(force_ascii=False, indent=2)
        return df.to_markdown()

    return decorated


def register(white_list, black_list, format: Literal["markdown", "csv", "json"]):
    # 有1000多个函数，只注册一部分，因为部分Client支持的函数有限，或LLM无法处理过长输入
    for name, func in inspect.getmembers(ak, inspect.isfunction):
        # 白名单不为空，且当前函数不在白名单中，跳过
        if white_list and name not in white_list:
            continue
        # 黑名单不为空，且当前函数在黑名单中，跳过
        if black_list and name in black_list:
            continue

        try:
            # TODO 参数能支持读取__doc__就好了
            mcp.tool()(output_format(func, format=format))
        except Exception as e:
            print(name, "注册失败，需要调整函数参数")


def serve(format: Literal["markdown", "csv", "json"], transport: Literal["stdio", "sse", "streamable-http"], host: str, port: int, config: str = None):
    if config:
        path = pathlib.Path(config)
        sys.path.insert(0, str(path.parent))
        cfg = __import__(path.stem, globals(), locals(), fromlist=[])
        sys.path.pop(0)
    else:
        from akshare_mcp import config as cfg

    register(cfg.white_list, cfg.black_list, format=format)

    fastmcp.settings.host = host
    fastmcp.settings.port = port
    mcp.run(transport=transport)
