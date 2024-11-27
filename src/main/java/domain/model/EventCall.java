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
public class EventCall {

    private Long id;
    private Long eventId;
    private Long donorId;
    private String phone;
    private Donor donor;
    private String status;
    private String duration;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
