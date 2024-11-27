package ui.application.form.donation.agenda;

import com.formdev.flatlaf.FlatClientProperties;
import domain.model.Event;
import domain.repository.DonorRepository;
import java.awt.Font;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import javax.swing.BorderFactory;
import javax.swing.DefaultListCellRenderer;
import javax.swing.DefaultListModel;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.SwingUtilities;
import javax.swing.border.EmptyBorder;
import ui.application.Application;
import ui.application.form.donation.agenda.dialog.AgendaNewDialog;
import domain.repository.EventRepository;
//import com.vdurmont.emoji.EmojiParser;

/**
 *
 * @author Raven
 */
public class AgendaForm extends javax.swing.JPanel {

    private EventRepository agendaRepo;
    private DonorRepository donorRepo;

    public AgendaForm(EventRepository agendaRepo, DonorRepository donorRepo) {
        initComponents();
        this.agendaRepo = agendaRepo;
        this.donorRepo = donorRepo;
        init();
    }

    private void init() {
        setBorder(new EmptyBorder(10, 10, 10, 10)); //Margin

        //setLayout(new MigLayout("wrap,fillx", "[fill]"));
        txtSearch.putClientProperty(FlatClientProperties.PLACEHOLDER_TEXT, "Pesquisar...");
        //txtPass.putClientProperty(FlatClientProperties.PLACEHOLDER_TEXT, "Password");
        jLabel1.putClientProperty(FlatClientProperties.STYLE, ""
                + "font:bold +3");
        jTextPane1.setText("Cadastrar, atualizar e excluir compromissos na agenda");
        jTextPane1.setEditable(false);
        jTextPane1.setBorder(BorderFactory.createEmptyBorder());

        // Dados de exemplo para a lista
        agendaList.setCellRenderer(new AgendaForm.AgendaListRenderer());

        loadEvents();
        //jScrollPane1.setViewportView(agendaList);
    }

    private DefaultListModel<Object> createAgendaModel(Map<String, List<String>> agendaData) {
        DefaultListModel<Object> model = new DefaultListModel<>();
        for (String date : agendaData.keySet()) {
            // Adiciona o cabeçalho da data
            model.addElement(date);
            // Adiciona os itens relacionados à data
            for (String item : agendaData.get(date)) {
                model.addElement("   " + item); // Indentação para diferenciar itens
            }
        }
        return model;
    }

    private class AgendaListRenderer extends DefaultListCellRenderer {

        @Override
        public java.awt.Component getListCellRendererComponent(JList<?> list, Object value, int index, boolean isSelected, boolean cellHasFocus) {
            JLabel label = (JLabel) super.getListCellRendererComponent(list, value, index, isSelected, cellHasFocus);
            if (!value.toString().startsWith("   ")) {
                // Estilo para cabeçalhos
                label.setFont(label.getFont().deriveFont(java.awt.Font.BOLD));
                label.setBackground(java.awt.Color.LIGHT_GRAY);
                label.setOpaque(true);
            } else {
                // Estilo para itens normais
                // label.setFont(label.getFont().deriveFont(java.awt.Font.PLAIN));
                // label.setOpaque(false);
            }
            return label;
        }
    }

