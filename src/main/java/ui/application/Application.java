package ui.application;

import com.formdev.flatlaf.FlatClientProperties;
import com.formdev.flatlaf.FlatLaf;
import com.formdev.flatlaf.extras.FlatAnimatedLafChange;
import com.formdev.flatlaf.fonts.roboto.FlatRobotoFont;
import com.formdev.flatlaf.themes.FlatMacLightLaf;
import domain.model.User;
import domain.service.DonationService;
import domain.service.AppointmentService;
import domain.service.DonorService;
import domain.service.UserService;
import infra.postgres.repository.DonationRepositoryPgsql;
import infra.postgres.repository.AppointmentRepositoryPgsql;
import infra.postgres.repository.DonorRepositoryPgsql;
import infra.postgres.repository.UserRepositoryPgsql;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Font;
import javax.swing.SwingUtilities;
import javax.swing.UIManager;
import ui.application.form.LoginForm;
import ui.application.form.MainForm;
//import raven.toast.Notifications;
import org.slf4j.LoggerFactory;
import org.slf4j.Logger;

/**
 *
 * @author Raven
 */
public class Application extends javax.swing.JFrame {

    private static final Logger logger = LoggerFactory.getLogger(Application.class);

    private static Application app;
    private final MainForm mainForm;
    private final LoginForm loginForm;
    private User currentUser;

    public Application() {
        initComponents();
        setSize(new Dimension(1366, 768));
        setLocationRelativeTo(null);

        var userRepo = new UserRepositoryPgsql();
        var donorRepo = new DonorRepositoryPgsql();
        var agendaRepo = new AppointmentRepositoryPgsql();
        var donationRepo = new DonationRepositoryPgsql();

        var userService = new UserService(userRepo);
        var eventService = new AppointmentService(agendaRepo);
        var donationService = new DonationService(donationRepo);
        var donorService = new DonorService(donorRepo);

        mainForm = new MainForm(donorService, eventService, donationService);

        loginForm = new LoginForm(userService);
        setContentPane(loginForm);
        getRootPane().putClientProperty(FlatClientProperties.FULL_WINDOW_CONTENT, true);
        // Notifications.getInstance().setJFrame(this);
        //pack();  // Ajusta automaticamente o tamanho da janela

    }

    public static void showForm(Component component) {
        component.applyComponentOrientation(app.getComponentOrientation());
        app.mainForm.showForm(component);
    }

    public static void login(User loggedUser) {
        FlatAnimatedLafChange.showSnapshot();
        app.setContentPane(app.mainForm);
        app.mainForm.applyComponentOrientation(app.getComponentOrientation());
        setSelectedMenu(0, 0);
        app.mainForm.hideMenu();
        SwingUtilities.updateComponentTreeUI(app.mainForm);
        FlatAnimatedLafChange.hideSnapshotWithAnimation();
        app.currentUser = loggedUser;
        setUserImage(loggedUser().getPhoto());
    }

    public static void logout() {
        FlatAnimatedLafChange.showSnapshot();
        app.setContentPane(app.loginForm);
        app.loginForm.applyComponentOrientation(app.getComponentOrientation());
        SwingUtilities.updateComponentTreeUI(app.loginForm);
        FlatAnimatedLafChange.hideSnapshotWithAnimation();
    }

    public static User loggedUser() {
        if (app != null) {
            return app.currentUser;
        }
        return null;
    }

    public static void setSelectedMenu(int index, int subIndex) {
        app.mainForm.setSelectedMenu(index, subIndex);
    }

    public static void setUserImage(byte[] image) {
        app.mainForm.setUserImage(image);
    }

    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 719, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 521, Short.MAX_VALUE)
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    public static void main(String args[]) {
        logger.trace("Entering method foo()");
        logger.debug("Received request from 198.12.34.56");
        logger.info("User logged in: john");
        logger.warn("Connection to server lost. Retrying...");
        logger.error("Failed to write data to file: myFile.txt");

        FlatRobotoFont.install();
        FlatLaf.registerCustomDefaultsSource("theme");
        UIManager.put("defaultFont", new Font(FlatRobotoFont.FAMILY, Font.PLAIN, 16));
        FlatMacLightLaf.setup();
        java.awt.EventQueue.invokeLater(() -> {
            app = new Application();
            //  app.applyComponentOrientation(ComponentOrientation.RIGHT_TO_LEFT);
            app.setVisible(true);
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    // End of variables declaration//GEN-END:variables
}
