# ExChAnge
The Website for Exchanging Items
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
```command line
git add .
git commit -m "敘述這次修改部分" # 用英文，盡量讓大家看得懂
```
3. Push 上 Github
```command line
git push
```
