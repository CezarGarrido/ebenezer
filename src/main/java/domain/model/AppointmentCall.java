/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package domain.model;

import java.time.LocalDateTime;
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
public class AppointmentCall {

    private Long id;
    private Long appointmentId;
    private Long donorId;
    private Long donationId;
    private String phone;
    private Donor donor;
    private String status = "Agendado";
    private String duration;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
