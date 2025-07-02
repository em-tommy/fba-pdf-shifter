import streamlit as st
from pypdf import PdfReader, PdfWriter, Transformation
from io import BytesIO
import os

st.title("FBAバーコードPDF位置調整ツール")
st.write("右に1mm、下に1mmずらしてPDFを再生成します。")

uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type="pdf")

if uploaded_file:
    try:
        # PDF読み込み
        reader = PdfReader(uploaded_file)
        writer = PdfWriter()

        for page in reader.pages:
            # 単位：1pt = 1/72 inch。1mm ≒ 2.8346 pt
            shift = Transformation().translate(tx=2.8346, ty=-2.8346)
            page.add_transformation(shift)
            writer.add_page(page)

        # メタデータ引き継ぎ（なくてもよいが推奨）
        writer.add_metadata(reader.metadata or {})

        # 書き出し
        output = BytesIO()
        writer.write(output)
        output.seek(0)

        # 元ファイル名に追記
        original_filename = uploaded_file.name.rsplit(".pdf", 1)[0]
        new_filename = f"{original_filename}_右1mm_下1mmずらし変換済.pdf"

        st.download_button(
            label="変換後のPDFをダウンロード",
            data=output,
            file_name=new_filename,
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"変換中にエラーが発生しました: {e}")
