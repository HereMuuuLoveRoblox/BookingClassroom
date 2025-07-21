from fastapi import FastAPI
from Database import connect
from pydantic import BaseModel

from Database.methods import Get as MGet
from Database.methods import Post as MPost

from fastapi.middleware.cors import CORSMiddleware

# Connect Database
conn = connect.ConnectDB()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# สร้าง model สำหรับรับค่าจาก client
class Classroom(BaseModel):
    roomNumber: int
    roomStatus: bool
    capacity: int
    osType: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    userName: str
    password: str
    email: str
    personnelId: str

@app.get("/classroom/all")
async def get_Classrom_All():
    res = MGet.getAllRoom(conn)
    return res

@app.get("/classroom/{roomNumber}")
async def get_Classrom_Number(roomNumber: int):
    res = MGet.getRoomNumber(conn,roomNumber)
    return res

@app.get("/classroom/roomStatus/True")
async def get_Classrom_RoomStatus_True():
    res = MGet.get_room_status_true(conn)
    return res

@app.post("/classroom")
async def post_classroom(data: Classroom):
    
    try:
        res = MPost.postClassRoom(conn, data)
        if "error" in res:
            return {"error": res["error"]}
        else:
            return {"message": "เพิ่มข้อมูลสำเร็จ", "result": res}
        
    except Exception as e:
        return {"error": str(e)}
    
    
@app.get("/users/all")
async def get_Users_All():
    res = MGet.getAllUsers(conn)
    return res

@app.get("/users/personnelId/{personnelId}")
async def get_User_By_PersonnelId(personnelId: str):
    res = MGet.getUserByPersonnelId(conn, personnelId)
    return res

@app.get("/users/userName/{UserName}")
async def get_User_By_UserName(UserName: str):
    res = MGet.getUserByUserName(conn, UserName)
    return res

@app.get("/users/userId/{userId}")
async def get_User_By_UserId(userId: int):
    res = MGet.getUserByUserId(conn, userId)
    return res

@app.get("/users/email/{email}")
async def get_User_By_Email(email: str):
    res = MGet.getUserByEmail(conn, email)
    return res

@app.post("/users/login")
async def post_user_login(data: UserLogin):
    try:
        res = MPost.postUserLogin(conn, data)
        if "error" in res:
            return {"error": res["error"]}
        else:
            return {"message": "User login successfully", "result": res}
        
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/users/register")
async def post_user_register(data: UserRegister):
    try:
        res = MPost.postUserRegister(conn, data)
        if "error" in res:
            return {"error": res["error"]}
        else:
            return {"message": "User registered successfully", "result": res}

    except Exception as e:
        return {"error": str(e)}

@app.put("/users/update/{userID}")
async def update_user(userID: int, data: UserRegister):
    try:
        res = MPost.postUserUpdate(conn, userID, data)
        if "error" in res:
            return {"error": res["error"]}
        else:
            return {"message": "User updated successfully", "result": res}
        
    except Exception as e:
        return {"error": str(e)}
