

def getAllRoom(conn):
    try:
        mycursor = conn.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM classroom")
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
    