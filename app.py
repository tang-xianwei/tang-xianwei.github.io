from flask import Flask, render_template, request, jsonify
import pandas as pd
import re
import socket

app = Flask(__name__)

# =========================================================
# 1. 读取 CSV（自动处理编码）
# =========================================================
try:
    df = pd.read_csv("格式化后的数据.csv", encoding="utf-8")
except UnicodeDecodeError:
    try:
        df = pd.read_csv("格式化后的数据.csv", encoding="gbk")
    except:
        df = pd.read_csv("格式化后的数据.csv", encoding="gb2312")

# =========================================================
# 2. 清理 CSV 中的 | 和 nan（核心）
# =========================================================
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text)

    # 删除竖线（全角 + 半角）
    text = text.replace("|", "")
    text = text.replace("｜", "")

    # 删除 nan / NaN / Nan
    text = re.sub(r"\bnans?\b", "", text, flags=re.I)

    return text.strip()

# 所有列统一清理
for col in df.columns:
    df[col] = df[col].apply(clean_text)

# 清理列名
df.columns = df.columns.str.strip()

# =========================================================
# 3. 首页：姓名下拉框
# =========================================================
@app.route("/")
def index():
    names = sorted([n for n in df["name"].unique() if n])
    return render_template("index.html", names=names)

# =========================================================
# 4. 搜索接口
# =========================================================
@app.route("/search", methods=["POST"])
def search():
    name = request.form.get("name", "").strip()
    if not name:
        return jsonify([])

    results = df[df["name"] == name]

    # 精确匹配失败 → 模糊匹配
    if results.empty:
        results = df[df["name"].str.contains(name, case=False, na=False)]

    return jsonify(results.to_dict(orient="records"))

# =========================================================
# 5. 获取所有姓名（前端用）
# =========================================================
@app.route("/api/all_names")
def all_names():
    names = sorted([n for n in df["name"].unique() if n])
    return jsonify({"count": len(names), "names": names})

# =========================================================
# 6. 启动服务器（允许局域网访问）
# =========================================================
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    local_ip = get_local_ip()

    print("\n" + "=" * 60)
    print("✅ 唐代县尉数据库已启动")
    print("=" * 60)
    print(f"本地访问：   http://127.0.0.1:{port}")
    print(f"局域网访问： http://{local_ip}:{port}")
    print("=" * 60)

    app.run(host=host, port=port, debug=True)









