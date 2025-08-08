#!/usr/bin/env python3
"""
原文ディレクトリの構造変更を日本語版に同期するスクリプト

使用方法:
    python scripts/sync-structure.py
    python scripts/sync-structure.py --dry-run
"""

import os
import shutil
import argparse
from pathlib import Path

class StructureSync:
    def __init__(self, original_path="../01-tutorials", ja_path="."):
        self.original_path = Path(original_path)
        self.ja_path = Path(ja_path)
        
        # 同期対象外のファイル/ディレクトリ
        self.exclude_patterns = {
            'scripts', 'glossary', 'sync-status.json', 'MAINTENANCE.md',
            '.git', '__pycache__', '.DS_Store', '*.pyc'
        }
    
    def should_exclude(self, path):
        """除外対象かどうかを判定"""
        path_name = path.name
        return any(pattern in path_name for pattern in self.exclude_patterns)
    
    def sync_structure(self, dry_run=False):
        """ディレクトリ構造を同期"""
        print("🔄 ディレクトリ構造を同期中...")
        
        if not self.original_path.exists():
            print(f"❌ 原文ディレクトリが見つかりません: {self.original_path}")
            return
        
        changes = {
            'new_dirs': [],
            'new_files': [],
            'removed_items': []
        }
        
        # 新規ディレクトリとファイルの検出
        for original_item in self.original_path.rglob('*'):
            if self.should_exclude(original_item):
                continue
                
            rel_path = original_item.relative_to(self.original_path)
            ja_item = self.ja_path / rel_path
            
            if original_item.is_dir() and not ja_item.exists():
                changes['new_dirs'].append(str(rel_path))
                if not dry_run:
                    ja_item.mkdir(parents=True, exist_ok=True)
                    print(f"📁 ディレクトリ作成: {rel_path}")
            
            elif original_item.is_file() and not ja_item.exists():
                changes['new_files'].append(str(rel_path))
                if not dry_run:
                    ja_item.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(original_item, ja_item)
                    print(f"📄 ファイル追加: {rel_path}")
        
        # 削除されたアイテムの検出（オプション）
        for ja_item in self.ja_path.rglob('*'):
            if self.should_exclude(ja_item):
                continue
                
            rel_path = ja_item.relative_to(self.ja_path)
            original_item = self.original_path / rel_path
            
            if not original_item.exists():
                changes['removed_items'].append(str(rel_path))
                # 注意: 自動削除は危険なので、手動確認を推奨
                print(f"⚠️  原文で削除されたアイテム: {rel_path} (手動確認が必要)")
        
        # 結果表示
        print(f"\n📊 同期結果:")
        print(f"   新規ディレクトリ: {len(changes['new_dirs'])}")
        print(f"   新規ファイル: {len(changes['new_files'])}")
        print(f"   削除されたアイテム: {len(changes['removed_items'])}")
        
        if dry_run:
            print("\n🔍 ドライランモード - 実際の変更は行われませんでした")
            if changes['new_dirs']:
                print("作成予定のディレクトリ:")
                for item in changes['new_dirs']:
                    print(f"   + {item}")
            if changes['new_files']:
                print("追加予定のファイル:")
                for item in changes['new_files']:
                    print(f"   + {item}")
        
        return changes

def main():
    parser = argparse.ArgumentParser(description='ディレクトリ構造を同期')
    parser.add_argument('--dry-run', action='store_true', help='実際の変更を行わずに確認のみ')
    parser.add_argument('--original', default='../01-tutorials', help='原文ディレクトリのパス')
    
    args = parser.parse_args()
    
    syncer = StructureSync(original_path=args.original)
    result = syncer.sync_structure(dry_run=args.dry_run)
    
    # 変更があった場合は終了コード1を返す
    if result and (result['new_dirs'] or result['new_files']):
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()
