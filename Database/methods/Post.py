from jose import jwt
from datetime import datetime, timedelta
import bcrypt

SECRET_KEY = "mysecretkey"  # 👉 แนะนำให้ใช้จาก .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def postClassRoom(conn, data):
    try:
        
        mycursor = conn.cursor()
        check_sql = "SELECT * FROM classroom WHERE roomNumber = %s"
        mycursor.execute(check_sql, (data.roomNumber,))
        existing = mycursor.fetchone()
        
        if existing:
            return {"error": f"ห้องหมายเลข {data.roomNumber} มีอยู่แล้ว"}
        
        
        sql = """
            INSERT INTO classroom (roomNumber, roomStatus, capacity, osType)
            VALUES (%s, %s, %s, %s)
        """
        values = (
            data.roomNumber,
            int(data.roomStatus),  # แปลง True/False เป็น 1/0
            data.capacity,
            data.osType
        )
        mycursor.execute(sql, values)
        conn.commit()
        return {
            "roomNumber": data.roomNumber,
            "roomStatus": data.roomStatus,
            "capacity": data.capacity,
            "osType": data.osType
        }

    except Exception as e:
        return {"error": str(e)}

def postUserLogin(conn, data):
    try:
        mycursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM users WHERE email = %s"
        mycursor.execute(sql, (data.email,))
        user = mycursor.fetchone()
        
        if user and bcrypt.checkpw(data.password.encode('utf-8'), user['password'].encode('utf-8')):
            # ✅ สร้าง JWT token
            token = create_access_token({"sub": user['email']})

            return {
                "email": user['email'],
                "message": "Login successful",
                "token": token
            }
        else:
            return {
                "error": "Invalid email or password"
            }
    except Exception as e:
        return {"error": str(e)}
    
def postUserRegister(conn, data):
    try:
        mycursor = conn.cursor()
        # เช็คว่าอีเมลมีอยู่แล้วหรือไม่
        check_sql = "SELECT * FROM users WHERE email = %s"
        mycursor.execute(check_sql, (data.email,))
        existing = mycursor.fetchone()
        
        # ถ้ามีอีเมลนี้อยู่แล้ว ให้คืนค่า error
        if existing:
            return {"error": "Email already exists"}
        
        # แฮชรหัสผ่าน
        hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())
        # เพิ่มข้อมูลผู้ใช้ใหม่
        sql = """
            INSERT INTO users (userName, password, email, personnelId)
            VALUES (%s, %s, %s, %s)
        """
        # เตรียมค่าเพื่อป้องกัน SQL Injection
        values = (data.userName, hashed_password.decode('utf-8'), data.email, data.personnelId)
        # รันคำสั่ง SQL
        mycursor.execute(sql, values)
        # บันทึกการเปลี่ยนแปลงในฐานข้อมูล
        conn.commit()
        
        return {"message": "User registered successfully"}
    
    except Exception as e:
        return {"error": str(e)}

def postUserUpdate(conn, userID, data):
    try:
        mycursor = conn.cursor()
        # เช็คว่าอีเมลมีอยู่แล้วหรือไม่
        check_sql = "SELECT * FROM users WHERE email = %s AND userID != %s"
        mycursor.execute(check_sql, (data.email, userID))
        existing = mycursor.fetchone()
        
        # ถ้ามีอีเมลนี้อยู่แล้ว ให้คืนค่า error
        if existing:
            return {"error": "Email already exists"}
        
        # แฮชรหัสผ่านถ้ามีการเปลี่ยนแปลง
        hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt()) if data.password else None
        
        sql = """
            UPDATE users 
            SET userName = %s, password = %s, email = %s, personnelId = %s 
            WHERE userID = %s
        """
        values = (
            data.userName,
            hashed_password.decode('utf-8') if hashed_password else None,
            data.email,
            data.personnelId,
            userID
        )
        
        mycursor.execute(sql, values)
        conn.commit()
        
        return {"message": "User updated successfully"}
    
    except Exception as e:
        return {"error": str(e)}
    
