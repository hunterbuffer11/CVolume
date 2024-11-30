import streamlit as st
import os
import script.automatic_covexhull as acv
import script.voxel as vl
import script.Delaunay_network as dn
import script.section_hull as sh    
import script.convex_voxel as cv
import pandas as pd
from pyecharts.charts import Bar, Line
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

# 配置页面布局为宽屏
st.set_page_config(layout="wide", initial_sidebar_state = "expanded")
# 使用CSS居中标题并设置颜色
st.markdown(
    '<style>h1 {text-align: center; color: orange;}</style>',
    unsafe_allow_html=True
)
with st.sidebar:
    st.header("Crown Volume Visualization") 
    st.subheader("可视化设置")
    chart_type = st.radio(
        label="选择可视化图表类型：",
        options=["柱状图", "折线图"],
        index=0
    )
     # 添加清空按钮
    if st.button("清空可视化图"):
        st.session_state.visualization_data = {}
    st.caption("该项目美化设计概念来自andfanilo在streamlit社区上发布的项目,同时使用了GPT-4进行了项目的美化")
# 设置标题
st.title("Crown Volume Calculator")
#设置分割线
horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"
st.markdown(horizontal_bar, True)

# 定义下拉框的选项
options = ['凸包法', '体元法', '过滤三角网法','分层凸包法','凸包-体元法']
# 创建下拉框部件
selected_option = st.selectbox("选择方法:", options)

if 'processed_volume' not in st.session_state:
    st.session_state.processed_volume = []
if 'visualization_data' not in st.session_state:
    st.session_state.visualization_data = {}
# 根据选择的方法显示不同的输入控件
if selected_option == '体元法':
    # 从用户获取体元大小输入
    voxel_size = st.number_input("请输入体元大小", min_value=0.1, format="%.2f")
    if voxel_size > 0:
        # 创建文件上传部件，允许上传多个文件
        uploaded_files = st.file_uploader("上传CSV文件", type=['csv'], accept_multiple_files=True)
        if uploaded_files:
            # 创建保存上传文件的目录
            os.makedirs("uploads", exist_ok=True)
            file_paths = []
            for uploaded_file in uploaded_files:
                file_path = os.path.join("uploads", uploaded_file.name)
                file_paths.append(file_path)
                # 保存上传的文件
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.read())
            # 创建处理文件的按钮
            if st.button("处理文件"):
                # 清空之前的处理结果
                st.session_state.processed_volume_voxel = []
                with st.spinner('处理中，请稍候...'):
                    # 创建进度条
                    progress_bar = st.progress(0)
                    total_files = len(file_paths)

                for i, file_path in enumerate(file_paths):
                    # 调用体元处理函数
                    volume = vl.process_single_file(file_path, voxel_size)
                    st.session_state.processed_volume_voxel.append(volume)
                    
                    st.write(f"文件 {os.path.basename(file_path)} 处理后的体积: {volume}")
                    st.success(f"文件 {os.path.basename(file_path)} 处理完成")
                    # 更新进度条
                    progress_bar.progress((i + 1) / total_files)
            # 获取数字按钮
            if st.button("获取数字"):
                df=pd.DataFrame({'体积': st.session_state.processed_volume_voxel},index=file_paths)
                if st.session_state.processed_volume_voxel:
                    st.dataframe(df.style.background_gradient(cmap='Blues'), width=600, height=400)
                    st.session_state.visualization_data = {"file_paths": file_paths, "volumes": st.session_state.processed_volume_voxel}
                else:
                    st.warning("请先处理文件")
    else:
        st.info("请输入有效的体元大小")
