import random
import string
import datetime
## Category nominal ##
# ตั้งเวลา 0
# ถามเวลาตอนนี้ 1
# เลื่อนเวลา 2
# รายงาน task 3
# ยืนยันว่าตื่นแล้ว 4
#######################

number = ["หนึ่ง","สอง","สาม","สี่","ห้า","หก","เจ็ด","แปด","เก้า","สิบ","สิบเอ็ด"]
num = [1,2,3,4,5,6,7,8,9,10,11]
# handle = ["สิบ","เอ็ด","บ่าย","ยี่","ครึ่ง"]
hr = ["โมง","นาฬิกา","ชั่วโมง"]
m = ["นาที"]
gwjResponse  = ["ไงเพื่อน","จ๋า","ว่าไง"]
work = ["เปิดตัวโกวาจี","ประชุมกับท่านโก","เดทกับน้องโก"]

test = "โกวาจี"
test0 = "เรา ตื่น หก โมง นะ พรุ่งนี้"
test1 = "ขณะ นี้ กี่โมง"
test2 = "นอน ต่อ อีก ครึ่ง ชั่วโมง"
test3 = "วันนี้ มี งาน อะไร ต้อง ทำ บ้าง"
test4 = "ตื่น แล้ว"

#more test set
test00 = "พรุ่งนี้ เช้า ตื่น สิบ โมง สิบ ห้า นะ"

print(type(number[2]))
print(type("สิบ"))

def generateResponseText(text,category):
    textList = text.split()
    h = 99
    m = 99
    count = 0
    for i,t in enumerate(textList):
        for n, nword in enumerate(number):
            if((t == nword) & (count > 1)):
                m = m + (n + 1)
            if((t == nword) & (count == 1)):
                m = n+1
                count+=1
                if(textList[i+1] == "สิบ"):
                    m = m*10
            if((t == nword) & (count == 0)):
                h = n+1
                count+=1
    if(text=="โกวาจี"):
         return gwjResponse[random.randint(0,len(gwjResponse)-1)]
    if(category == 0):
        if(h!=99 & m!=99):
            return "ตั้งปลุกตอน"+str(h)+"โมง"+str(m)+"นาทีเรียบร้อย"
        if(h!=99 & m==99):
            return "ตั้งปลุกตอน"+str(h)+"โมงเรียบร้อย"
    if(category == 1):
        currentTime = str(datetime.datetime.now().time());
        h=currentTime[0:2]
        m=currentTime[3:5]
        return "ตอนนี้เป็นเวลา"+h+"นาฬิกา"+m+"นาที"
    if(category == 2):
        return "เลื่อนเวลาปลุกเรียบร้อย"
    if(category == 3):
        return "วันนี้คุณมีงาน"+work[random.randint(0,len(work)-1)]+"ตอน"+str(random.randint(2,6))+"โมง"
    if(category == 4):
        return "รับทราบ"


print(generateResponseText("โกวาจี",0))
# print("".join(gwjResponse))
print(generateResponseText(test0,0))
print(generateResponseText(test1,1))
print(generateResponseText(test2,2))
print(generateResponseText(test3,3))
print(generateResponseText(test4,4))
