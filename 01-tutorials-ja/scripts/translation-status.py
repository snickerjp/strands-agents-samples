#!/usr/bin/env python3
"""
翻訳状況を確認・表示するスクリプト

使用方法:
    python scripts/translation-status.py
    python scripts/translation-status.py --format table
    python scripts/translation-status.py --format json
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime

class TranslationStatus:
    def __init__(self, original_path="../01-tutorials", ja_path="."):
        self.original_path = Path(original_path)
        self.ja_path = Path(ja_path)
        self.sync_status_file = self.ja_path / "sync-status.json"
    
    def load_sync_status(self):
        """同期状況ファイルを読み込み"""
        if self.sync_status_file.exists():
            try:
                with open(self.sync_status_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading sync status: {e}")
        return {"sync_status": {}}
    
    def check_translation_markers(self, file_path):
        """ファイル内の翻訳マーカーをチェック"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 翻訳マーカーの検出
            markers = {
                'has_ja_header': '<!-- 原文:' in content or '<!-- Original:' in content,
                'has_translation_note': '翻訳' in content or 'Translation' in content,
                'has_japanese_content': any(ord(char) > 127 for char in content[:1000])  # 簡易的な日本語検出
            }
            
            return markers
        except Exception:
            return {'has_ja_header': False, 'has_translation_note': False, 'has_japanese_content': False}
    
    def analyze_translation_status(self):
        """翻訳状況を分析"""
        sync_status = self.load_sync_status()
        translatable_extensions = {'.md', '.ipynb', '.py'}
        
        status_data = {
            'total_files': 0,
            'translated_files': 0,
            'pending_files': 0,
            'new_files': 0,
            'files': []
        }
        
        # 翻訳対象ファイルを検索
        for file_path in self.ja_path.rglob('*'):
            if (file_path.is_file() and 
                file_path.suffix in translatable_extensions and
                'scripts' not in file_path.parts and
                'glossary' not in file_path.parts):
                
                rel_path = str(file_path.relative_to(self.ja_path))
                original_file = self.original_path / rel_path
                
                status_data['total_files'] += 1
                
                # 翻訳状況の判定
                translation_markers = self.check_translation_markers(file_path)
                sync_info = sync_status.get('sync_status', {}).get(rel_path, {})
                
                # ステータス判定
                if not original_file.exists():
                    file_status = 'orphaned'  # 原文が存在しない
                elif translation_markers['has_japanese_content'] or translation_markers['has_ja_header']:
                    file_status = 'translated'
                    status_data['translated_files'] += 1
                elif sync_info.get('needs_update', True):
                    file_status = 'needs_update'
                    status_data['pending_files'] += 1
                else:
                    file_status = 'pending'
                    status_data['pending_files'] += 1
                
                file_info = {
                    'file': rel_path,
                    'status': file_status,
                    'has_original': original_file.exists(),
                    'original_modified': sync_info.get('original_modified', 'unknown'),
                    'needs_update': sync_info.get('needs_update', True),
                    'translation_markers': translation_markers
                }
                
                status_data['files'].append(file_info)
        
        return status_data
    
    def display_status(self, format_type='summary'):
        """翻訳状況を表示"""
        status_data = self.analyze_translation_status()
        
        if format_type == 'json':
            print(json.dumps(status_data, indent=2, ensure_ascii=False))
            return
        
        # サマリー表示
        print("📊 翻訳状況サマリー")
        print(f"   総ファイル数: {status_data['total_files']}")
        print(f"   翻訳済み: {status_data['translated_files']}")
        print(f"   翻訳待ち: {status_data['pending_files']}")
        print(f"   進捗率: {status_data['translated_files']/status_data['total_files']*100:.1f}%" if status_data['total_files'] > 0 else "   進捗率: 0%")
        
        if format_type == 'table':
            print(f"\n📋 詳細状況:")
            print(f"{'ファイル':<50} {'状態':<15} {'更新必要':<10} {'原文更新日':<20}")
            print("-" * 95)
            
            for file_info in sorted(status_data['files'], key=lambda x: x['file']):
                status_icon = {
                    'translated': '✅',
                    'pending': '⏳',
                    'needs_update': '🔄',
                    'orphaned': '❓'
                }.get(file_info['status'], '❓')
                
                update_needed = '要' if file_info['needs_update'] else '不要'
                original_date = file_info['original_modified'][:10] if file_info['original_modified'] != 'unknown' else 'unknown'
                
                print(f"{file_info['file']:<50} {status_icon} {file_info['status']:<12} {update_needed:<10} {original_date:<20}")
        
        # 翻訳が必要なファイルのリスト
        needs_translation = [f for f in status_data['files'] if f['status'] in ['pending', 'needs_update']]
        if needs_translation:
            print(f"\n🔄 翻訳が必要なファイル ({len(needs_translation)}件):")
            for file_info in needs_translation[:10]:  # 最初の10件のみ表示
                print(f"   - {file_info['file']} ({file_info['status']})")
            if len(needs_translation) > 10:
                print(f"   ... 他 {len(needs_translation) - 10} 件")

def main():
    parser = argparse.ArgumentParser(description='翻訳状況を確認')
    parser.add_argument('--format', choices=['summary', 'table', 'json'], default='summary', help='表示形式')
    parser.add_argument('--original', default='../01-tutorials', help='原文ディレクトリのパス')
    
    args = parser.parse_args()
    
    checker = TranslationStatus(original_path=args.original)
    checker.display_status(format_type=args.format)

if __name__ == "__main__":
    main()
