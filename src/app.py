# 必要なモジュールのインポート
import torch
from animal import transform, Net # animal.py から前処理とネットワークの定義を読み込み
from flask import Flask, request, render_template, redirect
import io
from PIL import Image
import base64

# 学習済みモデルをもとに推論する
def predict(img):
    # ネットワークの準備
    net = Net().cpu().eval()
    # # 学習済みモデルの重み（bird.pt）を読み込み
    net.load_state_dict(torch.load('./bird.pt', map_location=torch.device('cpu')))
#    net.load_state_dict(torch.load('./src/bird.pt', map_location=torch.device('cpu')))
    #　データの前処理
    img = transform(img)
    img =img.unsqueeze(0) # 1次元増やす
    #　推論
    y = torch.argmax(net(img), dim=1).cpu().detach().numpy()
    return y

#　推論したラベルからどの鳥かを返す関数
def getName(label):
    if label==0:
        return 'あおばと'
    elif label==1:
        return 'ハクチョウ'
    elif label==2:
        return 'カラス'
    elif label==3:
        return 'かるがも'
    elif label==4:
        return 'かわらバト'
    elif label==5:
        return 'きじばと'
    elif label==6:
        return 'こがも'
    elif label==7:
        return 'まがも'
    elif label==8:
        return 'オオワシ'
    elif label==9:
        return 'しじゅうから'
    elif label==10:
        return 'すずめ'

# Flask のインスタンスを作成
app = Flask(__name__)

# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'jpeg'])

#　拡張子が適切かどうかをチェック
def allwed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# URL にアクセスがあった場合の挙動の設定
@app.route('/', methods = ['GET', 'POST'])
def predicts():
    # リクエストがポストかどうかの判別
    if request.method == 'POST':
        # ファイルがなかった場合の処理
        if 'filename' not in request.files:
            return redirect(request.url)
        # データの取り出し
        file = request.files['filename']
        # ファイルのチェック
        if file and allwed_file(file.filename):

            #　画像ファイルに対する処理
            #　画像書き込み用バッファを確保
            buf = io.BytesIO()
            image = Image.open(file).convert('RGB')
            #　画像データをバッファに書き込む
            image.save(buf, 'png')
            #　バイナリデータを base64 でエンコードして utf-8 でデコード
            base64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
            #　HTML 側の src  の記述に合わせるために付帯情報付与する
            base64_data = 'data:image/png;base64,{}'.format(base64_str)

            # 入力された画像に対して推論
            pred = predict(image)
            animalName_ = getName(pred)
            return render_template('result.html', animalName=animalName_, image=base64_data)

    # GET メソッドの定義
    elif request.method == 'GET':
        return render_template('index.html')


# アプリケーションの実行の定義
if __name__ == '__main__':
    app.run(debug=True)