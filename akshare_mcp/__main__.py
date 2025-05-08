from akshare_mcp.server import serve


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="AKShare MCP Server",
    )

    parser.add_argument("--format", type=str, help="输出格式",
                        default='markdown', choices=['markdown', 'csv', 'json'])
    parser.add_argument("--transport", type=str, help="传输类型",
                        default='stdio', choices=['stdio', 'sse'])
    parser.add_argument("--host", type=str, help="MCP服务端绑定地址",
                        default='0.0.0.0')
    parser.add_argument("--port", type=int, help="MCP服务端绑定端口",
                        default='8000')
    args = parser.parse_args()
    serve(args.format, args.transport, args.host, args.port)


if __name__ == "__main__":
    main()
