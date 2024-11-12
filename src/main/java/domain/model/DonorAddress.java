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
public class DonorAddress {

    private Long id;
    private Long donorId;
    private String street;
    private String neighborhood;
    private String complement;
    private String city;
    private String state;
    private String postalCode;
    private String country = "Brazil";
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
