/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package infra.postgres.config;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 *
 * @author cezar.britez
 */
public class PGConnection {
    //TODO: .ini
    String url = "jdbc:postgresql://localhost:5432/ebenezer";
    String username = "admin";
    String password = "admin";

    private static Connection con;

    public void open() {
        synchronized ("") {
            try {
                if (this.getConnection() == null || this.getConnection().isClosed()) {
                    try {
                        Class.forName("org.postgresql.Driver");
                        setCon(DriverManager.getConnection(url, username, password));
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                } else {
                }
            } catch (SQLException ex) {
                ex.printStackTrace();
            }
        }
    }

    /**
     * @return the con
     */
    public static Connection getConnection() {
        return con;
    }

    /**
     * @param aCon the con to set
     */
    public static void setCon(Connection aCon) {
        con = aCon;
    }

    public static void close() {
        try {
            con.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
