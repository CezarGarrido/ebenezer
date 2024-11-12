/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package infra.mysql.config;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 *
 * @author cezar.britez
 */
public class DBConnection {

    private static Connection con;

    public void open() {
        synchronized ("") {
            try {
                if (this.getConnection() == null || this.getConnection().isClosed()) {
                    try {
                        String url = "jdbc:mysql://localhost:3306/ebenezer";
                        Class.forName("com.mysql.cj.jdbc.Driver");
                        setCon(DriverManager.getConnection(url, "root", "ebenezer"));
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
