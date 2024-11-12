/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package infra.mysql.repository;

/**
 *
 * @author cezar.britez
 */
import domain.model.Donor;
import domain.repository.DonorRepository;
import infra.mysql.config.DBConnection;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class DonorRepositoryMysql extends DBConnection implements DonorRepository {

    @Override
    public Optional<Donor> findById(Long id) {
        String query = "SELECT * FROM donors WHERE id = ?";
        try {
            open();
            PreparedStatement statement = getConnection().prepareStatement(query);
            statement.setLong(1, id);
            ResultSet resultSet = statement.executeQuery();
            if (resultSet.next()) {
                return Optional.of(mapResultSetToDonor(resultSet));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            close();
        }
        return Optional.empty();
    }

    @Override
    public List<Donor> findAll() {
        List<Donor> donors = new ArrayList<>();
        String query = "SELECT * FROM donors";
        try {
            open();
            PreparedStatement statement = getConnection().prepareStatement(query);
            ResultSet resultSet = statement.executeQuery();
            while (resultSet.next()) {
                donors.add(mapResultSetToDonor(resultSet));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            close();
        }
        return donors;
    }

    @Override
    public void save(Donor donor) {
        String query = "INSERT INTO donors (company_id, name, cnpj, ie, cpf, rg, rg_issuer, active, created_at, updated_at, user_creator_id) "
                + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        try {
            open();
            PreparedStatement statement = getConnection().prepareStatement(query, Statement.RETURN_GENERATED_KEYS);
            setDonorStatement(donor, statement);
            statement.executeUpdate();
            ResultSet generatedKeys = statement.getGeneratedKeys();
            if (generatedKeys.next()) {
                donor.setId(generatedKeys.getLong(1));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            close();
        }
    }

    @Override
    public void update(Donor donor) {
        String query = "UPDATE donors SET company_id = ?, name = ?, cnpj = ?, ie = ?, cpf = ?, rg = ?, rg_issuer = ?, active = ?, "
                + "created_at = ?, updated_at = ?, user_creator_id = ? WHERE id = ?";
        try {
            open();
            PreparedStatement statement = getConnection().prepareStatement(query);
            setDonorStatement(donor, statement);
            statement.setLong(12, donor.getId());
            statement.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            close();
        }
    }

    @Override
    public void deleteById(Long id) {
        String query = "DELETE FROM donors WHERE id = ?";
        try {
            open();
            PreparedStatement statement = getConnection().prepareStatement(query);
            statement.setLong(1, id);
            statement.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            close();
        }
    }

    private Donor mapResultSetToDonor(ResultSet resultSet) throws SQLException {
        return Donor.builder()
                .id(resultSet.getLong("id"))
                .companyId(resultSet.getLong("company_id"))
                .name(resultSet.getString("name"))
                .cnpj(resultSet.getString("cnpj"))
                .ie(resultSet.getString("ie"))
                .cpf(resultSet.getString("cpf"))
                .rg(resultSet.getString("rg"))
                .rgIssuer(resultSet.getString("rg_issuer"))
                .active(resultSet.getBoolean("active"))
                .createdAt(resultSet.getTimestamp("created_at").toLocalDateTime())
                .updatedAt(resultSet.getTimestamp("updated_at").toLocalDateTime())
                .userCreatorId(resultSet.getLong("user_creator_id"))
                .build();
    }

    private void setDonorStatement(Donor donor, PreparedStatement statement) throws SQLException {
        statement.setLong(1, donor.getCompanyId());
        statement.setString(2, donor.getName());
        statement.setString(3, donor.getCnpj());
        statement.setString(4, donor.getIe());
        statement.setString(5, donor.getCpf());
        statement.setString(6, donor.getRg());
        statement.setString(7, donor.getRgIssuer());
        statement.setBoolean(8, donor.getActive());
        statement.setTimestamp(9, Timestamp.valueOf(donor.getCreatedAt()));
        statement.setTimestamp(10, Timestamp.valueOf(donor.getUpdatedAt()));
        statement.setLong(11, donor.getUserCreatorId());
    }
}
