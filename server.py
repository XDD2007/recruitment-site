#!/usr/bin/env python3
"""招生表单数据接收服务 - 数据存本地，不经过云端"""
from flask import Flask, request, jsonify
import json, os, time
from datetime import datetime

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'submissions.json')

# IP提交频率限制: 60秒内同一IP只能提交一次
rate_limit = {}

def check_rate_limit(ip):
    now = time.time()
    if ip in rate_limit:
        if now - rate_limit[ip] < 60:
            return False, 60 - int(now - rate_limit[ip])
    rate_limit[ip] = now
    return True, 0

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(entries):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        ip = request.remote_addr
        allowed, wait = check_rate_limit(ip)
        if not allowed:
            return jsonify({'error': f'提交太频繁，请{wait}秒后再试'}), 429
        
        data = request.get_json()
        required = ['name', 'phone', 'idcard', 'examid']
        for field in required:
            if not data.get(field, '').strip():
                return jsonify({'error': f'必填字段缺失: {field}'}), 400
        
        entry = {
            'name': data['name'].strip(),
            'phone': data['phone'].strip(),
            'idcard': data['idcard'].strip(),
            'examid': data.get('examid', '').strip(),
            'school': data['school'].strip(),
            'message': data.get('message', '').strip() or '(未填写)',
            'submitted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        entries = load_data()
        entries.append(entry)
        save_data(entries)
        
        print(f"[+] 新提交: {entry['name']} {entry['phone']} - {entry['submitted_at']}")
        return jsonify({'success': True, 'message': '提交成功！'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

VIEW_PASSWORD = 'xdd888'

@app.route('/view', methods=['GET'])
def view():
    """查看所有提交 - 需要密码"""
    key = request.args.get('key', '')
    if key != VIEW_PASSWORD:
        html = '<html><head><meta charset="utf-8"><title>需要密码</title>'
        html += '<style>body{font-family:sans-serif;text-align:center;margin-top:80px}'
        html += 'input{padding:10px 16px;font-size:16px;border:1px solid #ccc;border-radius:6px}'
        html += 'button{padding:10px 24px;font-size:16px;background:#2563eb;color:#fff;border:none;border-radius:6px;cursor:pointer}'
        html += '</style></head><body>'
        html += '<h2>🔒 需要访问密码</h2>'
        html += '<form method="get"><input type="password" name="key" placeholder="请输入查看密码"><br><br><button type="submit">确认</button></form>'
        html += '</body></html>'
        return html, 403
    entries = load_data()
    html = '<html><head><meta charset="utf-8"><title>招生咨询 - 提交记录</title>'
    html += '<style>body{font-family:sans-serif;max-width:900px;margin:20px auto;padding:0 20px}'
    html += 'table{border-collapse:collapse;width:100%}th,td{border:1px solid #ddd;padding:8px;text-align:left}'
    html += 'th{background:#f5f5f5}tr:hover{background:#fafafa}</style></head><body>'
    html += f'<h2>📋 招生咨询提交记录 ({len(entries)}条)</h2>'
    html += '<table><tr><th>时间</th><th>姓名</th><th>手机号</th><th>身份证号</th><th>准考证号</th><th>毕业学校</th><th>留言</th></tr>'
    for e in reversed(entries):
        html += f'<tr><td>{e["submitted_at"]}</td><td>{e["name"]}</td><td>{e["phone"]}</td><td>{e["idcard"]}</td><td>{e.get("examid","")}</td><td>{e["school"]}</td><td>{e["message"]}</td></tr>'
    html += '</table></body></html>'
    return html

if __name__ == '__main__':
    print(f'📡 招生表单后端启动: http://127.0.0.1:5050')
    print(f'📁 数据文件: {DATA_FILE}')
    app.run(host='127.0.0.1', port=5050, debug=False)
