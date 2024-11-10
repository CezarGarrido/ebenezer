/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.ebenezer.pos.model;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.ToString;

/**
 *
 * @author cezar.britez
 */

@Data
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class Address {
    private Long id;
    private String street;
    private String city;
    private String state;
    private String neighborhood;
    private String zipCode;
}
