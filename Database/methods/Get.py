def getAllRoom(conn):
    try:
        mycursor = conn.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM classroom ORDER BY CAST(roomNumber AS UNSIGNED) ASC;")
        myresult = mycursor.fetchall()
        return myresult
    
    except Exception as e:
        return {"error": str(e)}

def getRoomNumber(conn, roomNumber):
    try:
        mycursor = conn.cursor(dictionary=True)
        mycursor.execute(f"SELECT * FROM classroom WHERE roomNumber = {roomNumber}")
        myresult = mycursor.fetchall()
        return myresult

    except Exception as e:
        return {"error": str(e)}

def get_room_status_true(conn):
    try:
        mycursor = conn.cursor(dictionary=True) 
        mycursor.execute("SELECT * FROM classroom WHERE roomStatus = 1  ORDER BY CAST(roomNumber AS UNSIGNED) ASC;")
        myresult = mycursor.fetchall()
        return myresult
    
    except Exception as e:
        return {"error": str(e)}

def getAllUsers(conn):
    try:
        mycursor = conn.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM users")
        myresult = mycursor.fetchall()
        return myresult

    except Exception as e:
        return {"error": str(e)}

def getUserByUserId(conn, userID):
    try:
        mycursor = conn.cursor(dictionary=True)
        mycursor.execute(f"SELECT * FROM users WHERE userID = {userID}")
        myresult = mycursor.fetchall()
        return myresult

    except Exception as e:
        return {"error": str(e)}

def getUserByUserName(conn, UserName):
    try:
        mycursor = conn.cursor(dictionary=True)
        mycursor.execute(f"SELECT * FROM users WHERE UserName = '{UserName}'")
        myresult = mycursor.fetchall()
        return myresult

    except Exception as e:
        return {"error": str(e)}

def getUserByEmail(conn, email):
    try:
        mycursor = conn.cursor(dictionary=True)
        mycursor.execute(f"SELECT userName , role FROM users WHERE email = '{email}'")
        myresult = mycursor.fetchall()
        return myresult

    except Exception as e:
        return {"error": str(e)}
    
def getUserByPersonnelId(conn, personnelId):
    try:
        mycursor = conn.cursor(dictionary=True)
        mycursor.execute(f"SELECT * FROM users WHERE personnelId = '{personnelId}'")
        myresult = mycursor.fetchall()
        return myresult

    except Exception as e:
        return {"error": str(e)}
