/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Interface.java to edit this template
 */
package domain.repository;

/**
 *
 * @author cezar.britez
 */
import domain.model.Donor;
import java.util.List;

public interface DonorRepository {

    Donor findById(Long companyId, Long id);

    List<Donor> findAll(Long companyId);

    List<Donor> findByQuery(Long companyId, String queryFilter);

    Long save(Donor donor);

    void update(Donor donor);

    void deleteById(Long id);
}
