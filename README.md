# QRコードとバイナリファイル変換ツール

以下のようなエンコーダ、デコーダ機能を持つツールです。

* バイナリファイルをQRコードにエンコードする機能
* 写真に写ったQRコードから、バイナリファイルを出力（デコード）する機能

## セットアップ

```bash
# venv環境を作成
python3 -m venv venv

# venv環境を有効化
source venv/bin/activate

# 必要なパッケージをインストール
pip install -r requirements.txt
```

## 使い方

### エンコード（ファイル → QRコード）

```bash
python qr_conv.py -e -i <入力ファイル> -o <出力画像ファイル>
```

例:
```bash
python qr_conv.py -e -i test.txt -o qrcode.png
```

### デコード（QRコード → ファイル）

```bash
python qr_conv.py -d -i <入力画像ファイル> -o <出力ファイル>
```

例:
```bash
python qr_conv.py -d -i qrcode.png -o output.txt
```

### オプション

- `-e`, `--encode`: エンコードモード（ファイル → QRコード）
- `-d`, `--decode`: デコードモード（QRコード → ファイル）
- `-i INPUT`, `--input INPUT`: 入力ファイル名（必須）
- `-o OUTPUT`, `--output OUTPUT`: 出力ファイル名（必須）
- `-h`, `--help`: ヘルプメッセージを表示

## 使用例

### 例1: テキストファイルをQRコードに変換

```bash
# テキストファイルを作成
echo "Hello, QR Code!" > message.txt

# QRコードにエンコード
python qr_conv.py -e -i message.txt -o message_qr.png
```

出力:
```
Successfully encoded 'message.txt' to QR code 'message_qr.png'
Original file size: 16 bytes
Encoded data size: 24 bytes
```

### 例2: QRコードからテキストファイルを復元

```bash
# QRコードからデコード
python qr_conv.py -d -i message_qr.png -o restored.txt

# 内容を確認
cat restored.txt
```

出力:
```
Successfully decoded QR code 'message_qr.png' to 'restored.txt'
Output file size: 16 bytes
Hello, QR Code!
```

### 例3: バイナリファイル（画像など）の変換

```bash
# 小さな画像ファイルをQRコードに変換
python qr_conv.py -e -i icon.png -o icon_qr.png

# QRコードから画像を復元
python qr_conv.py -d -i icon_qr.png -o icon_restored.png
```

### 例4: 完全なワークフロー

```bash
# 1. venv環境を有効化
source venv/bin/activate

# 2. 必要なパッケージをインストール（初回のみ）
pip install -r requirements.txt

# 3. ファイルをエンコード
python qr_conv.py -e -i secret.txt -o secret_qr.png

# 4. QRコードが生成されたことを確認
ls -lh secret_qr.png

# 5. QRコードをデコード
python qr_conv.py -d -i secret_qr.png -o secret_decoded.txt

# 6. 元のファイルと復元したファイルが同一か確認
diff secret.txt secret_decoded.txt && echo "ファイルは完全に一致しています！"
```

### 例5: ヘルプの表示

```bash
python qr_conv.py --help
```

## 仕様

- バイナリファイルはBase64エンコードしてQRコードに埋め込まれます
- QRコードの誤り訂正レベルは最高レベル(H)を使用しています
- OpenCVを使用してQRコードの検出とデコードを行います

