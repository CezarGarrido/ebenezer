/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package infra.postgres.repository;

import domain.model.Donation;
import domain.model.Event;
import domain.model.EventCall;
import infra.postgres.config.PGConnection;
import static infra.postgres.config.PGConnection.getConnection;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Time;
import java.sql.Timestamp;

/**
 *
 * @author cezar.britez
 */
public class ScheduleDonationRepository extends PGConnection {

    public Long saveAll(Event event, EventCall eventCall, Donation donation) throws SQLException {
        String insertEventSQL = "INSERT INTO events (company_id, user_creator_id, date, time, event_type, notes) "
                + "VALUES (?, ?, ?, ?, ?, ?) RETURNING id";

        String insertEventCallSQL = "INSERT INTO event_calls (event_id, donor_id, phone, status, duration) "
                + "VALUES (?, ?, ?, ?, ?)";

        String insertDonationSQL = "INSERT INTO donations (company_id, user_creator_id, event_id, donor_id, amount, received_at, received_time, paid, notes) "
                + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id";

        Long eventId = null;
        Long donationId = null;

        try (Connection connection = getConnection()) {
            connection.setAutoCommit(false); // Inicia a transação

            try (
                    PreparedStatement eventStmt = connection.prepareStatement(insertEventSQL); PreparedStatement eventCallStmt = connection.prepareStatement(insertEventCallSQL); PreparedStatement donationStmt = connection.prepareStatement(insertDonationSQL)) {
                // 1. Salvar o evento
                eventId = saveEvent(event, eventStmt);

                // 2. Salvar as chamadas associadas ao evento
                if (eventCall != null) {
                    eventCall.setEventId(eventId); // Relaciona ao evento criado
                    saveEventCall(eventCall, eventCallStmt);
                }

                // 3. Salvar a doação associada ao evento
                if (donation != null) {
                    donation.setEventId(eventId); // Relaciona ao evento criado
                    donationId = saveDonation(donation, donationStmt);
                }

                connection.commit(); // Finaliza a transação
            } catch (SQLException e) {
                connection.rollback(); // Reverte a transação em caso de erro
                throw e; // Propaga a exceção
            }
        }

        return eventId; // Retorna o ID do evento criado
    }

    // Método auxiliar para salvar um evento
    private Long saveEvent(Event event, PreparedStatement stmt) throws SQLException {
        stmt.setLong(1, event.getCompanyId());
        stmt.setLong(2, event.getUserCreatorId());
        stmt.setTimestamp(3, Timestamp.valueOf(event.getDate()));
        stmt.setTime(4, Time.valueOf(event.getTime()));
        stmt.setString(5, event.getEventType());
        stmt.setString(6, event.getNotes());

        try (ResultSet rs = stmt.executeQuery()) {
            if (rs.next()) {
                return rs.getLong("id");
            }
        }
        throw new SQLException("Failed to insert event");
    }

// Método auxiliar para salvar uma chamada associada a um evento
    private void saveEventCall(EventCall eventCall, PreparedStatement stmt) throws SQLException {
        stmt.setLong(1, eventCall.getEventId());
        stmt.setLong(2, eventCall.getDonorId());
        stmt.setString(3, eventCall.getPhone());
        stmt.setString(4, eventCall.getStatus());
        stmt.setString(5, eventCall.getDuration());

        stmt.executeUpdate();
    }

// Método auxiliar para salvar uma doação
    private Long saveDonation(Donation donation, PreparedStatement stmt) throws SQLException {
        stmt.setLong(1, donation.getCompanyId());
        stmt.setLong(2, donation.getUserCreatorId());
        stmt.setLong(3, donation.getEventId());
        stmt.setLong(4, donation.getDonorId());
        stmt.setBigDecimal(5, donation.getAmount());
        stmt.setTimestamp(6, Timestamp.valueOf(donation.getReceivedAt()));
        stmt.setTime(7, Time.valueOf(donation.getReceivedTime()));
        stmt.setBoolean(8, donation.getPaid());
        stmt.setString(9, donation.getNotes());

        try (ResultSet rs = stmt.executeQuery()) {
            if (rs.next()) {
                return rs.getLong("id");
            }
        }
        throw new SQLException("Failed to insert donation");
    }

}
