# 校园专升本招生宣传网站

## 本地预览

电脑上打开浏览器，访问：**http://localhost:8080**

（终端开着就不要关，关了网站就看不到了）

## 部署到 GitHub Pages（免费）

### 第一步：注册 GitHub 账号
1. 打开 https://github.com 点右上角 Sign up
2. 用邮箱注册，用户名随便取

### 第二步：创建仓库
1. 登录后点右上角 + 号 → New repository
2. Repository name 填：recruitment-site
3. 选 Public（公开）
4. 点 Create repository

### 第三步：上传网站文件
把这三个文件上传到仓库：
- index.html
- styles.css
- script.js

上传方法：在仓库页面点 "uploading an existing file"，把三个文件拖进去，点 Commit changes。

### 第四步：开启 GitHub Pages
1. 仓库页面 → Settings → 左侧菜单找到 Pages
2. Source 选 "Deploy from a branch"
3. Branch 选 "main" → / (root) → Save
4. 等2分钟，页面顶部会显示网址：https://你的用户名.github.io/recruitment-site/

### 第五步：配置表单接收
1. 打开 https://formspree.io 注册免费账号
2. 创建一个新表单，得到一串 FORM_ID
3. 把 script.js 里的 `YOUR_FORM_ID` 替换成你的真实ID
4. 重新上传 script.js 到 GitHub
5. 别人填的表单会发到你的 Formspree 注册邮箱

## 自定义内容

- 校园照片：把图片放到项目目录，把 index.html 里的 📷 占位符换成 `<img src="你的照片.jpg">`
- 专业列表：直接在 index.html 里改专业名称
- 政策信息：根据学校实际情况修改
- 颜色/风格：改 styles.css

## 文件说明

| 文件 | 作用 |
|------|------|
| index.html | 网页结构和内容 |
| styles.css | 颜色、字体、布局 |
| script.js | 表单提交逻辑 |
