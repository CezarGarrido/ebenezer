/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.ebenezer.pos.model;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDate;
import lombok.ToString;

/**
 *
 * @author cezar.britez
 */

@Data
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class Donor {
    private Long id;
    private String name;
    private String phone;
    private String contact;
    private Address address;
    private String cpf;
    private String cnpj;
    private String stateRegistration;
    private String identityNumber;
    private String issuingOrganization;
    private String classificationCode;
    private String classificationDescription;
    private String previousValue;
    private String frequencyCode;
    private String frequencyDescription;
    private LocalDate registrationDate;
    private int employeeId;
    private String active;
    private LocalDate lastDonationDate;
    private String lastDonationValue;
    private LocalDate contractDate;
    private String paymentCode;
    private String paymentDescription;
}
