/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/GUIForms/JPanel.java to edit this template
 */
package ui.application.form.donation.agenda;

import com.formdev.flatlaf.FlatClientProperties;
import com.mindfusion.common.DateTime;
import com.mindfusion.scheduling.Calendar;
import com.mindfusion.scheduling.CalendarAdapter;
import com.mindfusion.scheduling.CalendarView;
import com.mindfusion.scheduling.DateChangedEvent;
import com.mindfusion.scheduling.ItemMouseEvent;
import com.mindfusion.scheduling.ThemeType;
import com.mindfusion.scheduling.model.Appointment;
import com.mindfusion.scheduling.model.Item;
import com.mindfusion.scheduling.model.ItemEvent;
import com.mindfusion.scheduling.model.Reminder;
import com.mindfusion.scheduling.model.ReminderType;
import com.mindfusion.scheduling.model.ScheduleAdapter;
import domain.service.AppointmentService;
import domain.service.DonorService;
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.Rectangle;
import java.awt.Toolkit;
import java.awt.event.MouseEvent;
import java.time.LocalDateTime;
import javax.swing.JFrame;
import javax.swing.SwingUtilities;
import javax.swing.border.EmptyBorder;
import org.slf4j.LoggerFactory;
import ui.application.Application;
import ui.application.form.donation.agenda.dialog.AppointmentNewDialog;

/**
 *
 * @author cezar.britez
 */
public class AgendaForm extends javax.swing.JPanel {

    private static final org.slf4j.Logger logger = LoggerFactory.getLogger(AgendaForm.class);

    private String[] imageFileNames = {"0.png", "1.png", "2.png", "3.png", "4.png", "5.png"};
    private Calendar calendar;
    private String imagedir = "calendar/";

    private AppointmentService service;
    private DonorService donorService;

    /**
     * Creates new form AgendaForm
     */
    public AgendaForm(AppointmentService service, DonorService donorService) {
        initComponents();
        this.service = service;
        this.donorService = donorService;
        init();
    }

    public void init() {
        setBorder(new EmptyBorder(10, 10, 10, 10)); //Margin

        txtSearch.putClientProperty(FlatClientProperties.PLACEHOLDER_TEXT, "Pesquisar...");
        jLabel1.putClientProperty(FlatClientProperties.STYLE, ""
                + "font:bold +3");
        jLabel2.setText("Cadastrar, atualizar e excluir compromissos");

        calendar = new Calendar();
        calendar.setTheme(ThemeType.Light);
        jPanel1.setLayout(new BorderLayout());
        jPanel1.add(calendar, BorderLayout.CENTER);

        SwingUtilities.invokeLater(() -> {
            var frame = (JFrame) SwingUtilities.getWindowAncestor(this);
            var donorService = this.donorService;
            var appointmentService = this.service;

            if (frame == null) {
                logger.warn("O JFrame não foi encontrado!");
            }

            calendar.addCalendarListener(new CalendarAdapter() {

                private void showForm(Item item) {
                    var appointment = appointmentService.findById(Application.loggedUser(), Long.valueOf(item.getId()));

                    var form = new AppointmentNewDialog(frame, true, appointment);
                    form.setDonorService(donorService);
                    form.setAppointmentService(appointmentService);
                    
                    // Calcula a posição central da tela
                    // Obter tamanho e posição do JFrame
                    Rectangle bounds = frame.getBounds(); // Retorna as dimensões e posição do JFrame

                    // Obter tamanho do diálogo
                    Dimension dialogSize = form.getSize();

                    // Calcular posição central
                    int x = bounds.x + (bounds.width - dialogSize.width) / 2;
                    int y = bounds.y + (bounds.height - dialogSize.height) / 2;

                    // Definir a posição do diálogo
                    form.setLocation(x, y);
                    form.setVisible(true);
                }

                @Override
                public void itemClick(ItemMouseEvent e) {

                    showForm(e.getItem());
                    MouseEvent releaseEvent = new MouseEvent(
                            calendar, MouseEvent.MOUSE_RELEASED, System.currentTimeMillis(),
                            0, 0, 0, 1, false
                    );
                    Toolkit.getDefaultToolkit().getSystemEventQueue().postEvent(releaseEvent);
                }

                @Override
                public void visibleDateChanged(DateChangedEvent e) {
                    // Obtém o novo intervalo visível
                    var startDate = e.getNewDate();

                    LocalDateTime localDateTime = startDate.toJavaDateTime();

                    loadAppointments(localDateTime);
                }
            });

        });

        calendar.getSchedule().addScheduleListener(new ScheduleAdapter() {
            @Override
            public void itemReminderTriggered(ItemEvent ie) {
                java.util.logging.Logger.getGlobal().info(ie.getItem().getDescriptionText());
            }
        });

        loadAppointments(LocalDateTime.now());
    }

