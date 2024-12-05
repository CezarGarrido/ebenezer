/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Interface.java to edit this template
 */
package domain.repository;

import domain.model.User;

/**
 *
 * @author cezar.britez
 */
public interface UserRepository {
    public User login(User user);
}
