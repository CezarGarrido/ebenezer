package infra.postgres.repository;

import domain.model.Donation;
import domain.repository.DonationRepository;
import infra.postgres.config.PGConnection;

import java.sql.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class DonationRepositoryPgsql extends PGConnection implements DonationRepository {

    @Override
    public Donation findById(Long id) {
        String query = "SELECT * FROM donations WHERE id = ? AND deleted_at IS NULL";
        try (Connection connection = getConnection(); PreparedStatement preparedStatement = connection.prepareStatement(query)) {
            preparedStatement.setLong(1, id);
            ResultSet resultSet = preparedStatement.executeQuery();
            if (resultSet.next()) {
                //return mapResultSetToDonation(resultSet);
            }
        } catch (SQLException e) {
            e.printStackTrace(); // Substituir por logger na aplicação real
        }
        return null;
    }

    @Override
    public List<Donation> findAll() {
        String query = "SELECT * FROM donations WHERE deleted_at IS NULL";
        List<Donation> donations = new ArrayList<>();
        try (Connection connection = getConnection(); Statement statement = connection.createStatement(); ResultSet resultSet = statement.executeQuery(query)) {
            while (resultSet.next()) {
                //donations.add(mapResultSetToDonation(resultSet));
            }
        } catch (SQLException e) {
            e.printStackTrace(); // Substituir por logger na aplicação real
        }
        return donations;
    }

    @Override
    public List<Donation> findByQuery(Long companyId, String queryFilter) {
        String query = "SELECT * FROM donations WHERE company_id = ? AND (notes ILIKE ? OR CAST(amount AS TEXT) ILIKE ?) AND deleted_at IS NULL";
        List<Donation> donations = new ArrayList<>();
        try (Connection connection = getConnection(); PreparedStatement preparedStatement = connection.prepareStatement(query)) {
            preparedStatement.setLong(1, companyId);
            preparedStatement.setString(2, "%" + queryFilter + "%");
            preparedStatement.setString(3, "%" + queryFilter + "%");
            ResultSet resultSet = preparedStatement.executeQuery();
            while (resultSet.next()) {
                //donations.add(mapResultSetToDonation(resultSet));
            }
        } catch (SQLException e) {
            e.printStackTrace(); // Substituir por logger na aplicação real
        }
        return donations;
    }

    @Override
    public Long save(Donation donation) {
        String query = "INSERT INTO donations (company_id, user_creator_id, donor_id, amount, received_at, received_time, paid, notes, created_at, updated_at) "
                + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id";
        try (Connection connection = getConnection(); PreparedStatement preparedStatement = connection.prepareStatement(query)) {
            preparedStatement.setLong(1, donation.getCompanyId());
            preparedStatement.setLong(2, donation.getUserCreatorId());
            preparedStatement.setLong(3, donation.getDonorId());
            preparedStatement.setBigDecimal(4, donation.getAmount());
            LocalDateTime localDateTime = donation.getReceivedAt();
            Timestamp timestamp = Timestamp.valueOf(localDateTime);
            preparedStatement.setTimestamp(5, timestamp);
            preparedStatement.setString(6, donation.getReceivedTime());
            preparedStatement.setBoolean(7, donation.getPaid());
            preparedStatement.setString(8, donation.getNotes());
            ResultSet resultSet = preparedStatement.executeQuery();
            if (resultSet.next()) {
                return resultSet.getLong("id");
            }
        } catch (SQLException e) {
            e.printStackTrace(); // Substituir por logger na aplicação real
        }
        return null;
    }

    @Override
    public void update(Donation donation) {
        String query = "UPDATE donations SET company_id = ?, user_creator_id = ?, donor_id = ?, amount = ?, received_at = ?, received_time = ?, paid = ?, notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND deleted_at IS NULL";
        try (Connection connection = getConnection(); PreparedStatement preparedStatement = connection.prepareStatement(query)) {
            preparedStatement.setLong(1, donation.getCompanyId());
            preparedStatement.setLong(2, donation.getUserCreatorId());
            preparedStatement.setLong(3, donation.getDonorId());
            preparedStatement.setBigDecimal(4, donation.getAmount());
            LocalDateTime localDateTime = donation.getReceivedAt();
            Timestamp timestamp = Timestamp.valueOf(localDateTime);
            preparedStatement.setTimestamp(5, timestamp);
            preparedStatement.setString(6, donation.getReceivedTime());
            preparedStatement.setBoolean(7, donation.getPaid());
            preparedStatement.setString(8, donation.getNotes());
            preparedStatement.setLong(9, donation.getId());
            preparedStatement.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace(); // Substituir por logger na aplicação real
        }
    }

}
