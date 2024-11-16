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
public class Agenda {

    private Long id;
    private Long companyId;
    private Long userCreatorId;
    private LocalDateTime date;
    private String hour;
    private String eventType;
    private String Obs;
    private User user;
    private AgendaCall call;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
