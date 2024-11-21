package ui.money;

import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import javax.swing.JTextField;
import javax.swing.event.CaretEvent;
import javax.swing.event.CaretListener;
import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.PlainDocument;
import javax.swing.text.SimpleAttributeSet;

public class JMoneyField {

    private static final SimpleAttributeSet NULL_ATTRIBUTE = new SimpleAttributeSet();

    /**
     * Configura o JTextField para funcionar como um campo de valores
     * monetários.
     *
     * @param textField O JTextField a ser configurado.
     */
    public JMoneyField(JTextField textField) {
        // Alinhamento do texto à direita
        //textField.setHorizontalAlignment(JTextField.RIGHT);
        // Configura o documento personalizado para formatação de valores
        textField.setDocument(new MoneyFieldDocument());
        // Define o valor inicial
        textField.setText("0,00");
        // Adiciona listener para selecionar todo o texto ao ganhar foco
        textField.addFocusListener(new MoneyFieldFocusListener());
        // Impede que o cursor seja movido fora do final do texto
        textField.addCaretListener(new CaretListener() {
            @Override
            public void caretUpdate(CaretEvent e) {
                if (e.getDot() != textField.getText().length()) {
                    textField.getCaret().setDot(textField.getText().length());
                }
            }
        });
    }

    /**
     * Listener para selecionar todo o texto ao ganhar foco.
     */
    private static final class MoneyFieldFocusListener extends FocusAdapter {

        @Override
        public void focusGained(FocusEvent e) {
            JTextField textField = (JTextField) e.getSource();
            textField.selectAll();
        }
    }

    /**
     * Documento personalizado para formatar o texto como valores monetários.
     */
    private static final class MoneyFieldDocument extends PlainDocument {

        private static final long serialVersionUID = 1L;

        @Override
        public void insertString(int offs, String str, AttributeSet a) throws BadLocationException {
            if (!str.matches("\\d+")) {
                return; // Ignora se não for um número
            }

            String original = getText(0, getLength());

            if (!original.startsWith("R$ ")) {
                original = "R$ " + original.replaceAll("[^0-9]", "");
                super.remove(0, getLength());
                super.insertString(0, original, NULL_ATTRIBUTE);
            }

            // Permite apenas até 16 caracteres (9.999.999.999,99)
            if (original.length() < 16) {
                StringBuilder mascarado = new StringBuilder();
                if (a != NULL_ATTRIBUTE) {
                    // Limpa o campo
                    remove(-1, getLength());

                    mascarado.append((original + str).replaceAll("[^0-9]", ""));
                    for (int i = 0; i < mascarado.length(); i++) {
                        if (!Character.isDigit(mascarado.charAt(i))) {
                            mascarado.deleteCharAt(i);
                        }
                    }
                    Long number = Long.parseLong(mascarado.toString());

                    mascarado.replace(0, mascarado.length(), number.toString());

                    if (mascarado.length() < 3) {
                        if (mascarado.length() == 1) {
                            mascarado.insert(0, "0");
                            mascarado.insert(0, ",");
                            mascarado.insert(0, "0");
                        } else if (mascarado.length() == 2) {
                            mascarado.insert(0, ",");
                            mascarado.insert(0, "0");
                        }
                    } else {
                        mascarado.insert(mascarado.length() - 2, ",");
                    }

                    if (mascarado.length() > 6) {
                        mascarado.insert(mascarado.length() - 6, '.');
                        if (mascarado.length() > 10) {
                            mascarado.insert(mascarado.length() - 10, '.');
                            if (mascarado.length() > 14) {
                                mascarado.insert(mascarado.length() - 14, '.');
                            }
                        }
                    }

                    // Adiciona o prefixo "R$"
                    super.insertString(0, "R$ " + mascarado.toString(), a);
                } else {
                    if (original.length() == 0) {
                        super.insertString(0, "R$ 0,00", a);
                    }
                }
            }
        }

        @Override
        public void remove(int offs, int len) throws BadLocationException {
            // Obtém o texto atual
            String original = getText(0, getLength());

            // Verifica se a remoção está tentando apagar todo o conteúdo
            if (len == getLength()) {
                super.remove(0, len);
                insertString(0, "R$ 0,00", NULL_ATTRIBUTE);
                return;
            }

            // Ajusta o texto restante após a remoção parcial
            String updated = original.substring(0, offs) + original.substring(offs + len);

            super.remove(0, getLength());
            insertString(0, updated.replaceAll("[^0-9]", ""), null);
        }

    }
}
