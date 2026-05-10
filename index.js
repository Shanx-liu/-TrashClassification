//漢堡選單
const menuButton = document.querySelector('.menu');
const navList = document.querySelector('.nav-list');

menuButton.addEventListener('click', () => {
    navList.classList.toggle('active');
});

//垃圾種類及對應處理方式
let trashClassHandleArray = {
    '一般垃圾':         ['一般垃圾', '無法回收之廢棄物，請裝入垃圾袋後交由垃圾車清運'], 
    '塑膠類':           ['塑膠類', '請先清洗乾淨並瀝乾水分，依材質分類後交由回收車回收'], 
    '廚餘類':           ['廚餘類', '請去除塑膠袋與雜質，瀝乾後投入廚餘回收桶（可分為生熟廚餘）'], 
    '照明光源(增強)':   ['照明光源', '含汞照明光源，請勿丟入一般垃圾，交由超商或指定回收點回收'], 
    '玻璃類':           ['玻璃類', '請分色並清洗乾淨，破碎玻璃需妥善包裝後交由回收車回收'],
    '紙類':             ['紙類', '請保持乾燥並去除塑膠、釘書針等雜質，壓平後交由回收車回收'], 
    '舊衣類':           ['舊衣類', '可再使用之衣物請清洗後投入舊衣回收箱，不可回收者當一般垃圾處理'], 
    '金屬類':           ['金屬類', '請清洗乾淨，依鋁、鐵等分類後交由回收車回收'], 
    '電子電器':         ['電子電器', '屬公告應回收項目，請交由販售商、清潔隊或指定回收點回收'], 
    '電池類':           ['電池類', '含重金屬，請勿丟入一般垃圾，投入超商或回收點之廢電池回收箱']
}

//簡易插圖連結陣列
let trashPictureSrc = [
    '網頁介面垃圾垃類別簡易插圖/一般垃圾.jpg',
    '網頁介面垃圾垃類別簡易插圖/紙類.jpg',
    '網頁介面垃圾垃類別簡易插圖/塑膠類.jpg',
    '網頁介面垃圾垃類別簡易插圖/金屬類.jpg',
    '網頁介面垃圾垃類別簡易插圖/玻璃類.jpg',
    '網頁介面垃圾垃類別簡易插圖/電池類.jpg',
    '網頁介面垃圾垃類別簡易插圖/照明光源.jpg',
    '網頁介面垃圾垃類別簡易插圖/電子電器.jpg',
    '網頁介面垃圾垃類別簡易插圖/舊衣類.jpg',
    '網頁介面垃圾垃類別簡易插圖/廚餘類.jpg'
]

//左側垃圾類別選單
const Tclass_1 = document.getElementById('class-1');
const Tclass_2 = document.getElementById('class-2');
const Tclass_3 = document.getElementById('class-3');
const Tclass_4 = document.getElementById('class-4');
const Tclass_5 = document.getElementById('class-5');
const Tclass_6 = document.getElementById('class-6');
const Tclass_7 = document.getElementById('class-7');
const Tclass_8 = document.getElementById('class-8');
const Tclass_9 = document.getElementById('class-9');
const Tclass_10 = document.getElementById('class-10');
//左側垃圾類別選單訊息框
const simpleDialog = document.getElementById('simple-dialog');
const simplePicture = document.getElementById('simple-picture');
const simpleTrashClass = document.getElementById('simple-trash-class');
const simpleTrashHandle = document.getElementById('simple-trash-handle');
const simpleCloseButton = document.getElementById('simple-close-button');

//用ngrok取得之免費網址進行發佈  
//ngrok啟動指令/ngrok/ngrok.exe http --url=unannealed-controllingly-sarai.ngrok-free.dev 80  

//上傳圖片區塊相關
const fileInput = document.getElementById('fileinput');
const fileName = document.getElementById('filename');
const inputButton = document.getElementById('inputbutton');
const upButton = document.getElementById('upbutton');
const fileImg = document.getElementById('fileimg');
const placeHolder = document.getElementById('placeholder');

//下面變數為跳出訊息框
const resultDialog = document.getElementById('result-dialog');
const dialogImg = document.getElementById('dialog-img');
const trashClassElement = document.getElementById('trash-class');
const trashHandle = document.getElementById('trash-handle');
const closeButton = document.getElementById('close-button');

//初始化進用上傳按鈕
upButton.disabled = true;       //初始化進用上傳鈕
let jpgBlob = null;

