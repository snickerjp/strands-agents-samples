# Strands SDKでのツール作成

このガイドでは、Strands Agentsのためのツールを作成するさまざまな方法について説明します。

## ツール作成の方法

### 1. `@tool`デコレータの使用

ツールを作成する最もシンプルな方法は、Python関数に`@tool`デコレータを使用することです：

```python
from strands import tool

@tool
def my_tool(param1: str, param2: int) -> str:
    """
    このツールが何をするかの説明。
    
    Args:
        param1: 最初のパラメータの説明
        param2: 2番目のパラメータの説明
        
    Returns:
        返される内容の説明
    """
    # ダミー実装
    return f"結果: {param1}, {param2}"
```

注意: このアプローチでは、Pythonのdocstringを使用してツールを文書化し、型ヒントをパラメータ検証に使用します

### 2. TOOL_SPEC辞書の使用

ツール定義をより詳細に制御するには、TOOL_SPEC辞書アプローチを使用できます：

```python
from strands.types.tools import ToolResult, ToolUse
from typing import Any

TOOL_SPEC = {
    "name": "my_tool",
    "description": "このツールが何をするかの説明",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "最初のパラメータの説明"
                },
                "param2": {
                    "type": "integer",
                    "description": "2番目のパラメータの説明",
                    "default": 2
                }
            },
            "required": ["param1"]
        }
    }
}

# 関数名はツール名と一致する必要があります
def my_tool(tool: ToolUse, **kwargs: Any) -> ToolResult:
    tool_use_id = tool["toolUseId"]
    param1 = tool["input"].get("param1")
    param2 = tool["input"].get("param2", 2)
    
    # ツール実装
    result = f"結果: {param1}, {param2}"
    
    return {
        "toolUseId": tool_use_id,
        "status": "success",
        "content": [{"text": result}]
    }
```

このアプローチでは、入力スキーマ定義をより詳細に制御できます。ここでは、成功状態とエラー状態の明示的な処理を定義できます。

注意: これはAmazon Bedrock Converse API形式に従います

#### 使用方法

ツールは関数を通じて、または別のファイルから以下のようにインポートできます：

```python
agent = Agent(tools=[my_tool])
# または 
agent = Agent(tools=["./my_tool.py"])
```

### 3. MCP（Model Context Protocol）ツールの使用

Model Context Protocolを使用して外部ツールを統合することもできます：

```python
from mcp import StdioServerParameters, stdio_client
from strands.tools.mcp import MCPClient

# MCPサーバーに接続
mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uvx", args=["awslabs.aws-documentation-mcp-server@latest"]
        )
    )
)

# エージェントでツールを使用
with mcp_client:
    tools = mcp_client.list_tools_sync()
    agent = Agent(tools=tools)
```

このアプローチでは、MCPを通じて外部ツールプロバイダーに接続し、異なるサーバーからのツールを使用できます。stdioとHTTPの両方のトランスポートをサポートしています

## ベストプラクティス

1. **ツール命名**: ツールには明確で説明的な名前を使用する
2. **ドキュメント**: ツールが何をするか、そのパラメータについて詳細な説明を提供する
3. **エラーハンドリング**: ツールに適切なエラーハンドリングを含める
4. **パラメータ検証**: 処理前に入力を検証する
5. **戻り値**: エージェントが理解しやすい構造化されたデータを返す

## 例

このディレクトリのサンプルノートブックを確認してください：
- [MCPツールの使用](01-using-mcp-tools/mcp-agent.ipynb): エージェントとMCPツールを統合する方法を学習
- [カスタムツール](02-custom-tools/custom-tools-with-strands-agents.ipynb): カスタムツールの作成と使用方法を学習

詳細については、[Strandsツールドキュメント](https://strandsagents.com/0.1.x/user-guide/concepts/tools/python-tools/)を参照してください。
