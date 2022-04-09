# ExChAnge

The Website for Exchanging Items

## 專案結構

使用 flask 框架，執行 run.py 即可運行網頁。

## Git 操作

### 複製專案到 local

Local 端還沒有這個專案時，可執行 clone 取得 github 上面的程式碼。

```command line
git clone <github連結>
git clone https://github.com/joeroy5376998/ExChAnge.git
```

### 開發 SOP

Local 端修改完程式碼後，要上傳到 github 的步驟：

1. 把遠端的最新版本拉下來

```command line
git pull --rebase origin main
```

2. 暫存 local 端目前的版本
   記得要回到整個專案的資料夾最上層，才能把所有有更動的地方加入

```command line
git add .
git commit -m "敘述這次修改部分" #用英文，盡量讓大家看得懂
```

3. Push 上 Github

```command line
git push
```

### 遇到 confilct 怎辦

打開編輯器或是終端，就可以看到發生衝突的程式碼在哪裡，修改完之後執行上面開發 SOP 的 2. 3. 即可。
<br><br>

# Chieh 2022/04/05 Update

## 具體 commit description

1. 將 templates folder 分出 formalEdition，裡面裝確定要上線的東西，剩下草稿放在 templates folder
2. 分出 commonStyle.css，裝有普遍 global setting & style setting，請在每個頁面中先引入(除了 homepage 以外，我沒有切分 homepage.css 檔案)。未來新增每個頁面時請先引入 commonStyle.css by 以下程式碼

```
    <link href="../styles/commonStyle.css" rel="stylesheet" />
```

3. 刪除 js 檔案，將 aboutUs & backpack 獨立出來，並建立所有相互跳轉連結。
4. 對 uploadpage 版面修改，更改 js 檔案跳轉路徑，並套用 commonStyle
5. Login 頁面，進行簡易排版、處理 js 檔案 bug
6. 刪除失去效用、重複代碼

## Warning

請勿刪除.scss 檔案，另外請直接更動 scss 檔案，勿直接改動 css 檔案，不然<font color="#f00">**重新編譯會被直接蓋過。**</font>

若不熟悉 SCSS Syntax，可以直接在該 scss 檔案撰寫 css 語法即可，<font color="#f00">**總之若有 scss 同名檔就請在裡面編寫排版。**</font>
