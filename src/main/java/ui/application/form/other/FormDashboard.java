package ui.application.form.other;

import java.util.Date;
import java.text.SimpleDateFormat;
//import raven.toast.Notifications;
import net.sf.dynamicreports.report.builder.component.Components;
import net.sf.dynamicreports.report.builder.datatype.DataTypes;
import net.sf.dynamicreports.report.builder.style.Styles;
import net.sf.dynamicreports.report.builder.ReportTemplateBuilder;
import net.sf.dynamicreports.report.builder.DynamicReports;
import net.sf.dynamicreports.report.exception.DRException;
import net.sf.dynamicreports.report.datasource.DRDataSource;
import com.formdev.flatlaf.FlatClientProperties;
import java.io.FileNotFoundException;
import java.util.logging.Level;
import java.util.logging.Logger;
import net.sf.dynamicreports.report.builder.column.Columns;
import net.sf.dynamicreports.report.constant.HorizontalAlignment;

/**
 *
 * @author Raven
 */
public class FormDashboard extends javax.swing.JPanel {

    public FormDashboard() {
        initComponents();
        //  dateChooser2.clearDate();
        //dateChooser1.setLocale(Locale.FRENCH);
        lb.putClientProperty(FlatClientProperties.STYLE, ""
                + "font:$h1.font");
    }

    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        dateChooser1 = new com.raven.datechooser.DateChooser();
        lb = new javax.swing.JLabel();
        jButton1 = new javax.swing.JButton();

        lb.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        lb.setText("Boas Vindas");

        jButton1.setText("Imprimir");
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
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(lb, javax.swing.GroupLayout.PREFERRED_SIZE, 676, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(layout.createSequentialGroup()
                        .addGap(282, 282, 282)
                        .addComponent(jButton1)))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(lb)
                .addGap(163, 163, 163)
                .addComponent(jButton1)
                .addContainerGap(246, Short.MAX_VALUE))
        );
    }// </editor-fold>//GEN-END:initComponents

    private void jButton1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton1ActionPerformed
        try {
            // TODO add your handling code here:
            generateReciboWithDynamicReports();
        } catch (DRException ex) {
            Logger.getLogger(FormDashboard.class.getName()).log(Level.SEVERE, null, ex);
        } catch (FileNotFoundException ex) {
            Logger.getLogger(FormDashboard.class.getName()).log(Level.SEVERE, null, ex);
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

    // Método que gera o recibo usando DynamicReports
    public void generateReciboWithDynamicReports() throws DRException, FileNotFoundException {
        // Dados do recibo
        String dataAtual = new SimpleDateFormat("dd/MM/yyyy HH:mm").format(new Date());
        DRDataSource dataSource = new DRDataSource("descricao", "valor");
        dataSource.add("Serviço de Consultoria", "100,00");
        dataSource.add("Taxa de deslocamento", "15,00");

        // Relatório
        var b = DynamicReports.report()
                .setTemplate(createTemplate()) // Usando um template de estilo
                .columns(
                        Columns.column("Descrição", "descricao", DataTypes.stringType())
                                .setHorizontalAlignment(HorizontalAlignment.LEFT),
                        Columns.column("Valor (R$)", "valor", DataTypes.stringType())
                                .setHorizontalAlignment(HorizontalAlignment.RIGHT)
                )
                .title(Components.text("RECIBO DE PAGAMENTO")
                        .setHorizontalAlignment(HorizontalAlignment.CENTER))
                .pageFooter(Components.text("Data: " + dataAtual)
                        .setHorizontalAlignment(HorizontalAlignment.RIGHT))
                .setDataSource(dataSource)
                .show(false);
        
       
       // b.getReport().get
        //.toPdf(new java.io.FileOutputStream("recibo.pdf"));

        //JOptionPane.showMessageDialog(this, "Recibo gerado com sucesso! Verifique o arquivo 'recibo.pdf'.");
    }

    // Template de estilo para o relatório
    private ReportTemplateBuilder createTemplate() {
        return DynamicReports.template()
                //.setDefaultFont(Styles.style().setFontSize(12))
                .highlightDetailOddRows()
                .setColumnTitleStyle(Styles.style().bold().setHorizontalAlignment(HorizontalAlignment.CENTER));
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private com.raven.datechooser.DateChooser dateChooser1;
    private javax.swing.JButton jButton1;
    private javax.swing.JLabel lb;
    // End of variables declaration//GEN-END:variables
}
