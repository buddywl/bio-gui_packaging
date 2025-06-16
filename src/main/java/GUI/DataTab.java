package GUI;

import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

public class DataTab extends JPanel {
    Utility util = new Utility();
    private static Path DATA_DIR = null;

    public DataTab(Utility util) {
        this.util = util;
        DATA_DIR = util.getSQMSaveDirFromConfig();
        setSize(800, 560);
        setLayout(new BorderLayout());

        JLabel label = new JLabel("Browse data files in: " + DATA_DIR.toString());
        JFileChooser fileChooser = new JFileChooser(DATA_DIR.toFile());
        fileChooser.setControlButtonsAreShown(false); // hides approve/cancel buttons
        fileChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);

        JButton openDir = new JButton("Open Folder in File Explorer");
        openDir.addActionListener(e -> {
            try {
                Desktop.getDesktop().open(DATA_DIR.toFile());
            } catch (IOException ex) {
                util.append("[GUI] " + ex.getMessage());
            }
        });

        JPanel topPanel = new JPanel(new BorderLayout());
        topPanel.add(label, BorderLayout.CENTER);
        topPanel.add(openDir, BorderLayout.EAST);
        topPanel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));

        add(topPanel, BorderLayout.NORTH);
        add(fileChooser, BorderLayout.CENTER);
    }
}
