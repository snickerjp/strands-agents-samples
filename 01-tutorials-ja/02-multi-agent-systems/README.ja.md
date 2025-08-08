# マルチエージェントシステム

このチュートリアルセクションでは、Strands Agents SDKを使用してマルチエージェントシステムを構築するさまざまなアプローチを探求します。

## マルチエージェントシステムへのアプローチ

### 1. エージェントをツールとして使用
[ドキュメントへのリンク](https://strandsagents.com/latest/user-guide/concepts/multi-agent/agents-as-tools/)

「エージェントをツールとして使用」パターンは、専門化されたAIエージェントを他のエージェントが使用できる呼び出し可能な関数（ツール）としてラップする階層構造を作成します：

- **オーケストレーターエージェント**: ユーザーとのやり取りを処理し、専門エージェントにタスクを委任
- **専門ツールエージェント**: オーケストレーターから呼び出されたときにドメイン固有のタスクを実行
- **主な利点**: 関心の分離、階層的委任、モジュラーアーキテクチャ

実装では、`@tool`デコレータを使用して専門エージェントを呼び出し可能な関数に変換します：

```python
@tool
def research_assistant(query: str) -> str:
    """研究関連のクエリを処理して応答します。"""
    research_agent = Agent(system_prompt=RESEARCH_ASSISTANT_PROMPT)
    return str(research_agent(query))
```

### 2. エージェントスウォーム
[ドキュメントへのリンク](https://strandsagents.com/latest/user-guide/concepts/multi-agent/swarm/)

エージェントスウォームは、連携して動作する自律的なAIエージェントの集合を通じて集合知を活用します：

- **分散制御**: 単一のエージェントがシステム全体を指揮することはありません
- **共有メモリ**: エージェントが洞察を交換して集合的な知識を構築
- **協調メカニズム**: 協力的、競争的、またはハイブリッドアプローチ
- **通信パターン**: エージェント同士が通信できるメッシュネットワーク

組み込みの`swarm`ツールが実装を簡素化します：

```python
from strands import Agent
from strands_tools import swarm

agent = Agent(tools=[swarm])
result = agent.tool.swarm(
    task="このデータセットを分析して市場トレンドを特定する",
    swarm_size=4,
    coordination_pattern="collaborative"
)
```

### 3. エージェントグラフ
[ドキュメントへのリンク](https://strandsagents.com/latest/user-guide/concepts/multi-agent/graph/)

エージェントグラフは、明示的な通信経路を持つ相互接続されたAIエージェントの構造化ネットワークを提供します：

- **ノード（エージェント）**: 専門的な役割を持つ個別のAIエージェント
- **エッジ（接続）**: エージェント間の通信経路を定義
- **トポロジーパターン**: スター、メッシュ、または階層構造

`agent_graph`ツールにより、洗練されたエージェントネットワークの作成が可能になります：

```python
from strands import Agent
from strands_tools import agent_graph

agent = Agent(tools=[agent_graph])
agent.tool.agent_graph(
    action="create",
    graph_id="research_team",
    topology={
        "type": "star",
        "nodes": [
            {"id": "coordinator", "role": "team_lead"},
            {"id": "data_analyst", "role": "analyst"},
            {"id": "domain_expert", "role": "expert"}
        ],
        "edges": [
            {"from": "coordinator", "to": "data_analyst"},
            {"from": "coordinator", "to": "domain_expert"}
        ]
    }
)
```

### 4. エージェントワークフロー
[ドキュメントへのリンク](https://strandsagents.com/latest/user-guide/concepts/multi-agent/workflow/)

エージェントワークフローは、明確な依存関係を持つ定義されたシーケンスで複数のAIエージェント間のタスクを調整します：

- **タスク定義**: 各エージェントが達成する必要があることの明確な説明
- **依存関係管理**: 順次依存関係、並列実行、結合ポイント
- **情報フロー**: あるエージェントの出力を別のエージェントの入力に接続

`workflow`ツールがタスクの作成、依存関係の解決、実行を処理します：

```python
from strands import Agent
from strands_tools import workflow

agent = Agent(tools=[workflow])
agent.tool.workflow(
    action="create",
    workflow_id="data_analysis",
    tasks=[
        {
            "task_id": "data_extraction",
            "description": "レポートから主要データを抽出する"
        },
        {
            "task_id": "analysis",
            "description": "抽出されたデータを分析する",
            "dependencies": ["data_extraction"]
        }
    ]
)
```

## 適切なアプローチの選択

- **エージェントをツールとして使用**: 専門的な専門知識を持つ明確な階層構造に最適
- **エージェントスウォーム**: 創発的知能を持つ協力的問題解決に理想的
- **エージェントグラフ**: 通信パターンの正確な制御に最適
- **エージェントワークフロー**: 明確な依存関係を持つ順次プロセスに最適

各アプローチは、複雑さ、制御、協力パターンの観点で異なるトレードオフを提供します。適切な選択は、特定のユースケースと要件によって決まります。
