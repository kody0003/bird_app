# coding: utf-8

from flask import Flask, render_template

# app という変数でFlaskオブジェクトをインスタンス化
app = Flask(__name__)

# --- View 側の設定 ---
# rootディレクトリにアクセスした場合の挙動
@app.route('/')

# def 以下がアクセス後の操作
def index():
    # return 'Hello World!'
    return render_template('index.html') #追加

# メイン関数
if __name__ == '__main__':
    app.run()