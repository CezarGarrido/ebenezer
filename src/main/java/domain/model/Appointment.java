/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package domain.model;

import java.time.LocalDateTime;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 *
 * @author cezar.britez
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Appointment {

    private Long id;
    private Long companyId;
    private Long userCreatorId;
    private LocalDateTime date;
    private String time;
    private String eventType;
    private String notes;
    private User user;
    private AppointmentCall call;
    private Donation donation;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
