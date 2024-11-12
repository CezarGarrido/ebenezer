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
import java.util.Optional;

public interface DonorRepository {

    Optional<Donor> findById(Long id);

    List<Donor> findAll();

    void save(Donor donor);

    void update(Donor donor);

    void deleteById(Long id);
}
