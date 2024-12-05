/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package domain.repository;

import domain.model.Appointment;
import java.time.LocalDateTime;
import java.util.List;

/**
 *
 * @author cezar.britez
 */
public interface AppointmentRepository {

    Appointment findById(Long companyId, Long id);

    List<Appointment> findAll();

    List<Appointment> findByQuery(Long companyId, String queryFilter, LocalDateTime date);

    Long save(Appointment event);

    void update(Appointment event);

}
