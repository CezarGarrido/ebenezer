/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package domain.repository;

import domain.model.Event;
import domain.model.Donor;
import java.util.List;

/**
 *
 * @author cezar.britez
 */
public interface EventRepository {

    Event findById(Long id);

    List<Event> findAll();
    
    List<Event> findByQuery(Long companyId, String queryFilter);

    Long save(Event event);

    void update(Event event);

}