elif selected_option == '凸包法':
    # 创建文件上传部件，允许上传多个文件
    uploaded_files = st.file_uploader("上传CSV文件", type=['csv'], accept_multiple_files=True)
    if uploaded_files:
        # 创建保存上传文件的目录
        os.makedirs("uploads", exist_ok=True)
        file_paths = []
        for uploaded_file in uploaded_files:
            file_path = os.path.join("uploads", uploaded_file.name)
            file_paths.append(file_path)
            # 保存上传的文件
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.read())
        # 创建处理文件的按钮
        if st.button("处理文件"):
            st.session_state.processed_volume_convexhull = []
            with st.spinner('处理中，请稍候...'):
                    # 创建进度条
                    progress_bar = st.progress(0)
                    total_files = len(file_paths)
            for i,file_path in  enumerate(file_paths):
                # 调用凸包处理函数
                volume_convexhull = acv.process_single_file(file_path)
                st.write(f"文件 {os.path.basename(file_path)} 处理后的体积:", volume_convexhull)
                st.session_state.processed_volume_convexhull.append(volume_convexhull)
                st.success(f"文件 {os.path.basename(file_path)} 处理完成")
                # 更新进度条
                progress_bar.progress((i + 1) / total_files)
            # 获取数字按钮
        if st.button("获取数字"):
            df=pd.DataFrame({'体积': st.session_state.processed_volume_convexhull},index=file_paths)
            if st.session_state.processed_volume_convexhull:
                    st.dataframe(df.style.background_gradient(cmap='Blues'), width=600, height=400)
                    st.session_state.visualization_data = {"file_paths": file_paths, "volumes": st.session_state.processed_volume_convexhull}
            else:
                    st.warning("请先处理文件")

elif selected_option == '过滤三角网法':
        layer_height = st.number_input("请输入层高", min_value=0.1, format="%.2f")
        max_edge_length = st.number_input("请输入最大边长", min_value=0.1, format="%.2f")
        if(layer_height > 0 and max_edge_length > 0):
        # 创建文件上传部件，允许上传多个文件
          uploaded_files = st.file_uploader("上传CSV文件", type=['csv'], accept_multiple_files=True)
        if uploaded_files:
            # 创建保存上传文件的目录
            os.makedirs("uploads", exist_ok=True)
            file_paths = []
            for uploaded_file in uploaded_files:
                file_path = os.path.join("uploads", uploaded_file.name)
                file_paths.append(file_path)
                # 保存上传的文件
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.read())
                st.text("提示：该方法处理文件较慢请耐心等待")
                if st.button("处理文件"):
                  st.session_state.processed_volume_delaunay = []
                  with st.spinner('处理中，请稍候...'):
                    # 创建进度条
                    progress_bar = st.progress(0)
                    total_files = len(file_paths)

                  for i, file_path in enumerate(file_paths):
                    # 调用体元处理函数
                      volume_delaunay = dn.process_single_file(file_path, layer_height, max_edge_length)
                      st.session_state.processed_volume_delaunay.append(volume_delaunay)
                      st.write(f"文件 {os.path.basename(file_path)} 处理后的体积:", volume_delaunay)
                      st.success(f"文件 {os.path.basename(file_path)} 处理完成")
                      
                if st.button("获取数字"):
                  df=pd.DataFrame({'体积': st.session_state.processed_volume_delaunay},index=file_paths)
                  if st.session_state.processed_volume_delaunay:
                     st.dataframe(df.style.background_gradient(cmap='Blues'), width=600, height=400)
                     st.session_state.visualization_data = {"file_paths": file_paths, "volumes": st.session_state.processed_volume_delaunay}
                  else:
                    st.warning("请先处理文件")
elif selected_option=="分层凸包法":
    layer_height = st.number_input("请输入层高", min_value=0.1, format="%.2f")
    # 创建文件上传部件，允许上传多个文件
    uploaded_files = st.file_uploader("上传CSV文件", type=['csv'], accept_multiple_files=True)
    if uploaded_files:
        # 创建保存上传文件的目录
        os.makedirs("uploads", exist_ok=True)
        file_paths = []
        for uploaded_file in uploaded_files:
            file_path = os.path.join("uploads", uploaded_file.name)
            file_paths.append(file_path)
            # 保存上传的文件
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.read())
        # 创建处理文件的按钮
        if st.button("处理文件"):
            st.session_state.processed_volume_sectionhull = []
            with st.spinner('处理中，请稍候...'):
                    # 创建进度条
                    progress_bar = st.progress(0)
                    total_files = len(file_paths)
            for i, file_path in enumerate(file_paths):
                # 调用凸包处理函数
                volume_sectionhull,_ = sh.process_single_file(file_path, layer_height)
                st.write(f"文件 {os.path.basename(file_path)} 处理后的体积:", volume_sectionhull)
                st.session_state.processed_volume_sectionhull.append(volume_sectionhull)
                st.success(f"文件 {os.path.basename(file_path)} 处理完成")
                # 更新进度条
                progress_bar.progress((i + 1) / total_files)
            # 获取数字按钮
        if st.button("获取数字"):
            df=pd.DataFrame({'体积': st.session_state.processed_volume_sectionhull},index=file_paths)
            if st.session_state.processed_volume_sectionhull:
                    st.dataframe(df.style.background_gradient(cmap='Blues'), width=600, height=400)
                    st.session_state.visualization_data = {"file_paths": file_paths, "volumes": st.session_state.processed_volume_sectionhull}
            else:
                    st.warning("请先处理文件")
