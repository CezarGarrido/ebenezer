package ui.application.form.other;

import com.formdev.flatlaf.FlatClientProperties;
import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import java.text.SimpleDateFormat;
import javax.print.Doc;
import javax.print.DocFlavor;
import javax.print.DocPrintJob;
import javax.print.PrintException;
import javax.print.PrintService;
import javax.print.PrintServiceLookup;
import javax.print.SimpleDoc;
//import raven.toast.Notifications;

/**
 *
 * @author Raven
 */
public class FormDashboard extends javax.swing.JPanel {

    public FormDashboard() {
        initComponents();
        lb.putClientProperty(FlatClientProperties.STYLE, ""
                + "font:$h1.font");
    }

    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        lb = new javax.swing.JLabel();
        jButton1 = new javax.swing.JButton();

        lb.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        lb.setText("Dashboard");

        jButton1.setText("Show Notifications Test");
        jButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton1ActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(lb, javax.swing.GroupLayout.DEFAULT_SIZE, 794, Short.MAX_VALUE)
                .addContainerGap())
            .addGroup(layout.createSequentialGroup()
                .addGap(325, 325, 325)
                .addComponent(jButton1)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(lb)
                .addGap(173, 173, 173)
                .addComponent(jButton1)
                .addContainerGap(237, Short.MAX_VALUE))
        );
    }// </editor-fold>//GEN-END:initComponents

    private void jButton1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton1ActionPerformed
        // Notifications.getInstance().show(Notifications.Type.INFO, Notifications.Location.TOP_CENTER, "Hello sample message");
        // Texto do recibo formatado para a Epson LX-350
        String recibo = generateRecibo();

        // Converte o recibo para um InputStream
        InputStream stream = new ByteArrayInputStream(recibo.getBytes(StandardCharsets.UTF_8));

        // Define o tipo de dados como texto simples
        DocFlavor flavor = DocFlavor.INPUT_STREAM.AUTOSENSE;
        Doc doc = new SimpleDoc(stream, flavor, null);

        // Obtém o serviço de impressão padrão (ou escolha uma impressora específica)
        PrintService printService = PrintServiceLookup.lookupDefaultPrintService();

        if (printService != null) {
            try {
                // Cria um trabalho de impressão e imprime o recibo
                DocPrintJob printJob = printService.createPrintJob();
                printJob.print(doc, null);
                System.out.println("Recibo enviado para a impressora.");
            } catch (PrintException e) {
                e.printStackTrace();
            }
        } else {
            System.out.println("Nenhuma impressora encontrada.");
        }
    }//GEN-LAST:event_jButton1ActionPerformed

    // Gera o texto do recibo compatível com a Epson LX-350
    public static String generateRecibo() {
        StringBuilder recibo = new StringBuilder();

        // Data formatada
        SimpleDateFormat dateFormat = new SimpleDateFormat("dd/MM/yyyy HH:mm");
        String dataAtual = dateFormat.format(new Date());

        recibo.append("**************************************************\n");
        recibo.append("                RECIBO DE PAGAMENTO               \n");
        recibo.append("**************************************************\n");
        recibo.append("Data: " + dataAtual + "\n");
        recibo.append("Cliente: João Silva\n");
        recibo.append("--------------------------------------------------\n");
        recibo.append(String.format("%-40s %10s\n", "Descrição", "Valor (R$)"));
        recibo.append("--------------------------------------------------\n");
        recibo.append(String.format("%-40s %10s\n", "Serviço de Consultoria", "100,00"));
        recibo.append(String.format("%-40s %10s\n", "Taxa de deslocamento", "15,00"));
        recibo.append("--------------------------------------------------\n");
        recibo.append(String.format("%-40s %10s\n", "Total", "115,00"));
        recibo.append("--------------------------------------------------\n");
        recibo.append("        Obrigado pela preferência!                \n");
        recibo.append("**************************************************\n");

        return recibo.toString();
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton jButton1;
    private javax.swing.JLabel lb;
    // End of variables declaration//GEN-END:variables
}
