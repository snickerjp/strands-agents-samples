<!-- 原文: ../01-tutorials/README.md -->
<!-- 最終同期: 2024-08-08 -->

# Strands Agents チュートリアル（日本語版）

このディレクトリは、[Strands Agents](https://strandsagents.com) の日本語版チュートリアルです。

## 📚 目次

- [📚 目次](#-目次)
- [🎯 このチュートリアルについて](#-このチュートリアルについて)
- [🏁 はじめに](#-はじめに)
- [📖 チュートリアル構成](#-チュートリアル構成)
  - [01-fundamentals（基礎編）](#01-fundamentals基礎編)
  - [02-multi-agent-systems（マルチエージェントシステム）](#02-multi-agent-systemsマルチエージェントシステム)
  - [03-deployment（デプロイメント）](#03-deploymentデプロイメント)
- [🔧 メンテナンス](#-メンテナンス)
- [📝 翻訳について](#-翻訳について)

## 🎯 このチュートリアルについて

このチュートリアルでは、Strands Agentsを使用してAIエージェントを構築する方法を段階的に学習できます。基礎的な概念から実際のデプロイメントまで、実践的な例を通して理解を深めることができます。

## 🏁 はじめに

### 前提条件
- Python 3.8以上
- 基本的なPythonプログラミング知識
- AWS アカウント（AWSサービス連携の章で必要）

### インストール
```bash
pip install strands-agents
pip install strands-agents-tools
```

### モデルプロバイダーの設定
[こちらの手順](https://strandsagents.com/latest/user-guide/quickstart/#model-providers)に従って、使用するモデルプロバイダーを設定してください。

## 📖 チュートリアル構成

### 01-fundamentals（基礎編）
Strands Agentsの基本的な使い方を学習します。

| 例 | 説明 | 紹介する機能 |
|---------|------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| F1      | [初めてのStrands Agent作成](01-fundamentals/01-first-agent)                     | エージェントの初期化、デフォルトツールの使用、カスタムツールの作成                              |
| F2      | [モデルプロバイダー - OpenAI](01-fundamentals/02-model-providers/02-openai-model)     | GPT 4.0をモデルとしたエージェントの作成                                                                   |
| F2      | [モデルプロバイダー - Ollama](01-fundamentals/02-model-providers/01-ollama-model)     | Ollamaモデルを使用したエージェントの作成                                                                       |
| F3      | [AWSサービスとの連携](01-fundamentals/03-connecting-with-aws-services)    | Amazon Bedrock Knowledge BaseとAmazon DynamoDBへの接続                                      |
| F4      | [ツール - MCPツールの使用](01-fundamentals/04-tools/01-using-mcp-tools)                     | エージェントへのMCPツール呼び出しの統合                                                           |
| F4      | [ツール - カスタムツール](01-fundamentals/04-tools/02-custom-tools)                           | エージェントでのカスタムツールの作成と使用                                                      |
| F5      | [エージェント応答の高度な処理](01-fundamentals/05-advance-processing-agent-response)       | 非同期イテレータやコールバック（ストリームハンドラー）を使用したエージェント応答のストリーミング                 |
| F6      | [Bedrockガードレール統合](01-fundamentals/06-guardrail-integration)          | エージェントへのAmazon Bedrockガードレールの統合                                                  |
| F7      | [エージェントへのメモリ追加](01-fundamentals/07-memory-persistent-agents)         | メモリとウェブ検索ツールを使用したパーソナルアシスタント                                                  |
| F8     | [観測可能性と評価](01-fundamentals/08-observability-and-evaluation)    | エージェントへの観測可能性と評価の追加                                                    |

### 02-multi-agent-systems（マルチエージェントシステム）
複数のエージェントを組み合わせたシステムの構築方法を学習します。

| 例 | 説明 | 紹介する機能 |
|---------|------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| M1      | [エージェントをツールとして使用](02-multi-agent-systems/01-agent-as-tool) | エージェントをツールとして使用したマルチエージェント協調の例を作成                                |
| M2      | [スウォームエージェントの作成](02-multi-agent-systems/02-swarm-agent) | 複数のAIエージェントが連携して動作するマルチエージェントシステムの作成                   |
| M3      | [グラフエージェントの作成](02-multi-agent-systems/03-graph-agent) | 定義された通信パターンを持つ専門化されたAIエージェントの構造化ネットワークの作成         |

### 03-deployment（デプロイメント）
エージェントを本番環境にデプロイする方法を学習します。

| 例 | 説明 | 紹介する機能 |
|---------|------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| D1      | [AWS Lambdaデプロイメント](03-deployment/01-lambda-deployment)       | エージェントのAWS Lambda関数へのデプロイ                                                  |
| D2      | [AWS Fargateデプロイメント](03-deployment/02-fargate-deployment)     | エージェントのAWS Fargateへのデプロイ                                                             |

## 🔧 メンテナンス

このディレクトリには、原文の更新に追従するためのメンテナンス機能が含まれています。

### 更新チェック
```bash
cd 01-tutorials-ja
python scripts/check-updates.py
```

### 翻訳状況確認
```bash
python scripts/translation-status.py --format table
```

### 構造同期
```bash
python scripts/sync-structure.py
```

詳細は [MAINTENANCE.md](MAINTENANCE.md) を参照してください。

## 📝 翻訳について

### 翻訳方針
- 技術的正確性を保ちつつ、日本語として自然な表現を心がけています
- 専門用語は [glossary/technical-terms.json](glossary/technical-terms.json) で統一管理
- 翻訳スタイルは [glossary/style-guide.md](glossary/style-guide.md) に準拠

### 貢献方法
翻訳の改善提案や誤訳の報告は、GitHubのIssueまたはPull Requestでお願いします。

---

**注意**: このチュートリアルの例は**デモンストレーションと教育目的**のみです。本番環境で使用する前に、適切な**セキュリティ**と**テスト**手順を適用してください。
