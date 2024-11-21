/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package domain.repository;

import domain.model.Agenda;
import domain.model.Donor;
import java.util.List;

/**
 *
 * @author cezar.britez
 */
public interface AgendaRepository {

    Agenda findById(Long id);

    List<Agenda> findAll();
    
    List<Agenda> findByQuery(Long companyId, String queryFilter);

    Long save(Agenda agenda);

    void update(Agenda agenda);

}
