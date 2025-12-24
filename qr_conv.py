#!/usr/bin/env python3
import argparse
import sys
import base64
import qrcode
import cv2
import numpy as np


def encode_file_to_qr(input_file, output_file):
    """バイナリファイルをQRコードにエンコードする"""
    try:
        with open(input_file, 'rb') as f:
            binary_data = f.read()

        # バイナリデータをBase64エンコード（QRコードに埋め込みやすくするため）
        encoded_data = base64.b64encode(binary_data).decode('utf-8')

        # QRコード生成
        qr = qrcode.QRCode(
            version=None,  # 自動でサイズ調整
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(encoded_data)
        qr.make(fit=True)

        # 画像として保存
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_file)

        print(f"Successfully encoded '{input_file}' to QR code '{output_file}'")
        print(f"Original file size: {len(binary_data)} bytes")
        print(f"Encoded data size: {len(encoded_data)} bytes")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during encoding: {e}", file=sys.stderr)
        sys.exit(1)


def decode_qr_to_file(input_image, output_file):
    """QRコード画像からバイナリファイルをデコードする"""
    try:
        # OpenCVでQRコード検出器を作成
        detector = cv2.QRCodeDetector()

        # 画像を読み込み
        img = cv2.imread(input_image)

        if img is None:
            print(f"Error: Cannot read image '{input_image}'", file=sys.stderr)
            sys.exit(1)

        # QRコードをデコード
        qr_data, bbox, _ = detector.detectAndDecode(img)

        if not qr_data:
            print(f"Error: No QR code found in '{input_image}'", file=sys.stderr)
            sys.exit(1)

        # Base64デコード
        binary_data = base64.b64decode(qr_data)

        # ファイルに書き込み
        with open(output_file, 'wb') as f:
            f.write(binary_data)

        print(f"Successfully decoded QR code '{input_image}' to '{output_file}'")
        print(f"Output file size: {len(binary_data)} bytes")

    except FileNotFoundError:
        print(f"Error: Input image '{input_image}' not found", file=sys.stderr)
        sys.exit(1)
    except base64.binascii.Error:
        print(f"Error: Invalid QR code data (not valid Base64)", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during decoding: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='QRコードとバイナリファイル変換ツール',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用例:
  # バイナリファイルをQRコードにエンコード
  %(prog)s -e -i input.bin -o output.png

  # QRコード画像からバイナリファイルをデコード
  %(prog)s -d -i qrcode.png -o output.bin
        '''
    )

    # モード選択用のmutually exclusive group
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '-e', '--encode',
        action='store_true',
        help='エンコードモード: バイナリファイルをQRコードに変換'
    )
    mode_group.add_argument(
        '-d', '--decode',
        action='store_true',
        help='デコードモード: QRコードをバイナリファイルに変換'
    )

    parser.add_argument(
        '-i', '--input',
        required=True,
        help='入力ファイル名'
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        help='出力ファイル名'
    )

    args = parser.parse_args()

    if args.encode:
        encode_file_to_qr(args.input, args.output)
    elif args.decode:
        decode_qr_to_file(args.input, args.output)


if __name__ == '__main__':
    main()
