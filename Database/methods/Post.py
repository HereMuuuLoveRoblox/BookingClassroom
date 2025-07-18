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
