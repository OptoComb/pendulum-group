# pendulum-group

UEQ Quantum Base 光コム (OptoComb) グループ 振り子 (pendulum) 班.  
[ドキュメント(overleaf)](https://www.overleaf.com/read/gttmbhjdwssd#fc1ea5)

## 1. 依存ライブラリのインストール

OpenCVやnumpyといったアプリに必要なライブラリをインストールする．
バージョンの組み合わせによってはうまく動かないことがあるため，`.python-version`ファイルでPython自体のバージョンを，`requirements.txt`ファイルでライブラリ毎のバージョンをそれぞれ指定している．

```shell
$ cd pendulum-group
$ python3 --version
Python 3.11.5
$ pip3 install -r requirements.txt
```

## 2. 画像認識デスクトップアプリ

振り子の錘の部分を画像認識によって検出し，カメラの画角に対する座標をCSVファイルに記録する．

### 2.1 アプリの起動

リアルタイムで画像認識（円検出）が行えるとよいが，PCの性能によってはフレームレートが落ちてしまうため，録画済みファイルから円検出を行えるようにした．

```shell
# リアルタイム円検出用
$ python3 gui/circleDetection.py

# 動画ファイルから円検出を行う
$ python3 video_analysis/circleDetection.py
```

#### 2.1.1 カメラや動画ファイルの選択

リアルタイム検出アプリ (`gui/circleDetection.py`) に使用するカメラの選択は `video_source`引数で行う．
`0`がOS標準のカメラ，`1`や`2`などにPCに接続された他のカメラが設定される．これらの数値はOSが決定するため，PCの再起動ごとに確認する（OS毎に確認方法が異なるためググる）．

> [!NOTE]
> 存在しないカメラを選択すると映像が真っ黒になったり，アプリがエラーとなったりする．

動画ファイルから円検出を行う場合 (`video_analysis/circleDetection.py`) では，使用する動画ファイルは `video_source`引数で行う．

> [!CAUTION]
> ファイルの場所（フォルダ/ディレクトリ）はPythonアプリを実行したディレクトリからの相対パスになっており，Pythonファイルからの相対パスでないことに注意する．

### 2.2 アプリの操作

#### 2.2.1 基本操作

アプリ起動後の，画像認識を行いその結果をCSVに出力し，アプリを終了するまでの操作．

- 「円検出」トグルボタンを押すと円検出がはじまり，「円検出**中**」の表示になる．
- 「Close」ボタンを押すとアプリが終了する（廃止予定）
- 「CSV出力」トグルボタンを押すと動画1フレームごとに検出されている円の画像内x座標，y座標，半径がCSVファイルに出力されはじめる．
  「CSV出力**中**」となっている間のデータだけ出力される点に注意．

#### 2.2.2 パラメータ調整

「円検出**中**」であってもうまく画像認識（円検出）が行われない場合がある．
例えば，一つの円に対して二つ以上検出してしまったり，逆に全く検出されなかったりする．
そういった場合には周囲の明るさやカメラの特性に応じて画像認識のパラメータ調整を行う必要がある．

- 「min dist」パラメータ：検出される円の最小距離を設定する．これを大きくとることで，同じ円に対して複数の検出が行われにくくなる．
- 「param1」パラメータ（廃止予定）：Canny法におけるHysteresis処理の閾値（らしい）．基本的に`100`で固定するが，極端に明るい・暗い場合やコントラストが強い・弱い場合に変更するといいかもしれない．
- 「param2」パラメータ：円検出の閾値にあたるパラメータ．小さくとると誤検出が，大きくとると未検出が増える．1刻みで細かく調整するとよい．

### 2.3 出力CSV

1列目はフレームの検出時刻（動画内時刻ではない**要改善**）である．
以降2, 3, 4列目，5, 6, 7列目，8, 9, 10列目などは検出した円のx座標，y座標，半径となっている．
出力されたCSVのデータ解析（どれがどの錘に対応するか，誤検出かどうか等）はアプリ外で行う．

#### 2.3.1 CSV出力先

- リアルタイム検出用アプリ (`gui/circleDetection.py`) では，`self.csvfile`変数で出力先のCSVファイルを変更できる．
- 録画済み動画ファイルから検出する場合 (`video_analysis/circleDetection.py`) は，その動画ファイルと同名のCSVファイルが出力される．

> [!CAUTION]
> - 上書きする設定になっているので，連続して実験を行う際には注意する．
> - ファイルの場所（フォルダ/ディレクトリ）はPythonアプリを実行したディレクトリからの相対パスになっており，Pythonファイルからの相対パスでないことに注意する．


## 3. 解析

出力されたCSVファイルに対してExcelやスプレッドシート等を用いて解析を行う．

1. 検出された円（錘）を弁別する．
   y座標をもとに分別し，半径を用いて外れ値を取り除く．検出位置が極端に近い場合（パラメータ調整でほとんど失くせる）は平均をとったりして頑張る
2. 分別した円ごとに，時刻とx座標でグラフを描いてみる．
   単振動っぽいものが見えればOK!
3. `./video_analysis/time-freq-spect.py`を用いて時間周波数グラフを出力する
   ```sh
   $ python3 video_analysis/time-freq-spect.py
   ```

## 4. その他

注意事項等

#### 動画像の歪み

カメラの特性によって，動画が歪むことがある．
歪んでいる場合は，[`./CameraCalibration`](./CameraCalibration/)に移動し，[`./CameraCalibration/README.md`](./CameraCalibration/README.md)を読んでキャリブレーションを実行する．

#### パラメータ

アプリ上では設定できないが，ソースコードの円検出関数`cv2.HoughCircles()` の調整可能パラメータはまだ存在する．
順に紹介する．

1. `image`: 画像データ．動画の 1 `frame` を渡している．
2. `method`: Hough変換の手法．ドキュメントが見つからなかったので `cv2.HOUGH_GRADIENT` を渡している．
3. `dp`: 投票器の解像度（らしい）．`0.1`あたりだと基準が厳しく，検出されにくい．`1.9`あたりだと基準が緩く，誤検出が増える．
4. `minDist`: アプリ内で設定できる（`Float`型）．
5. `param1`: アプリ内で設定できる（`Float`型）．
6. `param2`: アプリ内で設定できる．
7. `minRadius`: 検出される円の半径の下限．半径がこの値以下の円の検出が行われなくなる（`Int`型，nullable）．
8. `maxRadius`: 検出される円の半径の上限．半径がこの値以上の円の検出が行われなくなる（`Int`型，nullable）．
