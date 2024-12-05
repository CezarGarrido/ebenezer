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
import java.awt.Color;
import java.io.FileNotFoundException;
import net.sf.dynamicreports.jasper.builder.JasperReportBuilder;
import static net.sf.dynamicreports.report.builder.DynamicReports.cmp;
import static net.sf.dynamicreports.report.builder.DynamicReports.stl;
import net.sf.dynamicreports.report.builder.column.Columns;
import net.sf.dynamicreports.report.builder.style.StyleBuilder;
import net.sf.dynamicreports.report.constant.HorizontalAlignment;
import net.sf.dynamicreports.report.constant.LineStyle;
import net.sf.dynamicreports.report.constant.PageOrientation;
import net.sf.dynamicreports.report.constant.PageType;
import com.mindfusion.common.*;
import com.mindfusion.scheduling.*;
import com.mindfusion.scheduling.model.Appointment;

import java.awt.BorderLayout;
import java.awt.Insets;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JToolBar;

/**
 *
 * @author Raven
 */
public class FormDashboard extends javax.swing.JPanel {

    private static final long serialVersionUID = 1L;
    private final Calendar calendar;

    public FormDashboard() {
        initComponents();
        //  dateChooser2.clearDate();
        //dateChooser1.setLocale(Locale.FRENCH);
        lb.putClientProperty(FlatClientProperties.STYLE, ""
                + "font:$h1.font");

        calendar = new Calendar();
        calendar.setTheme(ThemeType.Light);
        jPanel1.setLayout(new BorderLayout());        
        
        jPanel1.add(calendar, BorderLayout.CENTER);

        addSampleAppointments();

        //calendar.getSchedule().loadFrom("", ContentType.Xml);
    }

    private void addSampleAppointments() {
        // Clear existing items
        calendar.getSchedule().getItems().clear();

        // Create example appointments
        Appointment appointment1 = new Appointment();
        appointment1.setStartTime(getDateTime(2024, 11, 28, 10, 0)); // 28 Nov 2024, 10:00 AM
        appointment1.setEndTime(getDateTime(2024, 11, 28, 11, 30)); // 28 Nov 2024, 11:30 AM
        appointment1.setSubject("Team Meeting");
        appointment1.setDescriptionText("Discuss project updates with the team.");
        calendar.getSchedule().getItems().add(appointment1);

        Appointment appointment2 = new Appointment();
        appointment2.setStartTime(getDateTime(2024, 11, 29, 14, 0)); // 29 Nov 2024, 02:00 PM
        appointment2.setEndTime(getDateTime(2024, 11, 29, 15, 0)); // 29 Nov 2024, 03:00 PM
        appointment2.setSubject("Client Call");
        appointment2.setDescriptionText("Call with the client to finalize requirements.");
        calendar.getSchedule().getItems().add(appointment2);

        Appointment appointment3 = new Appointment();
        appointment3.setStartTime(getDateTime(2024, 12, 1, 9, 0)); // 1 Dec 2024, 09:00 AM
        appointment3.setEndTime(getDateTime(2024, 12, 1, 10, 0)); // 1 Dec 2024, 10:00 AM
        appointment3.setSubject("Code Review");
        appointment3.setDescriptionText("Review code for the latest sprint.");
        calendar.getSchedule().getItems().add(appointment3);

        Appointment appointment4 = new Appointment();
        appointment4.setStartTime(getDateTime(2024, 12, 2, 16, 0)); // 2 Dec 2024, 04:00 PM
        appointment4.setEndTime(getDateTime(2024, 12, 2, 17, 0)); // 2 Dec 2024, 05:00 PM
        appointment4.setSubject("Design Discussion");
        appointment4.setDescriptionText("Discuss UI/UX design with the team.");
        calendar.getSchedule().getItems().add(appointment4);
    }

    private DateTime getDateTime(int year, int month, int day, int hour, int minute) {
        return new DateTime(year, month, day, hour, minute, 0); // Second is set to 0
    }

    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        lb = new javax.swing.JLabel();
        jButton1 = new javax.swing.JButton();
        jPanel1 = new javax.swing.JPanel();
        jButton2 = new javax.swing.JButton();
        jPanel5 = new javax.swing.JPanel();
        jPanel4 = new javax.swing.JPanel();
        jLabel5 = new javax.swing.JLabel();
        jLabel6 = new javax.swing.JLabel();
        jPanel3 = new javax.swing.JPanel();
        jLabel3 = new javax.swing.JLabel();
        jLabel4 = new javax.swing.JLabel();
        jPanel2 = new javax.swing.JPanel();
        jLabel1 = new javax.swing.JLabel();
        jLabel2 = new javax.swing.JLabel();
        jLabel7 = new javax.swing.JLabel();

