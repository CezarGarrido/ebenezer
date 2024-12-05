/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/GUIForms/JDialog.java to edit this template
 */
package ui.application.form.donation.agenda.dialog;

import domain.model.Appointment;
import domain.model.AppointmentCall;
import domain.model.Donation;
import domain.model.Donor;
import domain.model.DonorContact;
import domain.service.AppointmentService;
import domain.service.DonorService;
import java.awt.Dimension;
import java.text.NumberFormat;
import java.text.ParseException;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Date;
import java.util.Locale;
import javax.swing.DefaultListModel;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.SwingUtilities;
import javax.swing.table.DefaultTableModel;
import javax.swing.text.DefaultFormatterFactory;
import javax.swing.text.MaskFormatter;
import org.slf4j.LoggerFactory;
import ui.application.Application;
import ui.application.form.donation.manage.dialog.DonationNewDialog;
import ui.application.form.donor.dialog.DonorSearchDialog;

enum Mode {
    EDIT, // Modo de edição
    CREATE; // Modo de criação
}

/**
 *
 * @author cezar.britez
 */
public class AppointmentNewDialog extends javax.swing.JDialog {

    private static final org.slf4j.Logger logger = LoggerFactory.getLogger(AppointmentNewDialog.class);

    private DonorService donorService;
    private AppointmentService appointmentService;

    private Appointment appointment = new Appointment();
    private Donor selectedDonor;
    private Donation donation;
    private Mode mode;

    /**
     * Creates new form AppointmentNewDialog
     */
    public AppointmentNewDialog(java.awt.Frame parent, boolean modal) {
        super(parent, modal);
        setLocationRelativeTo(parent); // Para centralizar na tela
        initComponents();
        init();
        this.mode = Mode.CREATE;
    }

    public AppointmentNewDialog(java.awt.Frame parent, boolean modal, Appointment appointment) {
        super(parent, modal);
        setLocationRelativeTo(parent); // Para centralizar na tela
        initComponents();
        init();
        loadAppointment(appointment);
        pack();
        this.mode = Mode.EDIT;
    }

    private void init() {
        setMinimumSize(new Dimension(548, 720)); // Exemplo de tamanho
        panelDonor.setVisible(false);
        LocalTime now = LocalTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm");
        String formattedTime = now.format(formatter);
        txtDate.setDate(new Date()); // Define a data atual, se necessário

        // Configurar o editor de célula com máscara
        try {
            MaskFormatter hourMask = new MaskFormatter("##:##");
            txtHour.setFormatterFactory(new DefaultFormatterFactory(hourMask));

            MaskFormatter phoneMask = new MaskFormatter("(##) #####-####");
            phoneMask.setPlaceholderCharacter('_');
            txtPhone.setFormatterFactory(new DefaultFormatterFactory(phoneMask));

        } catch (ParseException e) {
            logger.error(e.getMessage());
        }

        txtHour.setText(formattedTime);

        pack();
    }

    private void loadAppointment(Appointment appointment) {
        this.appointment = appointment;
        txtDate.setDate(Date.from(appointment.getDate().atZone(ZoneId.systemDefault()).toInstant()));
        txtHour.setText(appointment.getTime());
        txtObs.setText(appointment.getNotes());
        if (appointment.getCall() != null && appointment.getCall().getDonor() != null) {
            panelDonor.setVisible(true);
            selectedDonor = appointment.getCall().getDonor();
            txtDonor.setText(selectedDonor.getName());
            updateContactsTable(selectedDonor);
        }

        if (appointment.getDonation() != null) {
            this.donation = this.appointment.getDonation();
            updateDonationTable(this.donation);
        }
    }

    public void setDonorService(DonorService donorService) {
        this.donorService = donorService;
    }

    public void setAppointmentService(AppointmentService appointmentService) {
        this.appointmentService = appointmentService;
    }

    private void updateContactsTable(Donor donor) {
        DefaultListModel<String> model = (DefaultListModel<String>) listDonorContacts.getModel();
        model.clear(); // Adiciona um novo item

        try {
            MaskFormatter phoneMask = new MaskFormatter("(##) #####-####");
            phoneMask.setPlaceholderCharacter('_');

            if (donor.getContacts() != null) {
                for (DonorContact contact : donor.getContacts()) {
                    model.addElement(phoneMask.valueToString(contact.getPhone()));
                }
            }

        } catch (ParseException e) {
            logger.error(e.getMessage());
        }
    }

