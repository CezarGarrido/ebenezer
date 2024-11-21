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
    private Long agendaId; // Opcional, pode ser null
    private Long donorId;
    private BigDecimal receivedAmount;
    private LocalDateTime receivedAt;
    private String obs;

    private User user; // Relacionamento com User
    private Agenda agenda; // Relacionamento com Agenda
    private Donor donor; // Relacionamento com Donor

    private LocalDateTime deletedAt;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
