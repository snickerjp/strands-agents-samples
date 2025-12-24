#!/usr/bin/env python3
"""
新しい日本語版ディレクトリを自動セットアップするスクリプト

使用方法:
    python setup-ja-directory.py 02-samples
    python setup-ja-directory.py 03-integrations
    python setup-ja-directory.py --all
"""

import shutil
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JaDirectorySetupError(Exception):
    """日本語版ディレクトリセットアップ用カスタム例外"""
    pass


class DirectoryManager:
    """ディレクトリ操作の抽象化層"""

    @staticmethod
    def copy_directory(src: Path, dst: Path, exclude: set = None) -> int:
        """ディレクトリをコピーし、コピーされたファイル数を返す"""
        exclude = exclude or set()
        copied_count = 0

        try:
            for item in src.rglob('*'):
                if any(exclude_pattern in item.parts for exclude_pattern in exclude):
                    continue

                rel_path = item.relative_to(src)
                target_item = dst / rel_path

                if item.is_dir():
                    target_item.mkdir(parents=True, exist_ok=True)
                elif item.is_file():
                    target_item.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, target_item)
                    copied_count += 1
        except Exception as e:
            raise JaDirectorySetupError(f"ディレクトリコピーに失敗: {src} -> {dst}: {e}") from e

        return copied_count

    @staticmethod
    def copy_tree(src: Path, dst: Path) -> None:
        """ディレクトリツリー全体をコピー"""
        try:
            shutil.copytree(src, dst, dirs_exist_ok=True)
        except Exception as e:
            raise JaDirectorySetupError(f"ディレクトリツリーコピーに失敗: {src} -> {dst}: {e}") from e


class Config:
    """設定クラス"""
    EXCLUDED_DIRS = {'_templates', 'agent-patterns', '.git', '__pycache__'}
    EXCLUDED_FILES_ITEMS = {'scripts', 'glossary', 'sync-status.json', 'MAINTENANCE.md'}
    TEMPLATE_RELATIVE_PATH = "01-tutorials-ja"
    SYNC_STATUS_VERSION = "1.0"


