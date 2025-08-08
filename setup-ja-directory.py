#!/usr/bin/env python3
"""
新しい日本語版ディレクトリを自動セットアップするスクリプト

使用方法:
    python setup-ja-directory.py 02-samples
    python setup-ja-directory.py 03-integrations
    python setup-ja-directory.py --all
"""

import os
import shutil
import json
import argparse
from pathlib import Path
from datetime import datetime

class JaDirectorySetup:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.template_path = self.base_path / "01-tutorials-ja"
        
    def get_available_directories(self):
        """日本語化可能なディレクトリを検索"""
        directories = []
        for item in self.base_path.iterdir():
            if (item.is_dir() and 
                not item.name.endswith('-ja') and 
                not item.name.startswith('.') and
                item.name not in ['_templates', 'agent-patterns']):  # 除外ディレクトリ
                ja_dir = self.base_path / f"{item.name}-ja"
                directories.append({
                    'original': item.name,
                    'ja_dir': f"{item.name}-ja",
                    'exists': ja_dir.exists()
                })
        return directories
    
    def copy_maintenance_structure(self, target_dir, original_dir):
        """メンテナンス構造をコピー"""
        target_path = self.base_path / target_dir
        original_path = self.base_path / original_dir
        
        # 基本ディレクトリ作成
        target_path.mkdir(exist_ok=True)
        
        # scriptsディレクトリとファイルをコピー
        scripts_src = self.template_path / "scripts"
        scripts_dst = target_path / "scripts"
        if scripts_src.exists():
            shutil.copytree(scripts_src, scripts_dst, dirs_exist_ok=True)
            print(f"📁 scriptsディレクトリをコピー: {scripts_dst}")
        
        # glossaryディレクトリとファイルをコピー
        glossary_src = self.template_path / "glossary"
        glossary_dst = target_path / "glossary"
        if glossary_src.exists():
            shutil.copytree(glossary_src, glossary_dst, dirs_exist_ok=True)
            print(f"📁 glossaryディレクトリをコピー: {glossary_dst}")
        
        # MAINTENANCE.mdをコピー（パスを調整）
        maintenance_src = self.template_path / "MAINTENANCE.md"
        maintenance_dst = target_path / "MAINTENANCE.md"
        if maintenance_src.exists():
            with open(maintenance_src, 'r', encoding='utf-8') as f:
                content = f.read()
            # パスを調整
            content = content.replace('../01-tutorials', f'../{original_dir}')
            with open(maintenance_dst, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📄 MAINTENANCE.mdを作成: {maintenance_dst}")
        
        # 初期sync-status.jsonを作成
        sync_status = {
            "last_sync_check": datetime.now().isoformat(),
            "original_path": f"../{original_dir}",
            "sync_status": {},
            "created_date": datetime.now().isoformat(),
            "version": "1.0",
            "notes": f"初期セットアップ時に作成。{original_dir}の日本語版ディレクトリです。"
        }
        
        sync_status_path = target_path / "sync-status.json"
        with open(sync_status_path, 'w', encoding='utf-8') as f:
            json.dump(sync_status, f, indent=2, ensure_ascii=False)
        print(f"📄 sync-status.jsonを作成: {sync_status_path}")
        
        return target_path
    
    def copy_original_content(self, target_dir, original_dir):
        """原文コンテンツをコピー"""
        target_path = self.base_path / target_dir
        original_path = self.base_path / original_dir
        
        if not original_path.exists():
            print(f"❌ 原文ディレクトリが見つかりません: {original_path}")
            return False
        
        # 除外するアイテム
        exclude_items = {'scripts', 'glossary', 'sync-status.json', 'MAINTENANCE.md'}
        
        copied_count = 0
        for item in original_path.rglob('*'):
            if any(exclude in item.parts for exclude in exclude_items):
                continue
                
            rel_path = item.relative_to(original_path)
            target_item = target_path / rel_path
            
            if item.is_dir():
                target_item.mkdir(parents=True, exist_ok=True)
            elif item.is_file():
                target_item.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target_item)
                copied_count += 1
        
        print(f"📄 {copied_count}個のファイルをコピー")
        return True
    
    def create_readme(self, target_dir, original_dir):
        """日本語版READMEを作成"""
        target_path = self.base_path / target_dir
        readme_path = target_path / "README.md"
        
        # 原文READMEの存在確認
        original_readme = self.base_path / original_dir / "README.md"
        
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

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"📄 README.mdを作成: {readme_path}")
    
    def setup_directory(self, original_dir):
        """指定されたディレクトリの日本語版をセットアップ"""
        target_dir = f"{original_dir}-ja"
        
        print(f"🚀 {target_dir} のセットアップを開始...")
        
        # メンテナンス構造をコピー
        target_path = self.copy_maintenance_structure(target_dir, original_dir)
        
        # 原文コンテンツをコピー
        if self.copy_original_content(target_dir, original_dir):
            # READMEを作成
            self.create_readme(target_dir, original_dir)
            
            # スクリプトに実行権限を付与
            scripts_dir = target_path / "scripts"
            if scripts_dir.exists():
                for script in scripts_dir.glob("*.py"):
                    script.chmod(0o755)
            
            print(f"✅ {target_dir} のセットアップが完了しました")
            return True
        else:
            print(f"❌ {target_dir} のセットアップに失敗しました")
            return False
    
    def setup_all_directories(self):
        """すべての利用可能なディレクトリをセットアップ"""
        directories = self.get_available_directories()
        
        print("📋 利用可能なディレクトリ:")
        for dir_info in directories:
            status = "✅ 存在" if dir_info['exists'] else "❌ 未作成"
            print(f"   {dir_info['original']} -> {dir_info['ja_dir']} ({status})")
        
        print()
        success_count = 0
        for dir_info in directories:
            if not dir_info['exists']:
                if self.setup_directory(dir_info['original']):
                    success_count += 1
                print()
        
        print(f"🎉 {success_count}個のディレクトリをセットアップしました")

def main():
    parser = argparse.ArgumentParser(description='日本語版ディレクトリを自動セットアップ')
    parser.add_argument('directory', nargs='?', help='セットアップする原文ディレクトリ名')
    parser.add_argument('--all', action='store_true', help='すべての利用可能なディレクトリをセットアップ')
    parser.add_argument('--list', action='store_true', help='利用可能なディレクトリを一覧表示')
    
    args = parser.parse_args()
    
    setup = JaDirectorySetup()
    
    if args.list:
        directories = setup.get_available_directories()
        print("📋 利用可能なディレクトリ:")
        for dir_info in directories:
            status = "✅ 存在" if dir_info['exists'] else "❌ 未作成"
            print(f"   {dir_info['original']} -> {dir_info['ja_dir']} ({status})")
    elif args.all:
        setup.setup_all_directories()
    elif args.directory:
        setup.setup_directory(args.directory)
    else:
        print("使用方法:")
        print("  python setup-ja-directory.py 02-samples")
        print("  python setup-ja-directory.py --all")
        print("  python setup-ja-directory.py --list")

if __name__ == "__main__":
    main()
