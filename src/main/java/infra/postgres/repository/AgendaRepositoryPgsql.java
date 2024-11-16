/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package infra.postgres.repository;

import domain.model.Agenda;
import domain.model.AgendaCall;
import domain.repository.AgendaRepository;
import infra.postgres.config.PGConnection;
import static infra.postgres.config.PGConnection.close;
import static infra.postgres.config.PGConnection.getConnection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.List;

/**
 *
 * @author cezar.britez
 */
public class AgendaRepositoryPgsql extends PGConnection implements AgendaRepository {

    @Override
    public Agenda findById(Long id) {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }

    @Override
    public List<Agenda> findAll() {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }

    @Override
    public Long save(Agenda agenda) {
        String insertAgendaSql = "INSERT INTO agenda (company_id, user_creator_id, date, hour, event_type, obs) "
                + "VALUES (?, ?, ?, ?, ?, ?) RETURNING id";

        String insertAgendaCallSQL = "INSERT INTO agenda_calls (agenda_id, donor_id, phone) "
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

                agendaStmt.setString(4, agenda.getHour());
                agendaStmt.setString(5, agenda.getEventType());
                agendaStmt.setString(6, agenda.getObs());

                // Execute e capture o `id` gerado
                try (ResultSet rs = agendaStmt.executeQuery()) {
                    if (rs.next()) {
                        agenda.setId(rs.getLong("id"));
                    }
                }

                // Inserir ou atualizar endereço
                AgendaCall call = agenda.getCall();
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
    public void update(Agenda agenda) {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }

}
