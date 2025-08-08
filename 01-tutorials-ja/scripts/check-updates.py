#!/usr/bin/env python3
"""
原文の更新をチェックし、翻訳が必要なファイルを特定するスクリプト

使用方法:
    python scripts/check-updates.py
    python scripts/check-updates.py --verbose
"""

import os
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime

class UpdateChecker:
    def __init__(self, original_path="../01-tutorials", ja_path="."):
        self.original_path = Path(original_path)
        self.ja_path = Path(ja_path)
        self.sync_status_file = self.ja_path / "sync-status.json"
        
    def get_file_hash(self, file_path):
        """ファイルのハッシュ値を取得"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
    
    def get_file_mtime(self, file_path):
        """ファイルの最終更新時刻を取得"""
        try:
            return datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        except Exception:
            return None
    
    def load_sync_status(self):
        """同期状況ファイルを読み込み"""
        if self.sync_status_file.exists():
            try:
                with open(self.sync_status_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading sync status: {e}")
        
        return {
            "last_sync_check": datetime.now().isoformat(),
            "original_path": str(self.original_path),
            "sync_status": {}
        }
    
    def save_sync_status(self, status):
        """同期状況ファイルを保存"""
        status["last_sync_check"] = datetime.now().isoformat()
        try:
            with open(self.sync_status_file, 'w', encoding='utf-8') as f:
                json.dump(status, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving sync status: {e}")
    
    def find_translatable_files(self):
        """翻訳対象ファイルを検索"""
        translatable_extensions = {'.md', '.ipynb', '.py'}
        files = []
        
        for file_path in self.original_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in translatable_extensions:
                # 相対パスを取得
                rel_path = file_path.relative_to(self.original_path)
                files.append(rel_path)
        
        return files
    
    def check_updates(self, verbose=False):
        """更新チェックを実行"""
        print("🔍 原文の更新をチェック中...")
        
        if not self.original_path.exists():
            print(f"❌ 原文ディレクトリが見つかりません: {self.original_path}")
            return
        
        sync_status = self.load_sync_status()
        translatable_files = self.find_translatable_files()
        
        updates_needed = []
        new_files = []
        
        for rel_path in translatable_files:
            original_file = self.original_path / rel_path
            ja_file = self.ja_path / rel_path
            
            original_hash = self.get_file_hash(original_file)
            original_mtime = self.get_file_mtime(original_file)
            
            if original_hash is None:
                continue
            
            file_key = str(rel_path)
            
            # 新規ファイルかチェック
            if not ja_file.exists():
                new_files.append({
                    'file': file_key,
                    'original_path': str(original_file),
                    'ja_path': str(ja_file),
                    'status': 'new_file'
                })
                continue
            
            # 既存ファイルの更新チェック
            if file_key in sync_status["sync_status"]:
                stored_hash = sync_status["sync_status"][file_key].get("original_hash")
                if stored_hash != original_hash:
                    updates_needed.append({
                        'file': file_key,
                        'original_path': str(original_file),
                        'ja_path': str(ja_file),
                        'status': 'updated',
                        'original_mtime': original_mtime
                    })
            else:
                # 同期状況に記録がない場合
                updates_needed.append({
                    'file': file_key,
                    'original_path': str(original_file),
                    'ja_path': str(ja_file),
                    'status': 'not_tracked',
                    'original_mtime': original_mtime
                })
            
            # 同期状況を更新
            sync_status["sync_status"][file_key] = {
                "original_hash": original_hash,
                "original_modified": original_mtime,
                "needs_update": file_key in [item['file'] for item in updates_needed]
            }
        
        # 結果表示
        print(f"\n📊 チェック結果:")
        print(f"   翻訳対象ファイル総数: {len(translatable_files)}")
        print(f"   新規ファイル: {len(new_files)}")
        print(f"   更新が必要: {len(updates_needed)}")
        
        if new_files:
            print(f"\n🆕 新規ファイル:")
            for item in new_files:
                print(f"   - {item['file']}")
        
        if updates_needed:
            print(f"\n🔄 更新が必要なファイル:")
            for item in updates_needed:
                print(f"   - {item['file']} ({item['status']})")
        
        if not new_files and not updates_needed:
            print("✅ すべてのファイルが最新です")
        
        # 詳細表示
        if verbose and (new_files or updates_needed):
            print(f"\n📝 詳細情報:")
            for item in new_files + updates_needed:
                print(f"   ファイル: {item['file']}")
                print(f"   原文: {item['original_path']}")
                print(f"   日本語版: {item['ja_path']}")
                print(f"   状態: {item['status']}")
                if 'original_mtime' in item:
                    print(f"   原文更新日時: {item['original_mtime']}")
                print()
        
        # 同期状況を保存
        self.save_sync_status(sync_status)
        
        return {
            'new_files': new_files,
            'updates_needed': updates_needed,
            'total_files': len(translatable_files)
        }

def main():
    parser = argparse.ArgumentParser(description='原文の更新をチェック')
    parser.add_argument('--verbose', '-v', action='store_true', help='詳細情報を表示')
    parser.add_argument('--original', default='../01-tutorials', help='原文ディレクトリのパス')
    
    args = parser.parse_args()
    
    checker = UpdateChecker(original_path=args.original)
    result = checker.check_updates(verbose=args.verbose)
    
    # 終了コード設定（更新が必要な場合は1を返す）
    if result and (result['new_files'] or result['updates_needed']):
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()
