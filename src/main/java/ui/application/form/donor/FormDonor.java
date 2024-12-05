package ui.application.form.donor;

import com.formdev.flatlaf.FlatClientProperties;
import domain.model.Donor;
import domain.service.DonorService;
import java.util.List;
import javax.swing.BorderFactory;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.SwingUtilities;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableModel;
import ui.application.Application;
import ui.application.form.donor.dialog.DonorNewDialog;

/**
 *
 * @author Raven
 */
public class FormDonor extends javax.swing.JPanel {

    private DonorService service;

    public FormDonor(DonorService service) {
        initComponents();
        this.service = service;

        init();
    }

    private void init() {
        setBorder(new EmptyBorder(10, 10, 10, 10)); //Margin

        //setLayout(new MigLayout("wrap,fillx", "[fill]"));
        jScrollPane2.putClientProperty(FlatClientProperties.STYLE, "" + "arc:20;");

        txtSearch.putClientProperty(FlatClientProperties.PLACEHOLDER_TEXT, "Pesquisar...");
        //txtPass.putClientProperty(FlatClientProperties.PLACEHOLDER_TEXT, "Password");
        jLabel1.putClientProperty(FlatClientProperties.STYLE, ""
                + "font:bold +3");
        jTextPane1.setText("Cadastrar, atualizar e excluir doadores");
        jTextPane1.setEditable(false);
        jTextPane1.setBorder(BorderFactory.createEmptyBorder());

        loadTableData();
    }

    private void loadTableData() {
        // Obtenha todos os doadores do repositório
        List<Donor> donors = this.service.findAll(Application.loggedUser());

        // Defina o modelo da tabela
        DefaultTableModel model = (DefaultTableModel) tableDonors.getModel();
        model.setRowCount(0); // Limpa a tabela antes de preencher com novos dados

        // Adicione cada doador ao modelo da tabela
        for (Donor donor : donors) {
            var status = "Inativo";
            if (donor.getActive()) {
                status = "Ativo";
            }

            model.addRow(new Object[]{
                donor.getId(), // Supondo que há um método getId() em Donor
                donor.getName(), // Supondo que há um método getName() em Donor
                donor.getCpf(), // Supondo que há um método getPhone() em Donor
                status, // Supondo que há um método getStatus() em Donor
                donor.getUser().getName(),
                donor.getCreatedAt(),
                donor.getUpdatedAt(),});
        }
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
        jScrollPane2 = new javax.swing.JScrollPane();
        tableDonors = new javax.swing.JTable();

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

        jLabel1.setText("Doadores");

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
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 143, Short.MAX_VALUE)
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

        tableDonors.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {

            },
            new String [] {
                "Código", "Nome", "CPF/CNPJ", "Situação", "Criado por", "Criado em", "Atualizado em"
            }
        ) {
            boolean[] canEdit = new boolean [] {
                false, false, false, false, false, false, false
            };

            public boolean isCellEditable(int rowIndex, int columnIndex) {
                return canEdit [columnIndex];
            }
        });
        jScrollPane2.setViewportView(tableDonors);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGap(6, 6, 6)
                        .addComponent(jScrollPane2))
                    .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addComponent(jPanel1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jScrollPane2, javax.swing.GroupLayout.DEFAULT_SIZE, 500, Short.MAX_VALUE)
                .addContainerGap())
        );
    }// </editor-fold>//GEN-END:initComponents

    private void btnCreateActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnCreateActionPerformed
        // TODO add your handling code here:
        DonorNewDialog dialog = new DonorNewDialog((JFrame) SwingUtilities.getWindowAncestor(this), true);
        dialog.setService(this.service);
        dialog.setVisible(true);
    }//GEN-LAST:event_btnCreateActionPerformed

    private void btnDeleteActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnDeleteActionPerformed
        // TODO add your handling code here:

        int selectedRow = tableDonors.getSelectedRow();

        // Verifica se alguma linha está selecionada
        if (selectedRow == -1) {
            JOptionPane.showMessageDialog(this, "Selecione um doador para excluir.", "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        // Confirmação de exclusão
        int confirm = JOptionPane.showConfirmDialog(this,
                "Tem certeza que deseja excluir o doador selecionado?",
                "Confirmação de Exclusão",
                JOptionPane.YES_NO_OPTION);

        if (confirm == JOptionPane.YES_OPTION) {
            // Obter o ID do doador selecionado na tabela
            Long donorId = (Long) tableDonors.getValueAt(selectedRow, 0);

            // Excluir doador do repositório
            //repo.deleteById(donorId);
            // Atualizar a tabela após a exclusão
            loadTableData();

            // Mensagem de sucesso
            JOptionPane.showMessageDialog(this, "Doador excluído com sucesso.");
        }
    }//GEN-LAST:event_btnDeleteActionPerformed

    private void btnUpdateActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnUpdateActionPerformed
        // TODO add your handling code here:
        // Obtém as linhas selecionadas
        int[] selectedRows = tableDonors.getSelectedRows();

        // Verifica se nenhuma ou mais de uma linha está selecionada
        if (selectedRows.length == 0) {
            JOptionPane.showMessageDialog(this, "Selecione um doador para atualizar.", "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        } else if (selectedRows.length > 1) {
            JOptionPane.showMessageDialog(this, "Por favor, selecione apenas um doador para atualizar.", "Aviso", JOptionPane.WARNING_MESSAGE);
            return;
        }

        // Continua com a lógica para uma única seleção
        Long donorId = (Long) tableDonors.getValueAt(selectedRows[0], 0);
        Donor donor = this.service.findById(Application.loggedUser(), donorId);

        if (donor == null) {
            JOptionPane.showMessageDialog(this, "Doador não encontrado.", "Erro", JOptionPane.ERROR_MESSAGE);
            return;
        }

        DonorNewDialog dialog = new DonorNewDialog((JFrame) SwingUtilities.getWindowAncestor(this), true, donor);
        dialog.setService(this.service);
        // dialog.setDonor(donor);
        dialog.setVisible(true);

        loadTableData();
    }//GEN-LAST:event_btnUpdateActionPerformed

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnCreate;
    private javax.swing.JButton btnDelete;
    private javax.swing.JButton btnUpdate;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JTextPane jTextPane1;
    private javax.swing.JTable tableDonors;
    private javax.swing.JTextField txtSearch;
    // End of variables declaration//GEN-END:variables
}
