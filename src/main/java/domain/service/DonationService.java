/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package domain.service;

import domain.model.Donation;
import domain.model.User;
import domain.repository.DonationRepository;
import java.time.LocalDateTime;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

/**
 *
 * @author cezar.britez
 */
@NoArgsConstructor
@AllArgsConstructor
public class DonationService {

    private DonationRepository donationRepo;

    public List<Donation> findByQuery(User user, String queryFilter, LocalDateTime date) {
        return donationRepo.findByQuery(user.getCompanyId(), queryFilter);
    }

}