//初始化fileName狀態
fileName.textContent = '未選擇任何檔案'

//點擊"選擇圖片"按鈕觸發fileInput選擇介面
inputButton.addEventListener('click', ()=>{     
    fileInput.click();
});

//選擇圖片相關邏輯
fileInput.addEventListener('change', async ()=>{      //選擇檔案
    const file = fileInput.files[0];                  //即使選擇多個檔案也只會取第一張
    
    if(!file) {     //未選擇檔案時的處理
        fileName.textContent = '未選擇任何檔案';
        fileImg.src = '';
        fileImg.style.display = 'none';
        placeHolder.style.display = 'block';
        upButton.disabled = true;
        upButton.textContent = '上傳';
        return;
    }

    //有檔案則執行以下處理
    fileName.textContent = "已選擇檔案:" + file.name;
    const extension = file.name.split('.').pop().toLowerCase(); //取得檔案副檔名
    if(extension === 'heic') {          //將HEIC檔轉成jpg
        try{
            const convertedBlob = await heic2any({      //強制等待heic2any函示執行完成
                blob: file,                 //將file物件設給blob
                toType: 'image/jpeg',       //轉成jpeg格式
                quality: 0.8                //轉檔品質
            });
            upButton.textContent = '轉換中...';
            const reader = new FileReader();    //建立一個讀檔物件
            reader.onload = function(e) {       //讀取完後的執行邏輯
                const img = new Image();
                img.onload = function() {
                    const canvas = document.createElement('canvas');    //建一個隱形的畫板物件
                    canvas.width = img.width;
                    canvas.height = img.height;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0);           //將img物件從畫板的左上方開始畫
                    canvas.toBlob(function(blob) {      //將畫布上的內容轉成可傳送到伺服器的Blob物件
                        jpgBlob = blob,                 
                        upButton.disabled = false;      //解封上傳按鈕
                    }, 'image/jpeg', 0.8);
                };
                img.src = e.target.result;  //先將e.target.result設給img後才執行onload函式
                //下面三行為圖片預覽邏輯
                fileImg.src = e.target.result;      //將圖片設給預覽區塊
                dialogImg.src = e.target.result;    //將圖片設給訊息框
                fileImg.style.display = 'block';    //顯示預覽圖片
                placeHolder.style.display = 'none'; //隱藏提示文字
                upButton.textContent = '上傳';      //將上傳按鈕內容改回上傳
            };
            reader.readAsDataURL(convertedBlob);        //讀取檔案
        }catch(err){
            console.error("heic轉換失敗:",err);
            alert("HEIC 轉 JPG 失敗，請選擇其他圖片格式");
            return;
        }
    }else{
        //這段為非heic格式時的處理，同上
        upButton.textContent = '轉換中...';
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = new Image();
            img.onload = function() {
                const canvas = document.createElement('canvas');
                canvas.width = img.width;
                canvas.height = img.height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);
                canvas.toBlob(function(blob) {
                    jpgBlob = blob;
                    upButton.disabled = false;      //解封上傳按鈕
                }, 'image/jpeg', 0.8);
            };
            img.src = e.target.result;
            //下面三行為圖片預覽邏輯
            fileImg.src = e.target.result;      //將圖片設給預覽區塊
            dialogImg.src = e.target.result;    //將圖片設給訊息框
            fileImg.style.display = 'block';    //顯示預覽圖片
            placeHolder.style.display = 'none'; //隱藏提示文字
            upButton.textContent = '上傳';      //將上傳按鈕內容改回上傳
        };
        reader.readAsDataURL(file);
    }
});
//下面為與後端溝通邏輯
upButton.addEventListener('click', ()=>{
    if(!jpgBlob) {
        console.error('jpgBlob 未定義，無法上傳');
        alert('請先選擇圖片');
        return;
    }
    // 禁用上傳按鈕防止重複點擊
    upButton.disabled = true;       //禁用上傳鈕，防止重複點擊
    upButton.textContent = '上傳中...';

    const formData = new FormData();
    formData.append('image', jpgBlob, 'upload.jpg');

    fetch('/api/data', {    //本身網址加後端Python模組Flask虛擬路由
        method: 'POST',
        body: formData
    })
    .then(response => {     //回應失敗時
        if(!response.ok) {
            throw new Error(`HTTP錯誤: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {     //回應正確時
        console.log("上傳回應:",data);
        let trashClassResult = data.trashClass;   //將回傳的垃圾種類設給trashClass變數
        dialogImg.src = fileImg.src;
        resultDialog.showModal();       //顯示結果訊息框
        trashClassElement.textContent = trashClassHandleArray[trashClassResult][0]      //訊息框垃圾種類 
        trashHandle.textContent = trashClassHandleArray[trashClassResult][1]     //訊息框垃圾處理方式
        //清空檔案選擇器
        fileInput.value = '';
        fileName.textContent = '';
    })
    .catch(err => {
        console.error("上傳錯誤:",err);
        alert("錯誤，無法上傳: " + err.message);
        upButton.disabled = false;
    })
    .finally(() => {
        upButton.textContent = '上傳';
    });
});

//訊息框確定按鈕
closeButton.addEventListener('click', () => {
    resultDialog.close();
});

//左側垃圾類別選單相關邏輯
//加上事件監聽(點擊)、加上對應之類別名稱/處理方式、顯示訊息框
Tclass_1.addEventListener('click', () => {
    simpleTrashClass.textContent = trashClassHandleArray['一般垃圾'][0];    //放入類別名稱
    simpleTrashHandle.textContent = trashClassHandleArray['一般垃圾'][1];   //放入處理方式
    simplePicture.src = trashPictureSrc[0];         //從圖片路徑字串陣列，放入對應之垃圾插圖路徑
    simpleDialog.showModal();
});
Tclass_2.addEventListener('click', () => {
    simpleTrashClass.textContent = trashClassHandleArray['紙類'][0];
    simpleTrashHandle.textContent = trashClassHandleArray['紙類'][1];
    simplePicture.src = trashPictureSrc[1]; 
    simpleDialog.showModal();
});
Tclass_3.addEventListener('click', () => {
    simpleTrashClass.textContent = trashClassHandleArray['塑膠類'][0];
    simpleTrashHandle.textContent = trashClassHandleArray['塑膠類'][1];
    simplePicture.src = trashPictureSrc[2]; 
    simpleDialog.showModal();
});
Tclass_4.addEventListener('click', () => {
    simpleTrashClass.textContent = trashClassHandleArray['金屬類'][0];
    simpleTrashHandle.textContent = trashClassHandleArray['金屬類'][1];
    simplePicture.src = trashPictureSrc[3]; 
    simpleDialog.showModal();
});
Tclass_5.addEventListener('click', () => {
    simpleTrashClass.textContent = trashClassHandleArray['玻璃類'][0];
    simpleTrashHandle.textContent = trashClassHandleArray['玻璃類'][1];
    simplePicture.src = trashPictureSrc[4]; 
    simpleDialog.showModal();
});
Tclass_6.addEventListener('click', () => {
    simpleTrashClass.textContent = trashClassHandleArray['電池類'][0];
    simpleTrashHandle.textContent = trashClassHandleArray['電池類'][1];
    simplePicture.src = trashPictureSrc[5]; 
    simpleDialog.showModal();
});
Tclass_7.addEventListener('click', () => {
    simpleTrashClass.textContent = trashClassHandleArray['照明光源(增強)'][0];
    simpleTrashHandle.textContent = trashClassHandleArray['照明光源(增強)'][1];
    simplePicture.src = trashPictureSrc[6]; 
    simpleDialog.showModal();
});
Tclass_8.addEventListener('click', () => {
    simpleTrashClass.textContent = trashClassHandleArray['電子電器'][0];
    simpleTrashHandle.textContent = trashClassHandleArray['電子電器'][1];
    simplePicture.src = trashPictureSrc[7]; 
    simpleDialog.showModal();
});
Tclass_9.addEventListener('click', () => {
    simpleTrashClass.textContent = trashClassHandleArray['舊衣類'][0];
    simpleTrashHandle.textContent = trashClassHandleArray['舊衣類'][1];
    simplePicture.src = trashPictureSrc[8]; 
    simpleDialog.showModal();
});
Tclass_10.addEventListener('click', () => {
    simpleTrashClass.textContent = trashClassHandleArray['廚餘類'][0];
    simpleTrashHandle.textContent = trashClassHandleArray['廚餘類'][1];
    simplePicture.src = trashPictureSrc[9]; 
    simpleDialog.showModal();
});

//簡易插圖訊息框關閉
simpleCloseButton.addEventListener('click', () => {
    simpleDialog.close();
});