        lb.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        lb.setText("Boas Vindas");

        jButton1.setText("Imprimir");
        jButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton1ActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 719, Short.MAX_VALUE)
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 406, Short.MAX_VALUE)
        );

        jButton2.setText("Hoje");

        jPanel4.setBackground(new java.awt.Color(255, 202, 108));

        jLabel5.setText("Agenda");

        jLabel6.setFont(new java.awt.Font("sansserif", 0, 48)); // NOI18N
        jLabel6.setText("18");

        javax.swing.GroupLayout jPanel4Layout = new javax.swing.GroupLayout(jPanel4);
        jPanel4.setLayout(jPanel4Layout);
        jPanel4Layout.setHorizontalGroup(
            jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel4Layout.createSequentialGroup()
                .addGap(18, 18, 18)
                .addGroup(jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jLabel6)
                    .addComponent(jLabel5))
                .addContainerGap(145, Short.MAX_VALUE))
        );
        jPanel4Layout.setVerticalGroup(
            jPanel4Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel4Layout.createSequentialGroup()
                .addGap(20, 20, 20)
                .addComponent(jLabel5)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jLabel6, javax.swing.GroupLayout.PREFERRED_SIZE, 51, Short.MAX_VALUE)
                .addContainerGap())
        );

        jPanel3.setBackground(new java.awt.Color(83, 214, 212));

        jLabel3.setText("Doações");

        jLabel4.setFont(new java.awt.Font("sansserif", 0, 48)); // NOI18N
        jLabel4.setText("18");

        javax.swing.GroupLayout jPanel3Layout = new javax.swing.GroupLayout(jPanel3);
        jPanel3.setLayout(jPanel3Layout);
        jPanel3Layout.setHorizontalGroup(
            jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel3Layout.createSequentialGroup()
                .addGap(18, 18, 18)
                .addGroup(jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jLabel4)
                    .addComponent(jLabel3))
                .addContainerGap(145, Short.MAX_VALUE))
        );
        jPanel3Layout.setVerticalGroup(
            jPanel3Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel3Layout.createSequentialGroup()
                .addGap(20, 20, 20)
                .addComponent(jLabel3)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jLabel4, javax.swing.GroupLayout.PREFERRED_SIZE, 51, Short.MAX_VALUE)
                .addContainerGap())
        );

        jPanel2.setBackground(new java.awt.Color(77, 180, 247));

        jLabel1.setText("Doadores");

        jLabel2.setFont(new java.awt.Font("sansserif", 0, 48)); // NOI18N
        jLabel2.setText("18");

        javax.swing.GroupLayout jPanel2Layout = new javax.swing.GroupLayout(jPanel2);
        jPanel2.setLayout(jPanel2Layout);
        jPanel2Layout.setHorizontalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addGap(18, 18, 18)
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jLabel2)
                    .addComponent(jLabel1))
                .addContainerGap(145, Short.MAX_VALUE))
        );
        jPanel2Layout.setVerticalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addGap(20, 20, 20)
                .addComponent(jLabel1)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jLabel2, javax.swing.GroupLayout.PREFERRED_SIZE, 51, Short.MAX_VALUE)
                .addContainerGap())
        );

        javax.swing.GroupLayout jPanel5Layout = new javax.swing.GroupLayout(jPanel5);
        jPanel5.setLayout(jPanel5Layout);
        jPanel5Layout.setHorizontalGroup(
            jPanel5Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel5Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jPanel2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(18, 18, 18)
                .addComponent(jPanel4, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(18, 18, 18)
                .addComponent(jPanel3, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        jPanel5Layout.setVerticalGroup(
            jPanel5Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel5Layout.createSequentialGroup()
                .addGap(0, 0, Short.MAX_VALUE)
                .addGroup(jPanel5Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jPanel4, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jPanel3, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jPanel2, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)))
        );

        jLabel7.setText("Agenda");

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jPanel5, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addComponent(jButton2)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .addComponent(jButton1)
                        .addGap(141, 141, 141))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .addGap(6, 6, 6))
                    .addComponent(lb, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jLabel7)
                        .addGap(0, 0, Short.MAX_VALUE))))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(lb)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jPanel5, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(27, 27, 27)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jButton1, javax.swing.GroupLayout.Alignment.TRAILING)
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addComponent(jButton2)
                        .addGap(14, 14, 14)))
                .addGap(9, 9, 9)
                .addComponent(jLabel7)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addContainerGap())
        );
    }// </editor-fold>//GEN-END:initComponents

    private void jButton1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton1ActionPerformed
        gr();
    }//GEN-LAST:event_jButton1ActionPerformed

    private JButton nextButtonInToolbar(JToolBar bar, String imageName) {

        JButton button = new JButton();
        button.setIcon(new ImageIcon(imageName));

        button.setBorderPainted(false);
        button.setMargin(new Insets(5, 5, 5, 5));
        button.setSize(35, 35);

        bar.add(button);

        return button;
    }

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

    public void gr() {
        try {
            // Estilo base com largura fixa
            var fixedWidthFontStyle = Styles.style()
                    .setFontName("Monospaced") // Fonte monoespaçada
                    .setForegroundColor(Color.DARK_GRAY)
                    .setFontSize(10) // Tamanho adequado para matricial
                    .setHorizontalAlignment(HorizontalAlignment.LEFT);

            // Estilos derivados do fixedWidthFontStyle
            var smallFontStyle = Styles.style(fixedWidthFontStyle)
                    .setFontSize(6)
                    .setHorizontalAlignment(HorizontalAlignment.CENTER);

            var defaultFontStyle = Styles.style(fixedWidthFontStyle)
                    .setFontSize(10);

            var boldFontStyle = Styles.style(defaultFontStyle)
                    //.bold()
                    .setHorizontalAlignment(HorizontalAlignment.CENTER);

            var largeFontStyle = Styles.style(fixedWidthFontStyle)
                    .setFontSize(12)
                    .setHorizontalAlignment(HorizontalAlignment.CENTER);

            var defaultFontCenterStyle = Styles.style(defaultFontStyle)
                    .setHorizontalAlignment(HorizontalAlignment.CENTER);

            // Criando o relatório
            // Criar o relatório
            var report = DynamicReports.report();
            // report.setPage
            // Configuração de largura fixa para a página

            report.setPageFormat(PageType.A5, PageOrientation.LANDSCAPE).setPageMargin(DynamicReports.margin(5));

            // Cabeçalho do recibo (linhas com fonte menor)
            report.title(
                    Components.text("LAR EBENEZER = HILDA MARIA CORREA - ADAS").setStyle(largeFontStyle),
                    cmp.horizontalList()
                            .add(
                                    cmp.text("Utilidade Publica Municipal Lei N.º 1527 de 09/11/88").setStyle(Styles.style(fixedWidthFontStyle)
                                            .setFontSize(6).setHorizontalAlignment(HorizontalAlignment.LEFT)),
                                    cmp.text("Utilidade Publica Estadual Lei N.º 1493 de 13/05/94").setStyle(Styles.style(fixedWidthFontStyle)
                                            .setFontSize(6).setHorizontalAlignment(HorizontalAlignment.RIGHT))
                            ),
                    cmp.horizontalList()
                            .add(
                                    cmp.text("Utilidade Publica Federal Portaria N.º 735 de 13/08/01 DOU 14/08/01").setStyle(Styles.style(fixedWidthFontStyle)
                                            .setFontSize(6).setHorizontalAlignment(HorizontalAlignment.LEFT)),
                                    cmp.text("CEBAS: CCEAS 0030 Resolução N.º 05 de 02/02/04 DOU 05/02/04").setStyle(Styles.style(fixedWidthFontStyle)
                                            .setFontSize(6).setHorizontalAlignment(HorizontalAlignment.RIGHT))
                            ),
                    //Components.text("Utilidade Publica Municipal Lei N.º 1527 de 09/11/88          Utilidade Publica Estadual Lei N.º 1493 de 13/05/94").setStyle(smallFontStyle),
                    //  Components.text("    ").setStyle(smallFontStyle),
                    Components.text("Atest. de Reg. no Cons. Nasc. de Assist. Soc. R N.º 0018 Res n.º 05 de 02/02/04").setStyle(smallFontStyle),
                    //Components.text("").setStyle(smallFontStyle),
                    Components.text("RUA 20 DE DEZEMBRO, N.º 3170, JARDIM RASSLEN, CEP 79.813-280").setStyle(smallFontStyle),
                    Components.text("DOURADOS - MS").setStyle(largeFontStyle),
                    cmp.horizontalList()
                            .add(
                                    cmp.text("TELEFONE N.º : 67 3425-4118").setStyle(Styles.style(fixedWidthFontStyle)
                                            .setFontSize(12).setHorizontalAlignment(HorizontalAlignment.LEFT)),
                                    cmp.text("CNPJ Nº 03.471.216/0001-23").setStyle(Styles.style(fixedWidthFontStyle)
                                            .setFontSize(12).setHorizontalAlignment(HorizontalAlignment.RIGHT))
                            ),
                    Components.text("CELULARES    : 67 9201-6365 / 67 9201-6365 / 67 9201-6365").setStyle(Styles.style(fixedWidthFontStyle)
                            .setFontSize(12).setHorizontalAlignment(HorizontalAlignment.LEFT)),
                    Components.text("").setStyle(smallFontStyle), // Linha vazia para espaçamento
                    Components.text("").setStyle(smallFontStyle) // Linha vazia para espaçamento
            );

            // Título principal do recibo
            report.title(
                    Components.text("RECIBO DE DOAÇÕES").setStyle(largeFontStyle),
                    Components.line().setStyle(Styles.style().setFontSize(5).setHorizontalAlignment(HorizontalAlignment.CENTER)),
                    Components.text("").setStyle(Styles.style().setFontSize(1)), // Linha vazia para espaçamento
                    Components.line().setStyle(Styles.style().setFontSize(5).setHorizontalAlignment(HorizontalAlignment.CENTER)),
                    Components.text("").setStyle(defaultFontStyle), // Linha vazia para espaçamento
                    Components.text("").setStyle(defaultFontStyle) // Linha vazia para espaçamento
            );

            // Corpo do recibo
            report.title(
                    cmp.horizontalList()
                            .add(
                                    cmp.text("Recibo N.º .....: {{NUMERO_RECIBO}}").setStyle(defaultFontStyle),
                                    cmp.text("Emitido ....: {{DATA_EMISSAO}}").setStyle(Styles.style(fixedWidthFontStyle)
                                            .setFontSize(10).setHorizontalAlignment(HorizontalAlignment.RIGHT))
                            ),
                    Components.text("").setStyle(defaultFontStyle), // Linha vazia para espaçamento
                    cmp.horizontalList()
                            .add(
                                    cmp.text("Recebemos de ...:").setStyle(defaultFontStyle),
                                    cmp.text("{{NOME_DOADOR}}").setStyle(defaultFontStyle),
                                    cmp.text("({{CODIGO_DOADOR}})").setStyle(Styles.style(fixedWidthFontStyle)
                                            .setFontSize(10).setHorizontalAlignment(HorizontalAlignment.RIGHT))
                            ),
                    Components.text("Endereço .......: {{END_RUA_DOADOR}} Nº {{END_NUMERO_DOADOR}}").setStyle(defaultFontStyle),
                    Components.text("Bairro .........: {{END_BAIRRO_DOADOR}}").setStyle(defaultFontStyle),
                    Components.text("Contato ........: {{CONTATO_DOADOR}}").setStyle(defaultFontStyle),
                    Components.text("Cidade .........: {{END_CIDADE_DOADOR}} - {{END_ESTADO_DOADOR}}").setStyle(defaultFontStyle),
                    Components.text("Valor ..........: {{VALOR_DOADO}}  -  ________________________________").setStyle(defaultFontStyle),
                    Components.text("Por Extenso ....: {{VALOR_DOADO_EXTENSO}}").setStyle(defaultFontStyle),
                    Components.text("Referente a ....: Doação do mes de agosto").setStyle(defaultFontStyle)
            );

            report.title(
                    Components.text("").setStyle(largeFontStyle), // Linha vazia para espaçamento
                    Components.text("").setStyle(defaultFontCenterStyle), // Linha vazia para espaçamento
                    Components.text("").setStyle(largeFontStyle), // Linha vazia para espaçamento
                    // Components.text("").setStyle(largeFontStyle), // Linha vazia para espaçamento
                    Components.text("_______________________________").setStyle(defaultFontCenterStyle),
                    Components.text("").setStyle(smallFontStyle), // Linha vazia para espaçamento
                    Components.text("Assinatura").setStyle(defaultFontCenterStyle)
            );

            var pen = Styles.pen1Point().setLineStyle(LineStyle.DASHED); // Define o estilo como tracejado

            report.pageFooter(
                    Components.text("Agradecemos a preferência.").setStyle(defaultFontStyle),
                    Components.text("Agradecemos a preferência.").setStyle(defaultFontStyle),
                    Components.text("Agradecemos a preferência.").setStyle(defaultFontStyle),
                    //Components.text("Agradecemos a preferência."),
                    // Components.text("Agradecemos a preferência."),

                    Components.line().setPen(
                            pen).setStyle(Styles.style().setFontSize(5).setHorizontalAlignment(HorizontalAlignment.CENTER))
            );

            report.show(false);
        } catch (DRException e) {
            e.printStackTrace();
        }
    }

    public JasperReportBuilder build() {
        // Criação do relatório
        var report = DynamicReports.report();
        report.setPageFormat(PageType.A4, PageOrientation.LANDSCAPE) // Ajuste conforme o papel da impressora
                .setPageMargin(DynamicReports.margin(10));

        // Definição do estilo padrão para texto
        StyleBuilder defaultFontStyle = stl.style()
                .setFontSize(10)
                .setPadding(5);

        // Definindo o cabeçalho do recibo com os campos variáveis utilizando colunas
        report.title(
                cmp.text("Recibo N.º .....: {{NUMERO_RECIBO}}     Emitido ....: {{DATA_EMISSAO}}")
                        .setStyle(defaultFontStyle),
                // Layout com duas colunas para os dados do doador
                cmp.horizontalList()
                        .add(
                                cmp.text("Recebemos de ...: {{NOME_DOADOR}} ({{CODIGO_DOADOR}})").setStyle(defaultFontStyle),
                                cmp.text("Endereço .......: {{END_RUA_DOADOR}} Nº {{END_NUMERO_DOADOR}}").setStyle(defaultFontStyle)
                        ),
                cmp.horizontalList()
                        .add(
                                cmp.text("Bairro .........: {{END_BAIRRO_DOADOR}}").setStyle(defaultFontStyle),
                                cmp.text("Contato ........: {{CONTATO_DOADOR}}").setStyle(defaultFontStyle)
                        ),
                cmp.horizontalList()
                        .add(
                                cmp.text("Cidade .........: {{END_CIDADE_DOADOR}} - {{END_ESTADO_DOADOR}}").setStyle(defaultFontStyle),
                                cmp.text("Valor ..........: {{VALOR_DOADO}}  -  ________________________________").setStyle(defaultFontStyle)
                        ),
                cmp.text("Por Extenso ....: {{VALOR_DOADO_EXTENSO}}").setStyle(defaultFontStyle),
                // Linha de "Referente a"
                cmp.text("Referente a ....: ________________________________________________").setStyle(defaultFontStyle),
                cmp.text("                  ________________________________________________").setStyle(defaultFontStyle),
                cmp.text("                  ________________________________________________").setStyle(defaultFontStyle)
        );

        return report;
    }

    // Template de estilo para o relatório
    private ReportTemplateBuilder createTemplate() {
        return DynamicReports.template()
                //.setDefaultFont(Styles.style().setFontSize(12))
                .highlightDetailOddRows()
                .setColumnTitleStyle(Styles.style().bold().setHorizontalAlignment(HorizontalAlignment.CENTER));
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton jButton1;
    private javax.swing.JButton jButton2;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JLabel jLabel5;
    private javax.swing.JLabel jLabel6;
    private javax.swing.JLabel jLabel7;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel2;
    private javax.swing.JPanel jPanel3;
    private javax.swing.JPanel jPanel4;
    private javax.swing.JPanel jPanel5;
    private javax.swing.JLabel lb;
    // End of variables declaration//GEN-END:variables
}
