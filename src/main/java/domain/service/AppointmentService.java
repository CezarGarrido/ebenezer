/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package domain.service;

import domain.model.Appointment;
import domain.model.User;
import java.time.LocalDateTime;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import domain.repository.AppointmentRepository;

/**
 *
 * @author cezar.britez
 */
@NoArgsConstructor
@AllArgsConstructor
public class AppointmentService {

    private AppointmentRepository eventRepo;

    public Long save(User user, Appointment event) {
        event.setCompanyId(user.getCompanyId());
        event.setUserCreatorId(user.getId());
        return eventRepo.save(event);
    }

    public List<Appointment> findByQuery(User user, String queryFilter, LocalDateTime date) {
        return eventRepo.findByQuery(user.getCompanyId(), queryFilter, date);
    }

    public Appointment findById(User user, Long id) {
        return eventRepo.findById(user.getCompanyId(), id);
    }

    public void update(User user, Appointment event) {
        event.setCompanyId(user.getCompanyId());
        event.setUserCreatorId(user.getId());
        eventRepo.update(event);
    }

}
