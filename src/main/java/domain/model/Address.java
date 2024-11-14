/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package domain.model;

/**
 *
 * @author cezar.britez
 */
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;
import java.net.*;
import java.net.http.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Address {

    private String street;
    private String neighborhood;
    private String complement;
    private String city;
    private String state;
    private String postalCode;
    private String number;
    private String country = "Brazil";

    // Método para buscar informações de endereço a partir do CEP
    public static Address fetch(String postalCode) throws Exception {
        String url = "https://viacep.com.br/ws/" + postalCode + "/json/";  // URL da API ViaCEP
        HttpClient client = HttpClient.newBuilder().build();

        // Fazendo a requisição GET para a API
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Content-Type", "application/json")
                .build();

        // Enviando a requisição e recebendo a resposta
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        // Verificando se a resposta foi bem-sucedida
        if (response.statusCode() == 200) {
            // Convertendo a resposta JSON em um Map
            String json = response.body();
            ObjectMapper mapper = new ObjectMapper();
            Map<String, Object> map = mapper.readValue(json, Map.class);

            // Construindo o objeto Address usando os dados do Map
            return Address.builder()
                    .street((String) map.get("logradouro"))
                    .neighborhood((String) map.get("bairro"))
                    .complement((String) map.get("complemento"))
                    .city((String) map.get("localidade"))
                    .state((String) map.get("uf"))
                    .postalCode((String) map.get("cep"))
                    .country("Brazil")
                    .build();
        } else {
            throw new Exception("Erro ao consultar o ViaCEP: " + response.statusCode());
        }
    }
}