elif selected_option=='凸包-体元法':
    hull_por= st.number_input("请输入凸包所占比例", min_value=0.1, format="%.2f")
    voxel_size = st.number_input("请输入体元大小", min_value=0.1, format="%.2f")
    if voxel_size > 0 and hull_por>0:
        # 创建文件上传部件，允许上传多个文件
        uploaded_files = st.file_uploader("上传CSV文件", type=['csv'], accept_multiple_files=True)
        if uploaded_files:
            # 创建保存上传文件的目录
            os.makedirs("uploads", exist_ok=True)
            file_paths = []
            for uploaded_file in uploaded_files:
              file_path = os.path.join("uploads", uploaded_file.name)
              file_paths.append(file_path)
            # 保存上传的文件
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.read())
        # 创建处理文件的按钮
        if st.button("处理文件"):
            st.session_state.processed_volume_cv = []
            with st.spinner('处理中，请稍候...'):
                    # 创建进度条
                    progress_bar = st.progress(0)
                    total_files = len(file_paths)
            for i, file_path in enumerate(file_paths):
                # 调用凸包处理函数
                volume_cv= cv.process_single_file(file_path,hull_por,voxel_size )
                st.write(f"文件 {os.path.basename(file_path)} 处理后的体积:", volume_cv)
                st.session_state.processed_volume_cv.append(volume_cv)
                st.success(f"文件 {os.path.basename(file_path)} 处理完成")
                # 更新进度条
                progress_bar.progress((i + 1) / total_files)
            # 获取数字按钮
        if st.button("获取数字"):
            df=pd.DataFrame({'体积': st.session_state.processed_volume_cv},index=file_paths)
            if st.session_state.processed_volume_cv:
                    st.dataframe(df.style.background_gradient(cmap='Blues'), width=600, height=400)
                    st.session_state.visualization_data = {"file_paths": file_paths, "volumes": st.session_state.processed_volume_cv}
            else:
                    st.warning("请先处理文件")
# 可视化部分
if st.session_state.visualization_data:
    st.markdown("---")
    st.subheader("📊 可视化结果")
    file_paths = st.session_state.visualization_data.get("file_paths", [])
    volumes = st.session_state.visualization_data.get("volumes", [])

    if chart_type == "柱状图":
        bar = (
            Bar()
            .add_xaxis([os.path.basename(fp) for fp in file_paths])
            .add_yaxis("体积", volumes)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="体积统计柱状图"),
                xaxis_opts=opts.AxisOpts(name="文件名", axislabel_opts={"rotate": 45}),
                yaxis_opts=opts.AxisOpts(name="体积"),
                toolbox_opts=opts.ToolboxOpts(),
            )
        )
        st_pyecharts(bar, height="500px")

    elif chart_type == "折线图":
        line = (
            Line()
            .add_xaxis([os.path.basename(fp) for fp in file_paths])
            .add_yaxis("体积", volumes)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="体积统计折线图"),
                xaxis_opts=opts.AxisOpts(name="文件名", axislabel_opts={"rotate": 45}),
                yaxis_opts=opts.AxisOpts(name="体积"),
                toolbox_opts=opts.ToolboxOpts(),
            )
        )
        st_pyecharts(line, height="500px")

with st.expander("📝 使用说明"):
    st.markdown("""
    ### 使用步骤
    1. 选择计算方法
    2. 自定义设置参数
    3. 上传CSV文件
    4. 点击"处理文件"按钮
    5. 点击获取数字，查看结果
    6. 可视化结果选项在侧边栏选择

    ### 注意事项
    - 支持批量上传CSV文件
    - 过滤三角网计算速度较慢
    - 请确保上传的文件格式正确（只包含x, y, z三列数据）
    - 点击获取数字后，才会刷新可视化图
    - 可视化横坐标从尾部截断文件名，请注意文件名称
    """)
