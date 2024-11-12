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
public class Donor {

    private Long id;
    private Long companyId;
    private String name;
    private String cnpj;
    private String ie;
    private String cpf;
    private String rg;
    private String rgIssuer;
    private Boolean active = true;
    private Long userCreatorId;

    private DonorAddress address;
    private DonorContact[] contacts;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
