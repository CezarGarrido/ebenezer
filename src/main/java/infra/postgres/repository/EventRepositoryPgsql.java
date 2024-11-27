/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package infra.postgres.repository;

import domain.model.Event;
import domain.model.EventCall;
import domain.model.Donor;
import domain.model.User;
import infra.postgres.config.PGConnection;
import static infra.postgres.config.PGConnection.close;
import static infra.postgres.config.PGConnection.getConnection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import domain.repository.EventRepository;

/**
 *
 * @author cezar.britez
 */
public class EventRepositoryPgsql extends PGConnection implements EventRepository {

    @Override
    public Event findById(Long id) {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }

    @Override
    public List<Event> findAll() {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }

    @Override
    public Long save(Event agenda) {
        String insertAgendaSql = "INSERT INTO events (company_id, user_creator_id, date, time, event_type, notes) "
                + "VALUES (?, ?, ?, ?, ?, ?) RETURNING id";

        String insertAgendaCallSQL = "INSERT INTO event_calls (event_id, donor_id, phone) "
                + "VALUES (?, ?, ?)";

        try {
            open();

            var connection = getConnection();

            connection.setAutoCommit(false);  // Iniciar transação

            try (
                    PreparedStatement agendaStmt = connection.prepareStatement(insertAgendaSql); PreparedStatement agendaCallStmt = connection.prepareStatement(insertAgendaCallSQL);) {

                // Inserir ou atualizar Donor
                agendaStmt.setLong(1, agenda.getCompanyId());
                agendaStmt.setLong(2, agenda.getUserCreatorId());

                LocalDateTime localDateTime = agenda.getDate();
                Timestamp timestamp = Timestamp.valueOf(localDateTime);
                agendaStmt.setTimestamp(3, timestamp);

                agendaStmt.setString(4, agenda.getTime());
                agendaStmt.setString(5, agenda.getEventType());
                agendaStmt.setString(6, agenda.getNotes());

                // Execute e capture o `id` gerado
                try (ResultSet rs = agendaStmt.executeQuery()) {
                    if (rs.next()) {
                        agenda.setId(rs.getLong("id"));
                    }
                }

                // Inserir ou atualizar endereço
                EventCall call = agenda.getCall();
                if (call != null) {
                    agendaCallStmt.setLong(1, agenda.getId());
                    agendaCallStmt.setLong(2, call.getDonorId());
                    agendaCallStmt.setString(3, call.getPhone());

                    agendaCallStmt.executeUpdate();
                }

                connection.commit();  // Finalizar transação

            } catch (SQLException e) {
                e.printStackTrace();
                connection.rollback();  // Reverter transação em caso de erro
                throw e;
            }
        } catch (SQLException e) {
            e.printStackTrace();

            throw new RuntimeException("Erro ao cadastrar evento.", e);

        } finally {
            close();
        }

        return agenda.getId();
    }

    @Override
    public void update(Event agenda) {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }

    @Override
    public List<Event> findByQuery(Long companyId, String queryFilter) {
        List<Event> events = new ArrayList<>();

        // Monta a consulta com filtro opcional por companyId
        String query = """
            SELECT a.id, a.company_id, a.event_type, a.date, a.time, a.notes, 
                   a.user_creator_id, a.created_at, a.updated_at,
                   ac.id AS call_id, ac.donor_id AS call_donor_id, ac.phone AS call_phone,
                   u.id AS user_id, u.username AS user_name,
                   d.id AS donor_id, d.name AS donor_name
            FROM events a
            LEFT JOIN event_calls ac ON a.id = ac.event_id
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

                try (ResultSet rs = stmt.executeQuery()) {
                    while (rs.next()) {
                        // Cria um novo objeto Event com os dados do resultado
                        Event agenda = new Event();
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
                            EventCall agendaCall = new EventCall();
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

}
