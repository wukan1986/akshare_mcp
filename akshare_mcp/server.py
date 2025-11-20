import importlib
import inspect
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
            print(name, "注册成功")
        except Exception as e:
            print(name, "注册失败，需要调整函数参数")


def import_module_from_path(module_name, file_path):
    """
    从指定文件路径导入模块

    Args:
        module_name (str): 要导入的模块名称（自定义）
        file_path (str): Python 文件的绝对路径

    Returns:
        module: 导入的模块对象
    """
    # 根据文件路径创建模块规格
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"无法从路径 '{file_path}' 创建模块规格")
    # 根据规格创建新的模块对象
    module = importlib.util.module_from_spec(spec)
    # 将模块添加到 sys.modules 全局字典中
    sys.modules[module_name] = module
    # 执行模块代码（加载模块）
    spec.loader.exec_module(module)
    return module


def serve(format: Literal["markdown", "csv", "json"], transport: Literal["stdio", "sse", "streamable-http"], host: str, port: int, config: str = None):
    if config:
        import_module_from_path("akshare_mcp.config", config)

    from akshare_mcp import config as cfg
    register(cfg.white_list, cfg.black_list, format=format)

    if transport == "stdio":
        mcp.run(transport=transport)
    else:
        mcp.run(transport=transport, host=host, port=port)
