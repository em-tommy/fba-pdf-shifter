import streamlit as st
from PyPDF2 import PdfReader, PdfWriter, Transformation
import io
import os

st.set_page_config(page_title="FBAバーコードPDF位置調整ツール")

st.markdown("<h3>FBAバーコードPDF位置調整ツール</h3>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "元のPDFファイルをドラッグ＆ドロップ",
    type="pdf",
    label_visibility="visible",
    accept_multiple_files=False
)

if uploaded_file is not None:
    # 読み込み
    input_pdf = PdfReader(uploaded_file)
    output_pdf = PdfWriter()

    # 各ページを右1mm・下1mm移動（1mm ≒ 2.83465pt）
    shift_x = 2.83465  # 1mm
    shift_y = -2.83465  # 下方向

    for page in input_pdf.pages:
        page.add_transformation(Transformation().translate(tx=shift_x, ty=shift_y))
        output_pdf.add_page(page)

    # ファイル名を作成
    original_name = os.path.splitext(uploaded_file.name)[0]
    output_filename = f"{original_name}_右1mm_下1mmずらし変換済.pdf"

    # バイナリデータに書き出し
    output_stream = io.BytesIO()
    output_pdf.write(output_stream)
    output_stream.seek(0)

    # 成功メッセージとファイル名表示
    st.markdown(
        f"<p style='color:green; font-weight:bold;'>✅ 変換が成功しました！</p>",
        unsafe_allow_html=True
    )
    st.markdown(f"<p><b>生成ファイル名：</b>{output_filename}</p>", unsafe_allow_html=True)

    # ダウンロードボタン
    st.download_button(
        label="変換済PDFをダウンロード",
        data=output_stream,
        file_name=output_filename,
        mime="application/pdf"
    )
