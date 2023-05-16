import requests
import os
while True:
    menu = int(input("1. 정보 보기\n2. 등록하기\n3. 수정하기\n4. 삭제하기\n5. EXIT\n"))
    if menu == 1:
        os.system("cls")
        body = requests.get("http://127.0.0.1:8000/user")
        data = body.json()
        data_list = list(data)
        if data == "No user found":
            print(data,"\n")
            continue
        else:
            print("#idx-------이름-------------------나이----------------#")
            for d in range(len(data_list)):
                print(str(d)+"\t  "+data_list[d]["name"]+"\t\t  "+str(data_list[d]["age"]))
                
    elif menu == 2:
        os.system("cls")
        name = input("name: ")
        age = int(input("age: "))
        post_json_body = {
            "name":name,
            "age":age
        }
        post_body = requests.post("http://127.0.0.1:8000/user",json=post_json_body)
        
    elif menu == 3:
        os.system("cls")
        print("#idx-------이름-------------------나이----------------#")
        for d in range(len(data_list)):
            print(str(d)+"\t  "+data_list[d]["name"]+"\t\t  "+str(data_list[d]["age"]))
                
        idx = int(input("몇 번을 수정하시겠습니까? "))
        name = input("name: ")
        age = int(input("age: "))
        put_json_body = {
            "idx":idx,
            "name":name,
            "age":age
        }
        put_body = requests.put("http://127.0.0.1:8000/user",json=put_json_body)
        
    elif menu == 4:
        os.system("cls")
        print("#idx-------이름-------------------나이----------------#")
        for d in range(len(data_list)):
            print(str(d)+"\t  "+data_list[d]["name"]+"\t\t  "+str(data_list[d]["age"]))
             
        idx = int(input("몇 번을 지우시겠습니까? "))
        del_json={"idx":idx}
        del_body = requests.delete("http://127.0.0.1:8000/user",json=put_json_body)
    elif menu == 5:
        print("Bye")
        break
    else:
        print("Wrong input")
        continue