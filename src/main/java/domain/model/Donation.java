/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package domain.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 *
 * @author cezar.britez
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Donation {

    private Long id;
    private Long companyId;
    private Long userCreatorId;
    private Long eventId; // Opcional, pode ser null
    private Long donorId;
    private BigDecimal Amount;
    private LocalDateTime receivedAt;
    private String receivedTime;
    private Boolean paid;
    private String notes;

    private User user; // Relacionamento com User
    private Donor donor; // Relacionamento com Donor

    private LocalDateTime deletedAt;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
