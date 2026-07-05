from database.DB_connect import DBConnect
from model.airport import Airport
from model.tratta import Tratta


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(n, idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select t.id, t.iata_code, count(*) as N
                        from (select a.ID , a.IATA_CODE, f.AIRLINE_ID, count(*) from airports a, flights f where f.ORIGIN_AIRPORT_ID = a.ID or f.DESTINATION_AIRPORT_ID =a.ID group by a.ID , a.IATA_CODE, f.AIRLINE_ID) as t
                        group by t.id, t.iata_code
                        having N>= %s
                        order by N asc
                        """

        cursor.execute(query, (n,))

        for row in cursor:
            result.append(idMapA[row["id"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV1(idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as peso
                    from flights f
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                            """

        cursor.execute(query)

        for row in cursor:
            # result.append((idMapA[row["ORIGIN_AIRPORT_ID"]],
            #               idMapA[row["DESTINATION_AIRPORT_ID"]],
            #               row["peso"]))

            result.append(Tratta(
                idMapA[row["ORIGIN_AIRPORT_ID"]],
                idMapA[row["DESTINATION_AIRPORT_ID"]],
                row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV2(idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select 
                    t1.origin_airport_id, 
                    t1.destination_airport_id, 
                    coalesce(t1.n) + coalesce(t1.n, 0) as peso
                from (
                    select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                ) t1 
                left join (
                    select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID 
                ) t2
                on t1.origin_airport_id = t2.destination_airport_id 
                   and t1.destination_airport_id = t2.origin_airport_id 
                where t1.origin_airport_id < t1.destination_airport_id or t2.origin_airport_id < t2.destination_airport_id;"""

        cursor.execute(query)

        for row in cursor:
            # result.append((idMapA[row["ORIGIN_AIRPORT_ID"]],
            #               idMapA[row["DESTINATION_AIRPORT_ID"]],
            #               row["peso"]))

            result.append(Tratta(
                idMapA[row["ORIGIN_AIRPORT_ID"]],
                idMapA[row["DESTINATION_AIRPORT_ID"]],
                row["peso"]))

        cursor.close()
        conn.close()
        return result