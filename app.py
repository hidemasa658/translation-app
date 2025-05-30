# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from googletrans import Translator
import json

app = Flask(__name__)
translator = Translator()

# 言語コードの辞書
LANGUAGES = {
    'japanese': 'ja',
    'english': 'en',
    'chinese': 'zh'
}

# 言語ペアの設定
LANGUAGE_PAIRS = [
    {'name': '日本語 ⇔ 英語', 'lang1': 'ja', 'lang2': 'en', 'display1': '日本語', 'display2': 'English'},
    {'name': '日本語 ⇔ 中国語', 'lang1': 'ja', 'lang2': 'zh', 'display1': '日本語', 'display2': '中文'},
    {'name': '英語 ⇔ 中国語', 'lang1': 'en', 'lang2': 'zh', 'display1': 'English', 'display2': '中文'}
]

@app.route('/')
def index():
    return render_template('index.html', language_pairs=LANGUAGE_PAIRS)

@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        source_lang = data.get('source_lang', 'ja')
        target_lang = data.get('target_lang', 'en')
        
        if not text.strip():
            return jsonify({'error': 'テキストが空です'}), 400
        
        # 翻訳実行
        result = translator.translate(text, src=source_lang, dest=target_lang)
        
        return jsonify({
            'original_text': text,
            'translated_text': result.text,
            'source_lang': source_lang,
            'target_lang': target_lang
        })
        
    except Exception as e:
        print("翻訳エラー: " + str(e))
        return jsonify({'error': '翻訳に失敗しました'}), 500

@app.route('/detect_language', methods=['POST'])
def detect_language():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'テキストが空です'}), 400
        
        # 言語検出
        detection = translator.detect(text)
        detected_lang = detection.lang
        confidence = detection.confidence
        
        return jsonify({
            'detected_language': detected_lang,
            'confidence': confidence
        })
        
    except Exception as e:
        print("言語検出エラー: " + str(e))
        return jsonify({'error': '言語検出に失敗しました'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)