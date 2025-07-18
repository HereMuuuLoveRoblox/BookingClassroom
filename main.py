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

@app.get("/classroom/all")
async def get_Classrom_All():
    res = MGet.getAllRoom(conn)
    return res

@app.get("/classroom/{roomNumber}")
async def get_Classrom_Number(roomNumber: int):
    res = MGet.getRoomNumber(conn,roomNumber)
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