    private void loadEvents() {
        List<Event> events = agendaRepo.findByQuery(Application.loggedUser().getCompanyId(), txtSearch.getText());

        // Formato de data brasileiro
        DateTimeFormatter dateFormatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");

        // TreeMap com comparador decrescente para ordenar as datas
        Map<String, List<String>> agendaData = new TreeMap<>(Comparator.reverseOrder());

        //System.out.println(parsedText); // Saída: Eu amo programação
        for (Event agenda : events) {
            // Formata a data para ser usada como chave
            String formattedDate = agenda.getDate() != null ? agenda.getDate().toLocalDate().format(dateFormatter) : "Sem data";

            // Cria a entrada para a data, se não existir
            agendaData.putIfAbsent(formattedDate, new ArrayList<>());

            // Adiciona o compromisso à lista da data
            String eventDetails = String.format("%s - %s para %s",
                    agenda.getTime() != null ? agenda.getTime() : "00:00",
                    agenda.getEventType(), agenda.getCall().getDonor().getName());
            agendaData.get(formattedDate).add(eventDetails);
        }
        //agendaList.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 13));

        // Atualiza o modelo da lista
        agendaList.setModel(createAgendaModel(agendaData));
    }

    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jPanel1 = new javax.swing.JPanel();
        btnDelete = new javax.swing.JButton();
        btnUpdate = new javax.swing.JButton();
        btnCreate = new javax.swing.JButton();
        txtSearch = new javax.swing.JTextField();
        jLabel1 = new javax.swing.JLabel();
        jScrollPane1 = new javax.swing.JScrollPane();
        jTextPane1 = new javax.swing.JTextPane();
        jCalendar1 = new com.toedter.calendar.JCalendar();
        jScrollPane3 = new javax.swing.JScrollPane();
        agendaList = new javax.swing.JList<>();

        btnDelete.setText("Excluir");
        btnDelete.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnDeleteActionPerformed(evt);
            }
        });

        btnUpdate.setText("Atualizar");
        btnUpdate.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnUpdateActionPerformed(evt);
            }
        });

        btnCreate.setText("Novo");
        btnCreate.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnCreateActionPerformed(evt);
            }
        });

        jLabel1.setText("Agenda");

        jScrollPane1.setViewportView(jTextPane1);

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanel1Layout.createSequentialGroup()
                        .addComponent(jLabel1)
                        .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                        .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                            .addComponent(jScrollPane1)
                            .addGroup(jPanel1Layout.createSequentialGroup()
                                .addComponent(txtSearch, javax.swing.GroupLayout.PREFERRED_SIZE, 325, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 132, Short.MAX_VALUE)
                                .addComponent(btnCreate)
                                .addGap(18, 18, 18)
                                .addComponent(btnUpdate)
                                .addGap(18, 18, 18)
                                .addComponent(btnDelete)))
                        .addGap(15, 15, 15))))
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jLabel1)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 18, Short.MAX_VALUE)
                .addGroup(jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(btnDelete)
                    .addComponent(btnUpdate)
                    .addComponent(btnCreate)
                    .addComponent(txtSearch, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addContainerGap())
        );

        agendaList.setModel(new javax.swing.AbstractListModel<Object>() {
            String[] strings = { "12:00am - 6:39pm Ligar para Cezar", "12:00am - 6:39pm" };
            public int getSize() { return strings.length; }
            public Object getElementAt(int i) { return strings[i]; }
        });
        jScrollPane3.setViewportView(agendaList);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                    .addGroup(layout.createSequentialGroup()
                        .addGap(20, 20, 20)
                        .addComponent(jCalendar1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(jScrollPane3)))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jCalendar1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 475, Short.MAX_VALUE))
                    .addComponent(jScrollPane3))
                .addContainerGap())
        );
    }// </editor-fold>//GEN-END:initComponents

    private void btnCreateActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnCreateActionPerformed
        // TODO add your handling code here:
        AgendaNewDialog dialog = new AgendaNewDialog((JFrame) SwingUtilities.getWindowAncestor(this), true, this.agendaRepo, this.donorRepo);
        dialog.setVisible(true);
    }//GEN-LAST:event_btnCreateActionPerformed

    private void btnDeleteActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnDeleteActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_btnDeleteActionPerformed

    private void btnUpdateActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnUpdateActionPerformed

    }//GEN-LAST:event_btnUpdateActionPerformed

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JList<Object> agendaList;
    private javax.swing.JButton btnCreate;
    private javax.swing.JButton btnDelete;
    private javax.swing.JButton btnUpdate;
    private com.toedter.calendar.JCalendar jCalendar1;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane3;
    private javax.swing.JTextPane jTextPane1;
    private javax.swing.JTextField txtSearch;
    // End of variables declaration//GEN-END:variables
}
