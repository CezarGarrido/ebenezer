/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package infra.postgres.repository;

import domain.model.Donation;
import domain.model.Appointment;
import domain.model.AppointmentCall;
import domain.model.Donor;
import domain.model.User;
import infra.postgres.config.PGConnection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import domain.repository.AppointmentRepository;
import java.time.LocalDate;
import java.time.temporal.TemporalAdjusters;

/**
 *
 * @author cezar.britez
 */
public class AppointmentRepositoryPgsql extends PGConnection implements AppointmentRepository {

    @Override
    public Appointment findById(Long companyId, Long id) {
        String query = """
        SELECT a.id, a.company_id, a.event_type, a.date, a.time, a.notes, 
               a.user_creator_id, a.created_at, a.updated_at,
               ac.id AS call_id, ac.donor_id AS call_donor_id, ac.phone AS call_phone,
               u.id AS user_id, u.username AS user_name,
               d.id AS donor_id, d.name AS donor_name,
               dn.id AS donation_id, dn.amount AS donation_amount, dn.created_at AS donation_created_at
        FROM appointments a
        LEFT JOIN appointment_calls ac ON a.id = ac.appointment_id
        LEFT JOIN donors d ON d.id = ac.donor_id
        LEFT JOIN donations dn ON a.id = dn.appointment_id
        LEFT JOIN users u ON a.user_creator_id = u.id
        WHERE a.company_id = ? AND a.id = ?
    """;

        try {
            open();
            var connection = getConnection();

            try (PreparedStatement stmt = connection.prepareStatement(query)) {
                stmt.setLong(1, companyId);
                stmt.setLong(2, id);

                try (ResultSet rs = stmt.executeQuery()) {
                    if (rs.next()) {
                        // Cria o objeto Appointment com os dados do resultado
                        Appointment appointment = new Appointment();
                        appointment.setId(rs.getLong("id"));
                        appointment.setCompanyId(rs.getLong("company_id"));
                        appointment.setEventType(rs.getString("event_type"));
                        appointment.setDate(rs.getObject("date", LocalDateTime.class));
                        appointment.setTime(rs.getString("time"));
                        appointment.setNotes(rs.getString("notes"));
                        appointment.setUserCreatorId(rs.getLong("user_creator_id"));
                        appointment.setCreatedAt(rs.getObject("created_at", LocalDateTime.class));
                        appointment.setUpdatedAt(rs.getObject("updated_at", LocalDateTime.class));

                        // Configura a chamada associada ao Appointment, se presente
                        if (rs.getLong("call_id") != 0) {
                            AppointmentCall appointmentCall = new AppointmentCall();
                            appointmentCall.setId(rs.getLong("call_id"));
                            appointmentCall.setDonorId(rs.getLong("call_donor_id"));
                            appointmentCall.setPhone(rs.getString("call_phone"));

                            Donor donor = new Donor();
                            donor.setId(rs.getLong("donor_id"));
                            donor.setName(rs.getString("donor_name"));
                            appointmentCall.setDonor(donor);

                            appointment.setCall(appointmentCall);
                        }

                        if (rs.getLong("donation_id") != 0) {
                            var donation = new Donation();
                            donation.setId(rs.getLong("donation_id"));
                            donation.setAmount(rs.getBigDecimal("donation_amount"));
                            donation.setCreatedAt(rs.getObject("donation_created_at", LocalDateTime.class));
                            appointment.setDonation(donation);
                        }

                        // Configura o usuário criador associado ao Appointment
                        if (rs.getLong("user_id") != 0) {
                            User user = new User();
                            user.setId(rs.getLong("user_id"));
                            user.setName(rs.getString("user_name"));
                            appointment.setUser(user);
                        }

                        return appointment;
                    }
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException("Erro ao buscar o Appointment pelo ID: " + id + " e companyId: " + companyId, e);
        } finally {
            close();
        }

        return null; // Retorna null se nenhum registro for encontrado
    }

    @Override
    public List<Appointment> findAll() {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }

    @Override
    public Long save(Appointment event) {
        String insertEventSQL = "INSERT INTO appointments (company_id, user_creator_id, date, time, event_type, notes) "
                + "VALUES (?, ?, ?, ?, ?, ?) RETURNING id";

        String insertEventCallSQL = "INSERT INTO appointment_calls (appointment_id, donor_id, phone, status, duration) "
                + "VALUES (?, ?, ?, ?, ?)";

        String insertDonationSQL = "INSERT INTO donations (company_id, user_creator_id, appointment_id, donor_id, amount, received_at, received_time, paid, notes) "
                + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id";

        Long eventId = null;

        try {
            open();
            var connection = getConnection();

            connection.setAutoCommit(false); // Inicia a transação

            try (
                    PreparedStatement eventStmt = connection.prepareStatement(insertEventSQL); PreparedStatement eventCallStmt = connection.prepareStatement(insertEventCallSQL); PreparedStatement donationStmt = connection.prepareStatement(insertDonationSQL)) {
                // 1. Salvar o evento
                eventId = saveEvent(event, eventStmt);

                // 2. Salvar as chamadas associadas ao evento
                if (event.getCall() != null) {
                    var eventCall = event.getCall();
                    eventCall.setAppointmentId(eventId); // Relaciona ao evento criado
                    saveEventCall(eventCall, eventCallStmt);

                }

                // 3. Salvar a doação associada ao evento
                if (event.getDonation() != null) {
                    var donation = event.getDonation();
                    donation.setAppointmentId(eventId); // Relaciona ao evento criado
                    donation.setCompanyId(event.getCompanyId()); // Relaciona ao evento criado
                    donation.setUserCreatorId(event.getUserCreatorId()); // Relaciona ao evento criado
                    saveDonation(donation, donationStmt);
                }

                connection.commit(); // Finaliza a transação
            } catch (SQLException e) {
                e.printStackTrace();
                connection.rollback();  // Reverter transação em caso de erro
                throw e;
            }

        } catch (SQLException e) {
            throw new RuntimeException("Erro ao salvar doação: ", e);
        } finally {
            close();
        }

        return eventId; // Retorna o ID do evento criado
    }

    // Método auxiliar para salvar um evento
    private Long saveEvent(Appointment event, PreparedStatement stmt) throws SQLException {
        stmt.setLong(1, event.getCompanyId());
        stmt.setLong(2, event.getUserCreatorId());
        stmt.setTimestamp(3, Timestamp.valueOf(event.getDate()));
        stmt.setString(4, event.getTime());
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
    private void saveEventCall(AppointmentCall eventCall, PreparedStatement stmt) throws SQLException {
        stmt.setLong(1, eventCall.getAppointmentId());
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
        stmt.setLong(3, donation.getAppointmentId());
        stmt.setLong(4, donation.getDonorId());
        stmt.setBigDecimal(5, donation.getAmount());
        stmt.setTimestamp(6, Timestamp.valueOf(donation.getReceivedAt()));
        stmt.setString(7, donation.getReceivedTime());
        stmt.setBoolean(8, donation.getPaid());
        stmt.setString(9, donation.getNotes());

        try (ResultSet rs = stmt.executeQuery()) {
            if (rs.next()) {
                return rs.getLong("id");
            }
        }

        throw new SQLException("Failed to insert donation");
    }

    @Override
    public List<Appointment> findByQuery(Long companyId, String queryFilter, LocalDateTime date) {
        List<Appointment> events = new ArrayList<>();

        // Monta a consulta com filtro opcional por companyId
        String query = """
            SELECT a.id, a.company_id, a.event_type, a.date, a.time, a.notes, 
                   a.user_creator_id, a.created_at, a.updated_at,
                   ac.id AS call_id, ac.donor_id AS call_donor_id, ac.phone AS call_phone,
                   u.id AS user_id, u.username AS user_name,
                   d.id AS donor_id, d.name AS donor_name
            FROM appointments a
            LEFT JOIN appointment_calls ac ON a.id = ac.appointment_id
            LEFT JOIN donors d ON d.id = ac.donor_id            
            LEFT JOIN users u ON a.user_creator_id = u.id 
            WHERE 1=1
            """;

        // Adiciona filtro de companyId, se presente
        if (companyId != null) {
            query += "AND a.company_id = ? ";
        }

        // Adiciona filtro de queryFilter, se presente
        if (queryFilter != null && !queryFilter.isBlank()) {
            query += "AND (d.name ILIKE ? OR CAST(a.id AS TEXT) ILIKE ?) ";
        }

        // Adiciona filtro de data, se presente
        // if (date != null) {
        //     query += "AND a.date::DATE = ? ";
        // }
        if (date.toLocalDate() != null) {
            query += "AND a.date::DATE BETWEEN ? AND ? ";
        }

        try {
            open();
            var connection = getConnection();

            try (PreparedStatement stmt = connection.prepareStatement(query)) {
                int paramIndex = 1;

                // Configura o parâmetro companyId, se presente
                if (companyId != null) {
                    stmt.setLong(paramIndex++, companyId);
                }

                // Configura os parâmetros da queryFilter, se presente
                if (queryFilter != null && !queryFilter.isBlank()) {
                    String filter = "%" + queryFilter.trim() + "%";
                    stmt.setString(paramIndex++, filter);
                    stmt.setString(paramIndex++, filter);
                }

                // Configura o parâmetro de data, se presente
                if (date != null) {
                    LocalDate startDate = date.toLocalDate().with(TemporalAdjusters.firstDayOfMonth());
                    LocalDate endDate = date.toLocalDate().with(TemporalAdjusters.lastDayOfMonth());

                    stmt.setObject(paramIndex++, startDate);
                    stmt.setObject(paramIndex++, endDate);

                }

                try (ResultSet rs = stmt.executeQuery()) {
                    while (rs.next()) {
                        // Cria um novo objeto Appointment com os dados do resultado
                        Appointment agenda = new Appointment();
                        agenda.setId(rs.getLong("id"));
                        agenda.setCompanyId(rs.getLong("company_id"));
                        agenda.setEventType(rs.getString("event_type"));
                        agenda.setDate(rs.getObject("date", LocalDateTime.class));
                        agenda.setTime(rs.getString("time"));
                        agenda.setNotes(rs.getString("notes"));
                        agenda.setUserCreatorId(rs.getLong("user_creator_id"));
                        agenda.setCreatedAt(rs.getObject("created_at", LocalDateTime.class));
                        agenda.setUpdatedAt(rs.getObject("updated_at", LocalDateTime.class));

                        // Configura chamadas associadas à agenda
                        if (rs.getLong("call_id") != 0) {
                            AppointmentCall agendaCall = new AppointmentCall();
                            agendaCall.setId(rs.getLong("call_id"));
                            agendaCall.setDonorId(rs.getLong("call_donor_id"));
                            agendaCall.setPhone(rs.getString("call_phone"));

                            Donor donor = new Donor();
                            donor.setName(rs.getString("donor_name"));
                            agendaCall.setDonor(donor);

                            agenda.setCall(agendaCall);
                        }

                        if (rs.getLong("user_id") != 0) {
                            User user = new User();
                            user.setId(rs.getLong("user_id"));
                            user.setName(rs.getString("user_name"));
                            agenda.setUser(user);
                        }

                        events.add(agenda);
                    }
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException("Erro ao buscar eventos com o filtro: " + queryFilter + ", para companyId: " + companyId, e);
        } finally {
            close();
        }

        return events;
    }

    @Override
    public void update(Appointment event) {
        // SQL para atualizar o evento
        String updateEventSQL = "UPDATE appointments SET company_id = ?, user_creator_id = ?, date = ?, time = ?, event_type = ?, notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?";
        // SQL para atualizar chamadas do evento
        String updateEventCallSQL = "UPDATE appointment_calls SET donor_id = ?, phone = ?, status = ?, duration = ?, updated_at = CURRENT_TIMESTAMP WHERE appointment_id = ?";
        // SQL para verificar existência da doação
        String checkDonationSQL = "SELECT COUNT(*) FROM donations WHERE appointment_id = ?";
        // SQL para inserir doação
        String insertDonationSQL = "INSERT INTO donations (company_id, user_creator_id, appointment_id, donor_id, amount, received_at, received_time, paid, notes, created_at, updated_at) "
                + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)";
        // SQL para atualizar doação
        String updateDonationSQL = "UPDATE donations SET company_id = ?, user_creator_id = ?, donor_id = ?, amount = ?, received_at = ?, received_time = ?, paid = ?, notes = ?, updated_at = CURRENT_TIMESTAMP WHERE appointment_id = ?";

        try {
            open();
            var connection = getConnection();

            connection.setAutoCommit(false); // Inicia a transação

            try (
                    PreparedStatement eventStmt = connection.prepareStatement(updateEventSQL); PreparedStatement eventCallStmt = connection.prepareStatement(updateEventCallSQL); PreparedStatement checkDonationStmt = connection.prepareStatement(checkDonationSQL); PreparedStatement insertDonationStmt = connection.prepareStatement(insertDonationSQL); PreparedStatement updateDonationStmt = connection.prepareStatement(updateDonationSQL)) {

                // 1. Atualizar o evento
                updateEvent(event, eventStmt);

                // 2. Atualizar chamadas associadas ao evento
                if (event.getCall() != null) {
                    var eventCall = event.getCall();
                    eventCall.setAppointmentId(event.getId()); // Relaciona a chamada ao evento
                    updateEventCall(eventCall, eventCallStmt);
                }

                // 3. Verificar e inserir/atualizar a doação
                if (event.getDonation() != null) {
                    var donation = event.getDonation();
                    donation.setAppointmentId(event.getId());
                    donation.setCompanyId(event.getCompanyId());
                    donation.setUserCreatorId(event.getUserCreatorId());

                    if (donationExists(event.getId(), checkDonationStmt)) {
                        // Atualiza a doação se já existir
                        updateDonation(donation, updateDonationStmt);
                    } else {
                        // Insere uma nova doação
                        insertDonation(donation, insertDonationStmt);
                    }
                }

                connection.commit(); // Finaliza a transação
            } catch (SQLException e) {
                connection.rollback(); // Reverter transação em caso de erro
                throw new RuntimeException("Erro ao atualizar dados: ", e);
            }

        } catch (SQLException e) {
            throw new RuntimeException("Erro na conexão com o banco de dados: ", e);
        } finally {
            close();
        }
    }

    private boolean donationExists(Long appointmentId, PreparedStatement stmt) throws SQLException {
        stmt.setLong(1, appointmentId);
        try (var rs = stmt.executeQuery()) {
            if (rs.next()) {
                return rs.getInt(1) > 0; // Retorna true se encontrar registros
            }
        }
        return false;
    }

    private void updateDonation(Donation donation, PreparedStatement stmt) throws SQLException {
        stmt.setLong(1, donation.getCompanyId());
        stmt.setLong(2, donation.getUserCreatorId());
        stmt.setLong(3, donation.getDonorId());
        stmt.setBigDecimal(4, donation.getAmount());
        stmt.setTimestamp(5, Timestamp.valueOf(donation.getReceivedAt()));
        stmt.setString(6, donation.getReceivedTime());
        stmt.setBoolean(7, donation.getPaid());
        stmt.setString(8, donation.getNotes());
        stmt.setLong(9, donation.getAppointmentId());
        stmt.executeUpdate();
    }

    private void insertDonation(Donation donation, PreparedStatement stmt) throws SQLException {
        stmt.setLong(1, donation.getCompanyId());
        stmt.setLong(2, donation.getUserCreatorId());
        stmt.setLong(3, donation.getAppointmentId());
        stmt.setLong(4, donation.getDonorId());
        stmt.setBigDecimal(5, donation.getAmount());
        stmt.setTimestamp(6, Timestamp.valueOf(donation.getReceivedAt()));
        stmt.setString(7, donation.getReceivedTime());
        stmt.setBoolean(8, donation.getPaid());
        stmt.setString(9, donation.getNotes());
        stmt.executeUpdate();
    }

// Método auxiliar para atualizar um evento
    private void updateEvent(Appointment event, PreparedStatement stmt) throws SQLException {
        stmt.setLong(1, event.getCompanyId());
        stmt.setLong(2, event.getUserCreatorId());
        stmt.setTimestamp(3, Timestamp.valueOf(event.getDate()));
        stmt.setString(4, event.getTime());
        stmt.setString(5, event.getEventType());
        stmt.setString(6, event.getNotes());
        stmt.setLong(7, event.getId()); // ID do evento para atualização

        stmt.executeUpdate();
    }

// Método auxiliar para atualizar uma chamada associada a um evento
    private void updateEventCall(AppointmentCall eventCall, PreparedStatement stmt) throws SQLException {
        stmt.setLong(1, eventCall.getDonorId());
        stmt.setString(2, eventCall.getPhone());
        stmt.setString(3, eventCall.getStatus());
        stmt.setString(4, eventCall.getDuration());
        stmt.setLong(5, eventCall.getAppointmentId()); // Relaciona à ID do evento

        stmt.executeUpdate();
    }

// Método auxiliar para realizar o Upsert de uma doação
    private void insertOrUpdateDonation(Donation donation, PreparedStatement stmt) throws SQLException {
        stmt.setLong(1, donation.getCompanyId());
        stmt.setLong(2, donation.getUserCreatorId());
        stmt.setLong(3, donation.getAppointmentId());
        stmt.setLong(4, donation.getDonorId());
        stmt.setBigDecimal(5, donation.getAmount());
        stmt.setTimestamp(6, Timestamp.valueOf(donation.getReceivedAt()));
        stmt.setString(7, donation.getReceivedTime());
        stmt.setBoolean(8, donation.getPaid());
        stmt.setString(9, donation.getNotes());
        stmt.executeUpdate();
    }

}
