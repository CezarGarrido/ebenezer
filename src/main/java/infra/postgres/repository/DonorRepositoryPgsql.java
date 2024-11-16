/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package infra.postgres.repository;

import domain.model.Donor;
import domain.model.DonorAddress;
import domain.model.DonorContact;
import domain.model.User;
import domain.repository.DonorRepository;
import infra.postgres.config.PGConnection;
import static infra.postgres.config.PGConnection.close;
import static infra.postgres.config.PGConnection.getConnection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author cezar.britez
 */
public class DonorRepositoryPgsql extends PGConnection implements DonorRepository {

    @Override
    public Donor findById(Long id) {
        if (id == null) {
            throw new IllegalArgumentException("ID não pode ser nulo.");
        }

        Donor donor = null;

        // SQL para buscar o doador com seus contatos e endereços usando JOINs
        String query = "SELECT d.id, d.company_id, d.person_type, d.name, d.cnpj, d.ie, d.cpf, d.rg, d.rg_issuer, d.active, d.user_creator_id, d.created_at, d.updated_at, "
                + "dc.id as contact_id, dc.name as contact_name, dc.phone as contact_phone, dc.email as contact_email, "
                + "da.id as address_id, da.street as address_street, da.neighborhood as address_neighborhood, "
                + "da.complement as address_complement, da.city as address_city, da.state as address_state, da.postal_code as address_postal_code, "
                + "da.number as address_number, da.country as address_country, "
                + "u.id as user_id, u.username as user_name "
                + "FROM donors d "
                + "LEFT JOIN users u ON d.user_creator_id = u.id "
                + "LEFT JOIN donor_contacts dc ON d.id = dc.donor_id "
                + "LEFT JOIN donor_addresses da ON d.id = da.donor_id "
                + "WHERE d.id = ?"; // Adiciona filtro pelo ID do doador

        try {
            open();
            var connection = getConnection();

            try (PreparedStatement stmt = connection.prepareStatement(query)) {
                stmt.setLong(1, id); // Setando o ID do doador

                try (ResultSet rs = stmt.executeQuery()) {

                    if (rs.next()) {
                        donor = new Donor();
                        donor.setId(rs.getLong("id"));
                        donor.setCompanyId(rs.getLong("company_id"));
                        donor.setPersonType(rs.getString("person_type"));
                        donor.setName(rs.getString("name"));
                        donor.setCnpj(rs.getString("cnpj"));
                        donor.setIe(rs.getString("ie"));
                        donor.setCpf(rs.getString("cpf"));
                        donor.setRg(rs.getString("rg"));
                        donor.setRgIssuer(rs.getString("rg_issuer"));
                        donor.setActive(rs.getBoolean("active"));
                        donor.setUserCreatorId(rs.getLong("user_creator_id"));
                        donor.setCreatedAt(rs.getObject("created_at", LocalDateTime.class));
                        donor.setUpdatedAt(rs.getObject("updated_at", LocalDateTime.class));

                        // Adicionando usuário criador, se existir
                        if (rs.getString("user_name") != null) {
                            var user = new User();
                            user.setId(rs.getLong("user_id"));
                            user.setName(rs.getString("user_name"));
                            donor.setUser(user);
                        }

                        // Adicionando contatos, se existirem
                        String contactName = rs.getString("contact_name");
                        if (contactName != null) {
                            if (donor.getContacts() == null) {
                                donor.setContacts(new ArrayList<>());
                            }
                            DonorContact contact = new DonorContact();
                            contact.setId(rs.getLong("contact_id"));
                            contact.setName(rs.getString("contact_name"));
                            contact.setPhone(rs.getString("contact_phone"));
                            contact.setEmail(rs.getString("contact_email"));

                            donor.getContacts().add(contact);
                        }

                        // Adicionando endereço, se existir
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

                            donor.setAddress(address);
                        }
                    }
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException("Erro ao buscar o doador com ID: " + id, e);
        } finally {
            close();
        }

        return donor;
    }

    @Override
    public List<Donor> findAll() {
        List<Donor> donors = new ArrayList<>();

        // SQL para buscar os doadores com seus contatos e endereços usando JOINs
        String query = "SELECT d.id, d.company_id, d.person_type, d.name, d.cnpj, d.ie, d.cpf, d.rg, d.rg_issuer, d.active, d.user_creator_id, d.created_at, d.updated_at, "
                + "dc.id as contact_id, dc.name as contact_name, dc.phone as contact_phone, dc.email as contact_email,"
                + "da.id as address_id, da.street as address_street, da.neighborhood as address_neighborhood,"
                + "da.complement as address_complement, da.city as address_city,"
                + "da.state as address_state, da.postal_code as address_postal_code, da.number as address_number, da.country as address_country, "
                + "u.id as user_id, u.username as user_name "
                + "FROM donors d "
                + "LEFT JOIN users u ON d.user_creator_id = u.id "
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
                        currentDonor.setCreatedAt(rs.getObject("created_at", LocalDateTime.class));
                        currentDonor.setUpdatedAt(rs.getObject("updated_at", LocalDateTime.class));

                        // Adicionar o doador à lista de doadores
                        donors.add(currentDonor);
                    }

                    if (rs.getString("user_name") != null) {
                        var newUser = new User();
                        newUser.setId(rs.getLong("user_id"));
                        newUser.setName(rs.getString("user_name"));
                        currentDonor.setUser(newUser);
                    }

                    // Adicionar contatos, se existirem
                    String contactName = rs.getString("contact_name");
                    if (contactName != null) {
                        if (currentDonor.getContacts() == null) {
                            currentDonor.setContacts(new ArrayList<>());
                        }
                        DonorContact contact = new DonorContact();
                        contact.setId(rs.getLong("contact_id"));
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
    public List<Donor> findByQuery(Long companyId, String queryFilter) {
        List<Donor> donors = new ArrayList<>();

        // Monta a consulta com filtro opcional por companyId
        String query = "SELECT d.id, d.company_id, d.person_type, d.name, d.cnpj, d.ie, d.cpf, d.rg, d.rg_issuer, d.active, d.user_creator_id, d.created_at, d.updated_at, "
                + "dc.id as contact_id, dc.name as contact_name, dc.phone as contact_phone, dc.email as contact_email, "
                + "da.id as address_id, da.street as address_street, da.neighborhood as address_neighborhood, "
                + "da.complement as address_complement, da.city as address_city, "
                + "da.state as address_state, da.postal_code as address_postal_code, da.number as address_number, da.country as address_country, "
                + "u.id as user_id, u.username as user_name "
                + "FROM donors d "
                + "LEFT JOIN users u ON d.user_creator_id = u.id "
                + "LEFT JOIN donor_contacts dc ON d.id = dc.donor_id "
                + "LEFT JOIN donor_addresses da ON d.id = da.donor_id "
                + "WHERE 1=1 "; // Base para adicionar filtros dinamicamente

        // Adiciona filtro de companyId, se presente
        if (companyId != null) {
            query += "AND d.company_id = ? ";
        }

        // Adiciona filtro de queryFilter, se presente
        if (queryFilter != null && !queryFilter.isBlank()) {
            query += "AND (d.name ILIKE ? OR CAST(d.id AS TEXT) ILIKE ?) ";
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
                    Donor currentDonor = null;

                    while (rs.next()) {
                        // Mesma lógica para criar e adicionar doadores
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
                            currentDonor.setCreatedAt(rs.getObject("created_at", LocalDateTime.class));
                            currentDonor.setUpdatedAt(rs.getObject("updated_at", LocalDateTime.class));

                            donors.add(currentDonor);
                        }

                        if (rs.getString("user_name") != null) {
                            var newUser = new User();
                            newUser.setId(rs.getLong("user_id"));
                            newUser.setName(rs.getString("user_name"));
                            currentDonor.setUser(newUser);
                        }

                        String contactName = rs.getString("contact_name");
                        if (contactName != null) {
                            if (currentDonor.getContacts() == null) {
                                currentDonor.setContacts(new ArrayList<>());
                            }
                            DonorContact contact = new DonorContact();
                            contact.setId(rs.getLong("contact_id"));
                            contact.setName(rs.getString("contact_name"));
                            contact.setPhone(rs.getString("contact_phone"));
                            contact.setEmail(rs.getString("contact_email"));
                            currentDonor.getContacts().add(contact);
                        }

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
            }
        } catch (SQLException e) {
            throw new RuntimeException("Erro ao buscar doadores com o filtro: " + queryFilter + ", para companyId: " + companyId, e);
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
        try {
            updateDonor(donor);
        } catch (SQLException e) {
            throw new RuntimeException("Erro ao atualizar o doador.", e);
        }
    }

    @Override
    public void deleteById(Long id) {
        throw new UnsupportedOperationException("Not supported yet."); // Generated from nbfs://nbhost/SystemFileSystem/Templates/Classes/Code/GeneratedMethodBody
    }

    // Função para salvar Donor com contatos e endereço
    public Long saveDonor(Donor donor) throws SQLException {
        String insertOrUpdateDonorSQL = "INSERT INTO donors (company_id, person_type, name, cnpj, ie, cpf, rg, rg_issuer, active, user_creator_id) "
                + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id";

        String insertOrUpdateContactSQL = "INSERT INTO donor_contacts (donor_id, name, phone, email) "
                + "VALUES (?, ?, ?, ?)";

        String insertOrUpdateAddressSQL = "INSERT INTO donor_addresses (donor_id, street, neighborhood, complement, city, state, postal_code, number, country) "
                + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";

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

    public Long updateDonor(Donor donor) throws SQLException {
        var updateDonorSQL = "UPDATE donors SET company_id = ?, person_type = ?, name = ?, cnpj = ?, ie = ?, cpf = ?, rg = ?, rg_issuer = ?, active = ?, user_creator_id = ? "
                + "WHERE id = ?";

        String upsertContactSQL = "INSERT INTO donor_contacts (donor_id, name, phone, email) "
                + "VALUES (?, ?, ?, ?) "
                + "ON CONFLICT (donor_id, phone, email) "
                + "DO UPDATE SET name = EXCLUDED.name, phone = EXCLUDED.phone, email = EXCLUDED.email";

        String updateAddressSQL = "UPDATE donor_addresses SET street = ?, neighborhood = ?, complement = ?, city = ?, state = ?, postal_code = ?, number = ?, country = ? WHERE donor_id = ?";

        try {
            open();

            var connection = getConnection();
            connection.setAutoCommit(false);  // Iniciar transação

            try (
                    PreparedStatement donorStmt = connection.prepareStatement(updateDonorSQL); PreparedStatement contactStmt = connection.prepareStatement(upsertContactSQL); PreparedStatement addressStmt = connection.prepareStatement(updateAddressSQL)) {
                // Atualizar Donor
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
                donorStmt.setLong(11, donor.getId());
                donorStmt.executeUpdate();

                // Inserir ou atualizar contatos (upsert)
                if (donor.getContacts() != null) {
                    for (DonorContact contact : donor.getContacts()) {
                        contactStmt.setLong(1, donor.getId());
                        contactStmt.setString(2, contact.getName());
                        contactStmt.setString(3, contact.getPhone());
                        contactStmt.setString(4, contact.getEmail());
                        contactStmt.executeUpdate();
                    }
                }

                // Atualizar endereço
                DonorAddress address = donor.getAddress();
                if (address != null) {
                    addressStmt.setString(1, address.getStreet());
                    addressStmt.setString(2, address.getNeighborhood());
                    addressStmt.setString(3, address.getComplement());
                    addressStmt.setString(4, address.getCity());
                    addressStmt.setString(5, address.getState());
                    addressStmt.setString(6, address.getPostalCode());
                    addressStmt.setString(7, address.getNumber());
                    addressStmt.setString(8, address.getCountry());
                    addressStmt.setLong(9, donor.getId());
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
