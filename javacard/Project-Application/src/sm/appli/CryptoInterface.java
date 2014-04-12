package sm.appli;

import java.awt.Font;
import java.awt.SystemColor;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.smartcardio.CardException;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.border.BevelBorder;

/**
 * GUI Interface with the smartcard
 * 
 * use an intern crypto engine
 */
public class CryptoInterface {
	// instance variable
	private CryptoEngine engine;
	
	// interface component
	private JFrame frmProjetChiffrement;
	private JTextField txt_resultat;
	private JTextField txt_cle;
	private JTextField txt_message;
	private JTextField txt_erreur;
	private JButton btn_crypter;
	private JButton btn_decrypter;
	private JButton btn_cle;
	
	/**
	 * Interface Constructor
	 */
	public CryptoInterface() {
		initialize();
		addCustomEvents();
		this.engine = null;
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frmProjetChiffrement = new JFrame();
		frmProjetChiffrement.setForeground(SystemColor.menu);
		frmProjetChiffrement.setTitle("Projet - Chiffrement sym\u00E9trique");
		frmProjetChiffrement.setBounds(100, 100, 600, 500);
		frmProjetChiffrement.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frmProjetChiffrement.getContentPane().setLayout(null);
		
		JPanel pnl_cle = new JPanel();
		pnl_cle.setBorder(new BevelBorder(BevelBorder.LOWERED, null, null, null, null));
		pnl_cle.setBounds(0, 0, 584, 169);
		frmProjetChiffrement.getContentPane().add(pnl_cle);
		pnl_cle.setLayout(null);
		
		JLabel lbl_cle = new JLabel("Cl\u00E9 de chiffrement");
		lbl_cle.setBounds(54, 65, 131, 14);
		pnl_cle.add(lbl_cle);
		
		btn_cle = new JButton("Entrer cl\u00E9");
		btn_cle.setBounds(195, 93, 277, 20);
		pnl_cle.add(btn_cle);
		
		txt_cle = new JTextField();
		txt_cle.setBounds(195, 62, 277, 20);
		pnl_cle.add(txt_cle);
		txt_cle.setColumns(10);
		
		JButton btn_clear_cle = new JButton("Clear");
		btn_clear_cle.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				txt_cle.setText("");
			}
		});
		btn_clear_cle.setBounds(482, 61, 71, 23);
		pnl_cle.add(btn_clear_cle);
		
		JPanel pnl_crypto = new JPanel();
		pnl_crypto.setBorder(new BevelBorder(BevelBorder.LOWERED, null, null, null, null));
		pnl_crypto.setBounds(0, 168, 584, 188);
		frmProjetChiffrement.getContentPane().add(pnl_crypto);
		pnl_crypto.setLayout(null);
		
		btn_crypter = new JButton("Crypter");
		btn_crypter.setBounds(181, 63, 143, 23);
		pnl_crypto.add(btn_crypter);
		
		txt_message = new JTextField();
		txt_message.setBounds(181, 32, 299, 20);
		pnl_crypto.add(txt_message);
		txt_message.setColumns(10);
		
		JLabel lbl_resultat = new JLabel("R\u00E9sultat");
		lbl_resultat.setBounds(55, 120, 93, 14);
		pnl_crypto.add(lbl_resultat);
		
		btn_decrypter = new JButton("D\u00E9crypter");
		btn_decrypter.setBounds(334, 63, 146, 23);
		pnl_crypto.add(btn_decrypter);
		
		txt_resultat = new JTextField();
		txt_resultat.setEditable(false);
		txt_resultat.setBounds(181, 117, 299, 20);
		pnl_crypto.add(txt_resultat);
		txt_resultat.setColumns(10);
		
		JLabel lbl_message = new JLabel("Message \u00E0 chiffrer");
		lbl_message.setBounds(55, 35, 116, 14);
		pnl_crypto.add(lbl_message);
		lbl_message.setVerticalAlignment(SwingConstants.TOP);
		
		final JButton btn_clear_message = new JButton("Clear");
		btn_clear_message.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				txt_message.setText("");
			}
		});
		btn_clear_message.setBounds(485, 31, 71, 23);
		pnl_crypto.add(btn_clear_message);
		
		final JButton btn_clear_resultat = new JButton("Clear");
		btn_clear_resultat.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				txt_resultat.setText("");
			}
		});
		btn_clear_resultat.setBounds(485, 116, 71, 23);
		pnl_crypto.add(btn_clear_resultat);
		
		JPanel pnl_erreur = new JPanel();
		pnl_erreur.setBorder(new BevelBorder(BevelBorder.LOWERED, null, null, null, null));
		pnl_erreur.setBounds(0, 355, 584, 106);
		frmProjetChiffrement.getContentPane().add(pnl_erreur);
		pnl_erreur.setLayout(null);
		
		JLabel lbl_console = new JLabel("Console");
		lbl_console.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lbl_console.setBounds(250, 9, 108, 17);
		pnl_erreur.add(lbl_console);
		
		txt_erreur = new JTextField();
		txt_erreur.setEditable(false);
		txt_erreur.setBounds(10, 27, 550, 68);
		pnl_erreur.add(txt_erreur);
		txt_erreur.setColumns(10);
	}
	
	/**
	 * Custom events added on components
	 */
	private void addCustomEvents() {
		this.btn_cle.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent event) {
				setSymKeyAction();
			}
		});
		this.btn_crypter.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent event) {
				encryptDESAction();
			}
		});
		this.btn_decrypter.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent event) {
				decryptDESAction();
			}
		});
		frmProjetChiffrement.addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent event) {
				quitAction();
			}
		});
	}
	
	/**
	 * Engine setter
	 * 
	 * @param engine
	 */
	public void setEngine(CryptoEngine engine) {
		this.engine = engine;
	}
	
	/**
	 * Run the interface
	 * 
	 * check if the engine is set or fail
	 */
	public void run() {
		if (this.engine == null) {
			System.err.println("Aucun moteur de cryptage renseignée !");
			System.exit(1);
		}
		
		// go !
		this.frmProjetChiffrement.setVisible(true);
	}

	/**
	 * Action to set the key
	 */
	public void setSymKeyAction() {
		String key = this.txt_cle.getText();
		
		try {
			this.txt_erreur.setText("");
			this.engine.setSymKey(key);
			this.txt_erreur.setText("Nouvelle clé de cryptage renseignée: " + key);
		} catch (CardException e) {
			System.err.println(e);
		} catch (CommandError e) {
			this.txt_erreur.setText(e.toString());
		}
	}
	
	/**
	 * Action to encrypt a message
	 */
	public void encryptDESAction() {
		String message = this.txt_message.getText();
		
		try {
			this.txt_erreur.setText("");
			String res = this.engine.encryptDES(message);
			this.txt_resultat.setText(res);
		} catch (CardException e) {
			System.err.println(e);
		} catch (CommandError e) {
			this.txt_erreur.setText(e.toString());
		}
	}
	
	/**
	 * Action to decrypt the message
	 */
	public void decryptDESAction() {
		String message = this.txt_message.getText();
		
		try {
			this.txt_erreur.setText("");
			String res = this.engine.decryptDES(message);
			this.txt_resultat.setText(res);
		} catch (CardException e) {
			System.err.println(e);
		} catch (CommandError e) {
			this.txt_erreur.setText(e.toString());
		}
	}
	
	/**
	 * Quit the application
	 */
	public void quitAction() {
		try {
			this.engine.end();
		} catch (CardException e) {
			System.err.println(e);
		}
	}
}
