# ExChAnge

The Website for Exchanging Items

## 專案結構

1. images: 存放所有網頁會用到的圖片檔
2. scripts: js 檔案
3. styles: css 檔案
4. templates: html 檔案

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

阿榤到此一游，測試測試逼逼