    private void loadAppointments(LocalDateTime date) {
        try {
            // Obtém os compromissos do serviço
            var appointments = service.findByQuery(Application.loggedUser(), "", date);

            calendar.getSchedule().getItems().clear();

            for (domain.model.Appointment appointment : appointments) {
                // Cria uma instância de Appointment para o calendário
                Appointment calendarAppointment = new Appointment();

                calendarAppointment.setId(appointment.getId().toString());

                // Mapeia os atributos do modelo de domínio para os atributos do calendário
                calendarAppointment.setStartTime(new DateTime(
                        appointment.getDate().getYear(),
                        appointment.getDate().getMonthValue(),
                        appointment.getDate().getDayOfMonth(),
                        appointment.getDate().getHour(),
                        appointment.getDate().getMinute(),
                        0
                ));

                calendarAppointment.setEndTime(new DateTime(
                        appointment.getDate().getYear(),
                        appointment.getDate().getMonthValue(),
                        appointment.getDate().getDayOfMonth(),
                        appointment.getDate().getHour(),
                        appointment.getDate().getMinute(),
                        0
                ));

                calendarAppointment.setSubject(appointment.getCall().getDonor().getName());
                calendarAppointment.setDescriptionText(appointment.getNotes());

                // Adiciona o compromisso ao calendário
                calendar.getSchedule().getItems().add(calendarAppointment);
            }

            logger.info("Compromissos carregados com sucesso.");
        } catch (Exception e) {
            logger.warn("Erro ao carregar compromissos: " + e.getMessage());
        }
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
        appointment2.setStartTime(getDateTime(2024, 11, 29, 01, 45)); // 29 Nov 2024, 02:00 PM
        appointment2.setEndTime(getDateTime(2024, 11, 29, 01, 50)); // 29 Nov 2024, 03:00 PM
        appointment2.setSubject("Client Call");
        // Adicionando um lembrete (5 minutos antes do horário de início)
        var rem = new Reminder();
        rem.setType(ReminderType.Exact);
        rem.setTime(appointment2.getStartTime().addMinutes(-5)); // 5 minutos antes
        rem.setMessage("Lembrete");

        appointment2.setReminder(rem); // 5 minutos
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

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jPanel1 = new javax.swing.JPanel();
        jLabel1 = new javax.swing.JLabel();
        txtSearch = new javax.swing.JTextField();
        jLabel2 = new javax.swing.JLabel();
        jButton1 = new javax.swing.JButton();
        jButton2 = new javax.swing.JButton();
        jButton3 = new javax.swing.JButton();
        jButton4 = new javax.swing.JButton();

        javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(jPanel1);
        jPanel1.setLayout(jPanel1Layout);
        jPanel1Layout.setHorizontalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 0, Short.MAX_VALUE)
        );
        jPanel1Layout.setVerticalGroup(
            jPanel1Layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 530, Short.MAX_VALUE)
        );

        jLabel1.setText("Agenda");

        jLabel2.setText("Agenda de compromissos");

        jButton1.setText("Novo");
        jButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton1ActionPerformed(evt);
            }
        });

        jButton2.setText("mês");
        jButton2.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton2ActionPerformed(evt);
            }
        });

        jButton3.setText("semana");
        jButton3.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton3ActionPerformed(evt);
            }
        });

        jButton4.setText("dia");
        jButton4.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                jButton4ActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jLabel2, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addComponent(txtSearch, javax.swing.GroupLayout.PREFERRED_SIZE, 325, javax.swing.GroupLayout.PREFERRED_SIZE)
                            .addComponent(jLabel1))
                        .addGap(0, 344, Short.MAX_VALUE))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jButton2)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jButton3)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(jButton4)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                        .addComponent(jButton1)))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jLabel1)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jLabel2)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(txtSearch, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jButton2)
                    .addComponent(jButton3)
                    .addComponent(jButton4)
                    .addComponent(jButton1))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addContainerGap())
        );
    }// </editor-fold>//GEN-END:initComponents

    private void jButton3ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton3ActionPerformed
        // TODO add your handling code here:
        calendar.setCurrentView(CalendarView.List);
    }//GEN-LAST:event_jButton3ActionPerformed

    private void jButton1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton1ActionPerformed
        // TODO add your handling code here:
        var frame = (JFrame) SwingUtilities.getWindowAncestor(this);
        Rectangle bounds = frame.getBounds(); // Retorna as dimensões e posição do JFrame
        // Definir a posição do diálogo
        var form = new AppointmentNewDialog(frame, true);
        form.setDonorService(donorService);
        form.setAppointmentService(service);
        // Obter tamanho do diálogo
        Dimension dialogSize = form.getSize();
        // Calcular posição central
        int x = bounds.x + (bounds.width - dialogSize.width) / 2;
        int y = bounds.y + (bounds.height - dialogSize.height) / 2;
        form.setLocation(x, y);
        form.setVisible(true);
    }//GEN-LAST:event_jButton1ActionPerformed

    private void jButton4ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton4ActionPerformed
        // TODO add your handling code here:
        calendar.setCurrentView(CalendarView.Timetable);
    }//GEN-LAST:event_jButton4ActionPerformed

    private void jButton2ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_jButton2ActionPerformed
        // TODO add your handling code here:
        calendar.setCurrentView(CalendarView.SingleMonth);
    }//GEN-LAST:event_jButton2ActionPerformed


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton jButton1;
    private javax.swing.JButton jButton2;
    private javax.swing.JButton jButton3;
    private javax.swing.JButton jButton4;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JTextField txtSearch;
    // End of variables declaration//GEN-END:variables
}
