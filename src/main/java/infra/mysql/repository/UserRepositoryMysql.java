/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package infra.mysql.repository;

import domain.model.Role;
import domain.model.User;
import domain.repository.UserRepository;
import infra.mysql.config.DBConnection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Optional;

/**
 *
 * @author cezar.britez
 */
public class UserRepositoryMysql extends DBConnection implements UserRepository {

    @Override
    public Optional<User> login(User user) {
        try {
            open();
            // Query SQL para verificar o login e realizar o join com a tabela roles
            String sql = "SELECT u.id, u.company_id, u.username, u.password, u.email, u.active, u.photo, "
                    + "u.created_at, u.updated_at, "
                    + "r.id AS role_id, r.company_id AS role_company_id, r.active AS role_active, "
                    + "r.description AS role_description, r.role AS role_name "
                    + "FROM users u "
                    + "JOIN roles r ON u.role_id = r.id "
                    + "WHERE u.username = ?";

            // Preparando o statement
            PreparedStatement ps = getConnection().prepareStatement(sql);
            ps.setString(1, user.getUsername());  // Definindo o parâmetro da query (username)

            // Executando a query
            ResultSet rs = ps.executeQuery();

            // Verificando se encontrou o usuário
            if (rs.next()) {
                String dbPassword = rs.getString("password"); // Senha do banco de dados

                // Comparar a senha fornecida (user.getPassword()) com a senha armazenada no banco
                if (User.checkPassword(user.getPassword(), dbPassword)) {
                    // Criar o objeto User com os dados encontrados no banco
                    User foundUser = new User();
                    foundUser.setId(rs.getLong("id"));
                    foundUser.setCompanyId(rs.getLong("company_id"));
                    foundUser.setUsername(rs.getString("username"));
                    foundUser.setPassword(dbPassword); // Armazenando o hash da senha
                    foundUser.setEmail(rs.getString("email"));
                    foundUser.setActive(rs.getBoolean("active"));
                    foundUser.setPhoto(rs.getBytes("photo"));
                    foundUser.setCreatedAt(rs.getTimestamp("created_at").toLocalDateTime());
                    foundUser.setUpdatedAt(rs.getTimestamp("updated_at").toLocalDateTime());

                    // Atribuir a role ao usuário
                    Role role = new Role();
                    role.setId(rs.getLong("role_id"));
                    role.setCompanyId(rs.getLong("role_company_id"));
                    role.setActive(rs.getBoolean("role_active"));
                    role.setDescription(rs.getString("role_description"));
                    role.setRole(rs.getString("role_name"));
                    foundUser.setRole(role);

                    return Optional.of(foundUser);
                }
            }

            // Se não encontrou ou as senhas não coincidem, retorna um Optional vazio
            return Optional.empty();
        } catch (Exception e) {
            e.printStackTrace();
            return Optional.empty();
        } finally {
            close();
        }
    }
}
