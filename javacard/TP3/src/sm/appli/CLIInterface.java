package sm.appli;

import javax.smartcardio.CardException;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class CLIInterface {
	private Wallet wallet;
	private Scanner scanner;
	private List<Integer> commands;
	
	// singleton parameter
	private static CLIInterface instance = null;
	
	/**
	 * Private constructor
	 */
	private CLIInterface() {
		this.wallet = null;
		this.scanner = new Scanner(System.in);
		this.commands = new ArrayList<Integer>();
		
		this.commands.add(1); this.commands.add(2); this.commands.add(3); this.commands.add(9);
	}
	
	/**
	 * Singleton method
	 * 
	 * @return
	 */
	public static CLIInterface getInstance() {
		if (instance == null) {
			instance = new CLIInterface();
		}
		
		return instance;
	}
	
	/**
	 * Set the wallet
	 * 
	 * @param wallet
	 */
	public void setWallet(Wallet wallet) {
		this.wallet = wallet;
	}
	
	/**
	 * Credit opperation
	 * 
	 * @throws CardException
	 * @throws CommandError
	 */
	public void credit() throws CardException, CommandError {
		System.out.print("Montant: ");
		String line = scanner.nextLine();
		int value = fromLineToNumber(line);
		
		if (value <0) {
			System.err.println("Montant invalide");
			return;
		}
		
		System.out.println("Crédit de votre carte ...");
		wallet.credit(value);
	}
	
	/**
	 * Debit operation
	 * 
	 * @throws CardException
	 * @throws CommandError
	 */
	public void debit() throws CardException, CommandError {
		System.out.print("Montant: ");
		String line = scanner.nextLine();
		int value = fromLineToNumber(line);
		
		if (value <0) {
			System.out.println("Montant invalide");
			return;
		}
		
		System.out.println("Débit de votre carte ...");
		wallet.debit(value);
	}
	
	/**
	 * Reset operation
	 * 
	 * @throws CardException
	 * @throws CommandError
	 */
	public void reset() throws CardException, CommandError {
		System.out.println("Remise à zéro de votre solde ...");
		wallet.reset();
	}
	
	/**
	 * Authentification with PIN
	 * @throws CommandError 
	 * @throws CardException 
	 */
	public boolean authentificate() {
		do {
			System.out.print("Type your PIN: ");
			String line = scanner.nextLine();
			
			try {
				wallet.verify(line);
				
				return true;
			} catch (CardException exp) {
				System.err.println(exp);
				return false;
			} catch (CommandError err) {
				System.err.println(err);
				return false;
			}
		} while (true);
	}
	
	/**
	 * Chain prompt
	 */
	public void run() {
		if (this.wallet == null) {
			System.err.println("Aucun contrôleur de porte-monnaie déclaré pour l'interface");
			System.exit(1);
		}
		
		boolean continu = true;
		
		System.out.println("######################################################################");
		System.out.println("Bienvenue sur l'application de porte-monnaie électronique de Médéric");
		System.out.println("######################################################################");
		System.out.println("");

		// authentification
		if (wallet.isWithPIN()) {
			if (!authentificate()) {
				System.err.println("Impossible de vous authentifier :(\n");
				return;
			} else {
				System.out.println("Authentification réussie :)\n");
			}
		}
		
		do {
			try {
				displayPrompt();
				continu = dispatchCommand();
				System.out.println("");
			} catch (CardException exp) {
				System.out.println(exp);
				System.out.println("");
			} catch (CommandError err) {
				System.out.println(err);
				System.out.println("");
			}
		} while (continu);
	}
	
	/**
	 * Display the prompt
	 * 
	 * @throws CardException
	 */
	private void displayPrompt() throws CardException {
		System.out.println("BALANCE=" + wallet.getBalance());
		System.out.println("");
		System.out.println("Commandes: ");
		System.out.println("- [1] Créditer");
		System.out.println("- [2] Débiter");
		System.out.println("- [3] Mettre à zéro");
		System.out.println("- [9] Quitter");
		System.out.print(">>> ");
	}
	
	/**
	 * Scan and dispatch a command
	 * @return true if the user continues to command
	 * @throws CommandError 
	 * @throws CardException 
	 */
	private boolean dispatchCommand() throws CardException, CommandError {
		String line = scanner.nextLine();
		int c = fromLineToNumber(line);
		
		// errors
		if (!commands.contains(c)) {
			System.err.println("Commande inconnue.");
			return true;
		}
		
		switch (c) {
			case -1: System.err.println("Commande invalide."); return true;
			case 1: credit(); return true;
			case 2: debit(); return true;
			case 3: reset(); return true;
			case 9: return false;	// quit
			default: System.err.println("Commande non gérée."); return true;
		}
	}
	
	/**
	 * Returns a command number or -1 on error
	 * @param line
	 * @return
	 */
	private int fromLineToNumber(String line) {
		int c = -1;
		
		// errors
		if (line.isEmpty()) {
			return -1;
		}
		try {
			c = Integer.parseInt(line);
		} catch (NumberFormatException err) {
			return -1;
		}
		
		return c;
	}
}
