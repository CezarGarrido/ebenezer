/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package domain.service;

import domain.model.User;
import domain.repository.UserRepository;
import java.util.Optional;

/**
 *
 * @author cezar.britez
 */
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User login(User user) {
        return userRepository.login(user);
    }
}
