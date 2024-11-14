/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package infra.postgres.repository;

import domain.model.Donor;
import domain.model.DonorAddress;
import domain.model.DonorContact;
import domain.repository.DonorRepository;
import infra.postgres.config.PGConnection;
import static infra.postgres.config.PGConnection.close;
import static infra.postgres.config.PGConnection.getConnection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 *
 * @author cezar.britez
 */
public class DonorRepositoryPgsql extends PGConnection implements DonorRepository {

    @Override
    public Optional<Donor> findById(Long id) {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }

    @Override
    public List<Donor> findAll() {
        List<Donor> donors = new ArrayList<>();

        // SQL para buscar os doadores com seus contatos e endereços usando JOINs
        String query = "SELECT d.id, d.company_id, d.person_type, d.name, d.cnpj, d.ie, d.cpf, d.rg, d.rg_issuer, d.active, d.user_creator_id, "
                + "dc.id as contact_id, dc.name as contact_name, dc.phone as contact_phone, dc.email as contact_email,"
                + "da.id as address_id, da.street as address_street, da.neighborhood as address_neighborhood,"
                + "da.complement as address_complement, da.city as address_city,"
                + "da.state as address_state, da.postal_code as address_postal_code, da.number as address_number, da.country as address_country "
                + "FROM donors d "
                + "LEFT JOIN donor_contacts dc ON d.id = dc.donor_id "
                + "LEFT JOIN donor_addresses da ON d.id = da.donor_id";

        try {
            open();
            var connection = getConnection();

            try (PreparedStatement stmt = connection.prepareStatement(query); ResultSet rs = stmt.executeQuery()) {

                Donor currentDonor = null;

                while (rs.next()) {
                    // Recuperar os dados do doador
                    if (currentDonor == null || currentDonor.getId() != rs.getLong("id")) {
                        currentDonor = new Donor();
                        currentDonor.setId(rs.getLong("id"));
                        currentDonor.setCompanyId(rs.getLong("company_id"));
                        currentDonor.setPersonType(rs.getString("person_type"));
                        currentDonor.setName(rs.getString("name"));
                        currentDonor.setCnpj(rs.getString("cnpj"));
                        currentDonor.setIe(rs.getString("ie"));
                        currentDonor.setCpf(rs.getString("cpf"));
                        currentDonor.setRg(rs.getString("rg"));
                        currentDonor.setRgIssuer(rs.getString("rg_issuer"));
                        currentDonor.setActive(rs.getBoolean("active"));
                        currentDonor.setUserCreatorId(rs.getLong("user_creator_id"));

                        // Adicionar o doador à lista de doadores
                        donors.add(currentDonor);
                    }

                    // Adicionar contatos, se existirem
                    Long contactId = rs.getLong("contact_id");
                    if (contactId != null) {
                        if (currentDonor.getContacts() == null) {
                            currentDonor.setContacts(new ArrayList<>());
                        }
                        DonorContact contact = new DonorContact();
                        contact.setId(contactId);
                        contact.setName(rs.getString("contact_name"));

                        contact.setPhone(rs.getString("contact_phone"));
                        contact.setEmail(rs.getString("contact_email"));

                        currentDonor.getContacts().add(contact);
                    }

                    // Adicionar endereço, se existir
                    if (rs.getString("address_id") != null) {
                        DonorAddress address = new DonorAddress();
                        address.setId(rs.getLong("address_id"));
                        address.setStreet(rs.getString("address_street"));
                        address.setNeighborhood(rs.getString("address_neighborhood"));
                        address.setComplement(rs.getString("address_complement"));
                        address.setCity(rs.getString("address_city"));
                        address.setState(rs.getString("address_state"));
                        address.setPostalCode(rs.getString("address_postal_code"));
                        address.setNumber(rs.getString("address_number"));
                        address.setCountry(rs.getString("address_country"));
                        currentDonor.setAddress(address);
                    }
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException("Erro ao buscar todos os doadores com contatos e endereço.", e);
        } finally {
            close();
        }

        return donors;
    }

    @Override
    public Long save(Donor donor) {
        try {
            return saveDonor(donor);
        } catch (SQLException e) {
            throw new RuntimeException("Erro ao salvar o doador.", e);
        }
    }

    @Override
    public void update(Donor donor) {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }

    @Override
    public void deleteById(Long id) {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }

    // Função para salvar Donor com contatos e endereço
    public Long saveDonor(Donor donor) throws SQLException {
        String insertOrUpdateDonorSQL = "INSERT INTO donors (company_id, person_type, name, cnpj, ie, cpf, rg, rg_issuer, active, user_creator_id) "
                + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
                + "ON CONFLICT (id) DO UPDATE SET company_id = EXCLUDED.company_id, person_type = EXCLUDED.person_type, name = EXCLUDED.name, cnpj = EXCLUDED.cnpj, "
                + "ie = EXCLUDED.ie, cpf = EXCLUDED.cpf, rg = EXCLUDED.rg, rg_issuer = EXCLUDED.rg_issuer, active = EXCLUDED.active, "
                + "user_creator_id = EXCLUDED.user_creator_id "
                + "RETURNING id";

        String insertOrUpdateContactSQL = "INSERT INTO donor_contacts (donor_id, name, phone, email) "
                + "VALUES (?, ?, ?, ?) "
                + "ON CONFLICT (donor_id, phone, email) DO UPDATE SET name = EXCLUDED.name, phone = EXCLUDED.phone, email = EXCLUDED.email";

        String insertOrUpdateAddressSQL = "INSERT INTO donor_addresses (donor_id, street, neighborhood, complement, city, state, postal_code, number, country) "
                + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) "
                + "ON CONFLICT (donor_id) DO UPDATE SET street = EXCLUDED.street, neighborhood = EXCLUDED.neighborhood, "
                + "complement = EXCLUDED.complement, city = EXCLUDED.city, state = EXCLUDED.state, postal_code = EXCLUDED.postal_code, "
                + "number = EXCLUDED.number, country = EXCLUDED.country";

        try {
            open();

            var connection = getConnection();

            connection.setAutoCommit(false);  // Iniciar transação

            try (
                    PreparedStatement donorStmt = connection.prepareStatement(insertOrUpdateDonorSQL); PreparedStatement contactStmt = connection.prepareStatement(insertOrUpdateContactSQL); PreparedStatement addressStmt = connection.prepareStatement(insertOrUpdateAddressSQL)) {
                // Inserir ou atualizar Donor
                donorStmt.setLong(1, donor.getCompanyId());
                donorStmt.setString(2, donor.getPersonType());
                donorStmt.setString(3, donor.getName());
                donorStmt.setString(4, donor.getCnpj());
                donorStmt.setString(5, donor.getIe());
                donorStmt.setString(6, donor.getCpf());
                donorStmt.setString(7, donor.getRg());
                donorStmt.setString(8, donor.getRgIssuer());
                donorStmt.setBoolean(9, donor.getActive());
                donorStmt.setLong(10, donor.getUserCreatorId());
                // Execute e capture o `id` gerado
                try (ResultSet rs = donorStmt.executeQuery()) {
                    if (rs.next()) {
                        donor.setId(rs.getLong("id"));
                    }
                }

                // Inserir ou atualizar contatos
                if (donor.getContacts() != null) {

                    for (DonorContact contact : donor.getContacts()) {
                        contactStmt.setLong(1, donor.getId());
                        contactStmt.setString(2, contact.getName());
                        contactStmt.setString(3, contact.getPhone());
                        contactStmt.setString(4, contact.getEmail());

                        contactStmt.executeUpdate();
                    }
                }

                // Inserir ou atualizar endereço
                DonorAddress address = donor.getAddress();
                if (address != null) {
                    addressStmt.setLong(1, donor.getId());
                    addressStmt.setString(2, address.getStreet());
                    addressStmt.setString(3, address.getNeighborhood());
                    addressStmt.setString(4, address.getComplement());
                    addressStmt.setString(5, address.getCity());
                    addressStmt.setString(6, address.getState());
                    addressStmt.setString(7, address.getPostalCode());
                    addressStmt.setString(8, address.getNumber());
                    addressStmt.setString(9, address.getCountry());

                    addressStmt.executeUpdate();
                }

                connection.commit();  // Finalizar transação

            } catch (SQLException e) {
                e.printStackTrace();
                connection.rollback();  // Reverter transação em caso de erro
                throw e;
            }
        } catch (SQLException e) {
            e.printStackTrace();

            throw e;
        } finally {
            close();
        }

        return donor.getId();
    }

}
