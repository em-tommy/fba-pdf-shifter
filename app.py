import streamlit as st
from PyPDF2 import PdfReader, PdfWriter, Transformation
import io
import os

st.title("FBAバーコードPDF位置調整ツール")
st.write("右に1mm、下に1mmずらして印刷ずれを補正します")

uploaded_file = st.file_uploader("PDFファイルをアップロード", type=["pdf"])

if uploaded_file is not None:
    # 読み込み
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()

    # 1mm = 約2.834ポイント
    dx = 2.834  # 右に1mm
    dy = -2.834 # 下に1mm

    for page in reader.pages:
        page.add_transformation(Transformation().translate(dx, dy))
        writer.add_page(page)

    # 出力用バッファに保存
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    # 変換後のファイル名生成
    original_name = uploaded_file.name
    base, ext = os.path.splitext(original_name)
    adjusted_filename = f"{base}_右1mm_下1mmずらし変換済{ext}"

    # ダウンロードボタン表示
    st.success("変換が完了しました！")
    st.download_button(
        label="ずらしたPDFをダウンロード",
        data=output,
        file_name=adjusted_filename,
        mime="application/pdf"
    )
