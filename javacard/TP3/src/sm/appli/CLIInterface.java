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
		
		System.out.println("Cr�dit de votre carte ...");
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
		
		System.out.println("D�bit de votre carte ...");
		wallet.debit(value);
	}
	
	/**
	 * Reset operation
	 * 
	 * @throws CardException
	 * @throws CommandError
	 */
	public void reset() throws CardException, CommandError {
		System.out.println("Remise � z�ro de votre solde ...");
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
			System.err.println("Aucun contr�leur de porte-monnaie d�clar� pour l'interface");
			System.exit(1);
		}
		
		boolean continu = true;
		
		System.out.println("######################################################################");
		System.out.println("Bienvenue sur l'application de porte-monnaie �lectronique de M�d�ric");
		System.out.println("######################################################################");
		System.out.println("");

		// authentification
		if (wallet.isWithPIN()) {
			if (!authentificate()) {
				System.err.println("Impossible de vous authentifier :(\n");
				return;
			} else {
				System.out.println("Authentification r�ussie :)\n");
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
		System.out.println("- [1] Cr�diter");
		System.out.println("- [2] D�biter");
		System.out.println("- [3] Mettre � z�ro");
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
			default: System.err.println("Commande non g�r�e."); return true;
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
