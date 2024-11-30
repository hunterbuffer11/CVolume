import streamlit as st
# Set the layout to wide
st.set_page_config(layout="wide")

# Center the title using CSS
st.markdown(
    '<style>h1 {text-align: center; color: orange;}</style>',
    unsafe_allow_html=True
)
with st.sidebar:
  st.caption(
                """该项目使用[Streamlit](https://www.streamlit.io)构建。
                Streamlit是一个开源的Pytorch库，用于构建数据科学和机器学习的应用程序，并直接在Web浏览器中运行它们。
                需要补充的是，这是一个新人项目，为了追求简洁，程序设计可读性可能欠佳。
                """)
            
# Set the title
st.title("Crown volume calculator")
#设置分割线
horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"
st.markdown(horizontal_bar, True)
st.header('1. 使用方法')
st.text('在右边栏点击method,选择方法')
st.header('2. 输入数据')
st.text('输入CSV文件, 格式为: x, y, z')
st.header('3. 计算结果')
st.text('自动计算结果的体积,单位为立方米。保留两位小数')