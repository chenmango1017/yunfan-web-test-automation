import requests
def gain_verify(file):
    url="https://upload.chaojiying.net/Upload/Processing.php"

    data={
        "user":"chenmango",
        "pass2":"e10adc3949ba59abbe56e057f20f883e",
        "softid":"968701",
        "codetype":1902,

    }
    files={"userfile":("captcha.png",open(file,"rb"),"image/png")}
    res=requests.post(url,data=data,files=files).json()
    return res["pic_str"]

