/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package domain.service;

import domain.model.Donor;
import domain.model.User;
import domain.repository.DonorRepository;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

/**
 *
 * @author cezar.britez
 */
@NoArgsConstructor
@AllArgsConstructor
public class DonorService {

    private DonorRepository donorRepository;

    public List<Donor> findByQuery(User user, String queryFilter) {
        return donorRepository.findByQuery(user.getCompanyId(), queryFilter);
    }

    public Long save(User user, Donor donor) {
        donor.setCompanyId(user.getCompanyId());
        donor.setUserCreatorId(user.getId());
        return donorRepository.save(donor);
    }

    public void update(User user, Donor donor) {
        donor.setCompanyId(user.getCompanyId());
        donor.setUserCreatorId(user.getId());
        donorRepository.update(donor);
    }

    public Donor findById(User user, Long id) {
        return donorRepository.findById(user.getCompanyId(), id);
    }

    public List<Donor> findAll(User user) {
        return donorRepository.findAll(user.getCompanyId());
    }
}