    private void updateDonationTable(Donation donation) {
        // Modelo de tabela
        DefaultTableModel model = (DefaultTableModel) tableDonation.getModel();
        // Limpa a tabela
        model.setRowCount(0);

        Locale locale = new Locale("pt", "BR");
        NumberFormat numberFormat = NumberFormat.getCurrencyInstance(locale);

        // Verifica se o pagamento foi feito
        String paidLabel = "Sim";
        String receivedAtLabel = "-";
        if (donation.getPaid() == null || !donation.getPaid()) {
            paidLabel = "Não";
            //receivedAtLabel = donation.getReceivedAt().toString();
        }

        // Adiciona a linha à tabela com os valores ajustados
        model.addRow(new Object[]{
            numberFormat.format(donation.getAmount()),
            donation.getPaymentMethod(),
            paidLabel,
            receivedAtLabel,
        });
    }

    public void setDonorAvatar(String fullName) {
        if (fullName == null || fullName.isEmpty()) {
            txtDonorAvatar.setText(""); // Define vazio se o nome estiver nulo ou vazio
            return;
        }

        String[] nameParts = fullName.trim().split("\\s+"); // Divide o nome por espaços
        StringBuilder initials = new StringBuilder();

        // Adiciona a inicial do primeiro nome
        if (nameParts.length > 0) {
            initials.append(nameParts[0].charAt(0));
        }

        // Adiciona a inicial do último nome, se existir
        if (nameParts.length > 1) {
            initials.append(nameParts[nameParts.length - 1].charAt(0));
        }

        // Define as iniciais em maiúsculas (máximo de 2 caracteres)
        txtDonorAvatar.setText(initials.toString().toUpperCase());
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {
        java.awt.GridBagConstraints gridBagConstraints;

        txtDate = new com.toedter.calendar.JDateChooser();
        txtHour = new javax.swing.JFormattedTextField();
        jLabel1 = new javax.swing.JLabel();
        txtDonor = new javax.swing.JTextField();
        jLabel3 = new javax.swing.JLabel();
        panelDonor = new javax.swing.JPanel();
        txtDonorName = new javax.swing.JLabel();
        jSeparator1 = new javax.swing.JSeparator();
        jPanel4 = new javax.swing.JPanel();
        txtDonorAvatar = new javax.swing.JLabel();
        jPanel5 = new javax.swing.JPanel();
        jButton4 = new javax.swing.JButton();
        jScrollPane4 = new javax.swing.JScrollPane();
        listDonorContacts = new javax.swing.JList<>();
        jLabel4 = new javax.swing.JLabel();
        txtPhone = new javax.swing.JFormattedTextField();
        jLabel5 = new javax.swing.JLabel();
        jScrollPane2 = new javax.swing.JScrollPane();
        tableDonation = new javax.swing.JTable();
        jButton6 = new javax.swing.JButton();
        jButton5 = new javax.swing.JButton();
        jLabel2 = new javax.swing.JLabel();
        jScrollPane1 = new javax.swing.JScrollPane();
        txtObs = new javax.swing.JTextArea();
        jPanel2 = new javax.swing.JPanel();
        jButton1 = new javax.swing.JButton();
        jButton2 = new javax.swing.JButton();

        setDefaultCloseOperation(javax.swing.WindowConstants.DISPOSE_ON_CLOSE);

        txtDate.setDateFormatString("dd/MM/yyyy");

        txtHour.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                txtHourActionPerformed(evt);
            }
        });

        jLabel1.setText("Data");

        txtDonor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent evt) {
                txtDonorMouseClicked(evt);
            }
        });
        txtDonor.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyReleased(java.awt.event.KeyEvent evt) {
                txtDonorKeyReleased(evt);
            }
        });

        jLabel3.setText("Doador");

        panelDonor.setBackground(new java.awt.Color(255, 255, 255));
        panelDonor.setBorder(javax.swing.BorderFactory.createLineBorder(new java.awt.Color(0, 0, 0)));

        txtDonorName.setText("Cezar Garrido Britez");

        jPanel4.setBackground(new java.awt.Color(255, 242, 242));
        jPanel4.setPreferredSize(new java.awt.Dimension(40, 40));
        jPanel4.setLayout(new java.awt.GridBagLayout());

        txtDonorAvatar.setFont(new java.awt.Font("sansserif", 0, 24)); // NOI18N
        txtDonorAvatar.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        txtDonorAvatar.setText("CG");
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 0;
        gridBagConstraints.anchor = java.awt.GridBagConstraints.NORTHWEST;
        gridBagConstraints.insets = new java.awt.Insets(29, 28, 32, 26);
        jPanel4.add(txtDonorAvatar, gridBagConstraints);

        jButton4.setText("Remover");
        jButton4.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton4ActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout jPanel5Layout = new javax.swing.GroupLayout(jPanel5);
        jPanel5.setLayout(jPanel5Layout);
        jPanel5Layout.setHorizontalGroup(
            jPanel5Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel5Layout.createSequentialGroup()
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(jButton4)
                .addContainerGap())
        );
        jPanel5Layout.setVerticalGroup(
            jPanel5Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel5Layout.createSequentialGroup()
                .addContainerGap(10, Short.MAX_VALUE)
                .addComponent(jButton4)
                .addContainerGap())
        );

        // Criação da JList com DefaultListModel
        DefaultListModel<String> model = new DefaultListModel<>();
        listDonorContacts.setModel(model);
        jScrollPane4.setViewportView(listDonorContacts);

        javax.swing.GroupLayout panelDonorLayout = new javax.swing.GroupLayout(panelDonor);
        panelDonor.setLayout(panelDonorLayout);
        panelDonorLayout.setHorizontalGroup(
            panelDonorLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(panelDonorLayout.createSequentialGroup()
                .addGap(13, 13, 13)
                .addComponent(jPanel4, javax.swing.GroupLayout.PREFERRED_SIZE, 90, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGroup(panelDonorLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(panelDonorLayout.createSequentialGroup()
                        .addGap(14, 14, 14)
                        .addGroup(panelDonorLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(jSeparator1, javax.swing.GroupLayout.Alignment.TRAILING)
                            .addGroup(panelDonorLayout.createSequentialGroup()
                                .addComponent(txtDonorName)
                                .addContainerGap())))
                    .addGroup(panelDonorLayout.createSequentialGroup()
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(jScrollPane4)
                        .addContainerGap())))
            .addComponent(jPanel5, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
        );
        panelDonorLayout.setVerticalGroup(
            panelDonorLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(panelDonorLayout.createSequentialGroup()
                .addContainerGap(15, Short.MAX_VALUE)
                .addGroup(panelDonorLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                    .addGroup(panelDonorLayout.createSequentialGroup()
                        .addComponent(txtDonorName)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jSeparator1, javax.swing.GroupLayout.PREFERRED_SIZE, 10, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jScrollPane4, javax.swing.GroupLayout.PREFERRED_SIZE, 61, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(2, 2, 2))
                    .addComponent(jPanel4, javax.swing.GroupLayout.PREFERRED_SIZE, 90, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jPanel5, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
        );

        jLabel4.setText("Telefone Adicional");

        jLabel5.setText("Doação");

        tableDonation.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {

            },
            new String [] {
                "Valor", "Forma. Pgto", "Recebido?", "Dt. Recebimento"
            }
        ) {
            boolean[] canEdit = new boolean [] {
                false, false, false, false
            };

            public boolean isCellEditable(int rowIndex, int columnIndex) {
                return canEdit [columnIndex];
            }
        });
        jScrollPane2.setViewportView(tableDonation);

        jButton6.setText("Add");
        jButton6.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton6ActionPerformed(evt);
            }
        });

        jButton5.setText("Excluir");
        jButton5.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton5ActionPerformed(evt);
            }
        });

        jLabel2.setText("Observação");

        txtObs.setColumns(20);
        txtObs.setRows(5);
        jScrollPane1.setViewportView(txtObs);

        jButton1.setText("Fechar");
        jButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton1ActionPerformed(evt);
            }
        });

        jButton2.setText("Salvar");
        jButton2.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton2ActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout jPanel2Layout = new javax.swing.GroupLayout(jPanel2);
        jPanel2.setLayout(jPanel2Layout);
        jPanel2Layout.setHorizontalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanel2Layout.createSequentialGroup()
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(jButton2)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jButton1)
                .addContainerGap())
        );
        jPanel2Layout.setVerticalGroup(
            jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanel2Layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanel2Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jButton1)
                    .addComponent(jButton2))
                .addContainerGap(7, Short.MAX_VALUE))
        );

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(txtDate, javax.swing.GroupLayout.PREFERRED_SIZE, 452, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(18, 18, 18)
                        .addComponent(txtHour))
                    .addComponent(panelDonor, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(txtDonor, javax.swing.GroupLayout.Alignment.TRAILING)
                    .addComponent(txtPhone)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 443, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(jButton6, javax.swing.GroupLayout.Alignment.TRAILING)
                            .addComponent(jButton5, javax.swing.GroupLayout.Alignment.TRAILING)))
                    .addComponent(jScrollPane1)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel1)
                            .addComponent(jLabel3)
                            .addComponent(jLabel4)
                            .addComponent(jLabel5)
                            .addComponent(jLabel2))
                        .addGap(0, 0, Short.MAX_VALUE)))
                .addContainerGap())
            .addComponent(jPanel2, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGap(8, 8, 8)
                .addComponent(jLabel1)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(txtHour, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(txtDate, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jLabel3)
                .addGap(3, 3, 3)
                .addComponent(txtDonor, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(panelDonor, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(18, 18, 18)
                .addComponent(jLabel4)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(txtPhone, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(18, 18, 18)
                .addComponent(jLabel5)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jButton6)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jButton5))
                    .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 0, Short.MAX_VALUE))
                .addGap(18, 18, 18)
                .addComponent(jLabel2, javax.swing.GroupLayout.PREFERRED_SIZE, 17, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(jPanel2, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void jButton1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton1ActionPerformed
        // TODO add your handling code here:
        this.dispose();
    }//GEN-LAST:event_jButton1ActionPerformed

    private void jButton2ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton2ActionPerformed
        if (this.selectedDonor == null) {
            JOptionPane.showMessageDialog(this, "Selecione um doador!");
            return;
        }

        if (this.mode == Mode.CREATE) {
            int response = JOptionPane.showConfirmDialog(this, "Tem certeza que deseja salvar?", "Confirmar", JOptionPane.YES_NO_OPTION);
            if (response == JOptionPane.YES_OPTION) {
                this.appointment.setTime(txtHour.getText());
                this.appointment.setEventType("Ligação");
                this.appointment.setNotes(txtObs.getText());
                this.appointment.setDonation(donation);

                var selectedDate = txtDate.getDate(); // Obtém o java.util.Date
                if (selectedDate != null) {
                    LocalDateTime localDateTime = selectedDate.toInstant()
                            .atZone(ZoneId.systemDefault())
                            .toLocalDateTime();
                    this.appointment.setDate(localDateTime); // Usa o LocalDateTime
                }

                var call = new AppointmentCall();
                call.setDonorId(selectedDonor.getId());
                call.setPhone(txtPhone.getText());
                this.appointment.setCall(call);

                var id = this.appointmentService.save(Application.loggedUser(), this.appointment);
                if (id != null) {
                    JOptionPane.showMessageDialog(this, "Salvo com sucesso!");
                    this.dispose();
                }
            }
        } else if (this.mode == Mode.EDIT) {
            int response = JOptionPane.showConfirmDialog(this, "Tem certeza que deseja salvar?", "Confirmar", JOptionPane.YES_NO_OPTION);
            if (response == JOptionPane.YES_OPTION) {
                this.appointment.setTime(txtHour.getText());
                this.appointment.setEventType("Ligação");
                this.appointment.setNotes(txtObs.getText());
                
                
                this.appointment.setDonation(donation);

                var selectedDate = txtDate.getDate(); // Obtém o java.util.Date
                if (selectedDate != null) {
                    LocalDateTime localDateTime = selectedDate.toInstant()
                            .atZone(ZoneId.systemDefault())
                            .toLocalDateTime();
                    this.appointment.setDate(localDateTime); // Usa o LocalDateTime
                }

                var call = new AppointmentCall();
                call.setDonorId(selectedDonor.getId());
                call.setPhone(txtPhone.getText());
                this.appointment.setCall(call);

                this.appointmentService.update(Application.loggedUser(), this.appointment);
                this.dispose();
            }
        }
    }//GEN-LAST:event_jButton2ActionPerformed

    private void txtHourActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_txtHourActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_txtHourActionPerformed

    private void txtDonorMouseClicked(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_txtDonorMouseClicked
        // TODO add your handling code here:
        DonorSearchDialog sd = new DonorSearchDialog((JFrame) SwingUtilities.getWindowAncestor(this), true,
                this.donorService);

        sd.setVisible(true);

        selectedDonor = sd.getSelectedDonor(); // Captura o resultado após o fechamento

        if (selectedDonor != null) {
            panelDonor.setVisible(true);

            txtDonor.setText(selectedDonor.getName());
            txtDonorName.setText(selectedDonor.getName());
            setDonorAvatar(selectedDonor.getName());

            updateContactsTable(selectedDonor);

            // Recalculate and repaint the layout
            invalidate();
            validate();
            repaint();

            // Ensure the JDialog resizes correctly
            pack();
        }
    }//GEN-LAST:event_txtDonorMouseClicked

    private void txtDonorKeyReleased(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_txtDonorKeyReleased
        // TODO add your handling code here:
    }//GEN-LAST:event_txtDonorKeyReleased

    private void jButton6ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton6ActionPerformed
        // TODO add your handling code here:

        if (this.selectedDonor == null) {
            JOptionPane.showMessageDialog(this, "Selecione um doador!");
            return;
        }

        var dl = new DonationNewDialog((JFrame) SwingUtilities.getWindowAncestor(this), true, this.donorService);
        dl.setSourceCall(this.selectedDonor);
        dl.setVisible(true);
        donation = dl.getDonation();

        if (donation != null) {
            updateDonationTable(donation);
        }
    }//GEN-LAST:event_jButton6ActionPerformed

    private void jButton5ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton5ActionPerformed
        // TODO add your handling code here:
        this.donation = null;
        DefaultTableModel model = (DefaultTableModel) tableDonation.getModel();
        // Limpa a tabela
        model.setRowCount(0);
    }//GEN-LAST:event_jButton5ActionPerformed

    private void jButton4ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton4ActionPerformed
        // TODO add your handling code here:
        panelDonor.setVisible(false);
        txtDonor.setText("");
        selectedDonor = null;
        pack();
    }//GEN-LAST:event_jButton4ActionPerformed

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(AppointmentNewDialog.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(AppointmentNewDialog.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(AppointmentNewDialog.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(AppointmentNewDialog.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the dialog */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                AppointmentNewDialog dialog = new AppointmentNewDialog(new javax.swing.JFrame(), true);
                dialog.addWindowListener(new java.awt.event.WindowAdapter() {
                    @Override
                    public void windowClosing(java.awt.event.WindowEvent e) {
                        System.exit(0);
                    }
                });
                dialog.setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton jButton1;
    private javax.swing.JButton jButton2;
    private javax.swing.JButton jButton4;
    private javax.swing.JButton jButton5;
    private javax.swing.JButton jButton6;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JLabel jLabel5;
    private javax.swing.JPanel jPanel2;
    private javax.swing.JPanel jPanel4;
    private javax.swing.JPanel jPanel5;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JScrollPane jScrollPane4;
    private javax.swing.JSeparator jSeparator1;
    private javax.swing.JList<String> listDonorContacts;
    private javax.swing.JPanel panelDonor;
    private javax.swing.JTable tableDonation;
    private com.toedter.calendar.JDateChooser txtDate;
    private javax.swing.JTextField txtDonor;
    private javax.swing.JLabel txtDonorAvatar;
    private javax.swing.JLabel txtDonorName;
    private javax.swing.JFormattedTextField txtHour;
    private javax.swing.JTextArea txtObs;
    private javax.swing.JFormattedTextField txtPhone;
    // End of variables declaration//GEN-END:variables
}
