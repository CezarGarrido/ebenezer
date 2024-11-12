/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package domain.model;

import at.favre.lib.crypto.bcrypt.BCrypt;
import java.time.LocalDateTime;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 *
 * @author cezar.britez
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {

    Long id;
    Long companyId;
    String name;
    String username;
    String password;
    String email;
    Boolean active;
    private byte[] photo;
    
    private Role role;
    
    LocalDateTime createdAt;
    LocalDateTime updatedAt;

    // Gerar hash de senha
    public static String hashPassword(String password) {
        String bcryptHashString = BCrypt.withDefaults().hashToString(12, password.toCharArray());
        return bcryptHashString;
    }

    // Verificar se a senha fornecida corresponde ao hash armazenado
    public static boolean checkPassword(String password, String bcryptHashString) {
        BCrypt.Result result = BCrypt.verifyer().verify(password.toCharArray(), bcryptHashString);
        return result.verified;
    }
}