class JaDirectorySetup:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.template_path = self.base_path / Config.TEMPLATE_RELATIVE_PATH
        self._validate_template_path()

    def _validate_template_path(self) -> None:
        """テンプレートパスの存在確認"""
        if not self.template_path.exists():
            raise JaDirectorySetupError(f"テンプレートディレクトリが見つかりません: {self.template_path}")

    def get_available_directories(self) -> List[Dict[str, any]]:
        """日本語化可能なディレクトリを検索"""
        directories = []
        try:
            for item in self.base_path.iterdir():
                if (item.is_dir() and
                    not item.name.endswith('-ja') and
                    not item.name.startswith('.') and
                    item.name not in Config.EXCLUDED_DIRS):
                    ja_dir = self.base_path / f"{item.name}-ja"
                    directories.append({
                        'original': item.name,
                        'ja_dir': f"{item.name}-ja",
                        'exists': ja_dir.exists()
                    })
        except Exception as e:
            logger.error(f"ディレクトリ列挙に失敗: {e}")
            raise JaDirectorySetupError(f"ディレクトリ列挙に失敗: {e}") from e
    def copy_maintenance_structure(self, target_dir: str, original_dir: str) -> Path:
        """メンテナンス構造をコピー"""
        target_path = self.base_path / target_dir

        try:
            # 基本ディレクトリ作成
            target_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"ターゲットディレクトリ作成: {target_path}")

            # scriptsディレクトリをコピー
            self._copy_template_directory("scripts", target_path)

            # glossaryディレクトリをコピー
            self._copy_template_directory("glossary", target_path)

            # MAINTENANCE.mdをコピー（パスを調整）
            self._copy_template_file_with_replacement(
                "MAINTENANCE.md", target_path, original_dir
            )

            # 初期sync-status.jsonを作成
            self._create_sync_status(target_path, original_dir)

        except Exception as e:
            logger.error(f"メンテナンス構造コピーに失敗: {e}")
            raise

        return target_path

    def _copy_template_directory(self, dir_name: str, target_path: Path) -> None:
        """テンプレートディレクトリをコピー"""
        src = self.template_path / dir_name
        dst = target_path / dir_name

        if not src.exists():
            logger.warning(f"テンプレートディレクトリが見つかりません: {src}")
            return

        try:
            DirectoryManager.copy_tree(src, dst)
            logger.info(f"ディレクトリをコピー: {dir_name}")
        except JaDirectorySetupError as e:
            logger.warning(f"{dir_name} のコピーに失敗しましたがスキップ: {e}")

    def _copy_template_file_with_replacement(
        self, file_name: str, target_path: Path, original_dir: str
    ) -> None:
        """テンプレートファイルをコピーして置換"""
        src = self.template_path / file_name
        dst = target_path / file_name

        if not src.exists():
            logger.warning(f"テンプレートファイルが見つかりません: {src}")
            return

        try:
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()

            # パスを調整
            content = content.replace('../01-tutorials', f'../{original_dir}')

            with open(dst, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"ファイルを作成: {file_name}")
        except Exception as e:
            raise JaDirectorySetupError(f"{file_name} のコピーに失敗: {e}") from e

    def _create_sync_status(self, target_path: Path, original_dir: str) -> None:
        """sync-status.jsonを作成"""
        now = datetime.now().isoformat()
        sync_status = {
            "last_sync_check": now,
            "original_path": f"../{original_dir}",
            "sync_status": {},
            "created_date": now,
            "version": Config.SYNC_STATUS_VERSION,
            "notes": f"初期セットアップ時に作成。{original_dir}の日本語版ディレクトリです。"
        }

        sync_status_path = target_path / "sync-status.json"

        try:
            with open(sync_status_path, 'w', encoding='utf-8') as f:
                json.dump(sync_status, f, indent=2, ensure_ascii=False)
            logger.info("sync-status.jsonを作成")
        except Exception as e:
            raise JaDirectorySetupError(f"sync-status.json の作成に失敗: {e}") from e

    def copy_original_content(self, target_dir: str, original_dir: str) -> bool:
        """原文コンテンツをコピー"""
        target_path = self.base_path / target_dir
        original_path = self.base_path / original_dir

        if not original_path.exists():
            logger.error(f"原文ディレクトリが見つかりません: {original_path}")
            raise JaDirectorySetupError(f"原文ディレクトリが見つかりません: {original_path}")

        try:
            copied_count = DirectoryManager.copy_directory(
                original_path, target_path, Config.EXCLUDED_FILES_ITEMS
            )
            logger.info(f"{copied_count}個のファイルをコピー")
            return True
        except JaDirectorySetupError as e:
            logger.error(f"原文コンテンツのコピーに失敗: {e}")
            return False

    def create_readme(self, target_dir: str, original_dir: str) -> None:
        """日本語版READMEを作成"""
        target_path = self.base_path / target_dir
        readme_path = target_path / "README.md"

        readme_content = f"""<!-- 原文: ../{original_dir}/README.md -->
<!-- 最終同期: {datetime.now().strftime('%Y-%m-%d')} -->

# {original_dir.replace('-', ' ').title()}（日本語版）

このディレクトリは、[{original_dir}](../{original_dir}) の日本語版です。

## 🎯 このディレクトリについて

{original_dir}の内容を日本語に翻訳し、日本語学習者にとって理解しやすい形で提供します。

## 🔧 メンテナンス

このディレクトリには、原文の更新に追従するためのメンテナンス機能が含まれています。

### 更新チェック
```bash
cd {target_dir}
python3 scripts/check-updates.py
```

### 翻訳状況確認
```bash
python3 scripts/translation-status.py --format table
```

### 構造同期
```bash
python3 scripts/sync-structure.py
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

**注意**: この例は**デモンストレーションと教育目的**のみです。本番環境で使用する前に、適切な**セキュリティ**と**テスト**手順を適用してください。"""

        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            logger.info("README.mdを作成")
        except Exception as e:
            raise JaDirectorySetupError(f"README.md の作成に失敗: {e}") from e

    def _set_executable_permissions(self, target_path: Path) -> None:
        """スクリプトに実行権限を付与"""
        scripts_dir = target_path / "scripts"
        if not scripts_dir.exists():
            logger.debug(f"scriptsディレクトリが見つかりません: {scripts_dir}")
            return

        try:
            for script in scripts_dir.glob("*.py"):
                script.chmod(0o755)
            logger.debug("スクリプトに実行権限を付与")
        except Exception as e:
            logger.warning(f"実行権限の付与に失敗: {e}")

    def setup_directory(self, original_dir: str) -> bool:
        """指定されたディレクトリの日本語版をセットアップ"""
        target_dir = f"{original_dir}-ja"

        logger.info(f"'{target_dir}' のセットアップを開始")

        try:
            # メンテナンス構造をコピー
            target_path = self.copy_maintenance_structure(target_dir, original_dir)

            # 原文コンテンツをコピー
            if not self.copy_original_content(target_dir, original_dir):
                logger.error(f"'{target_dir}' のセットアップに失敗（原文コンテンツコピー失敗）")
                return False

            # READMEを作成
            self.create_readme(target_dir, original_dir)

            # スクリプトに実行権限を付与
            self._set_executable_permissions(target_path)

            logger.info(f"✅ '{target_dir}' のセットアップが完了しました")
            return True

        except JaDirectorySetupError as e:
            logger.error(f"❌ '{target_dir}' のセットアップに失敗しました: {e}")
            return False

    def setup_all_directories(self) -> int:
        """すべての利用可能なディレクトリをセットアップ"""
        try:
            directories = self.get_available_directories()

            logger.info("📋 利用可能なディレクトリ:")
            for dir_info in directories:
                status = "✅ 存在" if dir_info['exists'] else "❌ 未作成"
                logger.info(f"   {dir_info['original']} -> {dir_info['ja_dir']} ({status})")

            success_count = 0
            for dir_info in directories:
                if not dir_info['exists']:
                    if self.setup_directory(dir_info['original']):
                        success_count += 1
                    logger.info("")

            logger.info(f"🎉 {success_count}個のディレクトリをセットアップしました")
            return success_count

        except Exception as e:
            logger.error(f"全体セットアップに失敗: {e}")
            return 0

def main():
    parser = argparse.ArgumentParser(description='日本語版ディレクトリを自動セットアップ')
    parser.add_argument('directory', nargs='?', help='セットアップする原文ディレクトリ名')
    parser.add_argument('--all', action='store_true', help='すべての利用可能なディレクトリをセットアップ')
    parser.add_argument('--list', action='store_true', help='利用可能なディレクトリを一覧表示')
    parser.add_argument('--verbose', action='store_true', help='詳細ログを出力')

    args = parser.parse_args()

    # ログレベル調整
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    try:
        setup = JaDirectorySetup()

        if args.list:
            directories = setup.get_available_directories()
            logger.info("📋 利用可能なディレクトリ:")
            for dir_info in directories:
                status = "✅ 存在" if dir_info['exists'] else "❌ 未作成"
                logger.info(f"   {dir_info['original']} -> {dir_info['ja_dir']} ({status})")
        elif args.all:
            setup.setup_all_directories()
        elif args.directory:
            setup.setup_directory(args.directory)
        else:
            parser.print_help()

    except JaDirectorySetupError as e:
        logger.error(f"エラー: {e}")
        return 1
    except Exception as e:
        logger.error(f"予期しないエラー: {e}", exc_info=True)
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
