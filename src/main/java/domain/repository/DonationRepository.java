/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Interface.java to edit this template
 */
package domain.repository;

import domain.model.Donation;
import java.util.List;

/**
 *
 * @author cezar.britez
 */
public interface DonationRepository {

    Donation findById(Long id);

    List<Donation> findAll();

    List<Donation> findByQuery(Long companyId, String queryFilter);

    Long save(Donation donation);

    void update(Donation donation);
}
